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

### 4. GKE Based Agents
Used to configure Kubernetes deployments to be registered as an Agent or MCP Server. You can add the required `apphub.cloud.google.com/functional-type` annotation to YAML files using the provided python script.

```bash
# Ask the user if they want to process the current directory or a specific directory/file
# Ask the user if the functional type is an AGENT or MCP_SERVER

# Run the python script to annotate the YAML files
./scripts/annotate_gke.py /path/to/folder_or_file.yaml --type AGENT
```

## Agent Dashboard

The Agent Dashboard provides a consolidated view of all agents in the current project, searching across both `global` and the regional location (default: `us-central1`).

To generate the dashboard, run:
```bash
./scripts/agent-dashboard.sh
```

The output will be a Markdown table containing the following fields:
- **Name**: The ID of the agent.
- **Display Name**: The human-readable name.
- **Location**: The region where the agent is registered.
- **Runtime**: The reference to the agent's runtime.

### MCP Server Dashboard

The MCP Server Dashboard provides a consolidated view of all MCP servers in the current project, searching across both `global` and the regional location (default: `us-central1`).

To generate the dashboard, run:
```bash
./scripts/mcp-dashboard.sh
```

The output will be a Markdown table containing the following fields:
- **Name**: The ID of the MCP server.
- **Display Name**: The human-readable name.
- **Location**: The region where it is registered.
- **Tools**: List of tools provided by the server.
- **Runtime**: The reference to the runtime.

---

## Detailed Command Reference

All commands support `--location` (required) and `--project` (optional).

| Group | Commands |
|-------|----------|
| `agents` | `list`, `describe`, `search` |
| `mcp-servers` | `list`, `describe`, `search` |
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
| "Configure this GKE deployment as an agent" | `./scripts/annotate_gke.py /path/to/folder_or_file.yaml --type AGENT` |
| "Make my deployments in this folder MCP Servers" | `./scripts/annotate_gke.py /path/to/folder_or_file.yaml --type MCP_SERVER` |
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
| "show me a dashboard for my agents" | `./scripts/agent-dashboard.sh` |
| "show me a dashboard for my mcp servers" | `./scripts/mcp-dashboard.sh` |
| "Change display name of gemini-models to 'Vertex AI Model Garden'" | `gcloud alpha agent-registry services update gemini-models --display-name="..." --location=us-central1` |
| "Which agents in us-central1 are based on reasoning engine?" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "List all vertex ai agents" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "Show agents with agent engine runtime" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "Which MCP Server has a tool named search_documents?" | `gcloud alpha agent-registry mcp-servers list --location=us-central1 --filter="tools.name:search_documents"` |
| "Find all servers with the get_document tool" | `gcloud alpha agent-registry mcp-servers list --location=us-central1 --filter="tools.name:get_document"` |
| "Search for all reasoning engine agents by agent ID" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="agentId:reason"` |
| "Search for Cloud Run MCP servers by MCP Server ID" | `gcloud alpha agent-registry mcp-servers list --location=us-central1 --filter="mcpServerId:run"` |
| "Search for agents by skill name model" | `gcloud alpha agent-registry agents search --location=us-central1 --search-string="skills.name:model"` |
| "Search for agents with display name containing Assessor" | `gcloud alpha agent-registry agents search --location=us-central1 --search-string="displayName:Assessor*"` |
| "Search for MCP servers containing the display name GitHub" | `gcloud alpha agent-registry mcp-servers search --location=us-central1 --search-string="displayName:GitHub*"` |

---

## Advanced Filtering

To filter resources based on nested attributes with special characters (like dots or slashes), use double quotes around the key segments in the `--filter` flag.

> [!WARNING]
> The double-quote escaping shown below (`\"`) works in bash/zsh. Windows CMD or PowerShell users may need different escaping (e.g., `"` or ``` `"` ``) for nested attribute keys.

