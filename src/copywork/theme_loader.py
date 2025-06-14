"""
VSCode-style JSON theme loader for CoPywork
"""
import json
import os
from typing import Dict, List, Optional, Tuple


class ThemeLoader:
    """Loads and parses VSCode-style JSON themes"""
    
    def __init__(self, theme_path: str = "themes/my_theme.json"):
        self.theme_path = theme_path
        self.theme_data = None
        self.token_colors = {}
        self.editor_colors = {}
        self.load_theme()
    
    def load_theme(self) -> bool:
        """Load theme from JSON file"""
        try:
            if not os.path.exists(self.theme_path):
                print(f"Warning: Theme file {self.theme_path} not found. Using defaults.")
                self._load_default_theme()
                return False
                
            with open(self.theme_path, 'r', encoding='utf-8') as f:
                self.theme_data = json.load(f)
            
            self._parse_theme()
            return True
            
        except Exception as e:
            print(f"Error loading theme: {e}. Using defaults.")
            self._load_default_theme()
            return False
    
    def _parse_theme(self):
        """Parse the loaded theme data"""
        # Parse editor colors
        if 'colors' in self.theme_data:
            self.editor_colors = self.theme_data['colors']
        
        # Parse token colors
        if 'tokenColors' in self.theme_data:
            for token_rule in self.theme_data['tokenColors']:
                if 'scope' in token_rule and 'settings' in token_rule:
                    scopes = token_rule['scope']
                    if isinstance(scopes, str):
                        scopes = [scopes]
                    
                    settings = token_rule['settings']
                    for scope in scopes:
                        self.token_colors[scope] = settings
    
    def _load_default_theme(self):
        """Load default theme if file loading fails"""
        self.editor_colors = {
            "editor.background": "#333333",
            "editor.foreground": "#C1E4F6"
        }
        
        self.token_colors = {
            "comment": {"foreground": "#6A9955", "fontStyle": "italic"},
            "keyword": {"foreground": "#569CD6"},
            "keyword.control": {"foreground": "#C586C0"},
            "string": {"foreground": "#CE9178"},
            "constant.numeric": {"foreground": "#B5CEA8"},
            "constant.language": {"foreground": "#569CD6"},
            "entity.name.function": {"foreground": "#DCDCAA"},
            "entity.name.class": {"foreground": "#4EC9B0"},
            "variable": {"foreground": "#9CDCFE"},
            "keyword.operator": {"foreground": "#D4D4D4"},
            "punctuation": {"foreground": "#D4D4D4"}
        }
    
    def get_token_style(self, scope: str) -> Optional[Dict]:
        """Get style for a specific scope with fallback logic"""
        # Direct match
        if scope in self.token_colors:
            return self.token_colors[scope]
        
        # Try fallback to parent scope
        # e.g., "keyword.control.import" -> "keyword.control" -> "keyword"
        parts = scope.split('.')
        for i in range(len(parts) - 1, 0, -1):
            parent_scope = '.'.join(parts[:i])
            if parent_scope in self.token_colors:
                return self.token_colors[parent_scope]
        
        return None
    
    def get_editor_color(self, key: str, default: str = "#C1E4F6") -> str:
        """Get editor color with fallback to default"""
        return self.editor_colors.get(key, default)
    
    def get_foreground_color(self, scope: str, default: str = "#C1E4F6") -> str:
        """Get foreground color for a scope"""
        style = self.get_token_style(scope)
        if style and 'foreground' in style:
            return style['foreground']
        return default
    
    def get_font_style(self, scope: str) -> Tuple[bool, bool]:
        """Get font style (bold, italic) for a scope"""
        style = self.get_token_style(scope)
        if style and 'fontStyle' in style:
            font_style = style['fontStyle']
            bold = 'bold' in font_style.lower()
            italic = 'italic' in font_style.lower()
            return bold, italic
        return False, False
