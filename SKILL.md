---
name: agent-registry
description: >
  Use this skill whenever the user wants to interact with Google Cloud's Agent Registry
  using gcloud commands. Triggers on any mention of "agent registry", "agent-registry",
  "mcp-servers", "gcloud agents", "register an agent", "list agents", "create a service",
  "agent service", or any request to manage agents, MCP servers, endpoints, or services
  in Google Cloud Agent Registry. Also triggers on requests to integrate or use the
  Google Agent Development Kit (ADK) with the Agent Registry.
metadata:
  author: srinandan
  version: "0.1"
---

# Google Cloud Agent Registry Skill

Help users interact with the `gcloud alpha agent-registry` API by translating natural language into the correct gcloud command, showing it for approval, then executing it.

## Workflow

1. **Resolve session context** — at the start of each session, silently run:
   ```bash
   gcloud config get-value project 2>/dev/null
   gcloud config get-value compute/region 2>/dev/null
   ```
   Store the results as `SESSION_PROJECT` and `SESSION_LOCATION`. Use these as defaults.

2. **Parse** the user's request to identify the resource and action.
3. **Construct** the gcloud command using session defaults.
4. **Approval**:
   - For `list` and `describe` commands: Skip explicit approval and execute immediately.
   - For `create`, `delete`, or `update` commands: Show the command and ask for approval: _"Ready to run this command? (yes/no)"_
5. **Execute** and display the output.

## Auth & Setup

```bash
# Check auth
gcloud auth list

# Login
gcloud auth login

# Set project
gcloud config set project PROJECT_ID

# (Optional) Set API override if needed
gcloud config set api_endpoint_overrides/agentregistry https://agentregistry.googleapis.com/
```

### IAM Permissions

| Role | Access Level |
|------|--------------|
| `roles/agentregistry.admin` | Full administrative access |
| `roles/agentregistry.editor` | Editor access |
| `roles/agentregistry.viewer` | Read only access |

---

## Resource Types & Registration

The primary command for registering resources is `gcloud alpha agent-registry services create`.

### 1. MCP Servers
Used to register Model Context Protocol servers.

```bash
# Register an MCP Server (example: GitHub)
# Ask user to paste contents of mcp-spec.json for --mcp-server-spec-content
gcloud alpha agent-registry services create github \
  --location=us-central1 \
  --display-name="GitHub MCP Server" \
  --description="Connects to GitHub" \
  --mcp-server-spec-type=tool-spec \
  --mcp-server-spec-content='PASTE_MCP_SPEC_JSON_HERE' \
  --interfaces='[{"protocolBinding": "jsonrpc", "url": "https://api.github.com/mcp"}]'

# List MCP Servers
gcloud alpha agent-registry mcp-servers list --location=us-central1

# Filter MCP Servers by Runtime
gcloud alpha agent-registry mcp-servers list \
  --location=us-central1 \
  --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"

# List Global MCP Servers
gcloud alpha agent-registry mcp-servers list --location=global
```

### 2. Agents
Used to register AI agents (e.g., A2A, Salesforce).

```bash
# Register an Agent (example: Salesforce)
gcloud alpha agent-registry services create salesforce \
  --location=us-central1 \
  --display-name="Salesforce Agent" \
  --description="Salesforce Einstein Agent" \
  --agent-spec-type=no-spec \
  --interfaces='[{"protocolBinding": "http-json", "url": "https://api.salesforce.com/agent/v1"}]'

# Register an A2A Agent (Special Case)
# Ask user to paste contents of agent_card.json for --agent-spec-content
gcloud alpha agent-registry services create testa2a \
  --location=us-central1 \
  --display-name="Test A2A Agent" \
  --description="Sample A2A Agent" \
  --agent-spec-type=a2a-agent-card \
  --agent-spec-content='PASTE_AGENT_CARD_JSON_HERE'

# List Agents
gcloud alpha agent-registry agents list --location=us-central1

# List Global Agents
gcloud alpha agent-registry agents list --location=global
```

