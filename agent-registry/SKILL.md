---
name: agent-registry
description: >
  Use this skill whenever the user wants to interact with Google Cloud's Agent Registry
  using gcloud commands. Triggers on any mention of "agent registry", "agent-registry",
  "mcp-servers", "gcloud agents", "register an agent", "list agents", "create a service",
  "agent service", "management boundary", "boundary", "boundary-configs", "boundaries",
  "capability-configs", "capability config", "management project", or any request to
  manage agents, MCP servers, endpoints, services, bindings, skills, or management
  boundaries in Google Cloud Agent Registry. Also triggers on requests to integrate or
  use the Google Agent Development Kit (ADK) with the Agent Registry.
metadata:
  author: srinandan
  version: "0.1"
---

# Google Cloud Agent Registry Skill

Help users interact with Google Cloud Agent Registry using `gcloud agent-registry` (GA resources: agents, mcp-servers, services, endpoints, bindings, operations), `gcloud alpha agent-registry skills` (Alpha feature: skills and skill revisions), and `gcloud resource-manager` (`boundary-configs`, `capability-configs`, `boundaries`, and `tags bindings` for setting up Agent Registry management boundaries) by translating natural language into the correct gcloud command, showing it for approval, then executing it.

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
| `roles/resourcemanager.editor` | Create and update `BoundaryConfig`, `CapabilityConfig`, and `Boundary` on the parent folder or organization |
| `roles/resourcemanager.viewer` | Read `BoundaryConfig`, `CapabilityConfig`, and `Boundary` resources |
| `roles/resourcemanager.tagUser` | Bind tag values (`tags bindings create/delete`) to projects |
| `roles/owner` or `roles/editor` | Required on a candidate Bring-Your-Own project to associate it as a Management Project |

---

## Resource Types & Registration

The primary command for registering resources is `gcloud agent-registry services create`.

### 1. MCP Servers
Used to register Model Context Protocol servers.

```bash
# Register an MCP Server (example: GitHub)
# Ask user to paste contents of mcp-spec.json for --mcp-server-spec-content
gcloud agent-registry services create github \
  --location=us-central1 \
  --display-name="GitHub MCP Server" \
  --description="Connects to GitHub" \
  --mcp-server-spec-type=tool-spec \
  --mcp-server-spec-content='PASTE_MCP_SPEC_JSON_HERE' \
  --interfaces='[{"protocolBinding": "jsonrpc", "url": "https://api.github.com/mcp"}]'

# List MCP Servers
gcloud agent-registry mcp-servers list --location=us-central1

# Filter MCP Servers by Runtime
gcloud agent-registry mcp-servers list \
  --location=us-central1 \
  --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"

# List Global MCP Servers
gcloud agent-registry mcp-servers list --location=global
```

### 2. Agents
Used to register AI agents (e.g., A2A, Salesforce).

```bash
# Register an Agent (example: Salesforce)
gcloud agent-registry services create salesforce \
  --location=us-central1 \
  --display-name="Salesforce Agent" \
  --description="Salesforce Einstein Agent" \
  --agent-spec-type=no-spec \
  --interfaces='[{"protocolBinding": "http-json", "url": "https://api.salesforce.com/agent/v1"}]'

# Register an A2A Agent (Special Case)
# Ask user to paste contents of agent_card.json for --agent-spec-content
gcloud agent-registry services create testa2a \
  --location=us-central1 \
  --display-name="Test A2A Agent" \
  --description="Sample A2A Agent" \
  --agent-spec-type=a2a-agent-card \
  --agent-spec-content='PASTE_AGENT_CARD_JSON_HERE'

# List Agents
gcloud agent-registry agents list --location=us-central1

# List Global Agents
gcloud agent-registry agents list --location=global
```

### 3. Endpoints
Used to register service endpoints (e.g., Vertex AI models).

```bash
# Register an Endpoint (example: Gemini Models)
gcloud agent-registry services create gemini-models \
  --location=us-central1 \
  --display-name="Vertex AI Model Garden" \
  --description="List of all models in Vertex AI Model Garden" \
  --endpoint-spec-type=no-spec \
  --interfaces='[{"protocolBinding": "jsonrpc", "url": "https://us-central1-aiplatform.googleapis.com/v1beta1/publishers/*/models"}]'

# List Endpoints
gcloud agent-registry endpoints list --location=us-central1

# Update Endpoint Display Name
gcloud agent-registry services update gemini-models \
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

### 5. Bindings
Used to connect a source agent to a target resource (another agent, MCP server, or endpoint) or an auth provider for delegated permissions.

```bash
# Create a binding to connect a source agent to a target resource
gcloud agent-registry bindings create BINDING_NAME \
  --location=us-central1 \
  --display-name="My Custom Binding" \
  --source-identifier="SOURCE_ID" \
  --target-identifier="TARGET_ID"

