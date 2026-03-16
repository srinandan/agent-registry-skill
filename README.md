# Google Cloud Agent Registry Skill

[![CI](https://github.com/srinandan/agent-registry-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/srinandan/agent-registry-skill/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/srinandan/agent-registry-skill)](https://github.com/srinandan/agent-registry-skill/releases)
[![License](https://img.shields.io/github/license/srinandan/agent-registry-skill)](LICENSE)

A skill for the Gemini CLI and AI agents to interact with Google Cloud's Agent Registry using `gcloud alpha agent-registry` commands.

## Features

- **Automated Authentication**: Helps with `gcloud auth login` and project configuration.
- **Resource Management**: Create, list, describe, and delete Agents, MCP Servers, and Endpoints.
- **Smart Approvals**: Executes read-only commands (`list`, `describe`) immediately, while requesting approval for mutating commands (`create`, `update`, `delete`).
- **Rich Examples**: Built-in support for registering common resources like GitHub MCP Servers, Salesforce Agents, and Vertex AI Model Garden endpoints.
- **Python ADK Integration**: Specialized support and snippets for the Google Agent Development Kit (ADK).

## Installation

`agent-registry-skill` is an Agent Skill that can be used with your favorite CLI. Run this script to download and install the latest version:

```bash
curl -L https://raw.githubusercontent.com/srinandan/agent-registry-skill/refs/heads/main/installSkill.sh | sh -

To install a specific version or branch, set the `SKILL_VERSION` environment variable:

```bash
curl -L https://raw.githubusercontent.com/srinandan/agent-registry-skill/refs/heads/main/installSkill.sh | SKILL_VERSION=v1.0.0 sh -
```
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

## Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) version **560.0.0** or higher (minimum).
- `gcloud alpha` component version **2026.03.09** or higher (minimum).
- **Google ADK** version **1.26.0** or higher (minimum) for Python integration.
- Proper permissions to access Agent Registry in your Google Cloud project.

## Permissions

The following IAM roles are required to interact with the Agent Registry:

| Role | Access Level |
|------|--------------|
| `roles/agentregistry.admin` | Full administrative access |
| `roles/agentregistry.editor` | Editor access |
| `roles/agentregistry.viewer` | Read only access |

## Contributing
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Support
This demo is NOT endorsed by Google or Google Cloud. The repo is intended for educational/hobbyists use only.

## License
This project is licensed under the terms of the [LICENSE](LICENSE) file
