# gcloud agent-registry Documentation

Documentation for `gcloud agent-registry` (GA) and `gcloud alpha agent-registry skills` (Alpha).

## Main Command: `gcloud agent-registry`

```text
NAME
    gcloud agent-registry - manage Agent Registry resources

SYNOPSIS
    gcloud agent-registry GROUP [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    Manage Agent Registry resources.

GCLOUD WIDE FLAGS
    These flags are available to all commands: --help.

    Run $ gcloud help for details.

GROUPS
    GROUP is one of the following:

     agents
        Manage Agent resources.

     ai-applications
        Manage Ai Application resources.

     bindings
        Manage Binding resources.

     endpoints
        Manage Endpoint resources.

     mcp-servers
        Manage Mcp Server resources.

     operations
        Manage Operation resources.

     services
        Manage Service resources.

NOTES
    This variant is also available:

        $ gcloud alpha agent-registry
```

---

## Subcommands

### agents

```text
NAME
    gcloud agent-registry agents - manage Agent resources

SYNOPSIS
    gcloud agent-registry agents COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) Manage Agent resources.

GCLOUD WIDE FLAGS
    These flags are available to all commands: --help.

    Run $ gcloud help for details.

COMMANDS
    COMMAND is one of the following:

     describe
        (ALPHA) Describe agents.

     list
        (ALPHA) List agents.

     search
        (ALPHA) Search agents.


NOTES
    This command is currently in alpha and might change without notice. If this
    command fails with API permission errors despite specifying the correct
    project, you might be trying to access an API with an invitation-only early
    access allowlist.
```

#### `search`

```text
NAME
    gcloud agent-registry agents search - search agents

SYNOPSIS
    gcloud agent-registry agents search --location=LOCATION
        [--search-string=SEARCH_STRING] [--search-type=SEARCH_TYPE]
        [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) search agents

EXAMPLES
    To search all agents, run:

        $ gcloud agent-registry agents search

REQUIRED FLAGS
     Location resource - Parent value for SearchAgentsRequest This represents a
     Cloud resource. (NOTE) Some attributes are not given arguments in this
     group but can be set in other ways.

     To set the project attribute:
      ◆ provide the argument --location on the command line with a fully
        specified name;
      ◆ provide the argument --project on the command line;
      ◆ set the property core/project.

     This must be specified.

       --location=LOCATION
          ID of the location or fully qualified identifier for the location.

          To set the location attribute:
          ▸ provide the argument --location on the command line.

OPTIONAL FLAGS
     --search-string=SEARCH_STRING
        Search criteria used to select the Agents to return. If no search
        criteria is specified then all accessible Agents will be returned.

        Search expressions can be used to restrict results based upon skills,
        agentId, description, name and trust, where the operators =, NOT, AND
        and OR can be used along with the suffix wildcard symbol *.

     --search-type=SEARCH_TYPE
        The type of search. If set, must be set to KEYWORD. SEARCH_TYPE must be
        (only one value is supported):

         keyword
            Search for a keyword across all searchable fields.
```


### bindings

```text
NAME
    gcloud agent-registry bindings - manage Binding resources

SYNOPSIS
    gcloud agent-registry bindings COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) Manage Binding resources.

GCLOUD WIDE FLAGS
    These flags are available to all commands: --help.

    Run $ gcloud help for details.

COMMANDS
    COMMAND is one of the following:

     create
        (ALPHA) Create bindings.

     delete
        (ALPHA) Delete bindings.

     describe
        (ALPHA) Describe bindings.

     list
        (ALPHA) List bindings.

     update
        (ALPHA) Update bindings.
```

### endpoints

```text
NAME
    gcloud agent-registry endpoints - manage Endpoint resources

SYNOPSIS
    gcloud agent-registry endpoints COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) Manage Endpoint resources.

GCLOUD WIDE FLAGS
    These flags are available to all commands: --help.

    Run $ gcloud help for details.

COMMANDS
    COMMAND is one of the following:

     describe
        (ALPHA) Describe endpoints.

     list
        (ALPHA) List endpoints.

NOTES
    This command is currently in alpha and might change without notice. If this
    command fails with API permission errors despite specifying the correct
    project, you might be trying to access an API with an invitation-only early
    access allowlist.
```

### mcp-servers

