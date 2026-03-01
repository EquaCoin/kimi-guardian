#!/usr/bin/env python3
"""
🔍 Kimi Guardian Pre-commit Hook
Controlla i file staged prima del commit per operazioni pericolose.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .classifier_v2 import RiskClassifier, RiskLevel

console = Console() if RICH_AVAILABLE else None


class PreCommitChecker:
    """Controllore per hook pre-commit Git."""

    # Pattern pericolosi nei file
    DANGEROUS_PATTERNS = {
        "secrets": {
            "AWS Access Key": r"AKIA[0-9A-Z]{16}",
            "AWS Secret Key": r'["\']?aws[_-]?secret[_-]?access[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9/+=]{40}["\']?',
            "Generic API Key": r'["\']?api[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{20,}["\']?',
            "Private Key": r"-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----",
            "Password": r'["\']?password["\']?\s*[:=]\s*["\'][^"\']{8,}["\']',
            "Secret": r'["\']?secret["\']?\s*[:=]\s*["\'][^"\']{8,}["\']',
        },
        "dangerous_code": {
            "Eval": r"\beval\s*\(",
            "Exec": r"\bexec\s*\(",
            "System": r"\bsystem\s*\(",
            "Subprocess shell": r"subprocess\.\w+.*shell\s*=\s*True",
        },
        "commands_in_code": {
            "rm -rf": r'["\']rm\s+-rf',
            "curl pipe": r"curl.*\|.*(?:sh|bash)",
        },
    }

    def __init__(self):
        self.classifier = RiskClassifier()
        self.issues: List[Tuple[str, str, str, str]] = []  # (file, line, type, content)

    def get_staged_files(self) -> List[str]:
        """Ottiene la lista dei file staged per il commit."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                capture_output=True,
                text=True,
                check=True,
            )
            return [f for f in result.stdout.strip().split("\n") if f]
        except subprocess.CalledProcessError:
            return []

    def get_file_diff(self, filepath: str) -> str:
        """Ottiene il diff del file staged."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", filepath],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    def check_file_content(self, filepath: str, content: str):
        """Controlla il contenuto del file per pattern pericolosi."""
        lines = content.split("\n")

        for category, patterns in self.DANGEROUS_PATTERNS.items():
            for pattern_name, pattern in patterns.items():
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        # Estrai il match
                        match = re.search(pattern, line, re.IGNORECASE)
                        matched_text = match.group(0) if match else "<match>"

                        self.issues.append(
                            (
                                filepath,
                                str(i),
                                f"{category}: {pattern_name}",
                                matched_text[:50],  # Tronca per privacy
                            )
                        )

    def check_shell_scripts(self, filepath: str, content: str):
        """Controlla script shell per comandi pericolosi."""
        if not filepath.endswith((".sh", ".bash", ".zsh")):
            return

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Rimuovi commenti
            code_line = line.split("#")[0].strip()
            if not code_line:
                continue

            # Analizza comando
            result = self.classifier.classify(code_line)

            if result.action in ("block", "ask"):
                self.issues.append(
                    (
                        filepath,
                        str(i),
                        f"dangerous_command: {result.level.value}",
                        code_line[:50],
                    )
                )

    def run_checks(self) -> bool:
        """Esegue tutti i controlli."""
        files = self.get_staged_files()

        if not files:
            if console:
                console.print("[yellow]⚠️  Nessun file staged per il commit[/yellow]")
            else:
                print("⚠️  Nessun file staged per il commit")
            return True

        if console:
            console.print(f"[dim]🔍 Controllo {len(files)} file staged...[/dim]")

        for filepath in files:
            # Ottieni contenuto del file
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue

            # Controlla pattern
            self.check_file_content(filepath, content)

            # Controlla script shell
            self.check_shell_scripts(filepath, content)

        return len(self.issues) == 0

    def print_report(self):
        """Stampa il report dei problemi trovati."""
        if not self.issues:
            if console:
                console.print("[green]✅ Nessun problema trovato![/green]")
            else:
                print("✅ Nessun problema trovato!")
            return

        if console:
            # Table con rich
            table = Table(title=f"🛡️  Trovati {len(self.issues)} problemi")
            table.add_column("File", style="cyan")
            table.add_column("Linea", style="dim", justify="right")
            table.add_column("Tipo", style="yellow")
            table.add_column("Contenuto", style="red")

            for file, line, issue_type, content in self.issues:
                table.add_row(file, line, issue_type, content + "...")

            console.print(table)

            # Panel con suggerimenti
            console.print(
                Panel(
                    "Usa 'git commit --no-verify' per saltare questo controllo (sconsigliato)\n"
                    "Oppure rimuovi/riscrivi i contenuti problematici.",
                    title="[yellow]⚠️  Commit Bloccato[/yellow]",
                    border_style="red",
                )
            )
        else:
            # Plain text
            print(f"\n🛡️  Trovati {len(self.issues)} problemi:\n")
            for file, line, issue_type, content in self.issues:
                print(f"  {file}:{line} - {issue_type}")
                print(f"    {content}...")
            print("\n⚠️  Commit bloccato. Usa --no-verify per saltare.")

    def should_block(self) -> bool:
        """Determina se bloccare il commit."""
        # Blocca sempre se ci sono secrets
        for _, _, issue_type, _ in self.issues:
            if "secrets:" in issue_type:
                return True
            if issue_type.startswith("dangerous_command: critical"):
                return True

        # Per altri, dipende dal livello
        critical_count = sum(1 for _, _, t, _ in self.issues if "critical" in t)
        return critical_count > 0


def install_hook(repo_path: str = ".") -> bool:
    """Installa l'hook pre-commit nel repository."""
    repo = Path(repo_path)
    hook_file = repo / ".git" / "hooks" / "pre-commit"

    if not hook_file.parent.exists():
        print("❌ Non trovata directory .git/hooks/")
        return False

    hook_content = """#!/bin/bash
# 🛡️ Kimi Guardian Pre-commit Hook
# Controlla file staged per operazioni pericolose

cd "$(dirname "$0")/../.."

# Esegui guardian pre-commit
python3 -m guardian.precommit check

# Se il check fallisce, blocca il commit
exit $?
"""

    # Backup se esiste
    if hook_file.exists():
        backup = hook_file.with_suffix(".backup")
        hook_file.rename(backup)
        print(f"📦 Backup creato: {backup}")

    # Scrivi nuovo hook
    hook_file.write_text(hook_content)
    hook_file.chmod(0o755)

    print(f"✅ Hook installato in: {hook_file}")
    return True


