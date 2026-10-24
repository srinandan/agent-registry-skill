# Google Cloud Agent Registry Skill

[![CI](https://github.com/srinandan/agent-registry-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/srinandan/agent-registry-skill/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/srinandan/agent-registry-skill)](https://github.com/srinandan/agent-registry-skill/releases)
[![License](https://img.shields.io/github/license/srinandan/agent-registry-skill)](LICENSE)

A skill for the Gemini CLI and AI agents to interact with Google Cloud's Agent Registry using `gcloud agent-registry` commands (and `gcloud alpha agent-registry skills` for Skills).

## Features

- **Automated Authentication**: Helps with `gcloud auth login` and project configuration.
- **Resource Management**: Create, list, describe, and delete Agents, MCP Servers, Endpoints, Services, Bindings, and Skills (Alpha).
- **Smart Approvals**: Executes read-only commands (`list`, `describe`) immediately, while requesting approval for mutating commands (`create`, `update`, `delete`).
- **Rich Examples**: Built-in support for registering common resources like GitHub MCP Servers, Salesforce Agents, and Vertex AI Model Garden endpoints.
- **Python ADK Integration**: Specialized support and snippets for the Google Agent Development Kit (ADK).
- **GKE Based Agents**: Support for configuring Kubernetes Deployments to act as Agents or MCP Servers.
- **Skills Management**: Built-in support for exploring and managing Skills and Skill Revisions via the `agentregistry` MCP server tools (`list_skills`, `get_skill`, `create_skill`, `update_skill`, `delete_skill`, `search_skills`, `list_skill_revisions`, `get_skill_revision`, `create_skill_revision`, `delete_skill_revision`) and `gcloud alpha agent-registry skills`.
- **Management Boundary Governance**: Interactive guidance and best practices for Agent Registry administrators to configure hub-and-spoke perimeters (`BoundaryConfig`, `CapabilityConfig`, `Boundary`, and Tag Bindings) and verify cross-project agent discovery.

## Installation

You can install the `agent-registry-skill` using the GitHub CLI (`gh`):

```bash
gh skill install srinandan/agent-registry-skill
```

## Usage Examples

Once installed, you can talk to Gemini in natural language:

-   *"List my agents in us-central1"*
-   *"Describe the MCP server named github-mcp"*
-   *"Register a new Salesforce agent at https://api.salesforce.com/v1"*
-   *"Show me all registered endpoints"*
-   *"Delete the service called old-test-service"*
-   *"Show me all the agents where the runtime is reasoningEngine"*
-   *"Show agents with identity matching 'my-service-sa'"*
-   *"Which MCP Server has a tool named search_documents?"*
-   *"List agents based on reasoning engine in us-central1"*
-   *"Help me set up a management boundary for dev and prod under folder 849163983723"*
-   *"Create a capability config and boundary for agent management"*

## Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) version **565.0.0** or higher (minimum).
- `gcloud alpha` component version **2026.04.10** or higher (minimum).
- **Google ADK** version **1.31.0** or higher (minimum) for Python integration.
- Proper permissions to access Agent Registry in your Google Cloud project.

## Permissions

The following IAM roles are required to interact with the Agent Registry and configure Management Boundaries:

| Role | Target Resource | Access Level |
|------|-----------------|--------------|
| `roles/agentregistry.admin` | Project / Management Project | Full administrative access to Agent Registry |
| `roles/agentregistry.editor` | Project / Management Project | Editor access to Agent Registry |
| `roles/agentregistry.viewer` | Project / Management Project | Read-only access to Agent Registry |
| `roles/resourcemanager.editor` | Parent Folder or Organization | Create, update, link, and delete `BoundaryConfig`, `CapabilityConfig`, and `Boundary` resources |
| `roles/resourcemanager.viewer` | Parent Folder or Organization | Read `BoundaryConfig`, `CapabilityConfig`, `Boundary`, and `BoundaryMember` resources |
| `roles/owner` or `roles/editor` | Candidate BYO Management Project | Grants `resourcemanager.projects.associateToCapabilityConfig` to designate an existing project as a Management Project |
| `roles/resourcemanager.tagUser` | Tag Value + Target Projects | Bind/unbind tag values (`tags bindings create/delete`) to enroll projects in a boundary |

## Contributing
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Support
This demo is NOT endorsed by Google or Google Cloud. The repo is intended for educational/hobbyists use only.

## License
This project is licensed under the terms of the [LICENSE](LICENSE) file