```text
NAME
    gcloud agent-registry mcp-servers - manage Mcp Server resources

SYNOPSIS
    gcloud agent-registry mcp-servers COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) Manage Mcp Server resources.

GCLOUD WIDE FLAGS
    These flags are available to all commands: --help.

    Run $ gcloud help for details.

COMMANDS
    COMMAND is one of the following:

     describe
        (ALPHA) Describe mcpServers.

     list
        (ALPHA) List mcpServers.

     search
        (ALPHA) Search mcpServers.


NOTES
    This command is currently in alpha and might change without notice. If this
    command fails with API permission errors despite specifying the correct
    project, you might be trying to access an API with an invitation-only early
    access allowlist.
```

#### `search`

```text
NAME
    gcloud agent-registry mcp-servers search - search MCP servers

SYNOPSIS
    gcloud agent-registry mcp-servers search --location=LOCATION
        [--search-string=SEARCH_STRING] [--search-type=SEARCH_TYPE]
        [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) search MCP servers

EXAMPLES
    To search all MCP servers, run:

        $ gcloud agent-registry mcp-servers search

REQUIRED FLAGS
     Location resource - Parent value for SearchMcpServersRequest This represents a
     Cloud resource.

     This must be specified.

       --location=LOCATION
          ID of the location or fully qualified identifier for the location.

OPTIONAL FLAGS
     --search-string=SEARCH_STRING
        Search criteria used to select the MCP Servers to return. If no search
        criteria is specified then all accessible MCP Servers will be returned.

        Search expressions can be used to restrict results based upon mcpServerId,
        name and displayName, where the operators =, NOT, AND and OR can be used
        along with the suffix wildcard symbol *.
```


### operations

```text
NAME
    gcloud agent-registry operations - manage Operation resources

SYNOPSIS
    gcloud agent-registry operations [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) Manage Operation resources.

GCLOUD WIDE FLAGS
    These flags are available to all commands: --access-token-file, --account,
    --billing-project, --configuration, --flags-file, --flatten, --format,
    --help, --impersonate-service-account, --log-http, --project, --quiet,
    --trace-token, --user-output-enabled, --verbosity.

    Run $ gcloud help for details.

NOTES
    This command is currently in alpha and might change without notice. If this
    command fails with API permission errors despite specifying the correct
    project, you might be trying to access an API with an invitation-only early
    access allowlist.
```

### services

```text
NAME
    gcloud agent-registry services - manage Service resources

SYNOPSIS
    gcloud agent-registry services COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) Manage Service resources.

GCLOUD WIDE FLAGS
    These flags are available to all commands: --help.

    Run $ gcloud help for details.

COMMANDS
    COMMAND is one of the following:

     create
        (ALPHA) Create services.

     delete
        (ALPHA) Delete services.

     describe
        (ALPHA) Describe services.

     list
        (ALPHA) List services.

     update
        (ALPHA) Update services.

NOTES
    If this command fails with API permission errors despite specifying the correct
    project, you might be trying to access an API with an invitation-only early
    access allowlist.
```

---

### skills (Alpha)

```text
NAME
    gcloud alpha agent-registry skills - manage Skill resources

SYNOPSIS
    gcloud alpha agent-registry skills GROUP | COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) Manage Skill resources.

GCLOUD WIDE FLAGS
    These flags are available to all commands: --help.

    Run $ gcloud help for details.

GROUPS
    GROUP is one of the following:

     revisions
        (ALPHA) Manage Skill Revision resources.

COMMANDS
    COMMAND is one of the following:

     add-iam-policy-binding
        (ALPHA) Add IAM policy binding to a Skill.

     create
        (ALPHA) Create skills.

     delete
        (ALPHA) Delete skills.

     describe
        (ALPHA) Describe skills.

     get-iam-policy
        (ALPHA) Get IAM policy for a Skill.

     list
        (ALPHA) List skills.

     remove-iam-policy-binding
        (ALPHA) Remove IAM policy binding from a Skill.

     search
        (ALPHA) search skills.

     set-iam-policy
        (ALPHA) Set the IAM policy for a Skill.

     update
        (ALPHA) Update skills.

NOTES
    This command is currently in alpha and might change without notice. If this
    command fails with API permission errors despite specifying the correct
    project, you might be trying to access an API with an invitation-only early
    access allowlist.
```

#### `create`

