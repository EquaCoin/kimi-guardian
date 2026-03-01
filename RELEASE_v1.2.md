# 🚀 Kimi Guardian v1.2 - Release Notes

**Release Date**: 2026-03-01  
**Codename**: "Secure Bridge"

---

## 🎯 Release Focus

Due feature major:
1. **Sage-compatible YAML Rules**
2. **MCP Plugin Integration**

---

## ✨ Feature #1: YAML Rules System

### 38 Regole in 5 Categorie

```
filesystem/   - 7 regole (rm, chmod, mkfs...)
network/      - 7 regole (curl, wget, nc...)
execution/    - 8 regole (sudo, eval, docker...)
git/          - 8 regole (push --force, reset...)
secrets/      - 8 regole (.ssh, .env, AWS...)
```

### Formato

```yaml
rules:
  - id: KG-FILE-001
    name: "Root filesystem deletion"
    severity: critical
    patterns:
      - pattern: 'rm\s+-rf\s+/\s*$'
        regex: true
    action: block
    message: "🛑 CRITICAL: Attempted deletion!"
```

### Vantaggi
- ✅ Leggibile e modificabile
- ✅ Versionabile (git)
- ✅ Compatibile Sage (DRL 1.1)

---

## ✨ Feature #2: MCP Plugin

### Model Context Protocol Server

```python
# guardian/mcp_server.py
class GuardianMCPServer:
    def handle_tool_call(self, name, arguments):
        if name == "guardian_check":
            return self._check_command(arguments["command"])
```

### Tool MCP

| Tool | Scopo |
|------|-------|
| `guardian_check` | Analizza comando shell |
| `guardian_check_file` | Verifica file operation |
| `guardian_stats` | Statistiche regole |

### Configurazione Kimi

```json
{
  "mcpServers": {
    "kimi-guardian": {
      "command": "python3",
      "args": ["-m", "guardian.mcp_server"]
    }
  }
}
```

---

## 📊 Statistiche

| Metrica | Valore |
|---------|--------|
| Regole totali | 38 |
| Categorie | 5 |
| File YAML | 6 |
| Linee codice | ~2000 |
| Dipendenze | 2 (rich, pyyaml) |

---

## 🧪 Test

```bash
$ ./kg "rm -rf /"
☠️ [CRITICAL] block
   Score: 100/100
   Motivo: Cancellazione filesystem root

$ ./kg "git status"
✅ [LOW] auto
   Comando sicuro

$ echo '{"method":"tools/call",...}' | python3 -m guardian.mcp_server
{"result": {"level": "critical", "action": "block"}}
```

---

## 🔄 Confronto v1.0 → v1.2

| v1.0 | v1.2 |
|------|------|
| Regex hardcoded | ✅ YAML rules |
| Solo wrapper | ✅ + MCP server |
| 15 regole | ✅ 38 regole |
| No categorie | ✅ 5 categorie |

---

## 🙏 Credit

- **Sage (Gen Digital/Avast)**: Ispirazione formato YAML
- **MCP**: Protocollo aperto per AI assistants
- **Kimi**: AI assistant che stiamo proteggendo

---

## 🚀 Prossima Release

**v1.3** - Pre-commit hooks per Git

---

🛡️ **Versione 1.2 pronta per l'uso!**