### 3. Endpoints
Used to register service endpoints (e.g., Vertex AI models).

```bash
# Register an Endpoint (example: Gemini Models)
gcloud alpha agent-registry services create gemini-models \
  --location=us-central1 \
  --display-name="Vertex AI Model Garden" \
  --description="List of all models in Vertex AI Model Garden" \
  --endpoint-spec-type=no-spec \
  --interfaces='[{"protocolBinding": "jsonrpc", "url": "https://us-central1-aiplatform.googleapis.com/v1beta1/publishers/*/models"}]'

# List Endpoints
gcloud alpha agent-registry endpoints list --location=us-central1

# Update Endpoint Display Name
gcloud alpha agent-registry services update gemini-models \
  --display-name="Model Garden on Vertex AI" \
  --location=us-central1
```

---

## Detailed Command Reference

All commands support `--location` (required) and `--project` (optional).

| Group | Commands |
|-------|----------|
| `agents` | `list`, `describe` |
| `mcp-servers` | `list`, `describe` |
| `endpoints` | `list`, `describe` |
| `services` | `create`, `list`, `describe`, `update`, `delete` |
| `operations` | `list`, `describe` |

### Service Creation Flags

| Flag | Description |
|------|-------------|
| `--display-name` | Human-readable name |
| `--description` | Brief summary of the service |
| `--interfaces` | JSON array of protocol bindings and URLs |
| `--mcp-server-spec-type` | Type: `no-spec`, `tool-spec` |
| `--mcp-server-spec-content`| JSON content of the spec |
| `--agent-spec-type` | Type: `no-spec`, `a2a-agent-card` |
| `--agent-spec-content` | JSON content for `a2a-agent-card` |
| `--endpoint-spec-type` | Type: `no-spec` |

---

## Natural Language → Command Examples

| User says | Command |
|-----------|---------|
| "List my MCP servers" | `gcloud alpha agent-registry mcp-servers list --location=us-central1` |
| "Show me information on agent X" | `gcloud alpha agent-registry agents describe X --location=us-central1` |
| "Register a new GitHub MCP server with this spec..." | `gcloud alpha agent-registry services create github ... --mcp-server-spec-content='...'` |
| "Check status of operation Y" | `gcloud alpha agent-registry operations describe Y --location=us-central1` |
| "List all registered services" | `gcloud alpha agent-registry services list --location=us-central1` |
| "Show all agents where the runtime is reasoningEngine" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "Show agents with identity containing 'service-432423'" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeIdentity\".principal:service-432423"` |
| "Create a new A2A agent called my-a2a" | `gcloud alpha agent-registry services create my-a2a --agent-spec-type=a2a-agent-card ...` |
| "Show me all MCP servers where the runtime is my-runtime" | `gcloud alpha agent-registry mcp-servers list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:my-runtime"` |
| "List all global agents" | `gcloud alpha agent-registry agents list --location=global` |
| "List global MCP servers" | `gcloud alpha agent-registry mcp-servers list --location=global` |
| "Change display name of gemini-models to 'Vertex AI Model Garden'" | `gcloud alpha agent-registry services update gemini-models --display-name="..." --location=us-central1` |

---

## Advanced Filtering

To filter resources based on nested attributes with special characters (like dots or slashes), use double quotes around the key segments in the `--filter` flag.

