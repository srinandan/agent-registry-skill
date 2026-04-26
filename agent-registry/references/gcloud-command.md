# gcloud alpha agent-registry Documentation

Documentation for `gcloud alpha agent-registry` and its subcommands.

## Main Command: `gcloud alpha agent-registry`

```text
NAME
    gcloud alpha agent-registry - manage Agent Registry resources

SYNOPSIS
    gcloud alpha agent-registry GROUP [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) Manage Agent Registry resources.

GCLOUD WIDE FLAGS
    These flags are available to all commands: --help.

    Run $ gcloud help for details.

GROUPS
    GROUP is one of the following:

     agents
        (ALPHA) Manage Agent resources.

     bindings
        (ALPHA) Manage Binding resources.

     endpoints
        (ALPHA) Manage Endpoint resources.

     mcp-servers
        (ALPHA) Manage Mcp Server resources.

     operations
        (ALPHA) Manage Operation resources.

     services
        (ALPHA) Manage Service resources.

NOTES
    This command is currently in alpha and might change without notice. If this
    command fails with API permission errors despite specifying the correct
    project, you might be trying to access an API with an invitation-only early
    access allowlist.
```

---

## Subcommands

### agents

```text
NAME
    gcloud alpha agent-registry agents - manage Agent resources

SYNOPSIS
    gcloud alpha agent-registry agents COMMAND [GCLOUD_WIDE_FLAG ...]

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
    gcloud alpha agent-registry agents search - search agents

SYNOPSIS
    gcloud alpha agent-registry agents search --location=LOCATION
        [--search-string=SEARCH_STRING] [--search-type=SEARCH_TYPE]
        [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) search agents

EXAMPLES
    To search all agents, run:

        $ gcloud alpha agent-registry agents search

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
    gcloud alpha agent-registry bindings - manage Binding resources

SYNOPSIS
    gcloud alpha agent-registry bindings COMMAND [GCLOUD_WIDE_FLAG ...]

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
    gcloud alpha agent-registry endpoints - manage Endpoint resources

SYNOPSIS
    gcloud alpha agent-registry endpoints COMMAND [GCLOUD_WIDE_FLAG ...]

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
    gcloud alpha agent-registry mcp-servers - manage Mcp Server resources

SYNOPSIS
    gcloud alpha agent-registry mcp-servers COMMAND [GCLOUD_WIDE_FLAG ...]

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
    gcloud alpha agent-registry mcp-servers search - search MCP servers

SYNOPSIS
    gcloud alpha agent-registry mcp-servers search --location=LOCATION
        [--search-string=SEARCH_STRING] [--search-type=SEARCH_TYPE]
        [GCLOUD_WIDE_FLAG ...]

DESCRIPTION
    (ALPHA) search MCP servers

EXAMPLES
    To search all MCP servers, run:

        $ gcloud alpha agent-registry mcp-servers search

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
    gcloud alpha agent-registry operations - manage Operation resources

SYNOPSIS
    gcloud alpha agent-registry operations [GCLOUD_WIDE_FLAG ...]

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
    gcloud alpha agent-registry services - manage Service resources

SYNOPSIS
    gcloud alpha agent-registry services COMMAND [GCLOUD_WIDE_FLAG ...]

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
    This command is currently in alpha and might change without notice. If this
    command fails with API permission errors despite specifying the correct
    project, you might be trying to access an API with an invitation-only early
    access allowlist.
```
