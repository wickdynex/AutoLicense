---
name: Pull Request
about: Submit a PR to contribute code or fix an issue
title: "[PR] "
labels: ''
assignees: ''
---

### Description

Briefly explain what the PR does or the issue it addresses.

---

### Changes Made

List the main changes in this PR:

- [ ] Added support for a new license type.
- [ ] Fixed file type detection issue.
- [ ] Updated documentation for the `LICENSE_FILE` argument.

---

### Related Issues

Link to any related issues or tasks:

- Closes #123 (Fixed license addition logic)
- Part of [JIRA-456](https://jira.company.com/browse/JIRA-456) (Optimized batch processing feature)

---

### Testing Instructions

How to verify this PR:

- Run `python main.py --license-file=LICENSE_FILE --license-type=MIT --start-year=2024 --author="John Doe" --target-folder=target_folder` to ensure the license header is correctly added.
- Run with `--detail` flag to verify the detailed output showing which files were modified.

---

### Screenshots

If there are UI-related changes, attach screenshots:

- N/A (This is a command-line tool)

---

### Dependencies

List any dependencies this PR has (if any):

- N/A (No dependencies)