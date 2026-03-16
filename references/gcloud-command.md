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

NOTES
    This command is currently in alpha and might change without notice. If this
    command fails with API permission errors despite specifying the correct
    project, you might be trying to access an API with an invitation-only early
    access allowlist.
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

NOTES
    This command is currently in alpha and might change without notice. If this
    command fails with API permission errors despite specifying the correct
    project, you might be trying to access an API with an invitation-only early
    access allowlist.
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
