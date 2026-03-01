#!/usr/bin/env python3
"""
🔌 Kimi Guardian MCP Server
Model Context Protocol implementation for native Kimi CLI integration
"""

import json
import sys
from pathlib import Path

# Add parent to path for imports
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
                "tools": {"listChanged": False},
                "resources": {},
                "prompts": {},
            },
            "serverInfo": {"name": self.name, "version": self.version},
        }

    def handle_tools_list(self):
        """Return available tools"""
        return {
            "tools": [
                {
                    "name": "guardian_check",
                    "description": "Check if a shell command is safe to execute. "
                    "Analyzes the command for dangerous patterns "
                    "like 'rm -rf /', 'curl | bash', etc.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Shell command to analyze",
                            }
                        },
                        "required": ["command"],
                    },
                },
                {
                    "name": "guardian_check_file",
                    "description": "Check if a file operation is safe",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "File path being accessed",
                            },
                            "operation": {
                                "type": "string",
                                "enum": ["read", "write", "delete"],
                                "description": "Type of file operation",
                            },
                        },
                        "required": ["path", "operation"],
                    },
                },
                {
                    "name": "guardian_stats",
                    "description": "Get statistics about loaded security rules",
                    "inputSchema": {"type": "object", "properties": {}},
                },
            ]
        }

    def handle_tool_call(self, name, arguments):
        """Handle tool invocations"""
        if name == "guardian_check":
            return self._check_command(arguments.get("command", ""))
        elif name == "guardian_check_file":
            return self._check_file(
                arguments.get("path", ""), arguments.get("operation", "read")
            )
        elif name == "guardian_stats":
            return self._get_stats()
        else:
            return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

    def _check_command(self, command):
        """Check command safety and return MCP response"""
        if not command:
            return {
                "content": [{"type": "text", "text": "❌ No command provided"}],
                "isError": True,
            }

        result = self.classifier.classify(command)

        # Format response
        icons = {
            RiskLevel.LOW: "✅",
            RiskLevel.MEDIUM: "⚠️",
            RiskLevel.HIGH: "🛑",
            RiskLevel.CRITICAL: "☠️",
        }

        icon = icons.get(result.level, "❓")

        # Build response text
        lines = [
            f"{icon} **{result.level.value.upper()}** - Score: {result.score}/100",
            "",
            f"**Action:** {result.action.upper()}",
            "",
            "**Reasons:**",
        ]

        for reason in result.reasons:
            lines.append(f"  • {reason}")

        if result.suggestion:
            lines.extend(["", f"💡 **Suggestion:** {result.suggestion}"])

        if result.matched_rules:
            lines.extend(["", "**Matched Rules:**"])
            for rule in result.matched_rules[:3]:  # Show max 3
                lines.append(f"  • {rule.id}: {rule.name}")

        # Determine if blocked
        is_blocked = result.action == "block"

        return {
            "content": [{"type": "text", "text": "\n".join(lines)}],
            "isError": is_blocked,
            "data": {
                "level": result.level.value,
                "score": result.score,
                "action": result.action,
                "allowed": not is_blocked,
                "requires_confirmation": result.action == "ask",
            },
        }

    def _check_file(self, path, operation):
        """Check file operation safety"""
        sensitive_patterns = [
            (r"\.ssh/id_", "SSH private key"),
            (r"\.aws/credentials", "AWS credentials"),
            (r"\.env", "Environment file"),
            (r"\.gnupg", "GPG keys"),
            (r"passwd$", "Password file"),
            (r"shadow$", "Shadow password file"),
            (r"\.docker/config", "Docker registry credentials"),
        ]

        risks = []
        for pattern, desc in sensitive_patterns:
            import re

            if re.search(pattern, path, re.IGNORECASE):
                risks.append(desc)

        if risks:
            text = f"⚠️ **Sensitive file access detected**\n\n"
            text += f"**Path:** `{path}`\n"
            text += f"**Operation:** {operation}\n\n"
            text += "**Sensitive content:**\n"
            for risk in risks:
                text += f"  • {risk}\n"
            text += "\nEnsure you have authorization to access this file."

            return {
                "content": [{"type": "text", "text": text}],
                "data": {"sensitive": True, "risks": risks},
            }

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"✅ File operation appears safe\n\nPath: `{path}`\nOperation: {operation}",
                }
            ],
            "data": {"sensitive": False},
        }

    def _get_stats(self):
        """Get rule statistics"""
        stats = self.classifier.get_rule_stats()

        lines = [
            "📊 **Kimi Guardian Rules Statistics**",
            "",
            f"**Total Rules:** {stats['total']}",
            "",
            "**By Severity:**",
        ]

        for sev, count in stats["by_severity"].items():
            lines.append(f"  • {sev.capitalize()}: {count}")

        lines.extend(
            [
                "",
                "**Categories:**",
                "  • filesystem: Filesystem operations",
                "  • network: Network operations",
                "  • execution: Command execution",
                "  • git: Git operations",
                "  • secrets: Sensitive data access",
            ]
        )

        return {"content": [{"type": "text", "text": "\n".join(lines)}], "data": stats}

    def run_stdio(self):
        """Run in stdio mode (MCP standard)"""
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
                    response["result"] = self.handle_tools_list()
                elif method == "tools/call":
                    name = params.get("name", "")
                    arguments = params.get("arguments", {})
                    result = self.handle_tool_call(name, arguments)
                    response["result"] = result
                elif method == "notifications/initialized":
                    continue  # No response needed for notifications
                else:
                    response["error"] = {
                        "code": -32601,
                        "message": f"Method not found: {method}",
                    }

                print(json.dumps(response), flush=True)

            except EOFError:
                break
            except json.JSONDecodeError as e:
                self._send_error(-32700, f"Parse error: {e}", None)
            except Exception as e:
                self._send_error(
                    -32603,
                    f"Internal error: {e}",
                    msg_id if "msg_id" in locals() else None,
                )

    def _send_error(self, code, message, msg_id):
        """Send error response"""
        print(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": code, "message": message},
                }
            ),
            flush=True,
        )


def main():
    """Entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Kimi Guardian MCP Server")
    parser.add_argument("--version", action="version", version="%(prog)s 1.1.0")
    args = parser.parse_args()

    server = GuardianMCPServer()
    server.run_stdio()


if __name__ == "__main__":
    main()
