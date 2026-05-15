# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `DomainsAPI.set_nameservers(domain, nameservers, *, reset=False)` method
  - Set custom nameservers via `namecheap.domains.dns.setCustom` API
  - Reset to Namecheap BasicDNS via `namecheap.domains.dns.setDefault` API
  - Supports up to 5 nameservers, validates domain format and count limits
- `namecheap-cli domain nameservers set` CLI command
  - Usage: `namecheap-cli domain nameservers set <domain> <ns1> [<ns2> ...]`
  - Reset: `namecheap-cli domain nameservers set <domain> --reset`
- Unit tests for `set_nameservers` (10 tests covering validation, API calls, edge cases)
- Integration tests for `set_nameservers` (6 tests covering HTTP params, URLs, auth, sandbox)

### Changed

- Refactored `pyproject.toml` to uv format: `[dependency-groups]` for dev/test deps
