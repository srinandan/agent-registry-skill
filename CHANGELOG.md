# Changelog

All notable changes to the Google Cloud Agent Registry Skill are recorded here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this
project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Quick Add GCP Service (5-Variant Endpoint Registration for Agent Gateway)** (#22):
  - Added [`agent-registry/scripts/quick-add-gcp-service.sh`](agent-registry/scripts/quick-add-gcp-service.sh) and documentation in [`agent-registry/SKILL.md`](agent-registry/SKILL.md) to register all 5 Google Cloud API endpoint URL variants (`Base`, `Base mTLS`, `Locational`, `Locational mTLS`, and `Regional REP`) for Governed Target Services (`aiplatform`, `discoveryengine`, `pubsub`, `storage`).
- **AI Applications (`ai-applications`) & Resource-Level IAM Policy Management** (#22):
  - Added Section 7 (`AI Applications (ai-applications)`) to [`agent-registry/SKILL.md`](agent-registry/SKILL.md) and CLI reference documentation to [`agent-registry/references/gcloud-command.md`](agent-registry/references/gcloud-command.md) covering `list`, `describe`, `search` (`--search-string` / `--filter`), `create`, `update`, and `delete` for AI Applications, child resource discovery (`gcloud agent-registry ai-applications {agents,mcp-servers,endpoints} {list,describe,search}`), and `agentregistry` MCP tools (`mcp_agentregistry_list_ai_applications`, `mcp_agentregistry_get_ai_application`, `mcp_agentregistry_list_ai_application_agents`, `mcp_agentregistry_get_ai_application_agent`, `mcp_agentregistry_list_ai_application_mcp_servers`, `mcp_agentregistry_get_ai_application_mcp_server`, `mcp_agentregistry_list_ai_application_endpoints`, `mcp_agentregistry_get_ai_application_endpoint`).
  - Added resource-level IAM policy commands (`get-iam-policy`, `set-iam-policy`, `add-iam-policy-binding`, `remove-iam-policy-binding`) and required IAM permissions (`agentregistry.googleapis.com/aiApplications.{getIamPolicy,setIamPolicy}` and `agentregistry.googleapis.com/skills.{getIamPolicy,setIamPolicy}`) for both **AI Applications** (`gcloud agent-registry ai-applications`) and **Skills** (`gcloud alpha agent-registry skills`), with read-only vs. mutating confirmation guardrails.
  - Expanded [`agent-registry/agent_registry.evalset.json`](agent-registry/agent_registry.evalset.json) to 31 evaluation cases covering AI Applications discovery, subresources, resource-level IAM policy operations on AI Applications and Skills, and 5-variant Quick Add GCP Service registration for Agent Gateway.
- **Full MCP Server support for Skills & Skill Revisions** (#21):
  - Updated [`agent-registry/SKILL.md`](agent-registry/SKILL.md) to support managing all Skills and Skill Revisions operations via the `agentregistry` MCP server tools (`mcp_agentregistry_list_skills`, `mcp_agentregistry_get_skill`, `mcp_agentregistry_create_skill`, `mcp_agentregistry_update_skill`, `mcp_agentregistry_delete_skill`, `mcp_agentregistry_search_skills`, `mcp_agentregistry_list_skill_revisions`, `mcp_agentregistry_get_skill_revision`, `mcp_agentregistry_create_skill_revision`, and `mcp_agentregistry_delete_skill_revision`), defaulting to `mcp_agentregistry_search_skills` for keyword and semantic skill searches with `gcloud alpha agent-registry skills` as CLI fallback.
- **Management Boundary setup & admin governance** (#21):
  - Added Section 7 (`Management Boundary Setup (Admin Governance)`) to [`agent-registry/SKILL.md`](agent-registry/SKILL.md) guiding administrators through `BoundaryConfig`, `CapabilityConfig`, `Boundary`, and Tag Binding setup using `gcloud resource-manager`.
  - Added interactive scoping prompts (Folder vs. Organization anchor, tag-key partitioning strategy, dedicated vs. shared Management Project per perimeter for `dev`/`prod` catalog and IAM isolation, Bring-Your-Own vs. Google-managed Management Project, `agent-management` vs. `agent-management,app-management` capability types, and member project enrollment).
  - Added a dedicated **Required IAM Roles & Permissions for Boundary Setup** reference table detailing target attachment points and underlying `resourcemanager.*` permissions (`roles/resourcemanager.editor` and `roles/resourcemanager.viewer` on the parent Folder/Organization, `roles/owner` or `roles/editor` granting `resourcemanager.projects.associateToCapabilityConfig` on a candidate BYO Management Project, `roles/resourcemanager.tagUser` on the Tag Value and target projects, and `roles/agentregistry.admin`/`viewer` on the Management Project).
  - Documented architectural best practices and guardrails: configuring `BoundaryConfig` `tagKey` before attaching boundaries, using project numbers (`projects/<PROJECT_NUMBER>`), delete-then-create tag rebinding semantics, centralizing manual `Services`/`Bindings` in the Management Project, and required teardown ordering.
  - Added CLI reference documentation for `gcloud resource-manager boundary-configs`, `capability-configs`, and `boundaries` to [`agent-registry/references/gcloud-command.md`](agent-registry/references/gcloud-command.md).
- **ADK skill evaluation suite & LLM-as-a-judge CI workflow** (#21):
  - Added a 27-case ADK `EvalSet` evaluation suite ([`agent-registry/agent_registry.evalset.json`](agent-registry/agent_registry.evalset.json)) covering MCP servers, Agents, Endpoints, Bindings, GKE deployment annotations, Skills & Revisions (Alpha), Dashboards, Management Boundary governance (including IAM roles & permissions), and Python ADK integration.
  - Added documentation-only `LlmAgent` builder ([`evals/doc_only_agent.py`](evals/doc_only_agent.py)), heuristic + Gemini LLM-as-a-judge runner ([`evals/runner.py`](evals/runner.py)), Markdown report generator ([`evals/report.py`](evals/report.py)), pytest suite ([`tests/test_skill_evalsets.py`](tests/test_skill_evalsets.py)), and GitHub Actions workflow ([`.github/workflows/skill-evals.yml`](.github/workflows/skill-evals.yml)).

### Fixed
- **Skills supported regions guardrail** (#19):
  Restricted `gcloud alpha agent-registry skills` locations strictly to `global`, `us`, or `eu`, instructing the agent not to pass single-region locations (such as `us-central1`) and to prompt the user to select a supported multi-region or `global`.

## [0.7.0] - 2026-07-24

### Added
- **Skills & Skill Revisions (Alpha)** (#18):
  - Added support for creating, listing, describing, updating, deleting, and searching (keyword and semantic) Agent Registry Skills using `gcloud alpha agent-registry skills`.
  - Added support for managing Skill Revisions (`list`, `describe`, `download`) via `gcloud alpha agent-registry skills revisions`.
  - Added consolidated Skill Dashboard script ([`agent-registry/scripts/skill-dashboard.sh`](agent-registry/scripts/skill-dashboard.sh)).

### Changed
- **Migration to GA `gcloud agent-registry` commands** (#18):
  Migrated core Agent Registry resources (`agents`, `mcp-servers`, `endpoints`, `services`, `bindings`, `operations`) from `gcloud alpha agent-registry` to GA `gcloud agent-registry` commands and updated [`agent-registry/references/adk-docs.md`](agent-registry/references/adk-docs.md) sample code references.

## [0.6.0] - 2026-04-26

### Added
- **Agent Registry Bindings capability** (#17):
  - Added support for creating, listing, describing, updating, and deleting `Bindings` (`gcloud agent-registry bindings`) to connect source agents to target resources or delegated auth providers (`--auth-provider`).
  - Updated [`agent-registry/references/gcloud-command.md`](agent-registry/references/gcloud-command.md) and [`agent-registry/references/adk-docs.md`](agent-registry/references/adk-docs.md) with bindings documentation, optional ADK dependencies, and authentication guidance.

## [0.5.0] - 2026-04-20

### Changed
- **Repository structure & GitHub templates** (#16):
  Refactored skill assets into the [`agent-registry/`](agent-registry/) directory structure, added `SKILL.md` frontmatter validation ([`.github/scripts/validate_skill.py`](.github/scripts/validate_skill.py)), and added GitHub issue templates and `gh skill install` instructions.

## [0.4.0] - 2026-04-10

### Added
- **Agent & MCP Server search (`search` commands & MCP tools)** (#15):
  Added support for searching agents (`mcp_agentregistry_search_agents` / `gcloud agent-registry agents search`) and MCP servers (`mcp_agentregistry_search_mcp_servers` / `gcloud agent-registry mcp-servers search`) with exact (`=`), token (`:`), and prefix (`*`) matching across `agentId`, `mcpServerId`, `displayName`, and A2A skill fields.
- **URN filtering by `agentId` and `mcpServerId`** (#14):
  Documented RFC 8141 URN formats (`urn:agent:...`, `urn:mcp:...`) and substring filtering for Vertex AI Reasoning Engine, GKE, and Cloud Run workloads.
- **OSV-Scanner security workflow** (#12):
  Added automated OSV vulnerability scanning in GitHub Actions ([`.github/workflows/osv-scanner.yml`](.github/workflows/osv-scanner.yml)).

### Changed
- **ADK integration documentation** (#13):
  Expanded [`agent-registry/references/adk-docs.md`](agent-registry/references/adk-docs.md) with comprehensive Python ADK initialization, discovery, `McpToolset`, and remote A2A sub-agent examples.

## [0.3.0] - 2026-03-17

### Added
- **GKE workload annotation script** (#11):
  Added [`agent-registry/scripts/annotate_gke.py`](agent-registry/scripts/annotate_gke.py) to annotate Kubernetes Deployment manifests with `apphub.cloud.google.com/functional-type` (`AGENT` or `MCP_SERVER`).
- **Agent & MCP Server Markdown dashboards** (#10):
  Added [`agent-registry/scripts/agent-dashboard.sh`](agent-registry/scripts/agent-dashboard.sh) and [`agent-registry/scripts/mcp-dashboard.sh`](agent-registry/scripts/mcp-dashboard.sh) to generate consolidated multi-region inventory tables.

## [0.2.0] - 2026-03-16

### Added
- **Advanced attribute & runtime filtering**:
  Added filtering mappings for runtime (`attributes."agentregistry.googleapis.com/system/RuntimeReference".uri`), identity (`attributes."agentregistry.googleapis.com/system/RuntimeIdentity".principal`), and MCP server tool names (`tools.name`).
- **IAM role reference & automated bug reporting** (#7, #8, #9):
  Added required Agent Registry IAM roles (`roles/agentregistry.admin`, `editor`, `viewer`), `gh issue create` bug-reporting workflow, and ShellCheck CI validation.

## [0.1.0] - 2026-03-14

### Added
- **Initial release of Google Cloud Agent Registry Skill** (#1, #2, #3, #4, #5):
  - Core natural-language-to-`gcloud` workflow for registering, listing, describing, updating, and deleting MCP Servers, Agents (including A2A agent cards), Endpoints, and Services.
  - Read-only vs. mutating command approval workflow.
  - Bundled `gcloud` CLI reference (`references/gcloud-command.md`) and initial Python ADK integration guide (`references/adk-docs.md`).
