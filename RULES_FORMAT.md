# 📋 Kimi Guardian Rules Format

> Formato YAML delle regole compatibile con **Sage (Avast/Gen Digital)**

---

## 🎯 Overview

Kimi Guardian usa un sistema di regole YAML che prende ispirazione da **Sage** di Gen Digital.

**Vantaggi del formato YAML:**
- ✅ Leggibile e modificabile
- ✅ Versionabile (git)
- ✅ Estendibile
- ✅ Compatibile con Sage ( Detection Rule License 1.1)

---

## 📁 Struttura

```
rules/
├── manifest.yml      # Manifest e configurazione globale
├── filesystem.yml    # Operazioni filesystem
├── network.yml       # Operazioni di rete
├── execution.yml     # Esecuzione comandi
├── git.yml           # Operazioni git
└── secrets.yml       # Dati sensibili
```

---

## 📝 Formato Regola

```yaml
version: "1.0"  # Versione del file
description: "Descrizione categoria"
author: "Nome Autore"

rules:
  - id: KG-CAT-001           # ID univoco (KG = Kimi Guardian)
    name: "Nome Regola"      # Nome leggibile
    category: filesystem     # Categoria
    severity: critical       # low | medium | high | critical
    description: "Descrizione"
    
    patterns:                # Lista pattern da matchare
      - pattern: 'regex.*pattern'
        regex: true          # true = regex, false = stringa
      - pattern: 'altro pattern'
        regex: true
    
    action: block            # allow | ask | block
    message: "Messaggio all'utente"
    suggestion: "Suggerimento alternativo"
    
    references:              # Link documentazione
      - https://example.com/docs
    
    exceptions:              # Eccezioni al match
      - pattern: 'eccezione.*specifica'
        reason: "Perché è sicuro"
```

---

## 🎨 Severity Levels

| Livello | Icona | Score | Uso |
|---------|-------|-------|-----|
| **low** | ℹ️ | 10 | Informativo |
| **medium** | ⚠️ | 30 | Richiede attenzione |
| **high** | 🛑 | 60 | Pericoloso |
| **critical** | ☠️ | 100 | Distruttivo |

---

## 🔧 Actions

| Azione | Descrizione |
|--------|-------------|
| **allow** | Esegui senza warning |
| **ask** | Chiedi conferma all'utente |
| **block** | Blocca e richiedi override |

---

## 💡 Esempio Completo

```yaml
# rules/filesystem.yml
version: "1.0"
description: "Filesystem operations"
author: "Kimi Guardian Team"

rules:
  - id: KG-FILE-001
    name: "Root filesystem deletion"
    category: filesystem
    severity: critical
    description: "Attempt to delete entire root filesystem"
    patterns:
      - pattern: 'rm\s+-rf\s+/\s*$'
        regex: true
      - pattern: 'rm\s+--recursive\s+--force\s+/\s*$'
        regex: true
    action: block
    message: "🛑 CRITICAL: Attempted deletion of root filesystem!"
    suggestion: "If you really want to wipe the system, use 'sudo mkfs.ext4 /dev/sda1'"
    references:
      - https://en.wikipedia.org/wiki/Rm_(Unix)
    
  - id: KG-FILE-002
    name: "Home directory deletion"
    category: filesystem
    severity: high
    description: "Attempt to delete home directory"
    patterns:
      - pattern: 'rm\s+-rf\s+~\b'
        regex: true
    action: ask
    message: "⚠️  HIGH RISK: Home directory deletion"
    suggestion: "Use 'rm -ri ~/' for interactive mode"
    exceptions:
      - pattern: 'rm\s+-rf\s+~/\.cache/'
        reason: "Cache cleanup is generally safe"
```

---

## 🎯 Pattern Regex

### Sintassi supportata

```yaml
patterns:
  # Match esatto
  - pattern: 'rm -rf /'
    regex: false
  
  # Regex semplice
  - pattern: 'rm\s+-rf\s+/'
    regex: true
  
  # Regex complesso
  - pattern: 'curl.*\|.*(ba)?sh'
    regex: true
```

