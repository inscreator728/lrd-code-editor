# lrd_code_editor_hacker_gamer.py
import sys
import os
import subprocess
import re
import time
import webbrowser
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ==================== HACKER GAMER THEME ====================

HACKER_GAMER_THEME = {
    # Dark Backgrounds - Solid for speed
    'bg_dark': '#0a0a0a',
    'bg_darker': '#050505',
    'bg_medium': '#111111',
    'bg_light': '#1a1a1a',
    
    # Neon Colors (Gamer/Hacker theme)
    'neon_green': '#00ff00',
    'neon_blue': '#00ffff',
    'neon_purple': '#ff00ff',
    'neon_red': '#ff0000',
    'neon_yellow': '#ffff00',
    'neon_cyan': '#00ffff',
    
    # Primary Colors
    'primary': '#00ff00',  # Green
    'primary_light': '#66ff66',
    'primary_dark': '#00cc00',
    
    # Secondary Colors (Blue)
    'secondary': '#00ffff',
    'secondary_light': '#66ffff',
    'secondary_dark': '#00cccc',
    
    # Accent Colors
    'accent': '#ff00ff',
    'warning': '#ffff00',
    'error': '#ff0000',
    'info': '#00ffff',
    
    # Text Colors
    'text_primary': '#00ff00',
    'text_secondary': '#00ffff',
    'text_tertiary': '#ffff00',
    'text_disabled': '#666666',
    'text_editor': '#ffffff',
    
    # Terminal Colors
    'terminal_bg': '#000000',
    'terminal_text': '#00ff00',
    
    # Selection & Highlight
    'selection': '#003300',
    'selection_light': '#002200',
    'highlight': '#004400',
    
    # Line Numbers
    'line_bg': '#111111',
    'line_fg': '#00cc00',
    
    # Status Colors
    'status_ready': '#00ff00',
    'status_modified': '#ffff00',
    'status_error': '#ff0000',
    'status_warning': '#ffff00',
    
    # Syntax Highlighting
    'syntax_keyword': '#ff00ff',
    'syntax_builtin': '#00ffff',
    'syntax_string': '#ffff00',
    'syntax_comment': '#666666',
    'syntax_function': '#00ff00',
    'syntax_class': '#ff0000',
    'syntax_number': '#ff6600',
    'syntax_operator': '#00ffff',
    'syntax_tag': '#ff00ff',
    'syntax_attribute': '#ffff00',
    'syntax_variable': '#00ffff',
}

# ==================== OPTIMIZED STYLESHEET ====================

HACKER_STYLESHEET = f"""
    /* Main Window - No transparency for speed */
    QMainWindow {{
        background-color: {HACKER_GAMER_THEME['bg_dark']};
        border: 2px solid {HACKER_GAMER_THEME['primary']};
        border-radius: 8px;
    }}
    
    /* Menu Bar */
    QMenuBar {{
        background-color: {HACKER_GAMER_THEME['bg_darker']};
        color: {HACKER_GAMER_THEME['text_primary']};
        border-bottom: 2px solid {HACKER_GAMER_THEME['primary']};
        padding: 3px;
    }}
    
    QMenuBar::item {{
        padding: 5px 10px;
        margin: 0 1px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {HACKER_GAMER_THEME['selection']};
    }}
    
    /* Menus */
    QMenu {{
        background-color: {HACKER_GAMER_THEME['bg_darker']};
        color: {HACKER_GAMER_THEME['text_primary']};
        border: 1px solid {HACKER_GAMER_THEME['primary']};
    }}
    
    QMenu::item:selected {{
        background-color: {HACKER_GAMER_THEME['selection']};
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: {HACKER_GAMER_THEME['bg_darker']};
        color: {HACKER_GAMER_THEME['text_secondary']};
        border-top: 1px solid {HACKER_GAMER_THEME['primary']};
    }}
    
    /* Buttons - Simple for speed */
    QPushButton {{
        background-color: {HACKER_GAMER_THEME['bg_medium']};
        color: {HACKER_GAMER_THEME['text_primary']};
        border: 1px solid {HACKER_GAMER_THEME['primary']};
        border-radius: 3px;
        padding: 5px 10px;
        font-weight: bold;
        min-width: 80px;
    }}
    
    QPushButton:hover {{
        background-color: {HACKER_GAMER_THEME['selection']};
        border: 1px solid {HACKER_GAMER_THEME['primary_light']};
    }}
    
    /* LineEdit */
    QLineEdit {{
        background-color: {HACKER_GAMER_THEME['bg_medium']};
        color: {HACKER_GAMER_THEME['text_editor']};
        border: 1px solid {HACKER_GAMER_THEME['primary']};
        border-radius: 3px;
        padding: 6px;
        font-family: 'Consolas', 'Monospace';
        font-size: 12px;
    }}
    
    QLineEdit:focus {{
        border: 2px solid {HACKER_GAMER_THEME['secondary']};
    }}
    
    /* Tab Widget */
    QTabWidget::pane {{
        background-color: transparent;
        border: none;
    }}
    
    QTabBar::tab {{
        background-color: {HACKER_GAMER_THEME['bg_medium']};
        color: {HACKER_GAMER_THEME['text_secondary']};
        padding: 6px 12px;
        margin-right: 1px;
        border: 1px solid {HACKER_GAMER_THEME['primary']};
        border-bottom: none;
        font-weight: bold;
    }}
    
    QTabBar::tab:selected {{
        background-color: {HACKER_GAMER_THEME['bg_dark']};
        color: {HACKER_GAMER_THEME['primary']};
        border-top: 2px solid {HACKER_GAMER_THEME['primary']};
    }}
    
    /* ScrollBar - Simplified for speed */
    QScrollBar:vertical {{
        background-color: {HACKER_GAMER_THEME['bg_medium']};
        width: 10px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {HACKER_GAMER_THEME['primary']};
        border-radius: 5px;
        min-height: 20px;
    }}
    
    QScrollBar:horizontal {{
        background-color: {HACKER_GAMER_THEME['bg_medium']};
        height: 10px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {HACKER_GAMER_THEME['primary']};
        border-radius: 5px;
        min-width: 20px;
    }}
    
    /* TreeView - Optimized */
    QTreeView {{
        background-color: transparent;
        color: {HACKER_GAMER_THEME['text_primary']};
        border: none;
        font-size: 11px;
        font-family: 'Consolas', 'Monospace';
    }}
    
    QTreeView::item:selected {{
        background-color: {HACKER_GAMER_THEME['selection']};
        color: white;
    }}
    
    /* Labels */
    QLabel {{
        background-color: transparent;
    }}
"""