# Create a binding for delegated permissions (using an auth provider)
gcloud agent-registry bindings create BINDING_NAME \
  --location=us-central1 \
  --display-name="Auth Provider Binding" \
  --source-identifier="SOURCE_ID" \
  --auth-provider="projects/PROJECT_ID/locations/REGION/connectors/AUTH_PROVIDER_ID"

# List Bindings
gcloud agent-registry bindings list --location=us-central1

# View Binding Details
gcloud agent-registry bindings describe BINDING_NAME --location=us-central1

# Update a Binding
gcloud agent-registry bindings update BINDING_NAME \
  --display-name="New Display Name" \
  --location=us-central1

# Delete a Binding
gcloud agent-registry bindings delete BINDING_NAME --location=us-central1
```

### 6. Skills (Alpha)
Used to manage reusable AI Skills and Skill Revisions via the **`agentregistry` MCP server tools** (preferred when the MCP server is available) or `gcloud alpha agent-registry skills` CLI commands.

> [!IMPORTANT]
> **Supported Locations for Skills:** Skills only work in `"global"`, `"us"`, or `"eu"` regions. If the user asks for something else (e.g. `us-central1`), **do not pass that region to the MCP tool or `gcloud` command**. Instead, inform the user that Skills are only supported in `global`, `us`, or `eu` regions and ask them to select one of those locations.

> [!NOTE]
> All Skills and Skill Revisions CRUD, list, and search operations are supported through the `agentregistry` MCP server as well as `gcloud alpha agent-registry skills`. Downloading a skill revision archive payload to disk uses `gcloud alpha agent-registry skills revisions download`. As with CLI commands, execute read-only MCP calls (`list_skills`, `get_skill`, `search_skills`, `list_skill_revisions`, `get_skill_revision`) immediately, and ask for user approval before invoking mutating MCP tools (`create_skill`, `update_skill`, `delete_skill`, `create_skill_revision`, `delete_skill_revision`).

#### MCP Tools for Skills & Skill Revisions (`agentregistry` MCP Server)

| Operation | MCP Tool (`agentregistry`) | Key Arguments |
|-----------|----------------------------|---------------|
| **List Skills** | `mcp_agentregistry_list_skills` | `parent`: `projects/{project}/locations/{location}` (`global`, `us`, or `eu`); optional `filter`, `orderBy`, `pageSize`, `pageToken` |
| **Get Skill** | `mcp_agentregistry_get_skill` | `name`: `projects/{project}/locations/{location}/skills/{skill}` |
| **Create Skill** | `mcp_agentregistry_create_skill` | `parent`: `projects/{project}/locations/{location}`, `skillId`, `skill`: `{displayName, type: "SIMPLE", targetState: "TARGET_STATE_DRAFT" \| "TARGET_STATE_ACTIVE", description, defaultRevision, scanningConfig, publisher}` |
| **Update Skill** | `mcp_agentregistry_update_skill` | `skill`: `{name: "projects/.../skills/{skill}", displayName, description, targetState, defaultRevision, scanningConfig}`, optional `updateMask` |
| **Delete Skill** | `mcp_agentregistry_delete_skill` | `name`: `projects/{project}/locations/{location}/skills/{skill}`, optional `force` (`true` to also delete revisions) |
| **Search Skills** | `mcp_agentregistry_search_skills` | `parent`: `projects/{project}/locations/{location}`, `searchString`, `searchType` (`KEYWORD` or `SEMANTIC`), optional `filter` (e.g., `state=ACTIVE`) |
| **List Revisions** | `mcp_agentregistry_list_skill_revisions` | `parent`: `projects/{project}/locations/{location}/skills/{skill}`, optional `pageSize`, `pageToken` |
| **Get Revision** | `mcp_agentregistry_get_skill_revision` | `name`: `projects/{project}/locations/{location}/skills/{skill}/revisions/{revision}` |
| **Create Revision** | `mcp_agentregistry_create_skill_revision` | `parent`: `projects/{project}/locations/{location}/skills/{skill}`, optional `skillRevisionId`, `skillRevision`: `{gcsSource: {uri: "gs://..."}}` or `{archiveUploadSource: {archiveContent: "<base64-bytes>"}}` |
| **Delete Revision** | `mcp_agentregistry_delete_skill_revision` | `name`: `projects/{project}/locations/{location}/skills/{skill}/revisions/{revision}` |

#### `gcloud` CLI Usage (`gcloud alpha agent-registry skills`)

```bash
# List Skills
gcloud alpha agent-registry skills list --location=us

# Create a Skill from local payload ZIP archive
gcloud alpha agent-registry skills create my-skill \
  --location=us \
  --display-name="My Custom Skill" \
  --description="Skill description" \
  --type=simple \
  --payload=/path/to/archive.zip

# Create a Skill from Cloud Storage object
gcloud alpha agent-registry skills create my-skill \
  --location=us \
  --display-name="My Custom Skill" \
  --gcs-source-uri=gs://my-bucket/skill.zip

# Describe a Skill
gcloud alpha agent-registry skills describe my-skill --location=us

