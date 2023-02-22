# License Header Checker

The [pre-commit](https://pre-commit.com/) plugin to check that source files has a header with a license. Also can be used as CLI script.

## Usage

Configuration for single line comments

```yaml
  - repo: http://github.com/Quard/license-header-checker
    rev: v0.1
    hooks:
      - id: license-header-checker
        files: \.py$
        args:
          - --license
          - "Copyright \\(c\\) \\d{4}(-\\d{4})? The Project Contributors\\nSPDX-License-Identifier: MIT\\n"
```

will look for `*.py` files and validate that file has such license header

```python
# Copyright (c) 2023 The Project Contributors
# SPDX-License-Identifier: MIT
```

And another configuration for C-style multiline comments

```yaml
  - repo: http://github.com/Quard/license-header-checker
    rev: v0.1
    hooks:
      - id: license-header-checker
        files: \.(c|h)$
        args:
          - --comment-style
          - "/*| *| */"
          - --license
          - "\\n Copyright \\(c\\) \\d{4}(-\\d{4})? The Project Contributors\\n\\nSPDX-License-Identifier: MIT\\n"
```

that will check `*.c` and `*.h` files for such license header

```c
/*
 * Copyright (c) 2023 The Project Contributors
 *
 * SPDX-License-Identifier: MIT
 */
```

Or it can be used as CLI script

`license_header_checker --license "Copyright \\(c\\) \\d{4}(-\\d{4})? The Project Contributors\\nSPDX-License-Identifier: MIT\\n" [files...]`

Check `license_header_checker --help` to list all available options.