> [!WARNING]
> The double-quote escaping shown below (`\"`) works in bash/zsh. Windows CMD or PowerShell users may need different escaping (e.g., `"` or ``` `"` ``) for nested attribute keys.

**Mapping Tips**:
- Map **"runtime"** to `attributes."agentregistry.googleapis.com/system/RuntimeReference".uri`.
- Map **"identity"** to `attributes."agentregistry.googleapis.com/system/RuntimeIdentity".principal`.

```bash
# Example: Show all agents where the runtime is reasoningEngine
gcloud alpha agent-registry agents list \
  --location=us-central1 \
  --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"

# Example: Show agents where identity contains a specific service account ID
gcloud alpha agent-registry agents list \
  --location=us-central1 \
  --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeIdentity\".principal:service-432423"
```

---

## Python ADK Integration

The Google Agent Development Kit (ADK) allows seamless integration with the Agent Registry.

### 1. Requirements & Setup
- **ADK Version**: 1.26.0 or higher (minimum).
- **Installation**:
  ```bash
  # Using pip
  pip install --upgrade google-adk

  # Using uv
  uv add google-adk
  ```

### 2. Import & Usage
Add the following import to your Python code:
```python
from google.adk.integrations.agent_registry import AgentRegistry
```

### 3. Invoking an MCP Server from Registry
Use this snippet to retrieve and use an MCP toolset:
```python
import os
from google.adk.integrations.agent_registry import AgentRegistry

# Initialize registry client
registry = AgentRegistry(project_id=SESSION_PROJECT, location=SESSION_LOCATION)

# Retrieve MCP Toolset using the full resource name
# Example resource name: projects/PRJ/locations/LOC/mcpServers/SERVER_NAME
mcp_toolset = registry.get_mcp_toolset(
    f"projects/{SESSION_PROJECT}/locations/{SESSION_LOCATION}/mcpServers/{MCP_SERVER_NAME}"
)
```

### 4. Integrating a Remote A2A Agent
Use this snippet to use a registry agent as a sub-agent:
```python
from google.adk import Agent, Gemini, types
from google.adk.integrations.agent_registry import AgentRegistry

# Initialize registry client
registry = AgentRegistry(project_id=SESSION_PROJECT, location=SESSION_LOCATION)

# Retrieve Remote A2A Agent
remote_agent = registry.get_remote_a2a_agent(
    f"projects/{SESSION_PROJECT}/locations/{SESSION_LOCATION}/agents/{AGENT_NAME}"
)

# Define a new Agent with the remote agent as a sub-agent
help_agent = Agent(
    name="help_agent",
    description="Helpful AI Assistant that uses a remote agent.",
    model=Gemini(model="gemini-2.0-flash"),
    sub_agents=[remote_agent]
)
```

---

## Interactive Prompts

Only ask if still missing after checking session context:
- **location**: "Which region? (e.g. `us-central1`)" — only if `compute/region` was not set
- **project**: "Which project?" — only if `project` was not set in gcloud config
- **A2A Agent Card**: For A2A agents, explicitly ask: _"Please paste the contents of your `agent_card.json` file."_ and use it for `--agent-spec-content`.
- **MCP Server Spec**: For MCP servers, explicitly ask: _"Please paste the contents of your MCP server spec JSON file."_ and use it for `--mcp-server-spec-content`.

Only ask for what's strictly needed — don't overwhelm the user.

---

## Error Handling

If a command fails:
1. Check if `gcloud alpha` component is installed.
   - Required (minimum): **Google Cloud SDK 560.0.0 or higher**
   - Required (minimum): **alpha component 2026.03.09 or higher**
2. Verify the `--location` (some resources may be in `global` or specific regions).
3. Ensure JSON payloads for `--interfaces` or specs are correctly quoted for the shell.
4. Check project permissions for `agentregistry.googleapis.com`.

### Bug Reporting

If you encounter an unexpected problem, bug, or a failure that you cannot resolve:
1. Ask the user if they would like to create a GitHub issue for this bug.
2. If the user agrees, generate a descriptive title and body for the issue based on the error context.
3. Show the user the proposed issue content and the command to create it.
4. Ask for final approval before running the command.
5. Once approved, use the `gh` CLI to create the issue in the repository. For example:
   ```bash
   gh issue create --repo agentskills/agent-registry-skill --title "Title of the bug" --body "Description of the bug, including error messages and steps to reproduce."
   ```

---

## ADK Reference

If the user asks about ADK, read `references/adk-docs.md` for instructions
on which URL to fetch.

