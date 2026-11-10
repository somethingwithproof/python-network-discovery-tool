---
# SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT
name: Release Planning
about: Plan a netprobe release
title: 'Release [VERSION] Planning'
labels: ''
assignees: ''
---

## Release [VERSION] Planning

**Target Release Date:** YYYY-MM-DD

### Release Goals

<!-- Describe the main goals and focus of this release -->

### Features

<!-- List the features that will be included in this release -->

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

### Bug Fixes

<!-- List the bugs that will be fixed in this release -->

- [ ] #123 - Bug description
- [ ] #456 - Bug description

### Breaking Changes

<!-- List any breaking changes that will be included in this release -->

- Breaking change 1
- Breaking change 2

### Dependencies

<!-- List any dependencies that need to be updated -->

- Dependency 1: v1.2.3 -> v2.0.0
- Dependency 2: v3.4.5 -> v3.5.0

### Documentation

<!-- List documentation that needs to be updated -->

- [ ] Update API documentation
- [ ] Update usage examples
- [ ] Update changelog

### Testing

<!-- List testing that needs to be done -->

- [ ] Unit tests for new features
- [ ] Integration tests
- [ ] Performance testing

### Release Checklist

- [ ] Every change merged with a Conventional Commit title (`!` for breaking changes)
- [ ] Breaking changes have a `BREAKING CHANGE:` footer with migration steps
- [ ] Deprecations follow docs/releasing.md
- [ ] release-please PR reviewed: version, `CHANGES.md`, checks green
- [ ] Release PR merged; draft release has wheel, sdist, `SHA256SUMS` and attestations
- [ ] Draft reviewed and published by a maintainer

### Post-Release Tasks

- [ ] Close related issues
- [ ] Plan next release
