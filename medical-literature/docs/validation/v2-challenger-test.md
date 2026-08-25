# V2 challenger validation

Status: `DEGRADED_BY_DEFAULT_UNTIL_PROVIDER_CONFIGURED`.

The thin wrapper preserves returned records when configured and converts an
upstream error into `DEGRADED` with an explicit warning and zero records. It
cannot fail the formal search and cannot alter formal counts. A real top-20
challenger-unique manual review remains pending provider activation.