# Search Skills
gcloud alpha agent-registry skills search --location=us \
  --query="weather" --search-type=keyword

# Update a Skill
gcloud alpha agent-registry skills update my-skill \
  --location=us \
  --display-name="Updated Skill Name"

# Delete a Skill
gcloud alpha agent-registry skills delete my-skill --location=us

# Manage Skill Revisions (Alpha)
gcloud alpha agent-registry skills revisions list --skill=my-skill --location=us
gcloud alpha agent-registry skills revisions describe REVISION_ID --skill=my-skill --location=us
gcloud alpha agent-registry skills revisions download REVISION_ID --skill=my-skill --location=us
gcloud alpha agent-registry skills revisions delete REVISION_ID --skill=my-skill --location=us
```

### 7. Management Boundary Setup (Admin Governance)
Used by Agent Registry administrators to configure hub-and-spoke governance perimeters across a Google Cloud Folder or Organization using Cloud Resource Manager (`BoundaryConfig`, `CapabilityConfig`, `Boundary`, and Tag Bindings). When member (spoke) projects match a boundary's tag filter, Agent Registry automatically discovers runtime agents and MCP servers deployed across those member projects and aggregates them into the designated Management Project (hub) catalog.

#### Resource Model Overview

| Resource | CLI Command Group | Purpose |
|----------|-------------------|---------|
| **`BoundaryConfig`** | `gcloud resource-manager boundary-configs` | Singleton resource on a Folder or Organization node (`folders/{id}/boundaryConfig` or `organizations/{id}/boundaryConfig`) that specifies the single partitioning `tagKey` (e.g., `975672035171/environment`) used by all boundaries under that node. |
| **`CapabilityConfig`** | `gcloud resource-manager capability-configs` | Designates a Management Project (hub) under the Folder or Organization, enables `--types=agent-management` (or `agent-management,app-management`), and associates one or more `Boundary` resources. |
| **`Boundary`** | `gcloud resource-manager boundaries` | Logical perimeter under a Folder or Organization that selects child projects matching a specific tag value (`--tag-key` and `--tag-value`) and links to a `CapabilityConfig`. |
| **Tag Bindings** | `gcloud resource-manager tags bindings` | Enrolls the Management Project and Member (Spoke) Projects into a boundary perimeter by binding the corresponding tag value (e.g., `975672035171/environment/dev`). |

#### Interactive Scoping Questions for Admins (Ask Before Provisioning)

When an administrator asks to set up a Management Boundary or `CapabilityConfig`, **proactively ask these scoping questions** (skipping any details they have already provided) to design the right topology before constructing mutating commands:

1. **Parent Hierarchy Node (Folder vs. Organization)**:
   _"Which Folder ID (`--folder=FOLDER_ID`) or Organization ID (`--organization=ORG_ID`) will anchor the boundary and management project(s)?"_
   *(Note: A `CapabilityConfig`, its Management Project, and all associated `Boundary` resources must share the exact same parent node.)*
2. **Perimeter Partitioning & Tag Key Strategy**:
   _"How do you want to partition projects under this node? Do you want multiple isolated perimeters using an Organization Tag Key (for example, `<ORG_ID>/environment` with values like `dev` and `prod`, or partitioning by business unit), or a single catch-all boundary covering all child projects?"_
3. **Catalog & IAM Isolation (`1 Hub per Perimeter` vs. `Shared Hub`)**:
   _"If you have multiple perimeters (such as `dev` and `prod`), do you want **strict catalog and IAM isolation** with a dedicated Management Project and `CapabilityConfig` per perimeter (recommended so `prod` agents never appear in `dev` queries and vice versa), or should multiple boundaries roll up into a single shared Management Project?"_
4. **Management Project Selection (Bring-Your-Own vs. Google-Managed)**:
   _"Do you want to designate existing project(s) under that parent node as your Management Project(s) (`--management-project=projects/<PROJECT_NUMBER>`), or have Cloud Resource Manager auto-provision a new Google-managed Management Project (by omitting `--management-project`)?"_
5. **Capability Types (`agent-management` vs. Shared with App Hub)**:
   _"Should the `CapabilityConfig` enable `agent-management` only, or both `agent-management,app-management` (to share the Management Project with App Hub)?"_
6. **Member (Spoke) Projects**:
   _"Which project IDs or project numbers should be enrolled into each boundary perimeter via tag bindings?"_

#### Best Practices & Architectural Guardrails

Always share relevant best practices with the admin as you guide them through setup:

- **Set `BoundaryConfig` Tag Key Before Attaching Boundaries**: Configure the partitioning `tagKey` (`gcloud resource-manager boundary-configs update`) *before* creating and attaching boundaries. Once any boundary under the node is attached to a `CapabilityConfig`, Cloud Resource Manager locks `tagKey` on that node (requiring all boundaries to be detached before `tagKey` can be changed). If `tagKey` is left unset, the node supports at most one filter-less boundary that matches every child project under the node.
- **Use Separate `CapabilityConfig` + Management Project for Strict `dev`/`prod` Isolation**: Every boundary attached to the same `CapabilityConfig` merges its discovered agents and MCP servers into one Management Project catalog. There is no `--boundary` filter on `gcloud agent-registry` queries, and granting `roles/agentregistry.viewer` on a Management Project exposes assets from all boundaries attached to it. To guarantee zero cross-perimeter leakage between environments (e.g., `dev` vs. `prod`), create a separate `CapabilityConfig`, Management Project, and `Boundary` for each environment.
- **Always Use Project Numbers (`projects/<PROJECT_NUMBER>`)**: Cloud Resource Manager v3 requires project **numbers** (not project IDs) for `--management-project=projects/<PROJECT_NUMBER>` on `capability-configs create` and `--parent=//cloudresourcemanager.googleapis.com/projects/<PROJECT_NUMBER>` on `tags bindings create`. Automatically resolve project IDs to project numbers for the user with:
  ```bash
  gcloud projects describe PROJECT_ID --format="value(projectNumber)"
  ```
