"""
Syntax highlighter for CoPywork using Pygments and VSCode themes
"""
import tkinter as tk
import tkinter.font as tkfont
from typing import Dict, List, Optional, Tuple
import re

try:
    from pygments import highlight
    from pygments.lexers import PythonLexer, get_lexer_by_name
    from pygments.token import Token
    from pygments.formatters import get_formatter_by_name
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False
    # Create a dummy Token class for when Pygments is not available
    class DummyToken:
        pass

    class Token:
        Comment = DummyToken()
        Keyword = DummyToken()
        String = DummyToken()
        Number = DummyToken()
        Name = DummyToken()
        Operator = DummyToken()
        Punctuation = DummyToken()
        Literal = DummyToken()

    # Add nested attributes
    Token.Comment.Single = DummyToken()
    Token.Comment.Multiline = DummyToken()
    Token.Keyword.Constant = DummyToken()
    Token.Keyword.Declaration = DummyToken()
    Token.Keyword.Namespace = DummyToken()
    Token.Keyword.Reserved = DummyToken()
    Token.String.Double = DummyToken()
    Token.String.Single = DummyToken()
    Token.Number.Integer = DummyToken()
    Token.Number.Float = DummyToken()
    Token.Name.Function = DummyToken()
    Token.Name.Class = DummyToken()
    Token.Name.Builtin = DummyToken()
    Token.Name.Variable = DummyToken()
    Token.Name.Decorator = DummyToken()
    Token.Literal.String = DummyToken()
    Token.Literal.String.Doc = DummyToken()

from .theme_loader import ThemeLoader