# ==================== FAST SYNTAX HIGHLIGHTER ====================

class FastHighlighter(QSyntaxHighlighter):
    def __init__(self, document, language='python'):
        super().__init__(document)
        self.language = language
        self.rules = []
        self.setup_rules()
    
    def set_language(self, language):
        self.language = language
        self.rules = []
        self.setup_rules()
        self.rehighlight()
    
    def setup_rules(self):
        formats = {
            'keyword': self.create_format(HACKER_GAMER_THEME['syntax_keyword'], bold=True),
            'builtin': self.create_format(HACKER_GAMER_THEME['syntax_builtin']),
            'string': self.create_format(HACKER_GAMER_THEME['syntax_string']),
            'comment': self.create_format(HACKER_GAMER_THEME['syntax_comment'], italic=True),
            'function': self.create_format(HACKER_GAMER_THEME['syntax_function'], bold=True),
            'class': self.create_format(HACKER_GAMER_THEME['syntax_class'], bold=True),
            'number': self.create_format(HACKER_GAMER_THEME['syntax_number']),
            'operator': self.create_format(HACKER_GAMER_THEME['syntax_operator']),
            'tag': self.create_format(HACKER_GAMER_THEME['syntax_tag'], bold=True),
            'attribute': self.create_format(HACKER_GAMER_THEME['syntax_attribute']),
            'variable': self.create_format(HACKER_GAMER_THEME['syntax_variable']),
        }
        
        # Python (most common)
        if self.language == 'python':
            keywords = [
                'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return',
                'import', 'from', 'as', 'try', 'except', 'finally', 'with',
                'and', 'or', 'not', 'in', 'is', 'None', 'True', 'False'
            ]
            for kw in keywords:
                self.rules.append((r'\b' + kw + r'\b', formats['keyword']))
            
            self.rules.append((r'\bdef\s+(\w+)', formats['function']))
            self.rules.append((r'\bclass\s+(\w+)', formats['class']))
            self.rules.append((r'#.*', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'[^']*'", formats['string']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # JavaScript
        elif self.language == 'javascript':
            js_keywords = ['function', 'class', 'const', 'let', 'var', 'if', 'else',
                          'for', 'while', 'return', 'try', 'catch', 'finally']
            for kw in js_keywords:
                self.rules.append((r'\b' + kw + r'\b', formats['keyword']))
            
            self.rules.append((r'\bfunction\s+(\w+)', formats['function']))
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'[^']*'", formats['string']))
            self.rules.append((r'`[^`]*`', formats['string']))
        
        # Other languages use simplified rules for speed
        elif self.language == 'java':
            self.rules.append((r'\bclass\s+(\w+)', formats['class']))
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
        
        elif self.language == 'cpp' or self.language == 'c':
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
        
        elif self.language == 'html':
            self.rules.append((r'</?\w+', formats['tag']))
            self.rules.append((r'"[^"]*"', formats['string']))
        
        elif self.language == 'css':
            self.rules.append((r'/\*[\s\S]*?\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
    
    def create_format(self, color, bold=False, italic=False):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Weight.Bold)
        if italic:
            fmt.setFontItalic(True)
        return fmt
    
    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in re.finditer(pattern, text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, fmt)

# ==================== FAST CODE EDITOR ====================

class FastCodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)
        self.highlighter = FastHighlighter(self.document())
        
        # Setup editor
        self.setup_editor()
        self.setup_signals()
        
        # Initial update
        self.update_line_number_area_width()
        self.highlight_current_line()
    
    def setup_editor(self):
        # Font - Monospaced for speed
        font = QFont("Consolas", 11)
        self.setFont(font)
        self.setTabStopDistance(40)
        
        # Simple colors - no transparency for speed
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {HACKER_GAMER_THEME['bg_dark']};
                color: {HACKER_GAMER_THEME['text_editor']};
                selection-background-color: {HACKER_GAMER_THEME['selection']};
                selection-color: #ffffff;
                border: 1px solid {HACKER_GAMER_THEME['primary']};
                font-family: 'Consolas', 'Monospace';
            }}
        """)
    
    def setup_signals(self):
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
    
    def line_number_area_width(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count //= 10
            digits += 1
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits
    
    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), 
                                        self.line_number_area.width(), rect.height())
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), width, cr.height()))
    
    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(HACKER_GAMER_THEME['line_bg']))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(HACKER_GAMER_THEME['line_fg']))
                painter.drawText(0, top, self.line_number_area.width() - 5, 
                                self.fontMetrics().height(),
                                Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1
    
    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(HACKER_GAMER_THEME['selection_light'])
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

# ==================== LINE NUMBER AREA ====================

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

# ==================== FAST INTERACTIVE TERMINAL ====================

class FastInteractiveTerminal(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setup_terminal()
        self.command_history = []
        self.history_index = -1
        self.current_dir = os.getcwd()
        self.compiler_paths = self.detect_compilers()
        
        # Enable typing
        self.setReadOnly(False)
        
        # Show welcome message
        self.append_welcome()
        
        # Store the last position for command input
        self.input_start_pos = self.textCursor().position()
    
    def setup_terminal(self):
        self.setFont(QFont("Consolas", 10))
        
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {HACKER_GAMER_THEME['terminal_bg']};
                color: {HACKER_GAMER_THEME['terminal_text']};
                border: 2px solid {HACKER_GAMER_THEME['primary']};
                font-family: 'Consolas', 'Monospace';
                selection-background-color: {HACKER_GAMER_THEME['selection']};
            }}
        """)
        
        # Make it fully interactive
        self.setAcceptRichText(False)
    
    def detect_compilers(self):
        """Detect available compilers - faster detection"""
        compilers = {}
        
        # Check common paths
        common_commands = {
            'python': ['python3', 'python'],
            'java': ['java', 'javac'],
            'node': ['node'],
            'php': ['php'],
            'gcc': ['gcc'],
            'g++': ['g++']
        }
        
        for lang, cmds in common_commands.items():
            for cmd in cmds:
                try:
                    result = subprocess.run([cmd, '--version'] if cmd != 'javac' else [cmd, '-version'],
                                          capture_output=True, timeout=1)
                    if result.returncode == 0 or result.stderr:
                        compilers[lang] = cmd
                        break
                except:
                    continue
        
        return compilers
    
    def append_welcome(self):
        self.append(f"[{datetime.now().strftime('%H:%M:%S')}] ⚡ HACKER-GAMER TERMINAL ⚡")
        self.append(f"Directory: {self.current_dir}")
        self.append("Type commands directly (Enter to execute, Ctrl+C to cancel)")
        self.append("")
        
        # Update input start position
        self.input_start_pos = self.textCursor().position()
    
    def keyPressEvent(self, event):
        # Handle Enter key to execute command
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.execute_current_line()
            event.accept()
            return
        
        # Handle Ctrl+C to clear line
        elif event.key() == Qt.Key.Key_C and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.clear_line()
            event.accept()
            return
        
        # Handle Up/Down for history
        elif event.key() == Qt.Key.Key_Up:
            self.show_history_previous()
            event.accept()
            return
        
        elif event.key() == Qt.Key.Key_Down:
            self.show_history_next()
            event.accept()
            return
        
        # Handle Ctrl+L to clear terminal
        elif event.key() == Qt.Key.Key_L and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.clear()
            self.append_welcome()
            event.accept()
            return
        
        # Let default handling for other keys
        super().keyPressEvent(event)
    
    def execute_current_line(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Get the last line (the command)
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        command = cursor.selectedText().strip()
        
        # Remove the selection
        cursor.clearSelection()
        
        if command:
            # Execute command
            self.execute_command(command)
        
        # Add new line for next command
        self.append("")
    
    def clear_line(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
    
    def show_history_previous(self):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.clear_line()
            cursor = self.textCursor()
            cursor.insertText(self.command_history[self.history_index])
    
    def show_history_next(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.clear_line()
            cursor = self.textCursor()
            cursor.insertText(self.command_history[self.history_index])
    
    def execute_command(self, command: str):
        # Add to history
        if not self.command_history or self.command_history[-1] != command:
            self.command_history.append(command)
            if len(self.command_history) > 100:  # Limit history size
                self.command_history.pop(0)
        self.history_index = -1
        
        # Show command with prompt
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(f"\n$ {command}\n")
        
        # Special commands
        if command.lower() == 'clear':
            self.clear()
            self.append_welcome()
            return
        
        if command.lower() == 'help':
            self.show_help()
            return
        
        if command.lower() == 'compilers':
            self.show_compilers()
            return
        
        if command.lower().startswith('cd '):
            self.handle_cd(command)
            return
        
        # Run command
        self.run_command(command)
    
    def run_command(self, command: str):
        try:
            # Check if it's a file execution
            if self.is_file_execution(command):
                self.handle_file_execution(command)
                return
            
            # Run external command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.current_dir,
                timeout=10
            )
            
            # Display output
            if result.stdout:
                self.append(result.stdout)
            if result.stderr:
                self.append(f"ERROR: {result.stderr}")
            
            if result.returncode != 0:
                self.append(f"[Exit code: {result.returncode}]")
        
        except subprocess.TimeoutExpired:
            self.append("Command timed out")
        except Exception as e:
            self.append(f"Error: {str(e)}")
    
    def is_file_execution(self, command: str) -> bool:
        """Check if command is for executing a file"""
        patterns = [
            r'\.py$', r'\.js$', r'\.php$', r'\.java$', r'\.c$', r'\.cpp$', r'\.sh$',
            r'python\s+\S+', r'node\s+\S+', r'php\s+\S+', r'java\s+\S+', 
            r'javac\s+\S+', r'gcc\s+\S+', r'g\+\+\s+\S+', r'\./'
        ]
        
        for pattern in patterns:
            if re.search(pattern, command):
                return True
        return False
    
    def handle_file_execution(self, command: str):
        """Handle execution of code files"""
        try:
            # Simple execution - just run it
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.current_dir,
                timeout=15
            )
            
            if result.stdout:
                self.append(result.stdout)
            if result.stderr:
                self.append(f"ERROR: {result.stderr}")
            
        except Exception as e:
            self.append(f"Execution error: {str(e)}")
    
    def handle_cd(self, command: str):
        path = command[3:].strip()
        try:
            if path == "..":
                os.chdir("..")
            elif path:
                if os.path.isdir(path):
                    os.chdir(path)
                else:
                    new_path = os.path.join(self.current_dir, path)
                    if os.path.isdir(new_path):
                        os.chdir(new_path)
                    else:
                        self.append(f"Directory not found: {path}")
                        return
            
            self.current_dir = os.getcwd()
            self.append(f"Current dir: {self.current_dir}")
        except Exception as e:
            self.append(f"cd error: {str(e)}")
    
    def show_help(self):
        help_text = """
═══════════════════════════════════════════════════════════════════════════════
                            TERMINAL HELP - HACKER MODE
═══════════════════════════════════════════════════════════════════════════════

BASIC COMMANDS:
  • cd [dir]          - Change directory
  • ls / dir          - List files
  • clear             - Clear terminal
  • help              - Show this help
  • compilers         - Show detected compilers

CODE EXECUTION:
  • python script.py  - Run Python
  • node script.js    - Run JavaScript
  • php script.php    - Run PHP
  • javac Main.java   - Compile Java
  • java Main         - Run Java
  • ./program         - Run executable

KEYBOARD SHORTCUTS:
  • Enter             - Execute command
  • Ctrl+C            - Clear current line
  • Ctrl+L            - Clear terminal
  • Up/Down           - Command history
  • Tab               - Auto-completion

EXAMPLES:
  $ python test.py
  $ ls -la
  $ cd projects
  $ clear
═══════════════════════════════════════════════════════════════════════════════
"""
        self.append(help_text)
    
    def show_compilers(self):
        if self.compiler_paths:
            self.append("⚡ DETECTED COMPILERS:")
            for lang, cmd in self.compiler_paths.items():
                self.append(f"  • {lang}: {cmd}")
        else:
            self.append("No compilers detected")

# ==================== GAMER FILE EXPLORER ====================

class GamerFileExplorer(QTreeView):
    def __init__(self):
        super().__init__()
        self.setup_explorer()
    
    def setup_explorer(self):
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        
        # Set custom icons
        icon_provider = GamerIconProvider()
        self.model.setIconProvider(icon_provider)
        
        self.setModel(self.model)
        
        # Hide unnecessary columns for speed
        for i in range(1, 4):
            self.hideColumn(i)
        
        self.setHeaderHidden(True)
        
        # Gamer style
        self.setStyleSheet(f"""
            QTreeView {{
                background-color: {HACKER_GAMER_THEME['bg_medium']};
                color: {HACKER_GAMER_THEME['text_primary']};
                border: 1px solid {HACKER_GAMER_THEME['primary']};
                font-family: 'Consolas', 'Monospace';
                font-size: 11px;
                outline: none;
            }}
            QTreeView::item {{
                height: 22px;
                padding: 1px;
            }}
            QTreeView::item:selected {{
                background-color: {HACKER_GAMER_THEME['selection']};
                color: white;
                font-weight: bold;
            }}
            QTreeView::item:hover {{
                background-color: {HACKER_GAMER_THEME['highlight']};
            }}
        """)
        
        # Set icon size
        self.setIconSize(QSize(16, 16))
    
    def set_root_path(self, path: str):
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))