- **Tag Binding Updates Require Delete-Then-Create**: GCP Tags allow at most one value per tag key on a resource (`tags bindings create` fails with `FAILED_PRECONDITION` if another value under the same tag key is already bound). To move a project from `dev` to `prod`, first run `tags bindings delete` for the old value and then `tags bindings create` for the new value. Tag changes take ~2–7 minutes to fully propagate.
- **Resource ID & Display Name Constraints**: `capability_config_id` and `boundary_id` must be 6–30 lowercase ASCII letters, digits, or hyphens, must start with a letter, and cannot end with a hyphen. `--display-name` must be 4–30 characters.
- **Centralize Manual Registrations in the Hub (Spoke Governance)**: Automatic runtime discovery (e.g., Vertex AI Agent Engine / Reasoning Engine and GKE agents/MCP servers) works across spoke member projects even when `agentregistry.googleapis.com` is disabled on the spoke projects. However, user-defined `Services` (`gcloud agent-registry services create`) and `Bindings` created locally in a spoke project stay isolated to that spoke and **do not roll up** to the Management Project. Register third-party MCP servers, custom agents, endpoints, and bindings centrally in the Management Project, and consider disabling `agentregistry.googleapis.com` (or restricting `services.*` and `bindings.*` write permissions via IAM Deny / Org Policy `gcp.restrictServiceUsage`) on spoke workload projects.
- **Follow Required Teardown Order**: Cloud Resource Manager blocks deleting an attached `Boundary` or a `CapabilityConfig` with attached boundaries. Always detach boundaries first (`gcloud resource-manager capability-configs update <ID> --folder=<FOLDER_ID> --clear-boundaries`), then delete the `Boundary`, and finally delete the `CapabilityConfig`. Deleting a `CapabilityConfig` preserves a Bring-Your-Own project (`isManagementProject` reverts to `false`), whereas a Google-managed Management Project is deleted.

#### Step-by-Step Boundary Provisioning Workflow

Below is the canonical end-to-end setup workflow (modeling a folder `849163983723` in organization `975672035171` partitioned by tag key `975672035171/environment` into isolated `dev` and `prod` management perimeters):

**Step 1: Configure Folder/Org `BoundaryConfig` and Bind Tags to Projects**
```bash
# 1a. Inspect current BoundaryConfig on the folder (or --organization=ORG_ID)
gcloud resource-manager boundary-configs describe --folder=849163983723

# 1b. Configure folder BoundaryConfig with the organization environment tag key
gcloud resource-manager boundary-configs update \
  --folder=849163983723 \
  --tag-key="975672035171/environment"

# 1c. Bind environment=dev to the dev management hub and dev spoke projects (using project numbers)
for pnum in 1066599796742 220378623452 553108137791; do
  gcloud resource-manager tags bindings create \
    --tag-value=975672035171/environment/dev \
    --parent=//cloudresourcemanager.googleapis.com/projects/$pnum
done

# 1d. Bind environment=prod to the prod management hub and prod spoke projects (using project numbers)
for pnum in 592695869630 455819280907 868507208815; do
  gcloud resource-manager tags bindings create \
    --tag-value=975672035171/environment/prod \
    --parent=//cloudresourcemanager.googleapis.com/projects/$pnum
done
```

**Step 2: Create `CapabilityConfig` Resources (Designate Management Projects)**
```bash
# Create folder-scoped CapabilityConfig for the dev management project
gcloud resource-manager capability-configs create agent-governance \
  --folder=849163983723 \
  --display-name="Agent Governance Capability" \
  --types=agent-management \
  --management-project=projects/1066599796742

# Create folder-scoped CapabilityConfig for the prod management project
gcloud resource-manager capability-configs create agent-governance-prod \
  --folder=849163983723 \
  --display-name="Agent Governance Capability" \
  --types=agent-management \
  --management-project=projects/592695869630
```

