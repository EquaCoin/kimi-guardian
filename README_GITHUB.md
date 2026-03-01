# 🛡️ Kimi Guardian

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> AI Agent Security Scanner for [Kimi Code CLI](https://kimi.moonshot.cn/) and terminal-based AI assistants

**Kimi Guardian** intercepts and analyzes AI tool calls (shell commands, file operations) before execution, protecting you from dangerous operations.

![Demo](docs/demo.gif)

---

## ✨ Features

### 🔒 Security First
- **38 threat detection rules** across 5 categories
- **Sage-compatible** YAML rule format
- **100% offline** - no data leaves your machine
- **Zero configuration** - works out of the box

### 🔌 Native Integration
- **MCP Plugin** - Model Context Protocol support
- **Pre-commit hooks** - Block secrets before git commit
- **CLI wrapper** - Quick command checking

### 🎯 Smart Detection
| Category | Detects | Action |
|----------|---------|--------|
| **Filesystem** | `rm -rf /`, `mkfs`, `chmod 777` | BLOCK/ASK |
| **Network** | `curl \| bash`, URL shorteners | ASK |
| **Execution** | `sudo`, `eval`, `docker --privileged` | ASK |
| **Git** | `push --force`, `reset --hard` | ASK |
| **Secrets** | `.ssh/id_rsa`, `.env`, API keys | ASK |

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/equacoin/kimi-guardian.git
cd kimi-guardian

# Install dependencies
pip install rich pyyaml

# Make executable
chmod +x kg
```

### Usage

```bash
# Check a command
./kg "rm -rf /"
# ☠️ [CRITICAL] block
#     Score: 100/100
#     Suggestion: Use 'rm -rf /specific/path'

# Check safe command
./kg "git status"
# ✅ [LOW] auto
#     Command is safe
```

### Interactive Mode

```bash
./kg interactive

📝 Command> rm -rf ~/old_project
⚠️ [MEDIUM] ask
   Score: 35/100
   Reason: Recursive deletion

📝 Command> ls -la
✅ [LOW] auto
   Command is safe
```

---

## 🔌 MCP Integration

Kimi Guardian can integrate with Kimi CLI via Model Context Protocol:

```bash
# Start MCP server
python3 -m guardian.mcp_server
```

Then configure Kimi:

```json
// ~/.config/kimi/mcp.json
{
  "mcpServers": {
    "kimi-guardian": {
      "command": "python3",
      "args": ["-m", "guardian.mcp_server"],
      "cwd": "/path/to/kimi-guardian"
    }
  }
}
```

---

## 🔍 Pre-commit Hooks

Install Git hooks to check staged files before commit:

```bash
# Install in your repository
cd your-repo
~/kimi-guardian/install-hooks.sh

# Or manually
cp ~/kimi-guardian/guardian/precommit.py .git/hooks/pre-commit
```

Now every `git commit` is automatically scanned for secrets and dangerous commands.

---

## 📋 Rule Categories

```
rules/
├── filesystem.yml    # 7 rules - rm, chmod, mkfs...
├── network.yml       # 7 rules - curl, wget, nc...
├── execution.yml     # 8 rules - sudo, eval, docker...
├── git.yml           # 8 rules - force push, reset...
├── secrets.yml       # 8 rules - .ssh, .env, keys...
└── manifest.yml      # Configuration
```

### Example Rule

```yaml
rules:
  - id: KG-FILE-001
    name: "Root filesystem deletion"
    category: filesystem
    severity: critical
    patterns:
      - pattern: 'rm\s+-rf\s+/\s*$'
        regex: true
    action: block
    message: "🛑 CRITICAL: Attempted deletion of root filesystem!"
    suggestion: "Use 'rm -rf /specific/path' instead"
```

---

## 🆚 Comparison with Sage

| Feature | Sage (Gen) | Kimi Guardian |
|---------|-----------|---------------|
| **Kimi CLI** | ❌ | ✅ **Native** |
| **MCP Plugin** | ❌ | ✅ **Built-in** |
| **Pre-commit hooks** | ❌ | ✅ **Included** |
| **100% offline** | ⚠️ Partial | ✅ **Always** |
| **Cloud ML** | ✅ | ❌ |
| **Cost** | Freemium | ✅ **Free** |

**Complementary approaches!** Use both for layered security.

---

## 🤝 Collaboration with Sage

We propose collaboration with [Sage](https://github.com/avast/sage) (Avast/Gen Digital) to:

1. **Standardize YAML rule format** across AI security tools
2. **Extend Sage coverage** to Kimi CLI via MCP
3. **Create shared open-source rule repository**

See: [SAGE_PROPOSAL.md](SAGE_PROPOSAL.md)

---

## 🛠️ Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black guardian/
```

---

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- [RULES_FORMAT.md](RULES_FORMAT.md) - Writing custom rules
- [MCP_PLUGIN.md](MCP_PLUGIN.md) - MCP integration guide
- [PRECOMMIT_GUIDE.md](PRECOMMIT_GUIDE.md) - Pre-commit setup
- [SAGE_COMPARISON.md](SAGE_COMPARISON.md) - Detailed comparison

---

## 🤔 Why Kimi Guardian?

> "AI assistants are becoming the primary interface for software development. Security must be built-in, not bolted-on."

- **Privacy-first**: No cloud dependency, no data sharing
- **Fast**: ~5ms response time (local processing)
- **Transparent**: Open source, auditable rules
- **Hackable**: Easy to customize and extend

---

## 📄 License

- **Code**: [MIT License](LICENSE)
- **Rules**: [Detection Rule License 1.1](https://github.com/avast/sage/blob/main/LICENSE) (compatible with Sage)

---

## 🙏 Acknowledgments

- [Sage](https://github.com/avast/sage) by Gen Digital - Inspiration for YAML rule format
- [Kimi](https://kimi.moonshot.cn/) - AI assistant we're protecting
- [MCP](https://modelcontextprotocol.io/) - Protocol for AI integration

---

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/equacoin/kimi-guardian/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/equacoin/kimi-guardian/discussions)

---

**🛡️ Protect your terminal, protect your data!**