# ==================== GAMER ICON PROVIDER ====================

class GamerIconProvider(QFileIconProvider):
    def __init__(self):
        super().__init__()
        
    def icon(self, info):
        # Override icons with gamer-style text/icons
        if info.isDir():
            # Folder icon
            pixmap = QPixmap(16, 16)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Draw folder icon
            painter.setPen(QPen(QColor(HACKER_GAMER_THEME['neon_blue']), 2))
            painter.setBrush(QColor(HACKER_GAMER_THEME['bg_dark']))
            painter.drawRect(2, 4, 12, 10)
            painter.drawRect(0, 2, 16, 12)
            
            painter.end()
            return QIcon(pixmap)
        
        elif info.isFile():
            ext = info.suffix().lower()
            
            # File type colors
            if ext in ['py', 'js', 'java', 'cpp', 'c', 'php', 'html', 'css']:
                color = HACKER_GAMER_THEME['neon_green']
            elif ext in ['exe', 'bin', 'sh', 'bat']:
                color = HACKER_GAMER_THEME['neon_yellow']
            elif ext in ['txt', 'md', 'json', 'xml', 'yml']:
                color = HACKER_GAMER_THEME['neon_cyan']
            else:
                color = HACKER_GAMER_THEME['text_secondary']
            
            # Create file icon
            pixmap = QPixmap(16, 16)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Draw file icon
            painter.setPen(QPen(QColor(color), 2))
            painter.setBrush(QColor(HACKER_GAMER_THEME['bg_dark']))
            painter.drawRect(2, 2, 12, 14)
            painter.drawLine(10, 2, 10, 4)
            painter.drawLine(12, 2, 12, 4)
            
            # Add extension indicator
            if ext in ['py']:
                painter.setPen(QPen(QColor(HACKER_GAMER_THEME['neon_green']), 1))
                painter.drawText(4, 12, "PY")
            elif ext in ['js']:
                painter.setPen(QPen(QColor(HACKER_GAMER_THEME['neon_yellow']), 1))
                painter.drawText(4, 12, "JS")
            elif ext in ['html', 'css']:
                painter.setPen(QPen(QColor(HACKER_GAMER_THEME['neon_red']), 1))
                painter.drawText(4, 12, "WEB")
            
            painter.end()
            return QIcon(pixmap)
        
        return super().icon(info)