**Step 3: Create `Boundary` Resources**
```bash
# Create dev and prod Boundaries on the parent folder
gcloud resource-manager boundaries create agents-dev \
  --folder=849163983723 \
  --display-name="Agent Dev Boundary" \
  --tag-key="975672035171/environment" \
  --tag-value="dev"

gcloud resource-manager boundaries create agents-prod \
  --folder=849163983723 \
  --display-name="Agent Prod Boundary" \
  --tag-key="975672035171/environment" \
  --tag-value="prod"
```

**Step 4: Associate Each `Boundary` with Its `CapabilityConfig`**
```bash
# Associate agents-dev boundary with the dev CapabilityConfig
gcloud resource-manager capability-configs update agent-governance \
  --folder=849163983723 \
  --boundaries=folders/849163983723/boundaries/agents-dev

# Associate agents-prod boundary with the prod CapabilityConfig
gcloud resource-manager capability-configs update agent-governance-prod \
  --folder=849163983723 \
  --boundaries=folders/849163983723/boundaries/agents-prod
```

**Step 5: Verify Cross-Project Rollup, Filtering, and Search on the Management Project**
```bash
# List all discovered agents aggregated across member projects in the boundary
gcloud agent-registry agents list --project=MANAGEMENT_PROJECT_ID --location=us-central1

# List multi-region and global agents aggregated in the management project
gcloud agent-registry agents list --project=MANAGEMENT_PROJECT_ID --location=global
gcloud agent-registry agents list --project=MANAGEMENT_PROJECT_ID --location=us

# Filter aggregated agents by runtime (Vertex AI Reasoning Engine) across all member projects
gcloud agent-registry agents list --project=MANAGEMENT_PROJECT_ID --location=us-central1 \
  --filter='attributes."agentregistry.googleapis.com/system/RuntimeReference".uri:reasoningEngine'

# Narrow aggregated agents to a specific spoke project number via agentId or RuntimeIdentity
gcloud agent-registry agents list --project=MANAGEMENT_PROJECT_ID --location=us-central1 \
  --filter="agentId:220378623452"

gcloud agent-registry agents list --project=MANAGEMENT_PROJECT_ID --location=us-central1 \
  --filter='attributes."agentregistry.googleapis.com/system/RuntimeIdentity".principal:service-553108137791'

# Search aggregated agents across spoke projects by displayName prefix, spoke URN prefix, or A2A skills
gcloud agent-registry agents search --project=MANAGEMENT_PROJECT_ID --location=us-central1 \
  --search-string="displayName:Aegis*"

gcloud agent-registry agents search --project=MANAGEMENT_PROJECT_ID --location=us-central1 \
  --search-string='agentId:"urn:agent:projects-553108137791*"'

gcloud agent-registry agents search --project=MANAGEMENT_PROJECT_ID --location=us-central1 \
  --search-string="skills.tags:fintech"

gcloud agent-registry agents search --project=MANAGEMENT_PROJECT_ID --location=us-central1 \
  --search-string="Clinical OR Pharmacovigilance"
```

