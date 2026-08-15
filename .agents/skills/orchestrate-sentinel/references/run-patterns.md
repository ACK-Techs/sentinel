# Reusable run graph patterns

## Single module

`scope-contract -> implement -> review -> verify -> pm-acceptance`

## Cross module

`pm-scope -> shared-contract -> producer/consumer implementations -> review -> verification -> integration -> acceptance`

Example: CLI `obs` command + gateway endpoint + docs.

## Gateway change

`read-only-contract -> gateway-implement -> security-review + gateway-verify -> cli-client-sync -> integration`

Never add write/admin/alert/dashboard/proxy without a `gateway-write-expansion` approval decision.

## Installer change

`install-path-spec -> implement -> docs/INSTALL sync -> review + verify -> integration`

Keep Compose, Kubernetes, and COS as separate items when behavior differs.

## Revision

Keep failed item immutable. Add a new item with `relations.revises=[failed-item]`, then new review and verify items.

## Alternatives

Create one candidate item per solution with identical acceptance rubric. Add a read-only `comparison` item depending on all candidates and record selection in `run.decisions`.
