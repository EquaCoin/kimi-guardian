#!/usr/bin/env python3
"""
🖥️ CLI per Kimi Guardian
"""

import argparse
import sys
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .classifier_v2 import RiskLevel, classify_command

console = Console()


def print_banner():
    """Stampa banner."""
    console.print("""
╔══════════════════════════════════════════════════════════╗
║               🛡️  KIMI GUARDIAN v1.0                     ║
║          AI Agent Security Scanner                       ║
╚══════════════════════════════════════════════════════════╝
""")


def cmd_check(args):
    """Comando check - analizza comando."""
    command = " ".join(args.command)

    with console.status("[bold green]Analisi comando in corso..."):
        result = classify_command(command, args.level)

    # Colore in base al rischio
    color_map = {
        RiskLevel.LOW: "green",
        RiskLevel.MEDIUM: "yellow",
        RiskLevel.HIGH: "red",
        RiskLevel.CRITICAL: "red bold",
    }
    color = color_map.get(result.level, "white")

    # Icona
    icon_map = {
        RiskLevel.LOW: "✅",
        RiskLevel.MEDIUM: "⚠️",
        RiskLevel.HIGH: "🛑",
        RiskLevel.CRITICAL: "☠️",
    }
    icon = icon_map.get(result.level, "❓")

    # Panel risultato
    content = f"""
Comando: [bold]{command}[/bold]

Rischio: [{color}]{icon} {result.level.value.upper()} ({result.score}/100)[/{color}]
Azione: [bold]{result.action.upper()}[/bold]

Motivi:
"""
    for reason in result.reasons:
        content += f"  • {reason}\n"

    if result.suggestion:
        content += f"\n💡 Suggerimento:\n  {result.suggestion}"

    panel = Panel(
        content,
        title=f"[bold]Analisi: {command[:50]}{'...' if len(command) > 50 else ''}[/bold]",
        border_style=color,
        box=box.DOUBLE,
    )

    console.print(panel)

    # Ritorna exit code appropriato
    if result.action == "block":
        return 1
    return 0


def cmd_daemon(args):
    """Comando daemon - modalità background."""
    console.print("[yellow]🚧 Modalità daemon in sviluppo[/yellow]")
    console.print("""
Nella versione completa, il daemon:
1. Monitora le sessioni Kimi CLI
2. Intercetta ogni tool call
3. Mostra prompt per operazioni rischiose
4. Logga tutto in ~/.kimi-guardian/logs/

Per ora usa: kimi-guardian check "comando"
""")
    return 0


def cmd_config(args):
    """Comando config - gestione configurazione."""
    config_dir = Path.home() / ".kimi-guardian"
    config_file = config_dir / "config.yml"

    if args.init:
        config_dir.mkdir(exist_ok=True)
        default_config = """# Kimi Guardian Configuration
security_level: normal  # paranoid | strict | normal | permissive

# Comandi sempre permessi (whitelist)
auto_allow:
  - "ls *"
  - "git status"
  - "git log"
  - "pwd"
  - "whoami"

# Comandi sempre bloccati (blacklist)
auto_block:
  - "rm -rf /"
  - "curl *|*bash"
  - "wget *|*bash"
  - "mkfs.*"

# Richiedi conferma per questi
ask_confirm:
  - "sudo *"
  - "rm -rf *"
  - "* ~/.ssh/*"
  - "* ~/.gnupg/*"
  - "git push --force"
  - "git reset --hard"

# Logging
log_file: ~/.kimi-guardian/guardian.log
log_level: INFO  # DEBUG | INFO | WARNING | ERROR
"""
        config_file.write_text(default_config)
        console.print(f"[green]✅ Configurazione creata in {config_file}[/green]")
        return 0

    if config_file.exists():
        console.print(f"[cyan]Configurazione attuale ({config_file}):[/cyan]")
        console.print(config_file.read_text())
    else:
        console.print(
            "[yellow]Configurazione non trovata. Usa --init per crearla.[/yellow]"
        )

    return 0


def cmd_interactive():
    """Modalità interattiva."""
    print_banner()
    console.print(
        "[dim]Modalità interattiva. Scrivi un comando da analizzare, o 'q' per uscire.\n"
    )

    while True:
        try:
            cmd = console.input("[bold green]📝 Comando> [/bold green]").strip()

            if cmd.lower() in ("q", "quit", "exit"):
                console.print("[dim]👋 Arrivederci![/dim]")
                break

            if not cmd:
                continue

            # Analizza
            result = classify_command(cmd)

            # Stampa risultato compatto
            icons = {
                RiskLevel.LOW: "✅",
                RiskLevel.MEDIUM: "⚠️",
                RiskLevel.HIGH: "🛑",
                RiskLevel.CRITICAL: "☠️",
            }

            console.print(
                f"{icons.get(result.level)} [{result.level.value.upper()}] {result.action}"
            )
            if result.reasons:
                console.print(f"   └─ {result.reasons[0]}")

            if result.action in ("ask", "block"):
                if result.suggestion:
                    console.print(f"   💡 {result.suggestion}")

                if result.action == "ask":
                    confirm = console.input(
                        "   [yellow]Procedere? [s/N]: [/yellow]"
                    ).lower()
                    if confirm == "s":
                        console.print("   [green]✓ Comando approvato[/green]")
                    else:
                        console.print("   [red]✗ Comando rifiutato[/red]")

            console.print()

        except KeyboardInterrupt:
            console.print("\n[dim]👋 Arrivederci![/dim]")
            break
        except EOFError:
            break

    return 0


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        prog="kimi-guardian",
        description="🛡️ Kimi Guardian - AI Agent Security Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  kimi-guardian check "rm -rf /tmp/old"     # Analizza comando
  kimi-guardian check --level strict "sudo apt update"
  kimi-guardian config --init               # Crea config default
  kimi-guardian                             # Modalità interattiva
        """,
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Comandi disponibili")

    # Comando check
    check_parser = subparsers.add_parser("check", help="Analizza un comando")
    check_parser.add_argument("command", nargs="+", help="Comando da analizzare")
    check_parser.add_argument(
        "--level",
        choices=["paranoid", "strict", "normal", "permissive"],
        default="normal",
        help="Livello di sicurezza (default: normal)",
    )

    # Comando daemon
    daemon_parser = subparsers.add_parser(
        "daemon", help="Modalità background (in sviluppo)"
    )
    daemon_parser.add_argument(
        "action", choices=["start", "stop", "status"], help="Azione daemon"
    )

    # Comando config
    config_parser = subparsers.add_parser("config", help="Gestione configurazione")
    config_parser.add_argument(
        "--init", action="store_true", help="Crea configurazione default"
    )

    # Parse args
    args = parser.parse_args()

    # Nessun comando = modalità interattiva
    if args.command is None:
        return cmd_interactive()

    # Esegui comando
    if args.command == "check":
        return cmd_check(args)
    elif args.command == "daemon":
        return cmd_daemon(args)
    elif args.command == "config":
        return cmd_config(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