**Step 6: Audit, Reassign, or Tear Down Boundaries**
```bash
# List and describe CapabilityConfigs and Boundaries under a folder
gcloud resource-manager capability-configs list --folder=FOLDER_ID
gcloud resource-manager capability-configs describe CAPABILITY_CONFIG_ID --folder=FOLDER_ID
gcloud resource-manager boundaries list --folder=FOLDER_ID
gcloud resource-manager boundaries describe BOUNDARY_ID --folder=FOLDER_ID

# Audit all Agent Registry management projects across the organization
gcloud projects list \
  --filter="isManagementProject=true" \
  --format="table(projectId, projectNumber, parent.id, configuredCapabilities)"

# Move a member project from dev to prod (delete old binding first, then create new binding)
gcloud resource-manager tags bindings delete \
  --tag-value=975672035171/environment/dev \
  --parent=//cloudresourcemanager.googleapis.com/projects/PROJECT_NUMBER

gcloud resource-manager tags bindings create \
  --tag-value=975672035171/environment/prod \
  --parent=//cloudresourcemanager.googleapis.com/projects/PROJECT_NUMBER

# Detach boundaries before deleting a Boundary or CapabilityConfig
gcloud resource-manager capability-configs update CAPABILITY_CONFIG_ID \
  --folder=FOLDER_ID \
  --clear-boundaries
gcloud resource-manager boundaries delete BOUNDARY_ID --folder=FOLDER_ID
gcloud resource-manager capability-configs delete CAPABILITY_CONFIG_ID --folder=FOLDER_ID
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

### Skill Dashboard (Alpha)

The Skill Dashboard provides a consolidated view of all skills in the current project, searching across both `global` and the regional location (default: `us-central1`).

To generate the dashboard, run:
```bash
./scripts/skill-dashboard.sh
```

The output will be a Markdown table containing the following fields:
- **Name**: The ID of the skill.
- **Display Name**: The human-readable name.
- **Location**: The region where it is registered.
- **Type**: Structural deployment type (e.g. `SIMPLE`).
- **Default Revision**: The default revision ID associated with the skill.

---

## Detailed Command Reference

All `gcloud agent-registry` commands support `--location` (required) and `--project` (optional). Cloud Resource Manager boundary governance commands (`gcloud resource-manager`) are scoped to `--folder` or `--organization`.

| Group | Commands | API Stage |
|-------|----------|-----------|
| `agents` | `list`, `describe`, `search` | GA |
| `mcp-servers` | `list`, `describe`, `search` | GA |
| `endpoints` | `list`, `describe` | GA |
| `services` | `create`, `list`, `describe`, `update`, `delete` | GA |
| `bindings` | `create`, `list`, `describe`, `update`, `delete` | GA |
| `operations` | `list`, `describe` | GA |
| `skills` | `create`, `list`, `describe`, `update`, `delete`, `search` | Alpha (`agentregistry` MCP tools + `gcloud alpha agent-registry skills`) |
| `skills revisions` | `create`, `list`, `describe`, `delete`, `download` | Alpha (`agentregistry` MCP tools + `gcloud alpha agent-registry skills revisions`) |
| `boundary-configs` | `describe`, `update` | GA (`gcloud resource-manager boundary-configs`) |
| `capability-configs` | `create`, `list`, `describe`, `update`, `delete` | GA (`gcloud resource-manager capability-configs`) |
| `boundaries` | `create`, `list`, `describe`, `update`, `delete` | GA (`gcloud resource-manager boundaries`) |
| `tags bindings` | `create`, `list`, `delete` | GA (`gcloud resource-manager tags bindings`) |

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
| "List my MCP servers" | `gcloud agent-registry mcp-servers list --location=us-central1` |
| "Configure this GKE deployment as an agent" | `./scripts/annotate_gke.py /path/to/folder_or_file.yaml --type AGENT` |
| "Make my deployments in this folder MCP Servers" | `./scripts/annotate_gke.py /path/to/folder_or_file.yaml --type MCP_SERVER` |
| "Show me information on agent X" | `gcloud agent-registry agents describe X --location=us-central1` |
| "Register a new GitHub MCP server with this spec..." | `gcloud agent-registry services create github ... --mcp-server-spec-content='...'` |
| "Check status of operation Y" | `gcloud agent-registry operations describe Y --location=us-central1` |
| "List all registered services" | `gcloud agent-registry services list --location=us-central1` |
| "Show all agents where the runtime is reasoningEngine" | `gcloud agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "Show agents with identity containing 'service-432423'" | `gcloud agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeIdentity\".principal:service-432423"` |
| "Create a new A2A agent called my-a2a" | `gcloud agent-registry services create my-a2a --agent-spec-type=a2a-agent-card ...` |
| "Show me all MCP servers where the runtime is my-runtime" | `gcloud agent-registry mcp-servers list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:my-runtime"` |
| "List all global agents" | `gcloud agent-registry agents list --location=global` |
| "List global MCP servers" | `gcloud agent-registry mcp-servers list --location=global` |
| "show me a dashboard for my agents" | `./scripts/agent-dashboard.sh` |
| "show me a dashboard for my mcp servers" | `./scripts/mcp-dashboard.sh` |
| "show me a dashboard for my skills" | `./scripts/skill-dashboard.sh` |
| "Change display name of gemini-models to 'Vertex AI Model Garden'" | `gcloud agent-registry services update gemini-models --display-name="..." --location=us-central1` |
| "Which agents in us-central1 are based on reasoning engine?" | `gcloud agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "List all vertex ai agents" | `gcloud agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "Show agents with agent engine runtime" | `gcloud agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "Which MCP Server has a tool named search_documents?" | `gcloud agent-registry mcp-servers list --location=us-central1 --filter="tools.name:search_documents"` |
| "Find all servers with the get_document tool" | `gcloud agent-registry mcp-servers list --location=us-central1 --filter="tools.name:get_document"` |
| "Search for all reasoning engine agents by agent ID" | `gcloud agent-registry agents list --location=us-central1 --filter="agentId:reason"` |
| "Search for Cloud Run MCP servers by MCP Server ID" | `gcloud agent-registry mcp-servers list --location=us-central1 --filter="mcpServerId:run"` |
| "Search for agents by skill name model" | `gcloud agent-registry agents search --location=us-central1 --search-string="skills.name:model"` |
| "Search for agents with display name containing Assessor" | `gcloud agent-registry agents search --location=us-central1 --search-string="displayName:Assessor*"` |
| "Search for MCP servers containing the display name GitHub" | `gcloud agent-registry mcp-servers search --location=us-central1 --search-string="displayName:GitHub*"` |
| "Create a binding between agent A and server B" | `gcloud agent-registry bindings create my-binding --source-identifier="URN_A" --target-identifier="URN_B" --location=us-central1` |
| "List all bindings" | `gcloud agent-registry bindings list --location=us-central1` |
| "Show details for binding X" | `gcloud agent-registry bindings describe X --location=us-central1` |
| "Delete binding Y" | `gcloud agent-registry bindings delete Y --location=us-central1` |
| "List all skills" | `gcloud alpha agent-registry skills list --location=us` |
| "Show details of skill my-skill" | `gcloud alpha agent-registry skills describe my-skill --location=us` |
| "Search skills matching query" | `gcloud alpha agent-registry skills search --location=us --query="QUERY"` |
| "Configure folder 849163983723 boundary config to use environment tag" | `gcloud resource-manager boundary-configs update --folder=849163983723 --tag-key="975672035171/environment"` |
| "Create a capability config for agent management on folder 849163983723" | `gcloud resource-manager capability-configs create agent-governance --folder=849163983723 --display-name="Agent Governance Capability" --types=agent-management --management-project=projects/1066599796742` |
| "Create a dev boundary under folder 849163983723 for environment=dev" | `gcloud resource-manager boundaries create agents-dev --folder=849163983723 --display-name="Agent Dev Boundary" --tag-key="975672035171/environment" --tag-value="dev"` |
| "Associate boundary agents-dev with capability config agent-governance" | `gcloud resource-manager capability-configs update agent-governance --folder=849163983723 --boundaries=folders/849163983723/boundaries/agents-dev` |
| "Bind tag environment=dev to project 220378623452" | `gcloud resource-manager tags bindings create --tag-value=975672035171/environment/dev --parent=//cloudresourcemanager.googleapis.com/projects/220378623452` |
| "List all boundaries under folder 849163983723" | `gcloud resource-manager boundaries list --folder=849163983723` |
| "List all capability configs under folder 849163983723" | `gcloud resource-manager capability-configs list --folder=849163983723` |
| "Filter aggregated agents in management project by spoke project number 220378623452" | `gcloud agent-registry agents list --project=MANAGEMENT_PROJECT_ID --location=us-central1 --filter="agentId:220378623452"` |
| "Search aggregated agents by skill tag fintech" | `gcloud agent-registry agents search --project=MANAGEMENT_PROJECT_ID --location=us-central1 --search-string="skills.tags:fintech"` |

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
- **Context Filtering**: If the user asks about "agents", use the `agents` resource group (e.g., `gcloud agent-registry agents list`), not `mcp-servers` or `endpoints`.

