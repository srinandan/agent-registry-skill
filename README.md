# Google Cloud Agent Registry skill

[![CI](https://github.com/srinandan/agent-registry-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/srinandan/agent-registry-skill/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/srinandan/agent-registry-skill)](https://github.com/srinandan/agent-registry-skill/releases)
[![License](https://img.shields.io/github/license/srinandan/agent-registry-skill)](LICENSE)

This skill connects [AntiGravity CLI](https://antigravity.google/product/antigravity-cli/) and other agent harnesses to Google Cloud Agent Registry. It runs `gcloud agent-registry` commands (including `gcloud alpha agent-registry skills`), `gcloud beta run` commands, `gcloud resource-manager` commands, and `agentregistry` and `developerknowledge` MCP server tools.

## Features

- **Authentication and project setup**: Runs `gcloud auth login` and configures the active Google Cloud project and region.
- **Resource management**: Creates, lists, describes, searches, updates, and deletes Agents, MCP Servers, Endpoints, Services, Bindings, AI Applications (`ai-applications` and child `agents`, `mcp-servers`, and `endpoints`), and Skills (`skills`).
- **Resource-level IAM policies**: Reads and updates IAM policies (`get-iam-policy`, `set-iam-policy`, `add-iam-policy-binding`, `remove-iam-policy-binding`) on individual AI Applications (`ai-applications`) and Skills (`skills`).
- **Approval workflow**: Runs read-only commands (`list`, `describe`, `search`, `get-iam-policy`) immediately. Requests user approval before running mutating commands (`create`, `update`, `delete`, `deploy`, `set-iam-policy`, `add-iam-policy-binding`, `remove-iam-policy-binding`).
- **Quick-add GCP services and resource examples**: Registers GitHub MCP Servers, Salesforce Agents, and Vertex AI Model Garden endpoints. Runs `./scripts/quick-add-gcp-service.sh` to register all 5 URL variants (Base, Base mTLS, Locational, Locational mTLS, and Regional REP) for governed GCP services (`aiplatform`, `discoveryengine`, `pubsub`, `storage`) behind Agent Gateway.
- **Python ADK integration**: Provides Python code snippets for the Google Agent Development Kit (ADK).
- **GKE and Cloud Run automatic registration (`--functional-type`)**: Configures Kubernetes `Deployment` manifests (`registry.gke.io/functional-type`, `a2a-protocol.org/agent-card`, `modelcontextprotocol.info/{urls,capabilities}`, `iam.gke.io/spiffe-identity-type: agent-identity`, and `./scripts/annotate_gke.py`). Deploys and updates Cloud Run services and jobs (`gcloud beta run deploy`, `services update`, `multi-region-services update`, `jobs create|deploy|update`) with `--functional-type=agent|mcp-server` and `--identity-type=agent-identity|service-account`.
- **Official documentation fallback (`developerknowledge` MCP server)**: If a request asks about an undocumented flag, schema, or error, the skill queries the `developerknowledge` MCP server (`search_documents`, `get_documents`, `answer_query`) against `docs.cloud.google.com/agent-registry` and `docs.cloud.google.com/run/docs/ai`.
- **Skills management**: Manages Skills, Skill Revisions, and Skill IAM policies through `agentregistry` MCP tools (`list_skills`, `get_skill`, `create_skill`, `update_skill`, `delete_skill`, `search_skills`, `list_skill_revisions`, `get_skill_revision`, `create_skill_revision`, `delete_skill_revision`) and `gcloud alpha agent-registry skills` / `gcloud agent-registry skills` (`get-iam-policy`, `set-iam-policy`, `add-iam-policy-binding`, `remove-iam-policy-binding`).
- **AI Applications management**: Lists, describes, searches, creates, updates, and deletes AI Applications (`ai-applications`) and child `agents`, `mcp-servers`, and `endpoints` through `agentregistry` MCP tools (`list_ai_applications`, `get_ai_application`, `list_ai_application_agents`, `get_ai_application_agent`, `list_ai_application_mcp_servers`, `get_ai_application_mcp_server`, `list_ai_application_endpoints`, `get_ai_application_endpoint`) and `gcloud agent-registry ai-applications`. Sets resource-level IAM policies (`get-iam-policy`, `set-iam-policy`, `add-iam-policy-binding`, `remove-iam-policy-binding`).
- **Management boundary governance**: Configures hub-and-spoke perimeters (`BoundaryConfig`, `CapabilityConfig`, `Boundary`, and Tag Bindings) and verifies cross-project agent discovery.

## Installation

Install the skill with the GitHub CLI (`gh`):

```bash
gh skill install srinandan/agent-registry-skill
```

## Usage examples

Send natural-language prompts to [AntiGravity CLI](https://antigravity.google/product/antigravity-cli/) or your agent harness:

- *"List my agents in us-central1"*
- *"Describe the MCP server named github-mcp"*
- *"Register a new Salesforce agent at https://api.salesforce.com/v1"*
- *"Show me all registered endpoints"*
- *"Delete the service called old-test-service"*
- *"Show me all the agents where the runtime is reasoningEngine"*
- *"Show agents with identity matching 'my-service-sa'"*
- *"Which MCP Server has a tool named search_documents?"*
- *"List agents based on reasoning engine in us-central1"*
- *"Help me set up a management boundary for dev and prod under folder 849163983723"*
- *"Create a capability config and boundary for agent management"*
- *"List all AI applications in us-central1 and show agents under the default AI application"*
- *"Grant group ai-team@example.com viewer access on AI application my-ai-app"*
- *"Set the IAM policy on skill my-skill in us"*

## Prerequisites

- Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) version 565.0.0 or later.
- Install the `gcloud alpha` component version 2026.04.10 or later.
- Install Google ADK version 1.31.0 or later for Python integration.
- Grant the caller the IAM roles listed in [Permissions](#permissions).

## Permissions

Grant the following IAM roles to the caller before running Agent Registry or management boundary commands:

| Role | Target resource | Access level |
|------|-----------------|--------------|
| `roles/agentregistry.admin` | Project / Management Project | Full administrative access to Agent Registry |
| `roles/agentregistry.editor` | Project / Management Project | Editor access to Agent Registry |
| `roles/agentregistry.viewer` | Project / Management Project | Read-only access to Agent Registry |
| `roles/resourcemanager.editor` | Parent Folder or Organization | Create, update, link, and delete `BoundaryConfig`, `CapabilityConfig`, and `Boundary` resources |
| `roles/resourcemanager.viewer` | Parent Folder or Organization | Read `BoundaryConfig`, `CapabilityConfig`, `Boundary`, and `BoundaryMember` resources |
| `roles/owner` or `roles/editor` | Candidate BYO Management Project | Grants `resourcemanager.projects.associateToCapabilityConfig` to designate an existing project as a Management Project |
| `roles/resourcemanager.tagUser` | Tag Value + Target Projects | Bind and unbind tag values (`tags bindings create`, `tags bindings delete`) to enroll projects in a boundary |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution steps.

## Support

Google and Google Cloud do not endorse this repository. Use this repository for educational and hobbyist purposes only.

## License

The [LICENSE](LICENSE) file defines the license for this project.
