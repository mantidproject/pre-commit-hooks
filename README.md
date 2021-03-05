# Custom pre-commit hooks for the pre-commit framework
The hooks present in this repository are:
* clang-format (self-contained hook not reliant on clang-format being available externally)

To use the hooks copy this to your .pre-commit-config.yaml:
```yaml
-   repo: https://github.com/mantidproject/pre-commit-hooks
    rev: main
    hooks:
    -   id: clang-format
```