```bash
# Example: Show all agents where the runtime is reasoningEngine
gcloud agent-registry agents list \
  --location=us-central1 \
  --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"

# Example: Show agents where identity contains a specific service account ID
gcloud agent-registry agents list \
  --location=us-central1 \
  --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeIdentity\".principal:service-432423"

# Example: Search for all reasoning engine agents using the agentId
gcloud agent-registry agents list \
  --location=us-central1 \
  --filter="agentId:reason"

# Example: Search for cloud run MCP servers using the mcpServerId
gcloud agent-registry mcp-servers list \
  --location=us-central1 \
  --filter="mcpServerId:run"
```

---

## Searching Agents

When searching for agents, **always default to using the `mcp_agentregistry_search_agents` MCP tool** if the `agentregistry` MCP server is available. Use the `gcloud agent-registry agents search` command as a fallback.

### MCP Tool Usage (`mcp_agentregistry_search_agents`)

- **`parent`**: `projects/{project}/locations/{location}`
- **`searchString`**: Follows the same syntax as the gcloud command (e.g., `skills.name:model`, `displayName:Assessor*`).

### gcloud Fallback Usage

You can search for agents using the `gcloud agent-registry agents search` command. This command supports a `--search-string` flag with specific match types:

- **Exact match (`=`)**: Matches the entire value exactly.
  Example: `--search-string="agentId=\"urn:agent:projects-123:projects:123:locations:us-central1:agentregistry:services:my-agent\""`
- **Token match (`:`)**: Matches individual words exactly.
  Example: `--search-string="agentId:\"urn:agent:projects-123\""`
- **Prefix match (`*`)**: Matches values that start with the given prefix.
  Example: `--search-string="agentId:\"urn:agent:projects-123*\""`

### Searchable Fields & Examples

You can search across fields such as `agentId`, `displayName`, `skills.name`, `skills.id`, `skills.tags`, and `skills.description`, as well as boolean `OR` / `AND` keyword expressions. Note that values containing colons (like URNs) must be escaped, and wildcard `*` is not supported on `skills.description` (use token match `:` instead).