# ==================== MAIN WINDOW ====================

class HackerGamerEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()
        
        # Setup timers
        self.setup_timers()
        
        # Create initial tab
        self.create_new_file()
        
        # Focus on editor
        QTimer.singleShot(50, self.focus_editor)  # Faster focus
    
    def setup_window(self):
        self.setWindowTitle("⚡ HACKER-GAMER CODE EDITOR ⚡")
        self.setGeometry(100, 50, 1600, 900)
        
        # Set window icon
        self.set_window_icon()
        
        # No transparency for speed
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        
        # Apply hacker style
        self.setStyleSheet(HACKER_STYLESHEET)
        
        # Set central widget
        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: {HACKER_GAMER_THEME['bg_dark']};")
        self.setCentralWidget(central_widget)
    
    def set_window_icon(self):
        # Create gamer/hacker icon
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw hacker skull or matrix symbol
        painter.setPen(QPen(QColor(HACKER_GAMER_THEME['neon_green']), 3))
        painter.setBrush(QColor(HACKER_GAMER_THEME['bg_darker']))
        
        # Draw matrix-style brackets
        painter.drawRect(15, 15, 34, 34)
        
        # Draw binary/hex pattern
        painter.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        painter.drawText(20, 30, "01")
        painter.drawText(40, 30, "10")
        painter.drawText(20, 50, "11")
        painter.drawText(40, 50, "00")
        
        painter.end()
        self.setWindowIcon(QIcon(pixmap))
    
    def setup_variables(self):
        self.current_file = None
        self.open_files = {}
        self.project_path = None
        self.font_size = 11
        self.current_language = 'python'
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self.centralWidget())
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Title bar
        self.create_title_bar(main_layout)
        
        # Main content
        self.create_main_content(main_layout)
        
        # Terminal
        self.create_terminal(main_layout)
        
        # Status bar
        self.create_status_bar()
    
    def create_title_bar(self, parent_layout):
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {HACKER_GAMER_THEME['bg_darker']};
                border: 2px solid {HACKER_GAMER_THEME['primary']};
                border-radius: 3px;
            }}
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Gamer logo
        logo = QLabel("⚡")
        logo.setStyleSheet(f"""
            font-size: 20px;
            color: {HACKER_GAMER_THEME['neon_green']};
            font-weight: bold;
        """)
        
        # Title with hacker effect
        title = QLabel("⚡ HACKER-GAMER CODE EDITOR ⚡")
        title.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {HACKER_GAMER_THEME['primary']};
            font-family: 'Consolas', 'Monospace';
        """)
        
        # System info
        self.system_info = QLabel("")
        self.system_info.setStyleSheet(f"""
            font-size: 10px;
            color: {HACKER_GAMER_THEME['text_secondary']};
            font-family: 'Consolas', 'Monospace';
        """)
        
        # Window controls
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(3)
        
        # Control buttons
        min_btn = QPushButton("─")
        min_btn.setFixedSize(25, 25)
        min_btn.clicked.connect(self.showMinimized)
        
        max_btn = QPushButton("□")
        max_btn.setFixedSize(25, 25)
        max_btn.clicked.connect(self.toggle_maximize)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(25, 25)
        close_btn.clicked.connect(self.close)
        
        controls_layout.addWidget(min_btn)
        controls_layout.addWidget(max_btn)
        controls_layout.addWidget(close_btn)
        
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.system_info)
        layout.addStretch()
        layout.addWidget(controls)
        
        parent_layout.addWidget(title_bar)
    
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.max_btn.setText("□")
        else:
            self.showMaximized()
            self.max_btn.setText("❐")
    
    def create_main_content(self, parent_layout):
        # Create splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar
        self.create_sidebar()
        
        # Editor area
        self.create_editor_area()
        
        parent_layout.addWidget(self.main_splitter, 1)
        self.main_splitter.setSizes([200, 1400])
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setMinimumWidth(200)
        sidebar.setMaximumWidth(300)
        sidebar.setStyleSheet(f"""
            QWidget {{
                background-color: {HACKER_GAMER_THEME['bg_medium']};
                border: 1px solid {HACKER_GAMER_THEME['primary']};
                border-radius: 3px;
            }}
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Explorer header
        explorer_header = QWidget()
        explorer_header.setFixedHeight(35)
        explorer_header.setStyleSheet(f"""
            QWidget {{
                background-color: {HACKER_GAMER_THEME['bg_darker']};
                border-bottom: 1px solid {HACKER_GAMER_THEME['primary']};
            }}
        """)
        
        header_layout = QHBoxLayout(explorer_header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        explorer_title = QLabel("📁 FILES")
        explorer_title.setStyleSheet(f"""
            color: {HACKER_GAMER_THEME['neon_blue']};
            font-weight: bold;
            font-size: 12px;
        """)
        
        # Quick action buttons
        open_btn = QPushButton("📂")
        open_btn.setFixedSize(25, 25)
        open_btn.setToolTip("Open Folder")
        open_btn.clicked.connect(self.open_folder)
        
        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedSize(25, 25)
        refresh_btn.setToolTip("Refresh")
        refresh_btn.clicked.connect(self.refresh_explorer)
        
        header_layout.addWidget(explorer_title)
        header_layout.addStretch()
        header_layout.addWidget(open_btn)
        header_layout.addWidget(refresh_btn)
        
        # File explorer
        self.file_explorer = GamerFileExplorer()
        self.file_explorer.doubleClicked.connect(self.on_file_double_clicked)
        
        layout.addWidget(explorer_header)
        layout.addWidget(self.file_explorer)
        
        self.main_splitter.addWidget(sidebar)
    
    def create_editor_area(self):
        editor_area = QWidget()
        
        layout = QVBoxLayout(editor_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Editor toolbar
        self.create_editor_toolbar(layout)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.setDocumentMode(True)
        
        layout.addWidget(self.tab_widget)
        
        self.main_splitter.addWidget(editor_area)
    
    def create_editor_toolbar(self, parent_layout):
        toolbar = QWidget()
        toolbar.setFixedHeight(40)
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: {HACKER_GAMER_THEME['bg_darker']};
                border: 1px solid {HACKER_GAMER_THEME['primary']};
                border-bottom: none;
            }}
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(5, 0, 5, 0)
        
        # Fast action buttons with icons
        actions = [
            ("⚡ NEW", self.create_new_file, "Ctrl+N", "New file"),
            ("📂 OPEN", self.open_file_dialog, "Ctrl+O", "Open file"),
            ("💾 SAVE", self.save_file, "Ctrl+S", "Save file"),
            ("🚀 RUN", self.run_current_file, "F5", "Run code"),
        ]
        
        for text, callback, shortcut, tooltip in actions:
            btn = QPushButton(text)
            btn.setMinimumHeight(30)
            btn.setToolTip(f"{tooltip} ({shortcut})")
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Language selector
        lang_label = QLabel("LANG:")
        lang_label.setStyleSheet(f"color: {HACKER_GAMER_THEME['text_secondary']}; font-weight: bold;")
        
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "Python", "JavaScript", "HTML", "CSS", 
            "Java", "C++", "C", "PHP", "Bash"
        ])
        self.language_combo.setCurrentText("Python")
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        
        layout.addWidget(lang_label)
        layout.addWidget(self.language_combo)
        
        parent_layout.addWidget(toolbar)
    
    def create_terminal(self, parent_layout):
        # Create dock widget for terminal
        self.terminal = FastInteractiveTerminal()
        
        terminal_container = QWidget()
        terminal_layout = QVBoxLayout(terminal_container)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        terminal_layout.setSpacing(0)
        
        # Terminal header
        terminal_header = QWidget()
        terminal_header.setFixedHeight(30)
        terminal_header.setStyleSheet(f"""
            QWidget {{
                background-color: {HACKER_GAMER_THEME['bg_darker']};
                border: 1px solid {HACKER_GAMER_THEME['primary']};
                border-bottom: none;
            }}
        """)
        
        header_layout = QHBoxLayout(terminal_header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        terminal_title = QLabel("💻 TERMINAL")
        terminal_title.setStyleSheet(f"""
            color: {HACKER_GAMER_THEME['neon_green']};
            font-weight: bold;
        """)
        
        clear_btn = QPushButton("🗑️")
        clear_btn.setFixedSize(20, 20)
        clear_btn.setToolTip("Clear Terminal")
        clear_btn.clicked.connect(self.clear_terminal)
        
        header_layout.addWidget(terminal_title)
        header_layout.addStretch()
        header_layout.addWidget(clear_btn)
        
        terminal_layout.addWidget(terminal_header)
        terminal_layout.addWidget(self.terminal, 1)
        
        # Create dock
        self.terminal_dock = QDockWidget("", self)
        self.terminal_dock.setWidget(terminal_container)
        self.terminal_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable | 
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal_dock)
        self.terminal_dock.setVisible(True)
        self.terminal_dock.setMaximumHeight(300)
    
    def clear_terminal(self):
        self.terminal.clear()
        self.terminal.append_welcome()
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status indicator
        self.status_indicator = QLabel("● READY")
        self.status_indicator.setStyleSheet(f"""
            color: {HACKER_GAMER_THEME['status_ready']};
            font-weight: bold;
            padding-right: 20px;
        """)
        
        # Cursor position
        self.cursor_label = QLabel("Ln 1, Col 1")
        self.cursor_label.setStyleSheet(f"color: {HACKER_GAMER_THEME['text_secondary']};")
        
        # File info
        self.file_label = QLabel("Untitled")
        self.file_label.setStyleSheet(f"color: {HACKER_GAMER_THEME['text_secondary']};")
        
        # Language
        self.language_label = QLabel("Python")
        self.language_label.setStyleSheet(f"color: {HACKER_GAMER_THEME['text_secondary']};")
        
        # Line count
        self.line_count_label = QLabel("Lines: 0")
        self.line_count_label.setStyleSheet(f"color: {HACKER_GAMER_THEME['text_secondary']};")
        
        # Add widgets
        self.status_bar.addWidget(self.status_indicator)
        self.status_bar.addPermanentWidget(self.cursor_label)
        self.status_bar.addPermanentWidget(self.file_label)
        self.status_bar.addPermanentWidget(self.language_label)
        self.status_bar.addPermanentWidget(self.line_count_label)
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        # File menu - hacker style
        file_menu = menubar.addMenu("💾 FILE")
        
        new_action = QAction("⚡ New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.create_new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("📂 Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        save_action = QAction("💾 Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("🚪 Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("✏️ EDIT")
        
        undo_action = QAction("↶ Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("↷ Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        find_action = QAction("🔍 Find", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.find_text)
        edit_menu.addAction(find_action)
        
        # Run menu
        run_menu = menubar.addMenu("🚀 RUN")
        
        run_action = QAction("⚡ Run", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_current_file)
        run_menu.addAction(run_action)
        
        # View menu
        view_menu = menubar.addMenu("👁️ VIEW")
        
        toggle_terminal = QAction("💻 Terminal", self)
        toggle_terminal.setShortcut("Ctrl+`")
        toggle_terminal.triggered.connect(self.toggle_terminal)
        view_menu.addAction(toggle_terminal)
        
        # Help menu - hacker themed
        help_menu = menubar.addMenu("❓ HELP")
        
        about_action = QAction("👾 About", self)
        about_action.triggered.connect(self.show_hacker_about)
        help_menu.addAction(about_action)
    
    def setup_shortcuts(self):
        # Essential shortcuts only for speed
        QShortcut(QKeySequence("Ctrl+W"), self, self.close_current_tab)
        QShortcut(QKeySequence("Ctrl+Tab"), self, self.next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, self.previous_tab)
    
    def setup_timers(self):
        # Clock timer
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()
        
        # Quick auto-save
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.auto_save)
        self.autosave_timer.start(300000)  # 5 minutes
    
    # ==================== FAST EDITOR MANAGEMENT ====================
    
    def create_new_file(self):
        editor = FastCodeEditor()
        index = self.tab_widget.addTab(editor, "⚡ New")
        self.tab_widget.setCurrentIndex(index)
        
        # Store file info
        self.open_files[editor] = {
            'path': None,
            'saved': False,
            'modified': False,
            'language': 'python'
        }
        
        # Connect signals
        editor.cursorPositionChanged.connect(lambda: self.update_cursor_position(editor))
        editor.textChanged.connect(lambda: self.on_text_changed(editor))
        
        # Update status
        self.update_status("New file", "ready")
        self.file_label.setText("New")
        self.update_cursor_position(editor)
        
        return editor
    
    def focus_editor(self):
        editor = self.get_current_editor()
        if editor:
            editor.setFocus()
    
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Code Files (*.py *.js *.html *.css *.java *.cpp *.c *.php *.sh);;All Files (*.*)"
        )
        
        if file_path:
            self.open_file(file_path)
    
    def open_file(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create editor
            editor = FastCodeEditor()
            editor.setPlainText(content)
            
            # Add tab
            filename = os.path.basename(file_path)
            index = self.tab_widget.addTab(editor, f"📄 {filename}")
            self.tab_widget.setCurrentIndex(index)
            
            # Store file info
            self.open_files[editor] = {
                'path': file_path,
                'saved': True,
                'modified': False,
                'language': self.detect_language(file_path)
            }
            
            # Connect signals
            editor.cursorPositionChanged.connect(lambda: self.update_cursor_position(editor))
            editor.textChanged.connect(lambda: self.on_text_changed(editor))
            
            # Set language
            self.set_editor_language(editor, self.open_files[editor]['language'])
            
            # Update status
            self.update_status(f"Opened: {filename}", "ready")
            self.file_label.setText(filename)
            self.update_cursor_position(editor)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file:\n{str(e)}")
    
    def save_file(self):
        editor = self.get_current_editor()
        if not editor:
            return
        
        info = self.open_files.get(editor)
        if not info:
            return
        
        if info['path']:
            # Save to existing file
            try:
                with open(info['path'], 'w', encoding='utf-8') as f:
                    f.write(editor.toPlainText())
                
                info['saved'] = True
                info['modified'] = False
                
                self.update_status(f"Saved: {os.path.basename(info['path'])}", "ready")
                self.update_tab_title(editor)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
        else:
            # Save As dialog
            self.save_as()
    
    def save_as(self):
        editor = self.get_current_editor()
        if not editor:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save As",
            "",
            "All Files (*.*);;Python (*.py);;JavaScript (*.js);;HTML (*.html);;CSS (*.css)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(editor.toPlainText())
                
                # Update file info
                info = self.open_files.get(editor)
                if info:
                    info['path'] = file_path
                    info['saved'] = True
                    info['modified'] = False
                    info['language'] = self.detect_language(file_path)
                
                # Update tab and language
                filename = os.path.basename(file_path)
                index = self.tab_widget.indexOf(editor)
                self.tab_widget.setTabText(index, f"💾 {filename}")
                self.set_editor_language(editor, info['language'])
                
                # Update status
                self.update_status(f"Saved as: {filename}", "ready")
                self.file_label.setText(filename)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
    
    def auto_save(self):
        """Quick auto-save"""
        for editor, info in self.open_files.items():
            if info['path'] and info['modified']:
                try:
                    with open(info['path'], 'w', encoding='utf-8') as f:
                        f.write(editor.toPlainText())
                    info['saved'] = True
                    info['modified'] = False
                except:
                    pass
    
    def close_tab(self, index):
        widget = self.tab_widget.widget(index)
        if isinstance(widget, FastCodeEditor):
            info = self.open_files.get(widget)
            if info and info['modified']:
                reply = QMessageBox.question(
                    self,
                    "Save Changes?",
                    f"Save changes to {self.tab_widget.tabText(index)}?",
                    QMessageBox.StandardButton.Save |
                    QMessageBox.StandardButton.Discard |
                    QMessageBox.StandardButton.Cancel
                )
                
                if reply == QMessageBox.StandardButton.Save:
                    self.save_file()
                elif reply == QMessageBox.StandardButton.Cancel:
                    return
            
            # Remove from open files
            self.open_files.pop(widget, None)
        
        self.tab_widget.removeTab(index)
        
        # If no tabs left, create new file
        if self.tab_widget.count() == 0:
            self.create_new_file()
    
    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.close_tab(current_index)
    
    def next_tab(self):
        current = self.tab_widget.currentIndex()
        next_index = (current + 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(next_index)
    
    def previous_tab(self):
        current = self.tab_widget.currentIndex()
        previous_index = (current - 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(previous_index)
    
    def on_tab_changed(self, index):
        if index >= 0:
            widget = self.tab_widget.widget(index)
            if isinstance(widget, FastCodeEditor):
                info = self.open_files.get(widget)
                if info:
                    # Update file label
                    if info['path']:
                        self.file_label.setText(os.path.basename(info['path']))
                    else:
                        self.file_label.setText("New")
                    
                    # Update language
                    self.language_label.setText(info['language'].capitalize())
                    self.language_combo.setCurrentText(info['language'].capitalize())
                    
                    # Update cursor position
                    self.update_cursor_position(widget)
                    
                    # Focus the editor
                    widget.setFocus()
    
    def update_tab_title(self, editor):
        info = self.open_files.get(editor)
        if info:
            index = self.tab_widget.indexOf(editor)
            filename = os.path.basename(info['path']) if info['path'] else "New"
            if info['modified']:
                self.tab_widget.setTabText(index, f"✎ {filename}")
            else:
                self.tab_widget.setTabText(index, f"📄 {filename}")
    
    # ==================== TEXT OPERATIONS ====================
    
    def on_text_changed(self, editor):
        info = self.open_files.get(editor)
        if info:
            info['modified'] = True
            self.update_tab_title(editor)
            self.update_line_count(editor)
    
    def update_cursor_position(self, editor=None):
        if not editor:
            editor = self.get_current_editor()
        
        if editor:
            cursor = editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            self.cursor_label.setText(f"Ln {line}, Col {col}")
            self.update_line_count(editor)
    
    def update_line_count(self, editor):
        if editor:
            line_count = editor.document().blockCount()
            self.line_count_label.setText(f"Lines: {line_count}")
    
    def undo(self):
        editor = self.get_current_editor()
        if editor:
            editor.undo()
    
    def redo(self):
        editor = self.get_current_editor()
        if editor:
            editor.redo()
    
    def find_text(self):
        editor = self.get_current_editor()
        if editor:
            text, ok = QInputDialog.getText(self, "Find", "Search:")
            if ok and text:
                if editor.find(text):
                    editor.setFocus()
    
    # ==================== LANGUAGE & SYNTAX ====================
    
    def detect_language(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.html': 'html', '.htm': 'html',
            '.css': 'css',
            '.java': 'java',
            '.cpp': 'cpp', '.cc': 'cpp',
            '.c': 'c',
            '.php': 'php',
            '.sh': 'bash',
        }
        
        return language_map.get(ext, 'text')
    
    def set_editor_language(self, editor, language):
        if isinstance(editor, FastCodeEditor):
            editor.highlighter.set_language(language)
            self.language_label.setText(language.capitalize())
            self.language_combo.setCurrentText(language.capitalize())
    
    def on_language_changed(self, language):
        editor = self.get_current_editor()
        if editor:
            lang_lower = language.lower()
            self.open_files[editor]['language'] = lang_lower
            self.set_editor_language(editor, lang_lower)
    
    # ==================== FILE EXPLORER ====================
    
    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folder:
            self.project_path = folder
            self.file_explorer.set_root_path(folder)
            self.update_status(f"Project: {os.path.basename(folder)}", "ready")
    
    def refresh_explorer(self):
        if self.project_path:
            self.file_explorer.set_root_path(self.project_path)
    
    def on_file_double_clicked(self, index):
        path = self.file_explorer.model.filePath(index)
        if os.path.isfile(path):
            self.open_file(path)
    
    # ==================== CODE EXECUTION ====================
    
    def run_current_file(self):
        editor = self.get_current_editor()
        if not editor:
            self.update_status("No file to run", "error")
            return
        
        info = self.open_files.get(editor)
        if not info or not info['path']:
            # Save file first
            reply = QMessageBox.question(
                self,
                "Save File",
                "Save file before running?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
                info = self.open_files.get(editor)
                if not info or not info['path']:
                    return
            else:
                return
        
        # Focus terminal
        self.terminal_dock.setVisible(True)
        self.terminal.setFocus()
        
        # Clear and run
        self.terminal.clear()
        self.terminal.append(f"[EXECUTE] {info['language'].upper()}: {os.path.basename(info['path'])}")
        self.terminal.append("═" * 60)
        
        # Run based on language
        try:
            if info['language'] == 'python':
                cmd = f'python "{info["path"]}"'
            elif info['language'] == 'javascript':
                cmd = f'node "{info["path"]}"'
            elif info['language'] == 'php':
                cmd = f'php "{info["path"]}"'
            elif info['language'] == 'java':
                cmd = f'javac "{info["path"]}" && java -cp "{os.path.dirname(info["path"])}" "{os.path.splitext(os.path.basename(info["path"]))[0]}"'
            elif info['language'] == 'html':
                webbrowser.open(f'file://{os.path.abspath(info["path"])}')
                self.terminal.append("[INFO] Opening in browser...")
                return
            else:
                cmd = f'"{info["path"]}"'
            
            self.terminal.execute_command(cmd)
            self.update_status("Execution started", "ready")
            
        except Exception as e:
            self.terminal.append(f"[ERROR] {str(e)}")
            self.update_status("Execution failed", "error")
    
    # ==================== VIEW CONTROLS ====================
    
    def toggle_terminal(self):
        self.terminal_dock.setVisible(not self.terminal_dock.isVisible())
    
    # ==================== UTILITIES ====================
    
    def get_current_editor(self):
        widget = self.tab_widget.currentWidget()
        if isinstance(widget, FastCodeEditor):
            return widget
        return None
    
    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, 'system_info'):
            self.system_info.setText(f"🕐 {current_time}")
    
    def update_status(self, message: str, status_type: str = "ready"):
        colors = {
            'ready': HACKER_GAMER_THEME['status_ready'],
            'error': HACKER_GAMER_THEME['status_error'],
            'warning': HACKER_GAMER_THEME['status_warning'],
        }
        
        color = colors.get(status_type, HACKER_GAMER_THEME['status_ready'])
        self.status_indicator.setText(f"● {message.upper()}")
        self.status_indicator.setStyleSheet(f"""
            color: {color};
            font-weight: bold;
            padding-right: 20px;
        """)
    
    # ==================== HACKER ABOUT DIALOG ====================
    
    def show_hacker_about(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("👾 SYSTEM INFO - HACKER-GAMER EDITOR")
        about_dialog.setFixedSize(600, 400)
        
        # Hacker-style background
        about_dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {HACKER_GAMER_THEME['bg_darker']};
                border: 3px solid {HACKER_GAMER_THEME['neon_green']};
                color: {HACKER_GAMER_THEME['neon_green']};
                font-family: 'Consolas', 'Monospace';
            }}
            QLabel {{
                color: {HACKER_GAMER_THEME['neon_green']};
                font-family: 'Consolas', 'Monospace';
            }}
            QPushButton {{
                background-color: {HACKER_GAMER_THEME['bg_medium']};
                color: {HACKER_GAMER_THEME['neon_green']};
                border: 1px solid {HACKER_GAMER_THEME['neon_green']};
                padding: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {HACKER_GAMER_THEME['selection']};
            }}
        """)
        
        layout = QVBoxLayout(about_dialog)
        
        # ASCII Art Header
        ascii_art = QLabel("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗                     ║
║  ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗                    ║
║  ███████║███████║██║     █████╔╝ █████╗  ██████╔╝                    ║
║  ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗                    ║
║  ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║                    ║
║  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                    ║
║                                                                      ║
║            ██████╗  █████╗ ███╗   ███╗███████╗██████╗                ║
║           ██╔════╝ ██╔══██╗████╗ ████║██╔════╝██╔══██╗               ║
║           ██║  ███╗███████║██╔████╔██║█████╗  ██████╔╝               ║
║           ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗               ║
║           ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗██║  ██║               ║
║            ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
        """)
        ascii_art.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ascii_art)
        
        # Info text
        info_text = QLabel("""
══════════════════════════════════════════════════════════════════════════════
                           SYSTEM INFORMATION
══════════════════════════════════════════════════════════════════════════════

[+] EDITOR: HACKER-GAMER CODE EDITOR v3.0
[+] BUILD:  ULTRA-FAST OPTIMIZED
[+] THEME:  NEON HACKER/GAMER
[+] MODE:   PERFORMANCE MAXIMIZED

[+] FEATURES:
    • Ultra-fast code editor with minimal overhead
    • Interactive hacker-style terminal
    • Gamer-optimized file explorer
    • Multi-language syntax highlighting
    • Real-time code execution
    • Custom gamer icons and interface

[+] DEVELOPER: LRD_SOUL
[+] CONTACT:   inscreator728@gmail.com
[+] TELEGRAM:  @lrd_soul
[+] GITHUB:    inscreator728

[+] WARNING:
    This system is optimized for maximum performance.
    All non-essential features have been disabled.
    Running at 100% efficiency.

══════════════════════════════════════════════════════════════════════════════
[SYSTEM] >> READY FOR HACKING...
══════════════════════════════════════════════════════════════════════════════
        """)
        info_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(info_text)
        
        # Close button
        close_btn = QPushButton("[CLOSE SYSTEM INFO]")
        close_btn.clicked.connect(about_dialog.accept)
        layout.addWidget(close_btn)
        
        about_dialog.exec()
    
    def closeEvent(self, event):
        # Quick close - no prompts for speed
        event.accept()

# ==================== FAST APPLICATION ====================

def main():
    # Disable High DPI scaling for speed
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.Round
    )
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Fast and clean
    
    # Set app info
    app.setApplicationName("Hacker-Gamer Code Editor")
    app.setOrganizationName("LRD-TECH")
    
    # Create and show window
    window = HackerGamerEditor()
    window.show()
    
    # Start app
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
