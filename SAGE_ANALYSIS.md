# 📊 Analisi Tecnica: Sage (Avast) vs Kimi Guardian

## 🏗️ Architettura Sage (dal repository ufficiale)

```
Sage (Avast/Gen Digital)
│
├── Hook Systems (Intercettazione)
│   ├── Claude Code → Plugin marketplace
│   ├── Cursor/VS Code → Extension
│   └── OpenClaw → NPM plugin
│
├── Detection Layers
│   ├── URL Reputation (cloud)
│   ├── Local Heuristics (YAML rules)
│   ├── Package Supply-chain (npm/PyPI)
│   └── Plugin Scanning
│
└── Verdicts
    ├── ALLOW
    ├── WARN
    └── BLOCK
```

### Componenti Chiave

| Componente | Tecnologia | Note |
|------------|-----------|------|
| **Hook System** | Node.js/TypeScript | Plugin-based |
| **Threat Rules** | YAML | Detection Rule License 1.1 |
| **URL Check** | Cloud API (Gen Digital) | Hash-based lookup |
| **Package Check** | Registry API | npm/PyPI metadata |
| **Privacy** | Parziale | URL hash inviati, comandi locali |

---

## 🔍 Confronto Dettagliato

### Intercettazione

| Aspetto | Sage | Kimi Guardian |
|---------|------|---------------|
| **Livello** | Plugin API | Shell/Wrapper |
| **Tecnologia** | Node.js/TS | Python |
| **Approccio** | Hook nativo | Pre-execution check |
| **Delay** | Minimo (hook) | ~5ms (pattern match) |

**Vantaggio Sage**: Hook nativo nelle API degli agenti
**Vantaggio Kimi**: Non richiede modifiche all'agente, funziona con qualsiasi terminale

### Detection Engine

| Feature | Sage | Kimi Guardian |
|---------|------|---------------|
| **Pattern Matching** | ✅ YAML rules | ✅ Regex Python |
| **URL Reputation** | ✅ Cloud API | ❌ Non ancora |
| **Package Checks** | ✅ npm/PyPI metadata | ❌ Non ancora |
| **Heuristics** | ✅ Multi-layer | ✅ Score-based |
| **ML/AI** | ✅ (cloud) | ❌ No (by design) |

### Privacy

| Dato | Sage | Kimi Guardian |
|------|------|---------------|
| **Comandi** | ✅ Locale | ✅ Locale |
| **File content** | ✅ Locale | ✅ Locale |
| **URL** | ⚠️ Hash a Gen Digital | ✅ Locale |
| **Package names** | ⚠️ A registry | ✅ Locale |
| **Fully offline** | ⚠️ Opzionale | ✅ Sempre |

### Deployment

| Piattaforma | Sage | Kimi Guardian |
|-------------|------|---------------|
| Claude Code | ✅ Plugin | ❌ No hook API |
| Cursor/VS Code | ✅ Extension | ❌ No extension API |
| OpenClaw | ✅ Plugin | ❌ No plugin system |
| **Kimi CLI** | ❌ Non supportato | ✅ **Nostro target** |
| Altri terminali | ❌ No | ✅ Shell wrapper |

---

## 📦 Cosa Possiamo Apprendere da Sage

### 1. **Threat Rules YAML**

Sage usa YAML per le regole. Possiamo adottare lo stesso formato:

```yaml
# threats/dangerous_commands.yml (inspired by Sage)
rules:
  - id: CMD-001
    name: "Filesystem destruction"
    pattern: 'rm\s+-rf\s+/\s*$'
    severity: critical
    action: block
    description: "Deletion of root filesystem"
    
  - id: CMD-002  
    name: "Remote code execution"
    pattern: 'curl.*\|.*bash'
    severity: high
    action: ask
    description: "Piping remote content to shell"
```

### 2. **Multi-Layer Detection**

Sage controlla su più livelli:
- Pattern matching (locale)
- URL reputation (cloud)
- Package metadata (registry)

Per Kimi Guardian potremmo aggiungere:
- Local file reputation (hash database)
- Static analysis di script scaricati
- Check di dipendenze (requirements.txt, package.json)

### 3. **Plugin Architecture**

Sage è modulare. Kimi Guardian potrebbe avere:
- Plugin system per check custom
- Community rules repository
- Integrazione con tool esterni (bandit, safety, etc.)

---

## 🚀 Miglioramenti Proposti per Kimi Guardian v1.1

### Basati su Sage

#### 1. **Threat Rules YAML Standard**
Adottare formato simile a Sage per compatibilità:

```yaml
# ~/.kimi-guardian/rules/custom.yml
version: "1.0"
rules:
  - id: KG-001
    name: "Dangerous deletion"
    category: filesystem
    patterns:
      - 'rm\s+-rf\s+/\s*'
      - 'rm\s+-rf\s+~'
    severity: critical
    action: block
    message: "Attempted filesystem deletion"
    suggestion: "Use 'rm -i' or specify exact paths"
```

#### 2. **URL Reputation Locale**
Invece di cloud (privacy), mantenere database locale:

```python
# Local URL blacklist
MALICIOUS_URLS = [
    "pastebin.com/raw",  # Often used for malware
    "bit.ly",           # URL shorteners
    # ... loaded from ~/.kimi-guardian/bad_urls.txt
]
```

#### 3. **Package Supply-Chain Check**
Controllo base dei pacchetti:

```python
def check_package_safety(package_name, registry="pypi"):
    """Check package against known vulnerabilities."""
    # Integrazione con safety-db o OSV
    # Locale, no API esterne
```

#### 4. **Session Scanning**
Come Sage scansiona plugin all'avvio:

```bash
# kimi-guardian session-start
# Verifica:
# - File .env esposti
# - Chiavi API hardcoded
# - Dipendenze vulnerabili (requirements.txt)
```

---

## 🎯 Differenziazione Strategica

### Kimi Guardian NON deve copiare Sage:

1. **No Cloud Dependencies**: Mantenere 100% offline
2. **No ML**: Pattern matching deterministico (spiegabile)
3. **Focus Terminal**: Non IDE extension
4. **Simplicity**: Un file Python principale, non monorepo

### Kimi Guardian DEVE essere:

1. **Kimi CLI Native**: Integrazione specifica con Kimi
2. **Zero Config**: Funziona out-of-the-box
3. **Fast**: <10ms overhead
4. **Hackable**: Facile da modificare (single file)

---

## 📚 Riferimenti

- **Sage Repository**: https://github.com/avast/sage
- **Licenza**: Apache 2.0 (codice), Detection Rule License 1.1 (regole)
- **Autore**: Gen Digital Inc. (Avast)

---

## ✅ Conclusione

Sage è un'ottima reference architetturale. Possiamo:

1. **Inspirarci** al formato YAML delle regole
2. **Adottare** il concetto di multi-layer detection
3. **Differenziarci** mantenendo 100% offline e lightweight
4. **Collaborare** se le regole YAML sono compatibili

**Kimi Guardian** rimane la scelta per:
- Utenti paranoici sulla privacy
- Ambienti air-gapped
- Chi usa Kimi CLI (non supportato da Sage)
- Developer che vogliono hackare il tool
