# 🔌 Kimi Guardian MCP Plugin

> Model Context Protocol (MCP) integration per Kimi CLI

---

## Cos'è MCP?

**Model Context Protocol (MCP)** è un protocollo aperto standardizzato per connettere AI assistants con tool e dati esterni.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Kimi CLI  │◄───►│  MCP Server │◄───►│   Tools     │
│   (Client)  │     │  (Guardian) │     │  (Security) │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 🏗️ Architettura

### MCP Server Mode

```python
# guardian/mcp_server.py

class GuardianMCPServer:
    """MCP Server per Kimi Guardian"""
    
    def __init__(self):
        self.classifier = RiskClassifier()
    
    def handle_tool_call(self, tool_name, params):
        """Intercetta tool calls da Kimi"""
        if tool_name == "Shell":
            return self.check_shell_command(params["command"])
        elif tool_name == "WriteFile":
            return self.check_file_write(params["path"], params["content"])
        elif tool_name == "ReadFile":
            return self.check_file_read(params["path"])
    
    def check_shell_command(self, command):
        result = self.classifier.classify(command)
        if result.action == "block":
            return {
                "allowed": False,
                "reason": result.reasons[0],
                "suggestion": result.suggestion
            }
        elif result.action == "ask":
            return {
                "allowed": True,
                "warning": result.reasons[0],
                "requires_confirmation": True
            }
        return {"allowed": True}
```

---

## 🔧 Implementazione

### 1. MCP Server

```python
#!/usr/bin/env python3
"""
🛡️ Kimi Guardian MCP Server
Integrazione nativa con Kimi CLI via MCP
"""

import json
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from guardian.classifier_v2 import RiskClassifier, RiskLevel


class GuardianMCPServer:
    """MCP Server implementation for Kimi Guardian"""
    
    def __init__(self):
        self.classifier = RiskClassifier()
        self.name = "kimi-guardian"
        self.version = "1.1.0"
    
    def handle_initialize(self, params):
        """Handle MCP initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listChanged": False
                },
                "resources": {},
                "prompts": {}
            },
            "serverInfo": {
                "name": self.name,
                "version": self.version
            },
            "tools": [
                {
                    "name": "guardian_check",
                    "description": "Check if a command is safe to execute",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Command to check"
                            },
                            "tool": {
                                "type": "string",
                                "enum": ["Shell", "WriteFile", "ReadFile"],
                                "description": "Tool being used"
                            }
                        },
                        "required": ["command", "tool"]
                    }
                },
                {
                    "name": "guardian_explain",
                    "description": "Explain why a command was flagged",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "rule_id": {
                                "type": "string",
                                "description": "Rule ID to explain"
                            }
                        },
                        "required": ["rule_id"]
                    }
                }
            ]
        }
    
    def handle_tool_call(self, name, arguments):
        """Handle tool invocations"""
        if name == "guardian_check":
            return self._check_command(
                arguments.get("command", ""),
                arguments.get("tool", "Shell")
            )
        elif name == "guardian_explain":
            return self._explain_rule(arguments.get("rule_id", ""))
        else:
            return {"error": f"Unknown tool: {name}"}
    
    def _check_command(self, command, tool_type):
        """Check command safety"""
        result = self.classifier.classify(command)
        
        # Map to MCP response
        icons = {
            RiskLevel.LOW: "✅",
            RiskLevel.MEDIUM: "⚠️",
            RiskLevel.HIGH: "🛑",
            RiskLevel.CRITICAL: "☠️"
        }
        
        response = {
            "level": result.level.value,
            "score": result.score,
            "action": result.action,
            "icon": icons.get(result.level, "❓"),
            "reasons": result.reasons,
            "allowed": result.action != "block"
        }
        
        if result.suggestion:
            response["suggestion"] = result.suggestion
        
        if result.matched_rules:
            response["matched_rules"] = [
                {"id": r.id, "name": r.name, "category": r.category}
                for r in result.matched_rules
            ]
        
        return response
    
    def _explain_rule(self, rule_id):
        """Explain a specific rule"""
        # Find rule
        for rule in self.classifier.loader.rules:
            if rule.id == rule_id:
                return {
                    "id": rule.id,
                    "name": rule.name,
                    "category": rule.category,
                    "severity": rule.severity.value,
                    "description": rule.description,
                    "message": rule.message,
                    "suggestion": rule.suggestion,
                    "references": rule.references
                }
        return {"error": f"Rule {rule_id} not found"}
    
    def run_stdio(self):
        """Run in stdio mode (for MCP)"""
        while True:
            try:
                line = input()
                if not line:
                    continue
                
                message = json.loads(line)
                method = message.get("method", "")
                msg_id = message.get("id")
                params = message.get("params", {})
                
                response = {"jsonrpc": "2.0", "id": msg_id}
                
                if method == "initialize":
                    response["result"] = self.handle_initialize(params)
                elif method == "tools/list":
                    response["result"] = {"tools": self.handle_initialize({})["tools"]}
                elif method == "tools/call":
                    name = params.get("name", "")
                    arguments = params.get("arguments", {})
                    response["result"] = self.handle_tool_call(name, arguments)
                elif method == "notifications/initialized":
                    continue  # No response needed
                else:
                    response["error"] = {"code": -32601, "message": f"Method not found: {method}"}
                
                print(json.dumps(response), flush=True)
                
            except EOFError:
                break
            except json.JSONDecodeError as e:
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": f"Parse error: {e}"}
                }), flush=True)
            except Exception as e:
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "error": {"code": -32603, "message": f"Internal error: {e}"}
                }), flush=True)


def main():
    """Entry point"""
    server = GuardianMCPServer()
    server.run_stdio()


if __name__ == "__main__":
    main()
```

