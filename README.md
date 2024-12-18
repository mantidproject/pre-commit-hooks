# Custom pre-commit hooks for the pre-commit framework
The hooks present in this repository are:
* mantid_release_note_check (checks and edits mantid release notes so that they use the ``-`` bullet point style)

To use the hooks copy this to your .pre-commit-config.yaml:
```yaml
-   repo: https://github.com/mantidproject/pre-commit-hooks
    rev: main
    hooks:
    - id: mantid-release-note-check
        files: docs\/source\/release\/v\d\.\d\.\d\/.*\/.*\.rst
    - id: cmake-missing-pytest-files
```