```text
NAME
    gcloud alpha agent-registry skills create - create skills

SYNOPSIS
    gcloud alpha agent-registry skills create SKILL [--async]
        [--default-revision=DEFAULT_REVISION] [--description=DESCRIPTION]
        [--display-name=DISPLAY_NAME] [--location=LOCATION]
        [--publisher=PUBLISHER] [--request-id=REQUEST_ID]
        [--target-state=TARGET_STATE] [--type=TYPE]
        [--initial-revision-name=INITIAL_REVISION_NAME --payload=PAYLOAD
          | [--gcs-source-uri=GCS_SOURCE_URI
          : --gcs-source-generation=GCS_SOURCE_GENERATION]]
        [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) Create a skill
```

#### `search`

```text
NAME
    gcloud alpha agent-registry skills search - search skills

SYNOPSIS
    gcloud alpha agent-registry skills search --location=LOCATION
        [--query=QUERY] [--search-type=SEARCH_TYPE] [--filter=EXPRESSION]
        [--limit=LIMIT] [--page-size=PAGE_SIZE] [--sort-by=[FIELD,...]]
        [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) search skills
```

#### `revisions`

```text
NAME
    gcloud alpha agent-registry skills revisions - manage Skill Revision resources

SYNOPSIS
    gcloud alpha agent-registry skills revisions COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) Manage Skill Revision resources.

COMMANDS
    COMMAND is one of the following:

     create
        (ALPHA) Create skillRevisions.

     delete
        (ALPHA) Delete skillRevisions.

     describe
        (ALPHA) Describe skillRevisions.

     download
        (ALPHA) Download the payload of a Skill Revision.

     list
        (ALPHA) List skillRevisions.
```

#### `get-iam-policy` / `set-iam-policy` / `add-iam-policy-binding` / `remove-iam-policy-binding`

```text
SYNOPSIS
    gcloud alpha agent-registry skills get-iam-policy (SKILL : --location=LOCATION)
        [--filter=EXPRESSION] [--limit=LIMIT] [--page-size=PAGE_SIZE]
        [--sort-by=[FIELD,...]] [GCLOUD_WIDE_FLAG ...]

    gcloud alpha agent-registry skills set-iam-policy (SKILL : --location=LOCATION)
        POLICY_FILE [GCLOUD_WIDE_FLAG ...]

    gcloud alpha agent-registry skills add-iam-policy-binding
        (SKILL : --location=LOCATION) --member=PRINCIPAL --role=ROLE
        [--condition=[KEY=VALUE,...] | --condition-from-file=PATH_TO_FILE]
        [GCLOUD_WIDE_FLAG ...]

    gcloud alpha agent-registry skills remove-iam-policy-binding
        (SKILL : --location=LOCATION) --member=PRINCIPAL --role=ROLE
        [--all | --condition=[KEY=VALUE,...]
          | --condition-from-file=PATH_TO_FILE] [GCLOUD_WIDE_FLAG ...]
```

---

### ai-applications

```text
NAME
    gcloud agent-registry ai-applications - manage Ai Application resources

SYNOPSIS
    gcloud agent-registry ai-applications GROUP | COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    Manage Ai Application resources (also available under
    `gcloud alpha agent-registry ai-applications`).

GROUPS
    GROUP is one of the following:

     agents
        Manage Agent resources scoped to an AI Application.

     endpoints
        Manage Endpoint resources scoped to an AI Application.

     mcp-servers
        Manage Mcp Server resources scoped to an AI Application.

COMMANDS
    COMMAND is one of the following:

     add-iam-policy-binding
        Add IAM policy binding to an AI Application.

     create
        Create aiApplications.

     delete
        Delete aiApplications.

     describe
        Describe aiApplications.

     get-iam-policy
        Get IAM policy for an AI Application.

     list
        List aiApplications.

     remove-iam-policy-binding
        Remove IAM policy binding from an AI Application.

     search
        Search aiApplications.

     set-iam-policy
        Set the IAM policy for an AI Application.

     update
        Update aiApplications.
```

#### `list` / `describe` / `search`

