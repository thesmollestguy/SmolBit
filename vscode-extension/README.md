# SmolBit Syntax Highlighting

You can change the colors of the syntax highlighting by changing the `"editor.tokenColorCustomizations": {"textMateRules": ...}` section of your settings.json file.
The scopes for the language are as follows:
Comments: comment.smolbit
Strings: string.smolbit
Block instructions: keyword.control.smolbit
Function IDs: entity.name.function.smolbit
Math functions: keyword.operator.smolbit
Comparison operators: keyword.operator.comparison.smolbit
Hex values: constant.numeric.smolbit
Registers: support.variable.smolbit
Specifically the `f` register: support.variable.global.smolbit
Page changes: storage.type.smolbit
General functions: support.function.smolbit

EX.
```json
"editor.tokenColorCustomizations": {
    "textMateRules": [
        {
            "scope": "support.variable.global.smolbit",
            "settings": {
                "foreground": "#7733ff"
            }
        }
    ]
}
```

# Installation

1. Download the VSIX file
2. Open VSCode
3. Press Ctrl+Shift+X (or open the Extensions sidebar tab)
4. Press Views and More Actions (the three dots in the corner of the Extensions window)
5. Click Install from VSIX...
6. Navigate to the VSIX file and open it
7. Restart VSCode
