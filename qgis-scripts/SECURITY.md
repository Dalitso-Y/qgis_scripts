# Security Policy

## Scope

This repository contains GIS automation scripts. Risks may include unintended edits or deletions, untrusted file inputs, external commands, exposed project data, and dependency vulnerabilities.

## Reporting

**Do not disclose security issues or confidential data in a public issue.** If GitHub Private Vulnerability Reporting is enabled, use **Security → Report a vulnerability** on the repository. Otherwise contact a maintainer through an established private channel.

## Safe usage

- Review scripts and dependencies before execution.
- Make backups and test on disposable datasets first.
- Never commit passwords, tokens, service account keys, customer datasets or proprietary map sources.
- Inspect output destinations; scripts must not overwrite production data without explicit authorization.
- Keep QGIS and relevant dependencies patched for the version used.
