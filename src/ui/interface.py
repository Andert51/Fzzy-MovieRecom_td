"""
Modern CLI Interface Manager

Provides clean, professional command-line interface components with:
- Box-drawing characters for elegant borders
- Styled headers and sections
- Tables for data display
- Progress indicators
- Color-coded output
"""

import os
import sys
import time
from typing import List, Dict, Any, Optional
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def disable():
        """Disable colors for Windows compatibility."""
        Colors.HEADER = ''
        Colors.BLUE = ''
        Colors.CYAN = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''
        Colors.END = ''


class UIManager:
    """
    Modern UI Manager for clean, professional terminal output.
    
    Uses box-drawing characters and structured layouts instead of emojis.
    """
    
    def __init__(self, use_colors: bool = True, width: int = 80, use_unicode: bool = None):
        """
        Initialize UI Manager.
        
        Args:
            use_colors: Enable ANSI colors (disable for Windows compatibility)
            width: Default width for boxes and lines
            use_unicode: Force unicode on/off (None = auto-detect)
        """
        self.use_colors = use_colors
        self.width = width
        
        # Auto-detect unicode support
        if use_unicode is None:
            # Windows PowerShell/CMD typically don't support box-drawing well
            use_unicode = os.name != 'nt'
        
        # Set box-drawing characters based on unicode support
        if use_unicode:
            # Unicode box drawing characters
            self.BOX_HORIZONTAL = '─'
            self.BOX_VERTICAL = '│'
            self.BOX_TOP_LEFT = '┌'
            self.BOX_TOP_RIGHT = '┐'
            self.BOX_BOTTOM_LEFT = '└'
            self.BOX_BOTTOM_RIGHT = '┘'
            self.BOX_CROSS = '┼'
            self.BOX_T_DOWN = '┬'
            self.BOX_T_UP = '┴'
            self.BOX_T_RIGHT = '├'
            self.BOX_T_LEFT = '┤'
            
            # Double line box characters
            self.DBOX_HORIZONTAL = '═'
            self.DBOX_VERTICAL = '║'
            self.DBOX_TOP_LEFT = '╔'
            self.DBOX_TOP_RIGHT = '╗'
            self.DBOX_BOTTOM_LEFT = '╚'
            self.DBOX_BOTTOM_RIGHT = '╝'
            
            # Bullet points and indicators
            self.BULLET = '•'
            self.ARROW_RIGHT = '→'
            self.ARROW_LEFT = '←'
            self.CHECK = '✓'
            self.CROSS = '✗'
            self.STAR = '★'
        else:
            # ASCII fallback for Windows
            self.BOX_HORIZONTAL = '-'
            self.BOX_VERTICAL = '|'
            self.BOX_TOP_LEFT = '+'
            self.BOX_TOP_RIGHT = '+'
            self.BOX_BOTTOM_LEFT = '+'
            self.BOX_BOTTOM_RIGHT = '+'
            self.BOX_CROSS = '+'
            self.BOX_T_DOWN = '+'
            self.BOX_T_UP = '+'
            self.BOX_T_RIGHT = '+'
            self.BOX_T_LEFT = '+'
            
            # Double line box characters (ASCII)
            self.DBOX_HORIZONTAL = '='
            self.DBOX_VERTICAL = '|'
            self.DBOX_TOP_LEFT = '+'
            self.DBOX_TOP_RIGHT = '+'
            self.DBOX_BOTTOM_LEFT = '+'
            self.DBOX_BOTTOM_RIGHT = '+'
            
            # Bullet points and indicators (ASCII)
            self.BULLET = '*'
            self.ARROW_RIGHT = '->'
            self.ARROW_LEFT = '<-'
            self.CHECK = '[OK]'
            self.CROSS = '[X]'
            self.STAR = '*'
        
        if not use_colors or os.name == 'nt':
            Colors.disable()
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str, subtitle: Optional[str] = None):
        """
        Print a styled header with double-line box.
        
        Args:
            title: Main title text
            subtitle: Optional subtitle text
        """
        print()
        print(f"{Colors.BOLD}{self.DBOX_TOP_LEFT}{self.DBOX_HORIZONTAL * (self.width - 2)}{self.DBOX_TOP_RIGHT}{Colors.END}")
        
        # Center the title
        title_line = title.center(self.width - 2)
        print(f"{Colors.BOLD}{self.DBOX_VERTICAL}{Colors.CYAN}{title_line}{Colors.END}{Colors.BOLD}{self.DBOX_VERTICAL}{Colors.END}")
        
        if subtitle:
            subtitle_line = subtitle.center(self.width - 2)
            print(f"{Colors.BOLD}{self.DBOX_VERTICAL}{subtitle_line}{self.DBOX_VERTICAL}{Colors.END}")
        
        print(f"{Colors.BOLD}{self.DBOX_BOTTOM_LEFT}{self.DBOX_HORIZONTAL * (self.width - 2)}{self.DBOX_BOTTOM_RIGHT}{Colors.END}")
        print()
    
    def print_section(self, title: str, content: Optional[str] = None):
        """
        Print a section with title and optional content.
        
        Args:
            title: Section title
            content: Optional section content
        """
        print()
        print(f"{Colors.BOLD}{Colors.BLUE}{self.BOX_TOP_LEFT}{self.BOX_HORIZONTAL * 2} {title} {self.BOX_HORIZONTAL * (self.width - len(title) - 6)}{self.BOX_TOP_RIGHT}{Colors.END}")
        
        if content:
            for line in content.split('\n'):
                print(f"{Colors.BLUE}{self.BOX_VERTICAL}{Colors.END} {line.ljust(self.width - 4)} {Colors.BLUE}{self.BOX_VERTICAL}{Colors.END}")
        
        print(f"{Colors.BOLD}{Colors.BLUE}{self.BOX_BOTTOM_LEFT}{self.BOX_HORIZONTAL * (self.width - 2)}{self.BOX_BOTTOM_RIGHT}{Colors.END}")
        print()
    
    def print_box(self, lines: List[str], title: Optional[str] = None):
        """
        Print content in a box.
        
        Args:
            lines: List of lines to display
            title: Optional box title
        """
        print()
        
        if title:
            print(f"{Colors.BOLD}{self.BOX_TOP_LEFT}{self.BOX_HORIZONTAL * 2} {title} {self.BOX_HORIZONTAL * (self.width - len(title) - 6)}{self.BOX_TOP_RIGHT}{Colors.END}")
        else:
            print(f"{Colors.BOLD}{self.BOX_TOP_LEFT}{self.BOX_HORIZONTAL * (self.width - 2)}{self.BOX_TOP_RIGHT}{Colors.END}")
        
        for line in lines:
            padded = line.ljust(self.width - 4)
            print(f"{self.BOX_VERTICAL} {padded} {self.BOX_VERTICAL}")
        
        print(f"{Colors.BOLD}{self.BOX_BOTTOM_LEFT}{self.BOX_HORIZONTAL * (self.width - 2)}{self.BOX_BOTTOM_RIGHT}{Colors.END}")
        print()
    
    def print_table(self, headers: List[str], rows: List[List[str]], title: Optional[str] = None):
        """
        Print a formatted table.
        
        Args:
            headers: Column headers
            rows: Data rows
            title: Optional table title
        """
        if not rows:
            return
        
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Ensure minimum width
        col_widths = [max(w, 10) for w in col_widths]
        
        total_width = sum(col_widths) + len(headers) * 3 + 1
        
        print()
        
        if title:
            print(f"{Colors.BOLD}{self.BOX_TOP_LEFT}{self.BOX_HORIZONTAL * 2} {title} {self.BOX_HORIZONTAL * (total_width - len(title) - 6)}{self.BOX_TOP_RIGHT}{Colors.END}")
        else:
            print(f"{Colors.BOLD}{self.BOX_TOP_LEFT}{self.BOX_HORIZONTAL * (total_width - 2)}{self.BOX_TOP_RIGHT}{Colors.END}")
        
        # Print headers
        header_line = f"{self.BOX_VERTICAL}"
        for i, header in enumerate(headers):
            header_line += f" {Colors.BOLD}{header.ljust(col_widths[i])}{Colors.END} {self.BOX_VERTICAL}"
        print(header_line)
        
        # Print separator
        separator = f"{self.BOX_T_RIGHT}"
        for i, width in enumerate(col_widths):
            separator += self.BOX_HORIZONTAL * (width + 2)
            if i < len(col_widths) - 1:
                separator += self.BOX_CROSS
            else:
                separator += self.BOX_T_LEFT
        print(separator)
        
        # Print rows
        for row in rows:
            row_line = f"{self.BOX_VERTICAL}"
            for i, cell in enumerate(row):
                row_line += f" {str(cell).ljust(col_widths[i])} {self.BOX_VERTICAL}"
            print(row_line)
        
        # Print bottom border
        print(f"{Colors.BOLD}{self.BOX_BOTTOM_LEFT}{self.BOX_HORIZONTAL * (total_width - 2)}{self.BOX_BOTTOM_RIGHT}{Colors.END}")
        print()
    
    def print_progress(self, current: int, total: int, prefix: str = '', bar_length: int = 40):
        """
        Print a progress bar.
        
        Args:
            current: Current progress value
            total: Total value
            prefix: Text before progress bar
            bar_length: Length of the progress bar
        """
        percent = int(100 * current / total)
        filled = int(bar_length * current / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f'\r{prefix} [{bar}] {percent}%', end='', flush=True)
        
        if current == total:
            print()
    
    def print_list(self, items: List[str], bullet: str = None):
        """
        Print a bulleted list.
        
        Args:
            items: List items
            bullet: Custom bullet character
        """
        bullet = bullet or self.BULLET
        for item in items:
            print(f"  {Colors.CYAN}{bullet}{Colors.END} {item}")
    
    def print_key_value(self, data: Dict[str, Any], indent: int = 2):
        """
        Print key-value pairs in a formatted way.
        
        Args:
            data: Dictionary of key-value pairs
            indent: Indentation spaces
        """
        max_key_len = max(len(str(k)) for k in data.keys()) if data else 0
        
        for key, value in data.items():
            padded_key = str(key).ljust(max_key_len)
            print(f"{' ' * indent}{Colors.BOLD}{padded_key}{Colors.END} {self.ARROW_RIGHT} {value}")
    
    def print_success(self, message: str):
        """Print a success message."""
        print(f"{Colors.GREEN}{self.CHECK}{Colors.END} {message}")
    
    def print_error(self, message: str):
        """Print an error message."""
        print(f"{Colors.RED}{self.CROSS}{Colors.END} {message}")
    
    def print_warning(self, message: str):
        """Print a warning message."""
        print(f"{Colors.YELLOW}!{Colors.END} {message}")
    
    def print_info(self, message: str):
        """Print an info message."""
        print(f"{Colors.CYAN}i{Colors.END} {message}")
    
    def print_separator(self, char: str = None):
        """Print a horizontal separator line."""
        char = char or self.BOX_HORIZONTAL
        print(char * self.width)
    
    def input_styled(self, prompt: str, default: Optional[str] = None) -> str:
        """
        Get user input with styled prompt.
        
        Args:
            prompt: Input prompt text
            default: Default value if user presses Enter
            
        Returns:
            User input string
        """
        if default:
            full_prompt = f"{Colors.CYAN}{self.ARROW_RIGHT}{Colors.END} {prompt} [{Colors.YELLOW}{default}{Colors.END}]: "
        else:
            full_prompt = f"{Colors.CYAN}{self.ARROW_RIGHT}{Colors.END} {prompt}: "
        
        value = input(full_prompt).strip()
        return value if value else (default or '')
    
    def print_menu(self, title: str, options: List[str]) -> str:
        """
        Display a menu and get user selection.
        
        Args:
            title: Menu title
            options: List of menu options
            
        Returns:
            Selected option number as string
        """
        print()
        print(f"{Colors.BOLD}{Colors.CYAN}{title}{Colors.END}")
        print(self.BOX_HORIZONTAL * len(title))
        print()
        
        for i, option in enumerate(options, 1):
            print(f"  {Colors.BOLD}[{i}]{Colors.END} {option}")
        
        print()
        return self.input_styled("Select option", "1")
    
    def wait_for_user(self, message: str = "Press Enter to continue..."):
        """Wait for user to press Enter."""
        input(f"\n{Colors.YELLOW}{message}{Colors.END}")