```text
SYNOPSIS
    gcloud agent-registry ai-applications list --location=LOCATION
        [--filter=EXPRESSION] [--limit=LIMIT] [--page-size=PAGE_SIZE]
        [--sort-by=[FIELD,...]] [GCLOUD_WIDE_FLAG ...]

    gcloud agent-registry ai-applications describe
        (AI_APPLICATION : --location=LOCATION) [GCLOUD_WIDE_FLAG ...]

    gcloud agent-registry ai-applications search --location=LOCATION
        [--search-string=SEARCH_STRING] [--filter=EXPRESSION]
        [--limit=LIMIT] [--page-size=PAGE_SIZE] [GCLOUD_WIDE_FLAG ...]
```

#### `create` / `update` / `delete`

```text
SYNOPSIS
    gcloud agent-registry ai-applications create
        (AI_APPLICATION : --location=LOCATION) [--async]
        [--description=DESCRIPTION] [--display-name=DISPLAY_NAME]
        [--labels=[KEY=VALUE,...]] [--members=[MEMBERS,...]]
        [--request-id=REQUEST_ID] [GCLOUD_WIDE_FLAG ...]

    gcloud agent-registry ai-applications update
        (AI_APPLICATION : --location=LOCATION) [--async]
        [--description=DESCRIPTION] [--display-name=DISPLAY_NAME]
        [--labels=[KEY=VALUE,...]] [--members=[MEMBERS,...]]
        [--request-id=REQUEST_ID] [GCLOUD_WIDE_FLAG ...]

    gcloud agent-registry ai-applications delete
        (AI_APPLICATION : --location=LOCATION) [--async] [--etag=ETAG]
        [--request-id=REQUEST_ID] [GCLOUD_WIDE_FLAG ...]
```

#### `get-iam-policy` / `set-iam-policy` / `add-iam-policy-binding` / `remove-iam-policy-binding`

```text
SYNOPSIS
    gcloud agent-registry ai-applications get-iam-policy
        (AI_APPLICATION : --location=LOCATION) [--filter=EXPRESSION]
        [--limit=LIMIT] [--page-size=PAGE_SIZE] [--sort-by=[FIELD,...]]
        [GCLOUD_WIDE_FLAG ...]

    gcloud agent-registry ai-applications set-iam-policy
        (AI_APPLICATION : --location=LOCATION) POLICY_FILE
        [GCLOUD_WIDE_FLAG ...]

    gcloud agent-registry ai-applications add-iam-policy-binding
        (AI_APPLICATION : --location=LOCATION) --member=PRINCIPAL --role=ROLE
        [--condition=[KEY=VALUE,...] | --condition-from-file=PATH_TO_FILE]
        [GCLOUD_WIDE_FLAG ...]

    gcloud agent-registry ai-applications remove-iam-policy-binding
        (AI_APPLICATION : --location=LOCATION) --member=PRINCIPAL --role=ROLE
        [--all | --condition=[KEY=VALUE,...]
          | --condition-from-file=PATH_TO_FILE] [GCLOUD_WIDE_FLAG ...]
```

#### `agents` / `mcp-servers` / `endpoints` (Subgroups under `ai-applications`)

```text
SYNOPSIS
    gcloud agent-registry ai-applications agents (list | describe | search)
        --ai-application=AI_APPLICATION --location=LOCATION
        [--search-string=SEARCH_STRING] [--filter=EXPRESSION]
        [GCLOUD_WIDE_FLAG ...]

    gcloud agent-registry ai-applications mcp-servers (list | describe | search)
        --ai-application=AI_APPLICATION --location=LOCATION
        [--search-string=SEARCH_STRING] [--filter=EXPRESSION]
        [GCLOUD_WIDE_FLAG ...]

    gcloud agent-registry ai-applications endpoints (list | describe | search)
        --ai-application=AI_APPLICATION --location=LOCATION
        [--search-string=SEARCH_STRING] [--filter=EXPRESSION]
        [GCLOUD_WIDE_FLAG ...]
```

---

## Cloud Resource Manager: Management Boundary Commands

Documentation for `gcloud resource-manager boundary-configs`, `gcloud resource-manager capability-configs`, and `gcloud resource-manager boundaries`.

### `boundary-configs`

```text
NAME
    gcloud resource-manager boundary-configs - manage Resource Manager boundary
        configurations

SYNOPSIS
    gcloud resource-manager boundary-configs COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    Commands to describe and update Resource Manager boundary configurations.

COMMANDS
    COMMAND is one of the following:

     describe
        Describe a boundary configuration.

     update
        Update a boundary configuration.
```

#### `update`

