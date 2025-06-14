# CoPywork Syntax Highlighting Feature

## Overview

CoPywork now supports VSCode-style syntax highlighting for Python files using Pygments and JSON themes. This feature enhances the coding experience by providing visual syntax highlighting while maintaining all the original typing practice functionality.

## New Features

### 1. File Type Support

- **`.py` files**: Python files with syntax highlighting
  - Save behavior: Creates `.py` file + `.py.colors` companion file (like `.txt` files)
  - Syntax highlighting: Full Python syntax highlighting enabled

- **`.py.cw` files**: Python CoPywork archive files
  - Save behavior: Creates `.py.cw` archive containing content and color data (like `.cw` files)
  - Syntax highlighting: Full Python syntax highlighting enabled

### 2. VSCode-Style JSON Themes

The application uses VSCode-compatible JSON theme files located in the `themes/` directory.

#### Theme Structure
```json
{
  "name": "Theme Name",
  "type": "dark",
  "colors": {
    "editor.background": "#333333",
    "editor.foreground": "#C1E4F6"
  },
  "tokenColors": [
    {
      "name": "Comment",
      "scope": ["comment", "punctuation.definition.comment"],
      "settings": {
        "fontStyle": "italic",
        "foreground": "#6A9955"
      }
    }
  ]
}
```

#### Supported Scopes
- `comment` - Comments
- `keyword` - Keywords (def, class, if, etc.)
- `keyword.control` - Control flow keywords
- `keyword.control.import` - Import statements
- `string` - String literals
- `constant.numeric` - Numbers
- `constant.language` - Built-in constants (True, False, None)
- `entity.name.function` - Function names
- `entity.name.class` - Class names
- `variable` - Variables
- `keyword.operator` - Operators (+, -, *, etc.)
- `punctuation` - Punctuation marks
- `entity.name.function.decorator` - Decorators (@property, etc.)

### 3. Font Styling

The theme system supports:
- **Bold** text (`"fontStyle": "bold"`)
- **Italic** text (`"fontStyle": "italic"`)
- **Bold Italic** text (`"fontStyle": "bold italic"`)

### 4. Fallback Logic

The theme system includes intelligent fallback logic:
- `keyword.control.import` falls back to `keyword.control` then to `keyword`
- Ensures consistent styling even for specific scopes not defined in the theme

## Directory Structure

```
copywork/
├── coPywork.py              # Main application
├── theme_loader.py          # VSCode theme parser
├── syntax_highlighter.py   # Pygments-based highlighter
├── config/                  # Configuration directory
├── themes/                  # Theme files directory
│   └── my_theme.json       # Default VSCode-style theme
└── tests/                   # Test files
```

## Installation Requirements

### Required Dependencies
```bash
pip install pygments
```

### Optional Dependencies
- `tkinter` (usually included with Python)
- `tkinter.font` (usually included with Python)

## Usage

### Opening Python Files

1. **From command line:**
   ```bash
   python coPywork.py script.py
   python coPywork.py script.py.cw
   ```

2. **From File menu:**
   - File → Open
   - Select Python files (`.py`) or Python CoPywork files (`.py.cw`)

### Saving Python Files

1. **`.py` files:**
   - Saves as plain text file
   - Creates companion `.py.colors` file with typing progress
   - Maintains syntax highlighting

2. **`.py.cw` files:**
   - Saves as compressed archive
   - Contains both content and color data
   - Maintains syntax highlighting

### Syntax Highlighting Behavior

- **Edit Mode**: Full syntax highlighting is active and updates on text changes
- **Practice Mode**:
  - Untyped text shows washed-out syntax highlighting (30% opacity)
  - Correctly typed text restores normal syntax highlighting colors
  - Incorrectly typed text shows bright red color (#FF0000)
  - Backspacing restores washed-out highlighting
- **Real-time Updates**: Highlighting updates on every keystroke in both modes

## Customization

### Creating Custom Themes

1. Create a new JSON file in the `themes/` directory
2. Follow the VSCode theme format
3. Update the theme path in `theme_loader.py` if needed

### Example Custom Theme
```json
{
  "name": "My Custom Theme",
  "type": "dark",
  "colors": {
    "editor.background": "#1e1e1e",
    "editor.foreground": "#d4d4d4"
  },
  "tokenColors": [
    {
      "name": "Keywords",
      "scope": ["keyword"],
      "settings": {
        "foreground": "#569cd6",
        "fontStyle": "bold"
      }
    }
  ]
}
```

## Technical Implementation

### Architecture

1. **ThemeLoader**: Parses VSCode JSON themes and provides style lookup
2. **SyntaxHighlighter**: Uses Pygments to tokenize Python code and apply themes
3. **Practice Mode Engine**: Manages washed-out colors and real-time restoration
4. **Integration**: Seamlessly integrates with existing CoPywork functionality

### Practice Mode Color Algorithm

The practice mode uses an intelligent color blending algorithm:

```python
def _wash_out_color(self, hex_color: str, wash_factor: float = 0.3) -> str:
    """Blend syntax color with background for washed-out effect"""
    fg_rgb = hex_to_rgb(hex_color)
    bg_rgb = hex_to_rgb(background_color)

    # Blend: 30% original color + 70% background color
    washed_rgb = (fg * 0.3 + bg * 0.7 for fg, bg in zip(fg_rgb, bg_rgb))
    return rgb_to_hex(washed_rgb)
```

### Performance Considerations

- Syntax highlighting runs in both edit and practice modes
- Uses `after_idle()` to prevent UI blocking
- Efficient tag management with separate normal/washed tag sets
- Position-specific highlighting updates for optimal performance

### Error Handling

- Graceful fallback when Pygments is not available
- Default theme loading if custom theme fails
- Maintains full functionality even without syntax highlighting

## Backward Compatibility

- All existing `.txt` and `.cw` files work unchanged
- Original color system (correct/incorrect typing) preserved
- No breaking changes to existing functionality

## Testing

Run the test suites to verify functionality:
```bash
python test_syntax_highlighting.py
python test_practice_mode_highlighting.py
```

The test suites verify:
- Theme loading and parsing
- Syntax highlighter initialization
- File type detection
- Save behavior for different file types
- Practice mode washed-out highlighting
- Color restoration on correct typing
- Bright red highlighting on incorrect typing
- Color blending algorithm accuracy

## Troubleshooting

### Common Issues

1. **"Pygments not available" warning:**
   - Install Pygments: `pip install pygments`
   - Ensure correct Python environment

2. **Theme not loading:**
   - Check `themes/my_theme.json` exists
   - Verify JSON syntax is valid
   - Check file permissions

3. **Syntax highlighting not working:**
   - Ensure file has `.py` or `.py.cw` extension
   - Check that you're in Edit mode
   - Verify Pygments is properly installed

### Debug Mode

Enable debug output by checking the console for warning messages when starting the application.

## Future Enhancements

Potential future improvements:
- Support for additional programming languages
- More VSCode theme compatibility
- Theme selection UI
- Custom color scheme editor
- Performance optimizations for large files