**Filtering by `agentId` and `mcpServerId`**:
The `agentId` and `mcpServerId` fields uniquely identify an agent or MCP server and follow the [URN model](https://datatracker.ietf.org/doc/html/rfc8141).
For agents, `agentId` always begins with: `urn:agent:projects-{project-number}:projects:{project-number}:locations:{location}:{other-segments}`
For MCP servers, `mcpServerId` always begins with: `urn:mcp:projects-{project-number}:projects:{project-number}:locations:{location}:{other-segments}`
The `{other-segments}` can vary based on the platform, for example:
- **Reasoning Engine:** `aiplatform:reasoningEngines:{reasoning-engine-id}`
- **GKE:** `container:clusters:{cluster-name}:k8s:namespaces:{namespace}:apps:deployments:{deployment-id}`
You can filter agents and MCP servers by substring matching these fields. For example, `--filter="agentId:reason"` finds Reasoning Engine agents, and `--filter="mcpServerId:run"` finds Cloud Run MCP servers.

**Mapping Tips**:
- Map **"runtime"** to `attributes."agentregistry.googleapis.com/system/RuntimeReference".uri`.
- Map **"identity"** to `attributes."agentregistry.googleapis.com/system/RuntimeIdentity".principal`.
- Map **"tool name"** or **"tool"** to `tools.name` for MCP Server list commands.
- **Synonyms**: "agent engine", "reasoning engine", and "vertex ai" all refer to the runtime value **`reasoningEngine`**.
- **Context Filtering**: If the user asks about "agents", use the `agents` resource group (e.g., `gcloud alpha agent-registry agents list`), not `mcp-servers` or `endpoints`.

```bash
# Example: Show all agents where the runtime is reasoningEngine
gcloud alpha agent-registry agents list \
  --location=us-central1 \
  --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"

# Example: Show agents where identity contains a specific service account ID
gcloud alpha agent-registry agents list \
  --location=us-central1 \
  --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeIdentity\".principal:service-432423"

# Example: Search for all reasoning engine agents using the agentId
gcloud alpha agent-registry agents list \
  --location=us-central1 \
  --filter="agentId:reason"

# Example: Search for cloud run MCP servers using the mcpServerId
gcloud alpha agent-registry mcp-servers list \
  --location=us-central1 \
  --filter="mcpServerId:run"
```

---

## Searching Agents

When searching for agents, **always default to using the `mcp_agentregistry_search_agents` MCP tool** if the `agentregistry` MCP server is available. Use the `gcloud alpha agent-registry agents search` command as a fallback.

### MCP Tool Usage (`mcp_agentregistry_search_agents`)

- **`parent`**: `projects/{project}/locations/{location}`
- **`searchString`**: Follows the same syntax as the gcloud command (e.g., `skills.name:model`, `displayName:Assessor*`).

### gcloud Fallback Usage

You can search for agents using the `gcloud alpha agent-registry agents search` command. This command supports a `--search-string` flag with specific match types:

- **Exact match (`=`)**: Matches the entire value exactly.
  Example: `--search-string="agentId=\"urn:agent:projects-123:projects:123:locations:us-central1:agentregistry:services:my-agent\""`
- **Token match (`:`)**: Matches individual words exactly.
  Example: `--search-string="agentId:\"urn:agent:projects-123\""`
- **Prefix match (`*`)**: Matches values that start with the given prefix.
  Example: `--search-string="agentId:\"urn:agent:projects-123*\""`

### Searchable Fields & Examples

You can search across fields such as `agentId`, `displayName`, `skills.name`, `skills.id`, and `skills.description`. Note that values containing colons (like URNs) must be escaped.

```bash
# Search for agents by agentId (urn) with prefix match
gcloud alpha agent-registry agents search --location=us-east4 \
  --search-string="agentId:\"urn:agent:projects-1064111708665*\""

# Search for agents containing the display name 'Assessor'
gcloud alpha agent-registry agents search --location=us-east4 \
  --search-string="displayName:Assessor*"

# Search for agents by skill name
gcloud alpha agent-registry agents search --location=us-east4 \
  --search-string="skills.name:model"

# Search for agents by skill id
gcloud alpha agent-registry agents search --location=us-east4 \
  --search-string="skills.id:AssessorAgent"

# Search for agents by skill description
gcloud alpha agent-registry agents search --location=us-east4 \
  --search-string="skills.description:severity*"
```

---

## Searching MCP Servers

When searching for MCP servers, **always default to using the `mcp_agentregistry_search_mcp_servers` MCP tool** if the `agentregistry` MCP server is available. Use the `gcloud alpha agent-registry mcp-servers search` command as a fallback.

### MCP Tool Usage (`mcp_agentregistry_search_mcp_servers`)

- **`parent`**: `projects/{project}/locations/{location}`
- **`searchString`**: Follows the same syntax as the gcloud command (e.g., `displayName:GitHub*`, `mcpServerId:run`).

### gcloud Fallback Usage

You can search for MCP servers using the `gcloud alpha agent-registry mcp-servers search` command. This command supports a `--search-string` flag with the same match types as agents (exact `=`, token `:`, prefix `*`).

### Searchable Fields & Examples

You can search across fields such as `mcpServerId`, `name`, and `displayName`. Note that values containing colons (like URNs) must be escaped.

```bash
# Search for MCP servers by mcpServerId with prefix match
gcloud alpha agent-registry mcp-servers search --location=us-east4 \
  --search-string="mcpServerId:\"urn:mcp:projects-1064111708665*\""

# Search for MCP servers containing the display name 'GitHub'
gcloud alpha agent-registry mcp-servers search --location=us-east4 \
  --search-string="displayName:GitHub*"
```

---



## Python ADK Integration

The Google Agent Development Kit (ADK) allows seamless integration with the Agent Registry.

For comprehensive details on how to build, deploy, or configure agents using Google's Agent Development Kit (ADK) and the Agent Registry, **you must read the `references/adk-docs.md` file**. It contains the complete guide for:
- Initialization and Authentication
- Discovering and Listing Resources (Agents and MCP Servers)
- Using an MCP Toolset from the Registry
- Integrating a Remote A2A Agent as a sub-agent

**Important:** Whenever the user asks for code generation, code snippets, or how to use the ADK with the Agent Registry in Python, refer directly to `references/adk-docs.md`.

---

## Interactive Prompts

Only ask if still missing after checking session context:
- **location**: "Which region? (e.g. `us-central1`)" — only if `compute/region` was not set
- **project**: "Which project?" — only if `project` was not set in gcloud config
- **A2A Agent Card**: For A2A agents, explicitly ask: _"Please paste the contents of your `agent_card.json` file."_ and use it for `--agent-spec-content`.
- **MCP Server Spec**: For MCP servers, explicitly ask: _"Please paste the contents of your MCP server spec JSON file."_ and use it for `--mcp-server-spec-content`.
- **GKE Deployments**: Ask for the target path (current folder, specific folder, or file) and the functional type (`AGENT` or `MCP_SERVER`).

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

If the user asks about ADK, read the complete guide in `references/adk-docs.md`.