```bash
# Search for agents by agentId (urn) with prefix match
gcloud agent-registry agents search --location=us-east4 \
  --search-string="agentId:\"urn:agent:projects-1064111708665*\""

# Search for agents containing the display name 'Assessor'
gcloud agent-registry agents search --location=us-east4 \
  --search-string="displayName:Assessor*"

# Search for agents by skill name
gcloud agent-registry agents search --location=us-east4 \
  --search-string="skills.name:model"

# Search for agents by skill id
gcloud agent-registry agents search --location=us-east4 \
  --search-string="skills.id:AssessorAgent"

# Search for agents by skill tag
gcloud agent-registry agents search --location=us-central1 \
  --search-string="skills.tags:fintech"

# Search for agents by skill description (token match; wildcard * is not supported on skills.description)
gcloud agent-registry agents search --location=us-central1 \
  --search-string="skills.description:MedDRA"

# Search for agents using boolean OR keyword matching
gcloud agent-registry agents search --location=us-central1 \
  --search-string="Clinical OR Pharmacovigilance"
```

---

## Searching MCP Servers

When searching for MCP servers, **always default to using the `mcp_agentregistry_search_mcp_servers` MCP tool** if the `agentregistry` MCP server is available. Use the `gcloud agent-registry mcp-servers search` command as a fallback.

### MCP Tool Usage (`mcp_agentregistry_search_mcp_servers`)

- **`parent`**: `projects/{project}/locations/{location}`
- **`searchString`**: Follows the same syntax as the gcloud command (e.g., `displayName:GitHub*`, `mcpServerId:run`).

### gcloud Fallback Usage

You can search for MCP servers using the `gcloud agent-registry mcp-servers search` command. This command supports a `--search-string` flag with the same match types as agents (exact `=`, token `:`, prefix `*`).

### Searchable Fields & Examples

You can search across fields such as `mcpServerId`, `name`, and `displayName`. Note that values containing colons (like URNs) must be escaped.

```bash
# Search for MCP servers by mcpServerId with prefix match
gcloud agent-registry mcp-servers search --location=us-east4 \
  --search-string="mcpServerId:\"urn:mcp:projects-1064111708665*\""

# Search for MCP servers containing the display name 'GitHub'
gcloud agent-registry mcp-servers search --location=us-east4 \
  --search-string="displayName:GitHub*"
```

---

## Searching Skills (Alpha)

When searching for skills, **always default to using the `mcp_agentregistry_search_skills` MCP tool** if the `agentregistry` MCP server is available. Use the `gcloud alpha agent-registry skills search` command as a fallback. **Remember:** Skills only work in `"global"`, `"us"`, or `"eu"` regions.

### MCP Tool Usage (`mcp_agentregistry_search_skills`)

- **`parent`**: `projects/{project}/locations/{location}` (where `{location}` is `global`, `us`, or `eu`)
- **`searchString`**: Search expression across `skillId`, `name`, `displayName`, `description`, `frontmatter.name`, `frontmatter.description`, `frontmatter.compatibility`, and `frontmatter.license` (supports `=`, `:`, `*`, `AND`, `OR`, `NOT`), or a natural-language query when `searchType` is `SEMANTIC`.
- **`searchType`**: `KEYWORD` or `SEMANTIC`.
- **`filter`**: Optional filter expression on `state`, `targetState`, `createTime`, or `updateTime` (e.g., `state=ACTIVE`).

### gcloud Fallback Usage

Search skills using keyword or semantic search via `gcloud alpha agent-registry skills search`:

```bash
# Keyword search across searchable fields
gcloud alpha agent-registry skills search --location=us \
  --query="weather" --search-type=keyword

# Semantic search based on natural language query meaning
gcloud alpha agent-registry skills search --location=us \
  --query="find skills that build documents" --search-type=semantic
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
- **location**: "Which region? (e.g. `us-central1`)" — only if `compute/region` was not set. **Note for Skills:** Skills only work in `"global"`, `"us"`, or `"eu"` regions. If the user asks for a Skill in any other region, **do not pass that region to the gcloud command**. Inform the user that Skills are only supported in `global`, `us`, or `eu` regions and ask them to select one of those options.
- **project**: "Which project?" — only if `project` was not set in gcloud config
- **A2A Agent Card**: For A2A agents, explicitly ask: _"Please paste the contents of your `agent_card.json` file."_ and use it for `--agent-spec-content`.
- **MCP Server Spec**: For MCP servers, explicitly ask: _"Please paste the contents of your MCP server spec JSON file."_ and use it for `--mcp-server-spec-content`.
- **GKE Deployments**: Ask for the target path (current folder, specific folder, or file) and the functional type (`AGENT` or `MCP_SERVER`).
- **Management Boundary Setup (`boundary-configs`, `capability-configs`, `boundaries`)**: Ask for the parent Folder ID (`--folder`) or Organization ID (`--organization`), how they want to partition perimeters (e.g., tag key `<ORG_ID>/environment` with values `dev`/`prod` vs. single boundary), whether each perimeter should have its own dedicated Management Project and `CapabilityConfig` (recommended for strict `dev`/`prod` catalog and IAM isolation) or share one hub, which project(s) to designate as Management Project(s) (resolving project IDs to project numbers `projects/<PROJECT_NUMBER>`), whether `--types` should be `agent-management` or `agent-management,app-management`, and which member projects to enroll via tag bindings.

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