### Caratteri speciali comuni

| Pattern | Significato |
|---------|-------------|
| `\s+` | Uno o più spazi |
| `.*` | Qualsiasi carattere (0+) |
| `\b` | Word boundary |
| `\w+` | Parola (lettere/numeri) |
| `()` | Gruppo di cattura |
| `\|` | OR logico |

---

## 🚫 Eccezioni

Le eccezioni permettono di escludere pattern specifici:

```yaml
rules:
  - id: KG-EXEC-001
    name: "Recursive deletion"
    patterns:
      - pattern: 'rm\s+-rf\s+'
        regex: true
    action: ask
    exceptions:
      # Non matchare se è /tmp
      - pattern: 'rm\s+-rf\s+/tmp/'
        reason: "Cleaning /tmp is safe"
      # Non matchare se è /var/tmp
      - pattern: 'rm\s+-rf\s+/var/tmp/'
        reason: "Cleaning /var/tmp is safe"
```

---

## 📊 Manifest

Il file `manifest.yml` contiene la configurazione globale:

```yaml
version: "1.0.0"
description: "Default threat rules"

# Categorie
categories:
  - name: filesystem
    description: "Filesystem operations"
    file: filesystem.yml
    default_action: ask

# Impostazioni globali
global:
  min_severity: low
  default_behavior: allow
  audit_mode: false
  allow_user_rules: true

# Whitelist
global_whitelist:
  - pattern: "^ls\\s+"
    description: "List commands"
  - pattern: "^git\\s+status"
    description: "Git status"
```

---

## 🔧 Regole Personalizzate

Gli utenti possono aggiungere regole personali:

```bash
mkdir -p ~/.kimi-guardian/rules
```

```yaml
# ~/.kimi-guardian/rules/custom.yml
version: "1.0"
description: "My custom rules"

rules:
  - id: KG-CUSTOM-001
    name: "Don't delete my project"
    category: custom
    severity: critical
    patterns:
      - pattern: 'rm\s+-rf\s+.*/my-important-project'
        regex: true
    action: block
    message: "NO! Don't delete my project!"
```

---

## 🔄 Compatibilità Sage

Le regole sono **ispirate** a Sage ma con alcune differenze:

| Feature | Sage | Kimi Guardian |
|---------|------|---------------|
| Format | YAML | ✅ YAML |
| ID | `SAGE-*` | `KG-*` |
| Severity | `INFO/WARNING/CRITICAL` | `low/medium/high/critical` |
| Action | `ALLOW/WARN/BLOCK` | `allow/ask/block` |
| Cloud | ✅ | ❌ Locale only |

### Convertire regole Sage

```python
# Sage rule -> Kimi Guardian
{
  "id": "SAGE-FILE-001",
  "severity": "CRITICAL",
  "action": "BLOCK"
}
# Diventa:
{
  "id": "KG-FILE-001",
  "severity": "critical",
  "action": "block"
}
```

---

## 📚 Best Practices

1. **ID univoci**: Usa formato `KG-CATEGORY-###`
2. **Regex tested**: Verifica i pattern con regex101.com
3. **Messaggi chiari**: Spiega il rischio e suggerisci alternative
4. **Eccezioni specifiche**: Evita falsi positivi
5. **Documenta**: Aggiungi references per apprendimento

---

## 🎓 Esempi per Categoria

### Filesystem
```yaml
- pattern: 'rm\s+-rf\s+/'
  severity: critical
  action: block
```

### Network
```yaml
- pattern: 'curl.*\|.*bash'
  severity: high
  action: ask
```

### Secrets
```yaml
- pattern: 'cat\s+.*\.ssh/id_rsa'
  severity: high
  action: ask
```

---

> 📖 **Nota**: Le regole sono con licenza **Detection Rule License 1.1**  
> (compatibile con Sage di Gen Digital)