def uninstall_hook(repo_path: str = ".") -> bool:
    """Disinstalla l'hook pre-commit."""
    repo = Path(repo_path)
    hook_file = repo / ".git" / "hooks" / "pre-commit"

    if hook_file.exists():
        hook_file.unlink()
        print(f"✅ Hook rimosso: {hook_file}")

        # Ripristina backup se esiste
        backup = hook_file.with_suffix(".backup")
        if backup.exists():
            backup.rename(hook_file)
            print(f"📦 Backup ripristinato")

        return True
    else:
        print("⚠️  Nessun hook trovato")
        return False


def main():
    """Entry point per CLI."""
    import argparse

    parser = argparse.ArgumentParser(description="🔍 Kimi Guardian Pre-commit Hook")
    parser.add_argument(
        "action",
        choices=["check", "install", "uninstall", "status"],
        help="Azione da eseguire",
    )

    args = parser.parse_args()

    if args.action == "check":
        checker = PreCommitChecker()
        success = checker.run_checks()
        checker.print_report()

        if not success and checker.should_block():
            sys.exit(1)
        sys.exit(0)

    elif args.action == "install":
        if install_hook():
            print("✅ Pre-commit hook installato!")
            print("Ogni 'git commit' verrà controllato automaticamente.")
        else:
            sys.exit(1)

    elif args.action == "uninstall":
        uninstall_hook()

    elif args.action == "status":
        hook_file = Path(".git/hooks/pre-commit")
        if hook_file.exists():
            content = hook_file.read_text()
            if "kimi-guardian" in content.lower() or "guardian" in content.lower():
                print("✅ Kimi Guardian hook is installed")
            else:
                print("⚠️  A pre-commit hook exists but it's not Kimi Guardian")
        else:
            print("❌ No pre-commit hook installed")


if __name__ == "__main__":
    main()
