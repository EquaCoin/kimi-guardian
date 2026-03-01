#!/bin/bash
# 🔧 Kimi Guardian - Installazione Pre-commit Hooks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(pwd)"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     🔧 Kimi Guardian Pre-commit Hook Installer          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Verifica che siamo in un repo git
if [ ! -d ".git" ]; then
    echo "❌ Errore: Non sei in un repository Git"
    echo "   Esegui 'git init' prima o vai nella root di un repo esistente"
    exit 1
fi

HOOK_FILE=".git/hooks/pre-commit"
GUARDIAN_CMD="python3 -m guardian.precommit check"

# Verifica se esiste già un hook
if [ -f "$HOOK_FILE" ]; then
    echo "⚠️  Esiste già un pre-commit hook"
    echo ""
    echo "Cosa vuoi fare?"
    echo "  [1] Sovrascrivi (backup automatico)"
    echo "  [2] Aggiungi Kimi Guardian all'hook esistente"
    echo "  [3] Annulla"
    echo ""
    read -p "Scelta [1/2/3]: " choice

    case $choice in
        1)
            # Backup
            cp "$HOOK_FILE" "$HOOK_FILE.backup.$(date +%Y%m%d%H%M%S)"
            echo "📦 Backup creato"

            # Crea nuovo hook
            cat > "$HOOK_FILE" << EOF
#!/bin/bash
# 🛡️ Kimi Guardian Pre-commit Hook
# Auto-generated on $(date)

cd "$(dirname "$0")/../.."

# Run Kimi Guardian check
echo "🔍 Running Kimi Guardian pre-commit check..."
$GUARDIAN_CMD
exit_code=\$?

if [ \$exit_code -ne 0 ]; then
    echo ""
    echo "⚠️  Kimi Guardian ha trovato problemi."
    echo "   Correggi prima di committare, o usa 'git commit --no-verify'"
    exit \$exit_code
fi
EOF
            ;;

        2)
            # Aggiungi a hook esistente
            echo "" >> "$HOOK_FILE"
            echo "# 🛡️ Kimi Guardian check" >> "$HOOK_FILE"
            echo "$GUARDIAN_CMD || exit 1" >> "$HOOK_FILE"
            echo "✅ Kimi Guardian aggiunto all'hook esistente"
            ;;

        3)
            echo "❌ Installazione annullata"
            exit 0
            ;;

        *)
            echo "❌ Scelta non valida"
            exit 1
            ;;
    esac
else
    # Crea nuovo hook
    cat > "$HOOK_FILE" << EOF
#!/bin/bash
# 🛡️ Kimi Guardian Pre-commit Hook
# Auto-generated on $(date)

cd "$(dirname "$0")/../.."

# Run Kimi Guardian check
echo "🔍 Running Kimi Guardian pre-commit check..."
$GUARDIAN_CMD
exit_code=\$?

if [ \$exit_code -ne 0 ]; then
    echo ""
    echo "⚠️  Kimi Guardian ha trovato problemi."
    echo "   Correggi prima di committare, o usa 'git commit --no-verify'"
    exit \$exit_code
fi
EOF
fi

# Rendi eseguibile
chmod +x "$HOOK_FILE"

echo ""
echo "✅ Pre-commit hook installato con successo!"
echo ""
echo "📍 Location: $HOOK_FILE"
echo ""
echo "📝 Cosa fa:"
echo "   • Controlla ogni file staged prima del commit"
echo "   • Cerca secrets (API keys, password, chiavi private)"
echo "   • Analizza script shell per comandi pericolosi"
echo "   • Blocca il commit se trova problemi critici"
echo ""
echo "⚡ Per saltare il controllo (emergenza):"
echo "   git commit --no-verify"
echo ""
echo "🔧 Per disinstallare:"
echo "   rm $HOOK_FILE"