---

## 🔌 Configurazione Kimi

### File di config MCP

```json
// ~/.config/kimi/mcp.json
{
  "mcpServers": {
    "kimi-guardian": {
      "command": "python3",
      "args": ["-m", "guardian.mcp_server"],
      "env": {
        "GUARDIAN_LEVEL": "normal"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Oppure via CLI

```bash
# Registra MCP server
kimi mcp add kimi-guardian \
  --command "python3 -m guardian.mcp_server" \
  --cwd ~/zed-plus-kimi/kimi_guardian

# Verifica
kimi mcp list
```

---

## 🎮 Uso con Kimi

### Esempio Interazione

```
Utente: Rimuovi tutti i file in /tmp

Kimi: Eseguo: rm -rf /tmp/*

🛡️ MCP kimi-guardian:
   Comando analizzato: rm -rf /tmp/*
   Risultato: ⚠️ MEDIUM (35/100)
   Azione: ask
   Motivo: Cancellazione ricorsiva in /tmp
   
   [Procedi] [Modifica] [Annulla]

Kimi: ⚠️ L'operazione richiede conferma. Procedo?

Utente: Sì

Kimi: ✅ Comando eseguito: rm -rf /tmp/*
```

### Tool MCP Disponibili

```python
# Kimi chiama automaticamente:

guardian_check(
    command="rm -rf /",
    tool="Shell"
)
# Ritorna: {"allowed": false, "reason": "...", "action": "block"}

guardian_explain(
    rule_id="KG-FILE-001"
)
# Ritorna: dettagli regola
```

---

## 🔄 Flusso Dati

```
1. Kimi CLI riceve richiesta utente
2. Kimi pensa: "Devo usare Shell tool"
3. Kimi → MCP guardian_check()
4. Guardian analizza e ritorna verdict
5. Se BLOCK: Kimi rifiuta
6. Se ASK: Kimi chiede conferma
7. Se ALLOW: Kimi procede
```

---

## 📊 Vantaggi MCP vs Wrapper

| Feature | Wrapper Script | MCP Plugin |
|---------|---------------|------------|
| **Integrazione** | Esterna | **Nativa** |
| **Trasparenza** | Utente vede check | **Trasparente** |
| **Azione su block** | Stop script | **Kimi gestisce** |
| **Setup** | Alias necessario | **Configura una volta** |
| **Portabilità** | Shell-specific | **Standard MCP** |

---

## 🧪 Test

```bash
# Avvia MCP server standalone
python3 -m guardian.mcp_server

# Test con input JSON
echo '{"method": "initialize", "id": 1, "params": {}}' | \
  python3 -m guardian.mcp_server

# Test tool call
echo '{
  "method": "tools/call",
  "id": 2,
  "params": {
    "name": "guardian_check",
    "arguments": {
      "command": "rm -rf /",
      "tool": "Shell"
    }
  }
}' | python3 -m guardian.mcp_server
```

---

## 🚀 Deployment

### Installazione completa

```bash
cd ~/zed-plus-kimi/kimi_guardian

# 1. Installa dipendenze
pip install -e .

# 2. Configura MCP
mkdir -p ~/.config/kimi
cat > ~/.config/kimi/mcp.json << 'EOF'
{
  "mcpServers": {
    "kimi-guardian": {
      "command": "python3",
      "args": ["-m", "guardian.mcp_server"],
      "cwd": "HOME/zed-plus-kimi/kimi_guardian"
    }
  }
}
EOF

# 3. Verifica
kimi mcp list
# dovrebbe mostrare: kimi-guardian ✅
```

---

## 📝 Note

- MCP è un protocollo **standard aperto**
- Supportato da Claude Desktop, Cursor, e **speriamo presto Kimi**
- Kimi Guardian MCP funziona con **qualsiasi client MCP**

---

🔌 **Integrazione nativa con MCP per sicurezza trasparente!**