```text
NAME
    gcloud resource-manager boundary-configs update - update a boundary
        configuration

SYNOPSIS
    gcloud resource-manager boundary-configs update
        (--clear-tag-key | --tag-key=TAG_KEY)
        (--folder=FOLDER_ID | --organization=ORGANIZATION_ID) [--async]
        [--etag=ETAG] [GCLOUD_WIDE_FLAG ...]

EXAMPLES
    To update the tag key of the boundary configuration in a folder with ID
    849163983723, run:

        $ gcloud resource-manager boundary-configs update \
            --folder=849163983723 --tag-key="975672035171/environment"
```

---

### `capability-configs`

```text
NAME
    gcloud resource-manager capability-configs - manage Cloud Resource Manager
        CapabilityConfigs

SYNOPSIS
    gcloud resource-manager capability-configs COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    A CapabilityConfig allows managing experiences like applications and agents
    on a logical administrative perimeter of Projects (Boundary).

COMMANDS
    COMMAND is one of the following:

     create
        Create a CapabilityConfig under a parent Organization, Folder, or
        Project.

     delete
        Delete a CapabilityConfig.

     describe
        Describe a CapabilityConfig.

     list
        List CapabilityConfigs that are direct children of a parent resource.

     update
        Update a CapabilityConfig.
```

#### `create`

```text
NAME
    gcloud resource-manager capability-configs create - create a
        CapabilityConfig under a parent Organization, Folder, or Project

SYNOPSIS
    gcloud resource-manager capability-configs create
        (CAPABILITY_CONFIG
          : --folder=FOLDER --organization=ORGANIZATION --project=PROJECT)
        --types=[TYPES,...] [--async] [--boundaries=[BOUNDARIES,...]]
        [--display-name=DISPLAY_NAME] [--management-project=MANAGEMENT_PROJECT]
        [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    Creating a CapabilityConfig triggers the creation of a Management Project
    if one is not supplied via --management-project.

REQUIRED FLAGS
     --types=[TYPES,...]
        Comma-separated list of CapabilityConfig types (e.g. app-management,
        agent-management). TYPES must be one of: app-management,
        agent-management.

OPTIONAL FLAGS
     --boundaries=[BOUNDARIES,...]
        List of Boundaries associated with this CapabilityConfig.

     --display-name=DISPLAY_NAME
        Human-readable display name of the CapabilityConfig (4 to 30
        characters).

     --management-project=MANAGEMENT_PROJECT
        Management Project associated with this CapabilityConfig (e.g.
        projects/1066599796742). Must use the project number.
```

#### `update`

```text
NAME
    gcloud resource-manager capability-configs update - update a
        CapabilityConfig

SYNOPSIS
    gcloud resource-manager capability-configs update
        (CAPABILITY_CONFIG
          : --folder=FOLDER --organization=ORGANIZATION --project=PROJECT)
        [--async] [--display-name=DISPLAY_NAME] [--etag=ETAG]
        [--types=[TYPES,...]]
        [--boundaries=[BOUNDARIES,...] | --clear-boundaries]
        [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    Updates the display name, types, or boundaries of an existing
    CapabilityConfig.
```

---

### `boundaries`

```text
NAME
    gcloud resource-manager boundaries - manage Resource Manager boundaries

SYNOPSIS
    gcloud resource-manager boundaries COMMAND [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    Commands to create, describe, list, update, and delete Resource Manager
    boundaries.

COMMANDS
    COMMAND is one of the following:

     create
        Create a new boundary.

     delete
        Delete a boundary.

     describe
        Describe a boundary.

     list
        List boundaries.

     update
        Update a boundary.
```

#### `create`

```text
NAME
    gcloud resource-manager boundaries create - create a new boundary

SYNOPSIS
    gcloud resource-manager boundaries create
        (BOUNDARY : --folder=FOLDER --organization=ORGANIZATION) [--async]
        [--display-name=DISPLAY_NAME] [--tag-key=TAG_KEY]
        [--tag-value=TAG_VALUE] [GCLOUD_WIDE_FLAG ...]

FLAGS
     --display-name=DISPLAY_NAME
        Friendly display name to use for the boundary.

     --tag-key=TAG_KEY
        The namespaced name of the tag key (e.g. 975672035171/environment).

     --tag-value=TAG_VALUE
        The short name of the tag value (e.g. dev or prod).
```
