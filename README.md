# Google Cloud Agent Registry Skill

A skill for the Gemini CLI and AI agents to interact with Google Cloud's Agent Registry using `gcloud alpha agent-registry` commands.

## Features

- **Automated Authentication**: Helps with `gcloud auth login` and project configuration.
- **Resource Management**: Create, list, describe, and delete Agents, MCP Servers, and Endpoints.
- **Smart Approvals**: Executes read-only commands (`list`, `describe`) immediately, while requesting approval for mutating commands (`create`, `update`, `delete`).
- **Rich Examples**: Built-in support for registering common resources like GitHub MCP Servers, Salesforce Agents, and Vertex AI Model Garden endpoints.

## Installation

`agent-registry-skill` is an Agent Skill that can be used with your favorite CLI. Run this script to download and install the latest version:

```bash
curl -L https://raw.githubusercontent.com/srinandan/agent-registry-skill/refs/heads/main/installSkill.sh | sh -
```

### Manual Installation (Local)

## Usage Examples

Once installed, you can talk to Gemini in natural language:

-   *"List my agents in us-central1"*
-   *"Describe the MCP server named github-mcp"*
-   *"Register a new Salesforce agent at https://api.salesforce.com/v1"*
-   *"Show me all registered endpoints"*
-   *"Delete the service called old-test-service"*
-   *"Show me all the agents where the runtime is reasoningEngine"*
-   *"Show all agents with identity matching 'my-service-sa'"*

## Prerequisites

- [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/docs/install) installed.
- `gcloud alpha` component installed (`gcloud components install alpha`).
- Proper permissions to access Agent Registry in your Google Cloud project.

## Contributing
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Support
This demo is NOT endorsed by Google or Google Cloud. The repo is intended for educational/hobbyists use only.

## License
This project is licensed under the terms of the [LICENSE](LICENSE) file