class SyntaxHighlighter:
    """Handles syntax highlighting for the text widget"""

    def __init__(self, text_widget: tk.Text, theme_loader: ThemeLoader):
        self.text_widget = text_widget
        self.theme_loader = theme_loader
        self.lexer = None
        self.configured_tags = set()
        self.configured_washed_tags = set()

        # Initialize lexer if Pygments is available
        if PYGMENTS_AVAILABLE:
            self.lexer = PythonLexer()

        # Configure base font
        self.base_font = tkfont.Font(family='Fira Code', size=12)
        self.bold_font = tkfont.Font(family='Fira Code', size=12, weight='bold')
        self.italic_font = tkfont.Font(family='Fira Code', size=12, slant='italic')
        self.bold_italic_font = tkfont.Font(family='Fira Code', size=12, weight='bold', slant='italic')
        
        # Map Pygments tokens to VSCode scopes
        self.token_scope_map = {
            Token.Comment: "comment",
            Token.Comment.Single: "comment",
            Token.Comment.Multiline: "comment",
            Token.Keyword: "keyword",
            Token.Keyword.Constant: "keyword.control",
            Token.Keyword.Declaration: "keyword.control",
            Token.Keyword.Namespace: "keyword.control.import",
            Token.Keyword.Reserved: "keyword.control",
            Token.String: "string",
            Token.String.Double: "string",
            Token.String.Single: "string",
            Token.Number: "constant.numeric",
            Token.Number.Integer: "constant.numeric",
            Token.Number.Float: "constant.numeric",
            Token.Name.Function: "entity.name.function",
            Token.Name.Class: "entity.name.class",
            Token.Name.Builtin: "support.function",
            Token.Name.Variable: "variable",
            Token.Operator: "keyword.operator",
            Token.Punctuation: "punctuation",
            Token.Name.Decorator: "entity.name.function.decorator",
            Token.Literal.String.Doc: "comment",
        }

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, rgb: tuple) -> str:
        """Convert RGB tuple to hex color"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def _wash_out_color(self, hex_color: str, wash_factor: float = 0.3) -> str:
        """Create a washed-out version of a color by blending with background"""
        # Background color from theme
        bg_color = self.theme_loader.get_editor_color("editor.background", "#333333")

        # Convert colors to RGB
        fg_rgb = self._hex_to_rgb(hex_color)
        bg_rgb = self._hex_to_rgb(bg_color)

        # Blend colors (wash_factor determines how much of original color to keep)
        washed_rgb = tuple(
            int(fg_rgb[i] * wash_factor + bg_rgb[i] * (1 - wash_factor))
            for i in range(3)
        )

        return self._rgb_to_hex(washed_rgb)
    
    def is_python_file(self, file_path: str) -> bool:
        """Check if file should have Python syntax highlighting"""
        if not file_path:
            return False
        return file_path.lower().endswith(('.py', '.py.cw'))
    
    def configure_tag(self, tag_name: str, scope: str, washed_out: bool = False):
        """Configure a text widget tag based on theme scope"""
        tag_set = self.configured_washed_tags if washed_out else self.configured_tags

        if tag_name in tag_set:
            return

        foreground = self.theme_loader.get_foreground_color(scope)

        # Apply wash-out effect if needed
        if washed_out:
            foreground = self._wash_out_color(foreground)

        bold, italic = self.theme_loader.get_font_style(scope)

        # Choose appropriate font
        font = self.base_font
        if bold and italic:
            font = self.bold_italic_font
        elif bold:
            font = self.bold_font
        elif italic:
            font = self.italic_font

        self.text_widget.tag_configure(tag_name, foreground=foreground, font=font)
        tag_set.add(tag_name)
    
    def clear_syntax_tags(self):
        """Clear all syntax highlighting tags"""
        for tag in self.configured_tags:
            self.text_widget.tag_remove(tag, "1.0", tk.END)
        for tag in self.configured_washed_tags:
            self.text_widget.tag_remove(tag, "1.0", tk.END)

    def highlight_text_practice_mode(self, file_path: str = None):
        """Apply washed-out syntax highlighting for practice mode"""
        if not PYGMENTS_AVAILABLE or not self.is_python_file(file_path):
            return

        # Get text content
        content = self.text_widget.get("1.0", tk.END)
        if not content.strip():
            return

        # Clear existing syntax tags
        self.clear_syntax_tags()

        try:
            # First, apply a default washed-out color to ALL text
            self._apply_default_washed_color()

            # Then, tokenize the content and apply specific syntax highlighting
            tokens = list(self.lexer.get_tokens(content))

            # Apply washed-out highlighting for syntax tokens
            self._apply_token_highlighting(tokens, washed_out=True)

        except Exception as e:
            print(f"Error during practice mode syntax highlighting: {e}")

    def _apply_default_washed_color(self):
        """Apply default washed-out color to all text"""
        # Get the default foreground color from theme
        default_color = self.theme_loader.get_editor_color("editor.foreground", "#C1E4F6")
        washed_default_color = self._wash_out_color(default_color)

        # Configure a default washed tag
        default_washed_tag = "default_text_washed"
        self.text_widget.tag_configure(default_washed_tag, foreground=washed_default_color)

        # Apply to all text
        self.text_widget.tag_add(default_washed_tag, "1.0", tk.END)
        self.configured_washed_tags.add(default_washed_tag)

    def restore_normal_color_at_position(self, position: str, file_path: str = None):
        """Restore normal syntax highlighting color at a specific position"""
        if not PYGMENTS_AVAILABLE or not self.is_python_file(file_path):
            return

        # Get the character at the position
        char = self.text_widget.get(position)
        if not char or char == '\n':
            return

        # Find which syntax tag should apply to this position
        # We'll need to re-tokenize to find the correct scope
        self._update_position_highlighting(position, file_path)

    def apply_incorrect_color_at_position(self, position: str):
        """Apply bright red color for incorrect typing at a specific position"""
        # Remove any existing syntax highlighting tags at this position
        for tag in list(self.configured_tags) + list(self.configured_washed_tags):
            self.text_widget.tag_remove(tag, position)

        # Also remove default tags
        self.text_widget.tag_remove("default_text_normal", position)
        self.text_widget.tag_remove("default_text_washed", position)

        # The incorrect tag will be applied by the main typing logic
        # This method just ensures syntax tags are cleared

    def restore_washed_color_at_position(self, position: str, file_path: str = None):
        """Restore washed-out syntax highlighting for a specific position"""
        if not PYGMENTS_AVAILABLE or not self.is_python_file(file_path):
            return

        # Remove any existing tags at this position
        for tag in list(self.configured_tags) + list(self.configured_washed_tags):
            self.text_widget.tag_remove(tag, position)

        # Also remove default tags
        self.text_widget.tag_remove("default_text_normal", position)
        self.text_widget.tag_remove("default_text_washed", position)

        # Get the character at the position
        char = self.text_widget.get(position)
        if not char or char == '\n':
            return

        # Find which syntax tag should apply to this position
        self._apply_washed_color_at_position(position, file_path)

    def _apply_washed_color_at_position(self, position: str, file_path: str):
        """Apply washed-out syntax highlighting for a specific position"""
        if not PYGMENTS_AVAILABLE or not self.is_python_file(file_path):
            return

        # Get text content
        content = self.text_widget.get("1.0", tk.END)
        if not content.strip():
            return

        try:
            # Convert position to character index
            line, col = position.split('.')
            line_num = int(line)
            col_num = int(col)
            next_pos = f"{line}.{int(col)+1}"

            # Tokenize the content
            tokens = list(self.lexer.get_tokens(content))

            # Find the token that contains this position
            current_line = 1
            current_col = 0
            found_token = False

            for token_type, text in tokens:
                if not text:
                    continue

                # Calculate token end position
                lines = text.split('\n')
                if len(lines) > 1:
                    end_line = current_line + len(lines) - 1
                    end_col = len(lines[-1])
                else:
                    end_line = current_line
                    end_col = current_col + len(text)

                # Check if our position is within this token
                if (current_line < line_num < end_line or
                    (current_line == line_num and current_col <= col_num < end_col) or
                    (end_line == line_num and col_num < end_col)):

                    found_token = True
                    # Apply washed-out tag for this position
                    scope = self._get_scope_for_token(token_type)
                    if scope:
                        washed_tag = f"syntax_{scope.replace('.', '_')}_washed"
                        # Configure and apply washed tag
                        self.configure_tag(washed_tag, scope, washed_out=True)
                        self.text_widget.tag_add(washed_tag, position, next_pos)
                    else:
                        # No specific scope, apply default washed color
                        self._apply_default_washed_at_position(position, next_pos)
                    break

                # Update position for next token
                current_line = end_line
                current_col = end_col

            # If no token was found, apply default washed color
            if not found_token:
                self._apply_default_washed_at_position(position, next_pos)

        except Exception as e:
            print(f"Error applying washed color at position: {e}")

    def _apply_default_washed_at_position(self, position: str, next_pos: str):
        """Apply default washed color to a specific position"""
        default_washed_tag = "default_text_washed"

        # Configure the tag if not already done
        if default_washed_tag not in self.configured_washed_tags:
            default_color = self.theme_loader.get_editor_color("editor.foreground", "#C1E4F6")
            washed_default_color = self._wash_out_color(default_color)
            self.text_widget.tag_configure(default_washed_tag, foreground=washed_default_color)
            self.configured_washed_tags.add(default_washed_tag)

        # Apply the tag
        self.text_widget.tag_add(default_washed_tag, position, next_pos)
    
    def highlight_text(self, file_path: str = None):
        """Apply syntax highlighting to the entire text"""
        if not PYGMENTS_AVAILABLE or not self.is_python_file(file_path):
            return
        
        # Get text content
        content = self.text_widget.get("1.0", tk.END)
        if not content.strip():
            return
        
        # Clear existing syntax tags
        self.clear_syntax_tags()
        
        try:
            # Tokenize the content
            tokens = list(self.lexer.get_tokens(content))
            
            # Apply highlighting
            self._apply_token_highlighting(tokens)
            
        except Exception as e:
            print(f"Error during syntax highlighting: {e}")
    
    def _apply_token_highlighting(self, tokens: List[Tuple], washed_out: bool = False):
        """Apply highlighting based on tokens"""
        line_num = 1
        col_num = 0

        for token_type, text in tokens:
            if not text:
                continue

            # Calculate positions
            start_pos = f"{line_num}.{col_num}"

            # Update position based on text content
            lines = text.split('\n')
            if len(lines) > 1:
                line_num += len(lines) - 1
                col_num = len(lines[-1])
            else:
                col_num += len(text)

            end_pos = f"{line_num}.{col_num}"

            # Get scope for this token type
            scope = self._get_scope_for_token(token_type)
            if scope:
                suffix = "_washed" if washed_out else ""
                tag_name = f"syntax_{scope.replace('.', '_')}{suffix}"
                self.configure_tag(tag_name, scope, washed_out=washed_out)
                self.text_widget.tag_add(tag_name, start_pos, end_pos)
    
    def _get_scope_for_token(self, token_type) -> Optional[str]:
        """Map Pygments token to VSCode scope"""
        # Direct mapping
        if token_type in self.token_scope_map:
            return self.token_scope_map[token_type]

        # Try parent token types
        for parent_type in token_type.split():
            if parent_type in self.token_scope_map:
                return self.token_scope_map[parent_type]

        return None

    def _update_position_highlighting(self, position: str, file_path: str):
        """Update syntax highlighting for a specific position"""
        if not PYGMENTS_AVAILABLE or not self.is_python_file(file_path):
            return

        # Get text content
        content = self.text_widget.get("1.0", tk.END)
        if not content.strip():
            return

        try:
            # Convert position to character index
            line, col = position.split('.')
            line_num = int(line)
            col_num = int(col)
            next_pos = f"{line}.{int(col)+1}"

            # Remove all washed tags from this position first
            for tag in self.configured_washed_tags:
                self.text_widget.tag_remove(tag, position)

            # Tokenize the content
            tokens = list(self.lexer.get_tokens(content))

            # Find the token that contains this position
            current_line = 1
            current_col = 0
            found_token = False

            for token_type, text in tokens:
                if not text:
                    continue

                # Calculate token end position
                lines = text.split('\n')
                if len(lines) > 1:
                    end_line = current_line + len(lines) - 1
                    end_col = len(lines[-1])
                else:
                    end_line = current_line
                    end_col = current_col + len(text)

                # Check if our position is within this token
                if (current_line < line_num < end_line or
                    (current_line == line_num and current_col <= col_num < end_col) or
                    (end_line == line_num and col_num < end_col)):

                    found_token = True
                    # Apply normal syntax highlighting for this position
                    scope = self._get_scope_for_token(token_type)
                    if scope:
                        normal_tag = f"syntax_{scope.replace('.', '_')}"
                        # Configure and apply normal tag
                        self.configure_tag(normal_tag, scope, washed_out=False)
                        self.text_widget.tag_add(normal_tag, position, next_pos)
                    else:
                        # No specific scope, apply default normal color
                        self._apply_default_normal_at_position(position, next_pos)
                    break

                # Update position for next token
                current_line = end_line
                current_col = end_col

            # If no token was found, apply default normal color
            if not found_token:
                self._apply_default_normal_at_position(position, next_pos)

        except Exception as e:
            print(f"Error updating position highlighting: {e}")

    def _apply_default_normal_at_position(self, position: str, next_pos: str):
        """Apply default normal color to a specific position"""
        default_normal_tag = "default_text_normal"

        # Configure the tag if not already done
        if default_normal_tag not in self.configured_tags:
            default_color = self.theme_loader.get_editor_color("editor.foreground", "#C1E4F6")
            self.text_widget.tag_configure(default_normal_tag, foreground=default_color)
            self.configured_tags.add(default_normal_tag)

        # Apply the tag
        self.text_widget.tag_add(default_normal_tag, position, next_pos)
    
    def highlight_range(self, start: str, end: str, file_path: str = None):
        """Highlight a specific range of text (for incremental updates)"""
        if not PYGMENTS_AVAILABLE or not self.is_python_file(file_path):
            return
        
        # For now, just re-highlight the entire text
        # This could be optimized for better performance
        self.highlight_text(file_path)
