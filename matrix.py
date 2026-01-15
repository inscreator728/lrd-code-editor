# lrd_code_editor_ultimate.py - GAMER/HACKER EDITION
import sys
import os
import subprocess
import re
import webbrowser
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ==================== GAMER HACKER THEME ====================

LRD_GAMER_THEME = {
    # Dark backgrounds (non-transparent for speed)
    'bg_main': '#0a0a0a',
    'bg_dark': '#050505',
    'bg_medium': '#0d0d0d',
    'bg_light': '#111111',
    'bg_lighter': '#1a1a1a',
    
    # Gamer Colors (Neon/Cyberpunk)
    'primary': '#00ff00',  # Matrix Green
    'primary_light': '#66ff66',
    'primary_dark': '#00cc00',
    
    'secondary': '#ff0066',  # Cyber Pink
    'secondary_light': '#ff66aa',
    'secondary_dark': '#cc0055',
    
    'accent': '#0066ff',  # Cyber Blue
    'accent_light': '#66aaff',
    'warning': '#ffff00',  # Warning Yellow
    'warning_light': '#ffff66',
    
    'matrix': '#00ff00',  # Matrix Green
    'cyber_blue': '#0066ff',
    'cyber_pink': '#ff0066',
    'cyber_purple': '#9900ff',
    'neon_orange': '#ff6600',
    
    # Text Colors
    'text_primary': '#00ff00',  # Matrix Green
    'text_secondary': '#66ff66',
    'text_tertiary': '#99ff99',
    'text_disabled': '#666666',
    'text_editor': '#00ff00',
    
    # Status Colors
    'status_ready': '#00ff00',
    'status_modified': '#ffff00',
    'status_error': '#ff0000',
    'status_warning': '#ffff00',
    
    # Syntax Highlighting
    'syntax_keyword': '#ff0066',  # Cyber Pink
    'syntax_builtin': '#0066ff',  # Cyber Blue
    'syntax_string': '#ffff00',  # Warning Yellow
    'syntax_comment': '#666666',
    'syntax_function': '#00ff00',  # Matrix Green
    'syntax_class': '#9900ff',  # Cyber Purple
    'syntax_number': '#ff6600',  # Neon Orange
    'syntax_operator': '#00ff00',
    'syntax_tag': '#ff0066',
    'syntax_attribute': '#ffff00',
    'syntax_variable': '#0066ff',
}

# ==================== GAMER STYLESHEET ====================

GAMER_STYLESHEET = f"""
    /* Main Window */
    QMainWindow {{
        background-color: {LRD_GAMER_THEME['bg_main']};
        border: 2px solid {LRD_GAMER_THEME['primary']};
        border-radius: 8px;
    }}
    
    /* Menu Bar */
    QMenuBar {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        color: {LRD_GAMER_THEME['primary']};
        border-bottom: 2px solid {LRD_GAMER_THEME['primary']};
        padding: 4px;
        font-family: 'Courier New';
        font-weight: bold;
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 4px 8px;
        margin: 0 2px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {LRD_GAMER_THEME['primary']};
        color: black;
    }}
    
    /* Menus */
    QMenu {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        color: {LRD_GAMER_THEME['primary']};
        border: 1px solid {LRD_GAMER_THEME['primary']};
        font-family: 'Courier New';
    }}
    
    QMenu::item {{
        padding: 6px 20px;
    }}
    
    QMenu::item:selected {{
        background-color: {LRD_GAMER_THEME['primary']};
        color: black;
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        color: {LRD_GAMER_THEME['primary']};
        border-top: 1px solid {LRD_GAMER_THEME['primary']};
        font-family: 'Courier New';
        font-size: 10px;
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {LRD_GAMER_THEME['bg_light']};
        color: {LRD_GAMER_THEME['primary']};
        border: 1px solid {LRD_GAMER_THEME['primary']};
        border-radius: 3px;
        padding: 5px 10px;
        font-family: 'Courier New';
        font-weight: bold;
        min-width: 80px;
    }}
    
    QPushButton:hover {{
        background-color: {LRD_GAMER_THEME['primary']};
        color: black;
        border: 1px solid {LRD_GAMER_THEME['primary_light']};
    }}
    
    QPushButton:pressed {{
        background-color: {LRD_GAMER_THEME['primary_dark']};
        color: white;
    }}
    
    /* ComboBox */
    QComboBox {{
        background-color: {LRD_GAMER_THEME['bg_light']};
        color: {LRD_GAMER_THEME['primary']};
        border: 1px solid {LRD_GAMER_THEME['primary']};
        border-radius: 3px;
        padding: 4px;
        font-family: 'Courier New';
        min-width: 100px;
    }}
    
    QComboBox::drop-down {{
        border: none;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        color: {LRD_GAMER_THEME['primary']};
        border: 1px solid {LRD_GAMER_THEME['primary']};
        selection-background-color: {LRD_GAMER_THEME['primary']};
        selection-color: black;
    }}
    
    /* LineEdit */
    QLineEdit {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        color: {LRD_GAMER_THEME['primary']};
        border: 1px solid {LRD_GAMER_THEME['primary']};
        border-radius: 3px;
        padding: 6px;
        font-family: 'Consolas';
        font-size: 11px;
    }}
    
    QLineEdit:focus {{
        border: 2px solid {LRD_GAMER_THEME['secondary']};
    }}
    
    /* Tab Widget */
    QTabWidget::pane {{
        background-color: transparent;
        border: none;
    }}
    
    QTabBar::tab {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        color: {LRD_GAMER_THEME['primary']};
        padding: 6px 12px;
        margin-right: 1px;
        border: 1px solid {LRD_GAMER_THEME['primary']};
        border-bottom: none;
        font-family: 'Courier New';
        font-weight: bold;
    }}
    
    QTabBar::tab:selected {{
        background-color: {LRD_GAMER_THEME['bg_main']};
        color: {LRD_GAMER_THEME['primary']};
        border-top: 2px solid {LRD_GAMER_THEME['primary']};
    }}
    
    QTabBar::tab:hover {{
        background-color: {LRD_GAMER_THEME['bg_light']};
    }}
    
    /* ScrollBar */
    QScrollBar:vertical {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        width: 10px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {LRD_GAMER_THEME['primary']};
        border-radius: 5px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {LRD_GAMER_THEME['primary_light']};
    }}
    
    QScrollBar:horizontal {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        height: 10px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {LRD_GAMER_THEME['primary']};
        border-radius: 5px;
        min-width: 20px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {LRD_GAMER_THEME['primary_light']};
    }}
    
    /* TreeView */
    QTreeView {{
        background-color: transparent;
        color: {LRD_GAMER_THEME['primary']};
        border: none;
        outline: none;
        font-family: 'Courier New';
        font-size: 10px;
    }}
    
    QTreeView::item {{
        height: 22px;
        padding: 1px;
    }}
    
    QTreeView::item:selected {{
        background-color: {LRD_GAMER_THEME['primary']};
        color: black;
    }}
    
    QTreeView::item:hover {{
        background-color: {LRD_GAMER_THEME['bg_light']};
    }}
    
    /* Labels */
    QLabel {{
        background-color: transparent;
        font-family: 'Courier New';
    }}
    
    /* TextEdit */
    QTextEdit {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        color: {LRD_GAMER_THEME['primary']};
        border: 1px solid {LRD_GAMER_THEME['primary']};
        border-radius: 3px;
        font-family: 'Consolas';
        font-size: 11px;
        selection-background-color: {LRD_GAMER_THEME['primary']};
        selection-color: black;
    }}
    
    /* PlainTextEdit */
    QPlainTextEdit {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        color: {LRD_GAMER_THEME['primary']};
        border: 1px solid {LRD_GAMER_THEME['primary']};
        border-radius: 3px;
        font-family: 'Consolas';
        font-size: 11px;
        selection-background-color: {LRD_GAMER_THEME['primary']};
        selection-color: black;
    }}
    
    /* Dock Widget */
    QDockWidget {{
        border: 1px solid {LRD_GAMER_THEME['primary']};
        border-radius: 3px;
    }}
    
    QDockWidget::title {{
        background-color: {LRD_GAMER_THEME['bg_dark']};
        color: {LRD_GAMER_THEME['primary']};
        padding: 4px 8px;
        font-weight: bold;
        border-bottom: 1px solid {LRD_GAMER_THEME['primary']};
    }}
"""

# ==================== SYNTAX HIGHLIGHTER ====================

class LRDHighlighter(QSyntaxHighlighter):
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
            'keyword': self.create_format(LRD_GAMER_THEME['syntax_keyword'], bold=True),
            'builtin': self.create_format(LRD_GAMER_THEME['syntax_builtin']),
            'string': self.create_format(LRD_GAMER_THEME['syntax_string']),
            'comment': self.create_format(LRD_GAMER_THEME['syntax_comment'], italic=True),
            'function': self.create_format(LRD_GAMER_THEME['syntax_function'], bold=True),
            'class': self.create_format(LRD_GAMER_THEME['syntax_class'], bold=True),
            'number': self.create_format(LRD_GAMER_THEME['syntax_number']),
            'operator': self.create_format(LRD_GAMER_THEME['syntax_operator']),
            'tag': self.create_format(LRD_GAMER_THEME['syntax_tag'], bold=True),
            'attribute': self.create_format(LRD_GAMER_THEME['syntax_attribute']),
            'variable': self.create_format(LRD_GAMER_THEME['syntax_variable']),
        }
        
        # Python
        if self.language == 'python':
            keywords = [
                'and', 'as', 'assert', 'break', 'class', 'continue',
                'def', 'del', 'elif', 'else', 'except', 'False',
                'finally', 'for', 'from', 'global', 'if', 'import',
                'in', 'is', 'lambda', 'None', 'nonlocal', 'not',
                'or', 'pass', 'raise', 'return', 'True', 'try',
                'while', 'with', 'yield', 'async', 'await'
            ]
            for kw in keywords:
                self.rules.append((r'\b' + kw + r'\b', formats['keyword']))
            
            builtins = [
                'print', 'len', 'range', 'str', 'int', 'float', 'list',
                'dict', 'set', 'tuple', 'open', 'input', 'type', 'isinstance',
                'enumerate', 'zip', 'map', 'filter', 'sorted', 'sum', 'min',
                'max', 'abs', 'round', 'all', 'any', 'dir', 'help', 'super'
            ]
            for b in builtins:
                self.rules.append((r'\b' + b + r'\b', formats['builtin']))
            
            self.rules.append((r'\bdef\s+(\w+)', formats['function']))
            self.rules.append((r'\bclass\s+(\w+)', formats['class']))
            self.rules.append((r'#.*', formats['comment']))
            self.rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', formats['string']))
            self.rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", formats['string']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # JavaScript
        elif self.language == 'javascript':
            js_keywords = [
                'function', 'class', 'const', 'let', 'var', 'if', 'else',
                'for', 'while', 'do', 'switch', 'case', 'break', 'continue',
                'return', 'try', 'catch', 'finally', 'throw', 'new', 'this',
                'super', 'extends', 'import', 'export', 'default', 'async',
                'await', 'yield', 'typeof', 'instanceof', 'in', 'of', 'null',
                'undefined', 'true', 'false'
            ]
            for kw in js_keywords:
                self.rules.append((r'\b' + kw + r'\b', formats['keyword']))
            
            self.rules.append((r'\bfunction\s+(\w+)', formats['function']))
            self.rules.append((r'\bclass\s+(\w+)', formats['class']))
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'/\*[\s\S]*?\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'[^']*'", formats['string']))
            self.rules.append((r'`[^`]*`', formats['string']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # Java
        elif self.language == 'java':
            java_keywords = [
                'public', 'private', 'protected', 'static', 'final', 'abstract',
                'class', 'interface', 'extends', 'implements', 'import', 'package',
                'new', 'return', 'if', 'else', 'for', 'while', 'do', 'switch',
                'case', 'break', 'continue', 'try', 'catch', 'finally', 'throw',
                'throws', 'void', 'int', 'double', 'float', 'boolean', 'char',
                'String', 'this', 'super', 'null', 'true', 'false'
            ]
            for kw in java_keywords:
                self.rules.append((r'\b' + kw + r'\b', formats['keyword']))
            
            self.rules.append((r'\bclass\s+(\w+)', formats['class']))
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'/\*[\s\S]*?\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # C++
        elif self.language == 'cpp':
            cpp_keywords = [
                'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
                'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
                'if', 'int', 'long', 'register', 'return', 'short', 'signed',
                'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
                'unsigned', 'void', 'volatile', 'while', 'class', 'private',
                'public', 'protected', 'template', 'new', 'delete', 'using',
                'namespace', 'try', 'catch', 'throw', 'true', 'false', 'nullptr'
            ]
            for kw in cpp_keywords:
                self.rules.append((r'\b' + kw + r'\b', formats['keyword']))
            
            self.rules.append((r'\bclass\s+(\w+)', formats['class']))
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'/\*[\s\S]*?\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # HTML
        elif self.language == 'html':
            self.rules.append((r'</?\w+', formats['tag']))
            self.rules.append((r'\b\w+\s*=', formats['attribute']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'[^']*'", formats['string']))
            self.rules.append((r'<!--.*-->', formats['comment']))
        
        # CSS
        elif self.language == 'css':
            self.rules.append((r'\b[\w-]+\s*:', formats['attribute']))
            self.rules.append((r'/\*[\s\S]*?\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # Bash/Shell
        elif self.language == 'bash':
            bash_keywords = [
                'if', 'then', 'else', 'elif', 'fi', 'case', 'esac', 'for',
                'while', 'until', 'do', 'done', 'function', 'select', 'in'
            ]
            for kw in bash_keywords:
                self.rules.append((r'\b' + kw + r'\b', formats['keyword']))
            
            self.rules.append((r'#.*', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r'\$\w+', formats['variable']))
            self.rules.append((r'\b\d+\b', formats['number']))
    
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

# ==================== GAMER CODE EDITOR ====================

class LRDGamerEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)
        self.highlighter = LRDHighlighter(self.document())
        
        # Setup editor
        self.setup_editor()
        self.setup_signals()
        
        # Initial update
        self.update_line_number_area_width()
        self.highlight_current_line()
    
    def setup_editor(self):
        # Font
        font = QFont("Consolas", 11)
        self.setFont(font)
        self.setTabStopDistance(30)
        
        # Colors
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(LRD_GAMER_THEME['bg_dark']))
        palette.setColor(QPalette.ColorRole.Text, QColor(LRD_GAMER_THEME['primary']))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(LRD_GAMER_THEME['primary']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("black"))
        self.setPalette(palette)
        
        # Cursor
        self.setCursorWidth(2)
    
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
        return 8 + self.fontMetrics().horizontalAdvance('9') * digits
    
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
        painter.fillRect(event.rect(), QColor(LRD_GAMER_THEME['bg_main']))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(LRD_GAMER_THEME['primary']))
                painter.drawText(0, top, self.line_number_area.width() - 3, 
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
            line_color = QColor(LRD_GAMER_THEME['primary'])
            line_color.setAlpha(30)
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

# ==================== ADVANCED TERMINAL ====================

class LRDGamerTerminal(QPlainTextEdit):
    command_executed = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.setup_terminal()
        self.command_history = []
        self.history_index = -1
        self.current_dir = os.getcwd()
        self.compiler_paths = self.detect_compilers()
        self.prompt = ">>> "
        self.current_input = ""
        self.input_position = 0
        
        # Show welcome message
        self.append_welcome()
        
        # Setup custom context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def setup_terminal(self):
        self.setFont(QFont("Consolas", 10))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(LRD_GAMER_THEME['bg_dark']))
        palette.setColor(QPalette.ColorRole.Text, QColor(LRD_GAMER_THEME['primary']))
        self.setPalette(palette)
    
    def detect_compilers(self):
        """Detect available compilers and interpreters"""
        compilers = {}
        
        # Python
        for cmd in ['python3', 'python']:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, check=True)
                compilers['python'] = cmd
                break
            except:
                pass
        
        # Java
        try:
            subprocess.run(['java', '-version'], capture_output=True, check=True)
            compilers['java'] = 'java'
            subprocess.run(['javac', '-version'], capture_output=True, check=True)
            compilers['javac'] = 'javac'
        except:
            pass
        
        # Node.js
        try:
            subprocess.run(['node', '--version'], capture_output=True, check=True)
            compilers['node'] = 'node'
        except:
            pass
        
        # PHP
        try:
            subprocess.run(['php', '--version'], capture_output=True, check=True)
            compilers['php'] = 'php'
        except:
            pass
        
        # GCC/G++
        for cmd in ['gcc', 'g++']:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, check=True)
                compilers[cmd] = cmd
            except:
                pass
        
        return compilers
    
    def append_welcome(self):
        self.appendPlainText("╔══════════════════════════════════════╗")
        self.appendPlainText("║   🎮 LRD GAMER TERMINAL v3.0 🎮      ║")
        self.appendPlainText("║   Matrix: ACTIVE | Systems: ONLINE   ║")
        self.appendPlainText("╚══════════════════════════════════════╝")
        self.appendPlainText(f"📁 Directory: {self.current_dir}")
        self.appendPlainText("💻 Type 'help' for commands or start coding")
        self.appendPlainText("")
        self.appendPlainText(self.prompt, move_cursor=False)
    
    def appendPlainText(self, text, move_cursor=True):
        super().appendPlainText(text)
        if move_cursor:
            self.moveCursor(QTextCursor.MoveOperation.End)
    
    def keyPressEvent(self, event):
        # Handle special keys
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.execute_current_command()
        elif event.key() == Qt.Key.Key_Up:
            self.navigate_history(-1)
        elif event.key() == Qt.Key.Key_Down:
            self.navigate_history(1)
        elif event.key() == Qt.Key.Key_Backspace:
            if len(self.current_input) > 0:
                self.current_input = self.current_input[:self.input_position-1] + self.current_input[self.input_position:]
                self.input_position = max(0, self.input_position - 1)
                self.update_display()
        elif event.key() == Qt.Key.Key_Delete:
            if self.input_position < len(self.current_input):
                self.current_input = self.current_input[:self.input_position] + self.current_input[self.input_position+1:]
                self.update_display()
        elif event.key() == Qt.Key.Key_Left:
            self.input_position = max(0, self.input_position - 1)
            self.update_display()
        elif event.key() == Qt.Key.Key_Right:
            self.input_position = min(len(self.current_input), self.input_position + 1)
            self.update_display()
        elif event.key() == Qt.Key.Key_Home:
            self.input_position = 0
            self.update_display()
        elif event.key() == Qt.Key.Key_End:
            self.input_position = len(self.current_input)
            self.update_display()
        elif event.key() == Qt.Key.Key_C and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.appendPlainText("^C")
            self.appendPlainText("")
            self.appendPlainText(self.prompt, move_cursor=False)
            self.current_input = ""
            self.input_position = 0
        elif event.key() == Qt.Key.Key_L and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.clear()
            self.append_welcome()
        elif event.text() and not event.modifiers():
            # Regular character input
            char = event.text()
            self.current_input = (self.current_input[:self.input_position] + 
                                 char + self.current_input[self.input_position:])
            self.input_position += 1
            self.update_display()
        else:
            super().keyPressEvent(event)
    
    def update_display(self):
        # Get the last block (prompt line)
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
        cursor.removeSelectedText()
        
        # Insert new prompt with current input
        cursor.insertText(f"{self.prompt}{self.current_input}")
        
        # Move cursor to correct position
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        for _ in range(len(self.prompt) + self.input_position):
            cursor.movePosition(QTextCursor.MoveOperation.Right)
        self.setTextCursor(cursor)
    
    def execute_current_command(self):
        command = self.current_input.strip()
        if command:
            # Add to history
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            
            # Execute command
            self.appendPlainText("")  # New line after command
            self.execute_command(command)
            
            # Reset for next command
            self.current_input = ""
            self.input_position = 0
            self.appendPlainText(self.prompt, move_cursor=False)
    
    def navigate_history(self, direction):
        if self.command_history:
            if direction < 0 and self.history_index > 0:  # Up
                self.history_index -= 1
            elif direction > 0 and self.history_index < len(self.command_history) - 1:  # Down
                self.history_index += 1
            elif direction > 0:  # Down at bottom of history
                self.history_index = len(self.command_history)
            
            if self.history_index < len(self.command_history):
                self.current_input = self.command_history[self.history_index]
                self.input_position = len(self.current_input)
                self.update_display()
            else:
                self.current_input = ""
                self.input_position = 0
                self.update_display()
    
    def execute_command(self, command: str):
        if not command.strip():
            return
        
        # Special commands
        if command.lower() == 'help':
            self.show_help()
            return
        
        if command.lower() == 'clear':
            self.clear()
            self.append_welcome()
            return
        
        if command.lower() == 'compilers':
            self.show_compilers()
            return
        
        if command.lower().startswith('cd '):
            self.handle_cd(command)
            return
        
        # Run external command
        self.run_external_command(command)
    
    def handle_cd(self, command: str):
        path = command[3:].strip()
        try:
            if not path:
                return
            
            if path == "..":
                os.chdir("..")
            elif os.path.isdir(path):
                os.chdir(path)
            else:
                # Try relative path
                new_path = os.path.join(self.current_dir, path)
                if os.path.isdir(new_path):
                    os.chdir(new_path)
                else:
                    self.appendPlainText(f"❌ Directory not found: {path}")
                    return
            
            self.current_dir = os.getcwd()
            self.appendPlainText(f"📁 Changed to: {self.current_dir}")
        except Exception as e:
            self.appendPlainText(f"❌ Error: {str(e)}")
    
    def run_external_command(self, command: str):
        try:
            # Run command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.current_dir,
                timeout=30
            )
            
            # Display output
            if result.stdout:
                self.appendPlainText(result.stdout)
            if result.stderr:
                self.appendPlainText(f"⚠️ {result.stderr}")
            
            if result.returncode != 0:
                self.appendPlainText(f"⚠️ Exit code: {result.returncode}")
        
        except subprocess.TimeoutExpired:
            self.appendPlainText("⏰ Command timed out after 30 seconds")
        except Exception as e:
            self.appendPlainText(f"❌ Error: {str(e)}")
    
    def show_help(self):
        help_text = """
╔══════════════════════════════════════╗
║        🎮 TERMINAL COMMANDS 🎮        ║
╠══════════════════════════════════════╣
║ • help              - Show this help ║
║ • clear             - Clear terminal ║
║ • cd [dir]          - Change dir     ║
║ • compilers         - Show compilers ║
║ • ls / dir         - List files      ║
║ • python script.py  - Run Python     ║
║ • node script.js    - Run JavaScript ║
║ • java Main.java    - Run Java       ║
║ • gcc file.c        - Compile C      ║
║ • g++ file.cpp      - Compile C++    ║
║ • php script.php    - Run PHP        ║
╚══════════════════════════════════════╝
        """
        self.appendPlainText(help_text)
    
    def show_compilers(self):
        if not self.compiler_paths:
            self.appendPlainText("❌ No compilers detected")
            return
        
        self.appendPlainText("🔧 Detected Compilers:")
        for lang, cmd in self.compiler_paths.items():
            self.appendPlainText(f"  • {lang}: {cmd}")
    
    def show_context_menu(self, position):
        menu = QMenu(self)
        
        copy_action = QAction("📋 Copy", self)
        copy_action.triggered.connect(self.copy_selected)
        menu.addAction(copy_action)
        
        paste_action = QAction("📥 Paste", self)
        paste_action.triggered.connect(self.paste_text)
        menu.addAction(paste_action)
        
        menu.addSeparator()
        
        clear_action = QAction("🗑️ Clear Terminal", self)
        clear_action.triggered.connect(lambda: [self.clear(), self.append_welcome()])
        menu.addAction(clear_action)
        
        menu.exec(self.mapToGlobal(position))
    
    def copy_selected(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            QApplication.clipboard().setText(cursor.selectedText())
    
    def paste_text(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            self.current_input = (self.current_input[:self.input_position] + 
                                 text + self.current_input[self.input_position:])
            self.input_position += len(text)
            self.update_display()

# ==================== GAMER FILE EXPLORER ====================

class LRDGamerFileExplorer(QTreeView):
    def __init__(self):
        super().__init__()
        self.setup_explorer()
    
    def setup_explorer(self):
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.setModel(self.model)
        
        # Hide unnecessary columns
        for i in range(1, 4):
            self.hideColumn(i)
        
        self.setHeaderHidden(True)
        self.setIconSize(QSize(16, 16))
        
        # Set custom icons for file types
        self.setup_icons()
    
    def setup_icons(self):
        # Use system icons - they're faster and more consistent
        pass
    
    def set_root_path(self, path: str):
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))

# ==================== GAMER MAIN WINDOW ====================

class LRDGamerCodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()
        self.setup_timers()
        
        # Create initial tab
        self.create_new_file()
        
        # Focus on editor
        QTimer.singleShot(100, self.focus_editor)
    
    def setup_window(self):
        self.setWindowTitle("🎮 LRD GAMER CODE EDITOR v3.0 | MATRIX MODE: ACTIVE")
        self.setGeometry(100, 50, 1400, 800)
        
        # Set window icon
        self.set_window_icon()
        
        # Apply stylesheet
        self.setStyleSheet(GAMER_STYLESHEET)
        
        # Set palette for performance
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(LRD_GAMER_THEME['bg_main']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(LRD_GAMER_THEME['primary']))
        palette.setColor(QPalette.ColorRole.Base, QColor(LRD_GAMER_THEME['bg_dark']))
        palette.setColor(QPalette.ColorRole.Text, QColor(LRD_GAMER_THEME['primary']))
        self.setPalette(palette)
    
    def set_window_icon(self):
        # Create a gamer-style icon
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw gamer icon
        painter.setPen(QPen(QColor(LRD_GAMER_THEME['primary']), 3))
        painter.setBrush(QColor(LRD_GAMER_THEME['bg_dark']))
        painter.drawRect(10, 10, 44, 44)
        
        # Draw LRD text
        painter.setPen(QPen(QColor(LRD_GAMER_THEME['primary']), 2))
        painter.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "LRD")
        
        painter.end()
        self.setWindowIcon(QIcon(pixmap))
    
    def setup_variables(self):
        self.open_files = {}
        self.project_path = None
        self.font_size = 11
        self.current_language = 'python'
        self.theme = LRD_GAMER_THEME
    
    def setup_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(3)
        
        # Title bar
        self.create_title_bar(main_layout)
        
        # Main content (sidebar + editor)
        self.create_main_content(main_layout)
        
        # Terminal
        self.create_terminal(main_layout)
        
        # Status bar
        self.create_status_bar()
    
    def create_title_bar(self, parent_layout):
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet(f"""
            background-color: {self.theme['bg_dark']};
            border: 1px solid {self.theme['primary']};
            border-radius: 3px;
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Logo/Icon
        icon_label = QLabel("🎮")
        icon_label.setStyleSheet("font-size: 16px;")
        
        # Title
        title = QLabel("LRD GAMER CODE EDITOR v3.0 | MATRIX MODE: ACTIVE")
        title.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {self.theme['primary']};
            font-family: 'Courier New';
        """)
        
        # Status indicator
        self.status_indicator = QLabel("● ONLINE")
        self.status_indicator.setStyleSheet(f"""
            font-size: 11px;
            font-weight: bold;
            color: {self.theme['status_ready']};
            background-color: {self.theme['bg_light']};
            padding: 3px 8px;
            border-radius: 10px;
            border: 1px solid {self.theme['primary']};
        """)
        
        # Time display
        self.time_display = QLabel()
        self.time_display.setStyleSheet(f"""
            font-size: 12px;
            color: {self.theme['primary']};
            padding: 3px 8px;
            background-color: {self.theme['bg_light']};
            border-radius: 3px;
        """)
        
        # Window controls
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(3)
        
        min_btn = QPushButton("─")
        min_btn.setFixedSize(25, 25)
        min_btn.clicked.connect(self.showMinimized)
        
        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(25, 25)
        self.max_btn.clicked.connect(self.toggle_maximize)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(25, 25)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton:hover {
                background-color: #ff0000;
                color: white;
            }
        """)
        
        controls_layout.addWidget(min_btn)
        controls_layout.addWidget(self.max_btn)
        controls_layout.addWidget(close_btn)
        
        layout.addWidget(icon_label)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status_indicator)
        layout.addSpacing(10)
        layout.addWidget(self.time_display)
        layout.addSpacing(10)
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
        self.main_splitter.setSizes([200, 1200])
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setMinimumWidth(180)
        sidebar.setMaximumWidth(300)
        sidebar.setStyleSheet(f"""
            background-color: {self.theme['bg_light']};
            border: 1px solid {self.theme['primary']};
            border-radius: 3px;
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Explorer header
        explorer_header = QWidget()
        explorer_header.setFixedHeight(35)
        explorer_header.setStyleSheet(f"""
            background-color: {self.theme['bg_dark']};
            border-bottom: 1px solid {self.theme['primary']};
        """)
        
        header_layout = QHBoxLayout(explorer_header)
        header_layout.setContentsMargins(8, 0, 8, 0)
        
        explorer_title = QLabel("📁 EXPLORER")
        explorer_title.setStyleSheet(f"""
            color: {self.theme['primary']};
            font-weight: bold;
            font-size: 11px;
        """)
        
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
        self.file_explorer = LRDGamerFileExplorer()
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
            background-color: {self.theme['bg_dark']};
            border: 1px solid {self.theme['primary']};
            border-bottom: none;
            border-radius: 3px 3px 0 0;
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)
        
        # Action buttons
        actions = [
            ("🆕 NEW", self.create_new_file, "Ctrl+N"),
            ("📂 OPEN", self.open_file_dialog, "Ctrl+O"),
            ("💾 SAVE", self.save_file, "Ctrl+S"),
            ("🚀 RUN", self.run_current_file, "F5"),
            ("🔧 SAVE AS", self.save_as, "Ctrl+Shift+S"),
        ]
        
        for text, callback, shortcut in actions:
            btn = QPushButton(text)
            btn.setMinimumHeight(30)
            btn.setToolTip(f"{shortcut}")
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Language selector
        lang_label = QLabel("LANG:")
        lang_label.setStyleSheet(f"color: {self.theme['primary']};")
        
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "Python", "JavaScript", "HTML", "CSS", 
            "Java", "C++", "C", "PHP", "Bash"
        ])
        self.language_combo.setCurrentText("Python")
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        self.language_combo.setMaximumWidth(120)
        
        layout.addWidget(lang_label)
        layout.addWidget(self.language_combo)
        
        parent_layout.addWidget(toolbar)
    
    def create_terminal(self, parent_layout):
        # Create dock widget
        self.terminal_dock = QDockWidget("💻 GAMER TERMINAL", self)
        self.terminal_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable | 
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        
        # Terminal widget
        self.terminal = LRDGamerTerminal()
        
        # Terminal toolbar
        terminal_toolbar = QWidget()
        terminal_toolbar.setFixedHeight(30)
        terminal_toolbar.setStyleSheet(f"""
            background-color: {self.theme['bg_dark']};
            border: 1px solid {self.theme['primary']};
            border-bottom: none;
        """)
        
        toolbar_layout = QHBoxLayout(terminal_toolbar)
        toolbar_layout.setContentsMargins(5, 0, 5, 0)
        
        clear_btn = QPushButton("🗑️ CLEAR")
        clear_btn.setFixedHeight(22)
        clear_btn.clicked.connect(lambda: [self.terminal.clear(), self.terminal.append_welcome()])
        
        run_btn = QPushButton("▶️ RUN SELECTED")
        run_btn.setFixedHeight(22)
        run_btn.clicked.connect(self.run_selected_code)
        
        toolbar_layout.addWidget(clear_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(run_btn)
        
        # Terminal container
        terminal_container = QWidget()
        terminal_layout = QVBoxLayout(terminal_container)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        terminal_layout.setSpacing(0)
        
        terminal_layout.addWidget(terminal_toolbar)
        terminal_layout.addWidget(self.terminal)
        
        self.terminal_dock.setWidget(terminal_container)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal_dock)
        self.terminal_dock.setVisible(True)
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status label
        self.status_label = QLabel("● READY")
        self.status_label.setStyleSheet(f"""
            color: {self.theme['status_ready']};
            font-weight: bold;
            padding-right: 15px;
        """)
        
        # Cursor position
        self.cursor_label = QLabel("Ln 1, Col 1")
        
        # File info
        self.file_label = QLabel("Untitled")
        
        # Language
        self.language_label = QLabel("Python")
        
        # Line count
        self.line_count_label = QLabel("Lines: 0")
        
        # Add widgets
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.cursor_label)
        self.status_bar.addPermanentWidget(self.file_label)
        self.status_bar.addPermanentWidget(self.language_label)
        self.status_bar.addPermanentWidget(self.line_count_label)
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("🎮 File")
        
        new_action = QAction("🆕 New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.create_new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("📂 Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        open_folder_action = QAction("📁 Open Folder...", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("💾 Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("🔧 Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("⏹️ Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("🎮 Edit")
        
        undo_action = QAction("↩️ Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("↪️ Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("✂️ Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("📋 Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("📥 Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        # View menu
        view_menu = menubar.addMenu("🎮 View")
        
        toggle_sidebar = QAction("📁 Toggle Sidebar", self)
        toggle_sidebar.setShortcut("Ctrl+B")
        toggle_sidebar.triggered.connect(self.toggle_sidebar)
        view_menu.addAction(toggle_sidebar)
        
        toggle_terminal = QAction("💻 Toggle Terminal", self)
        toggle_terminal.setShortcut("Ctrl+`")
        toggle_terminal.triggered.connect(self.toggle_terminal)
        view_menu.addAction(toggle_terminal)
        
        # Run menu
        run_menu = menubar.addMenu("🎮 Run")
        
        run_action = QAction("🚀 Run Code", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_current_file)
        run_menu.addAction(run_action)
        
        # Help menu
        help_menu = menubar.addMenu("🎮 Help")
        
        docs_action = QAction("📖 Documentation", self)
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)
        
        about_action = QAction("👨‍💻 About LRD", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+W"), self, self.close_current_tab)
        QShortcut(QKeySequence("Ctrl+Tab"), self, self.next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, self.previous_tab)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
    
    def setup_timers(self):
        # Clock timer
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()
        
        # Auto-save timer
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.auto_save)
        self.autosave_timer.start(180000)  # 3 minutes
    
    # ==================== EDITOR MANAGEMENT ====================
    
    def create_new_file(self):
        editor = LRDGamerEditor()
        index = self.tab_widget.addTab(editor, "🆕 Untitled")
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
        self.update_status("New file created", "success")
        self.file_label.setText("Untitled")
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
            "All Files (*.*);;"
            "Python Files (*.py);;"
            "JavaScript Files (*.js);;"
            "HTML Files (*.html *.htm);;"
            "CSS Files (*.css);;"
            "Java Files (*.java);;"
            "C++ Files (*.cpp);;"
            "C Files (*.c);;"
            "PHP Files (*.php);;"
            "Bash Files (*.sh)"
        )
        
        if file_path:
            self.open_file(file_path)
    
    def open_file(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create editor
            editor = LRDGamerEditor()
            editor.setPlainText(content)
            
            # Add tab
            filename = os.path.basename(file_path)
            index = self.tab_widget.addTab(editor, filename)
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
            self.update_status(f"Opened: {filename}", "success")
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
                
                self.update_status(f"Saved: {os.path.basename(info['path'])}", "success")
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
            "All Files (*.*);;"
            "Python Files (*.py);;"
            "JavaScript Files (*.js);;"
            "HTML Files (*.html);;"
            "CSS Files (*.css);;"
            "Java Files (*.java);;"
            "C++ Files (*.cpp);;"
            "C Files (*.c);;"
            "PHP Files (*.php);;"
            "Bash Files (*.sh)"
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
                self.tab_widget.setTabText(index, filename)
                self.set_editor_language(editor, info['language'])
                
                # Update status
                self.update_status(f"Saved as: {filename}", "success")
                self.file_label.setText(filename)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
    
    def auto_save(self):
        """Auto-save modified files"""
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
        if isinstance(widget, LRDGamerEditor):
            info = self.open_files.get(widget)
            if info and info['modified']:
                reply = QMessageBox.question(
                    self,
                    "Unsaved Changes",
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
            if isinstance(widget, LRDGamerEditor):
                info = self.open_files.get(widget)
                if info:
                    # Update file label
                    if info['path']:
                        self.file_label.setText(os.path.basename(info['path']))
                    else:
                        self.file_label.setText("Untitled")
                    
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
            filename = os.path.basename(info['path']) if info['path'] else "Untitled"
            if info['modified']:
                self.tab_widget.setTabText(index, f"*{filename}")
            else:
                self.tab_widget.setTabText(index, filename)
    
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
            
            # Update line count
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
    
    def cut(self):
        editor = self.get_current_editor()
        if editor:
            editor.cut()
    
    def copy(self):
        editor = self.get_current_editor()
        if editor:
            editor.copy()
    
    def paste(self):
        editor = self.get_current_editor()
        if editor:
            editor.paste()
    
    # ==================== LANGUAGE & SYNTAX ====================
    
    def detect_language(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.html': 'html',
            '.htm': 'html',
            '.css': 'css',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.php': 'php',
            '.sh': 'bash',
        }
        
        return language_map.get(ext, 'text')
    
    def set_editor_language(self, editor, language):
        if isinstance(editor, LRDGamerEditor):
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
            self.update_status(f"Project: {os.path.basename(folder)}", "success")
    
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
            QMessageBox.warning(self, "Warning", "No file open to run.")
            return
        
        info = self.open_files.get(editor)
        if not info or not info['path']:
            reply = QMessageBox.question(
                self,
                "Save File",
                "File must be saved before running. Save now?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
                info = self.open_files.get(editor)
                if not info or not info['path']:
                    return
            else:
                return
        
        # Clear terminal and show running message
        self.terminal.clear()
        self.terminal.appendPlainText("╔══════════════════════════════════════╗")
        self.terminal.appendPlainText(f"║   🚀 EXECUTING: {os.path.basename(info['path'])}   ║")
        self.terminal.appendPlainText("╚══════════════════════════════════════╝")
        
        # Run based on language
        try:
            if info['language'] == 'python':
                if 'python' in self.terminal.compiler_paths:
                    cmd = f"{self.terminal.compiler_paths['python']} \"{info['path']}\""
                    self.terminal.run_external_command(cmd)
                else:
                    self.terminal.appendPlainText("❌ Python not found")
                    
            elif info['language'] == 'javascript':
                if 'node' in self.terminal.compiler_paths:
                    cmd = f"node \"{info['path']}\""
                    self.terminal.run_external_command(cmd)
                else:
                    self.terminal.appendPlainText("❌ Node.js not found")
                    
            elif info['language'] == 'java':
                # Compile first
                compile_cmd = f"javac \"{info['path']}\""
                self.terminal.run_external_command(compile_cmd)
                
                # Run if compilation successful
                class_name = os.path.splitext(os.path.basename(info['path']))[0]
                run_cmd = f"java -cp \"{os.path.dirname(info['path'])}\" {class_name}"
                self.terminal.run_external_command(run_cmd)
                
            elif info['language'] == 'html':
                webbrowser.open(f'file://{os.path.abspath(info["path"])}')
                self.terminal.appendPlainText("✅ Opened in web browser")
                
            else:
                self.terminal.appendPlainText(f"⚠️ Language {info['language']} execution not fully supported")
                self.terminal.appendPlainText(f"Try running from terminal manually")
            
            self.update_status("Execution completed", "success")
            
        except Exception as e:
            self.terminal.appendPlainText(f"❌ Error: {str(e)}")
            self.update_status("Execution failed", "error")
    
    def run_selected_code(self):
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            if cursor.hasSelection():
                code = cursor.selectedText()
                self.terminal.appendPlainText(f"🎮 Running selected code...")
                self.terminal.appendPlainText("=" * 40)
                
                # Try to execute as Python
                try:
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                        f.write(code)
                        temp_file = f.name
                    
                    if 'python' in self.terminal.compiler_paths:
                        cmd = f"{self.terminal.compiler_paths['python']} \"{temp_file}\""
                        self.terminal.run_external_command(cmd)
                    
                    os.unlink(temp_file)
                except Exception as e:
                    self.terminal.appendPlainText(f"❌ Error: {str(e)}")
            else:
                self.terminal.appendPlainText("⚠️ No code selected")
    
    # ==================== VIEW CONTROLS ====================
    
    def toggle_sidebar(self):
        sidebar = self.main_splitter.widget(0)
        sidebar.setVisible(not sidebar.isVisible())
    
    def toggle_terminal(self):
        self.terminal_dock.setVisible(not self.terminal_dock.isVisible())
    
    # ==================== UTILITIES ====================
    
    def get_current_editor(self):
        widget = self.tab_widget.currentWidget()
        if isinstance(widget, LRDGamerEditor):
            return widget
        return None
    
    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_display.setText(f"🕒 {current_time}")
    
    def update_status(self, message: str, status_type: str = "info"):
        colors = {
            'success': LRD_GAMER_THEME['status_ready'],
            'error': LRD_GAMER_THEME['status_error'],
            'warning': LRD_GAMER_THEME['status_warning'],
            'info': LRD_GAMER_THEME['primary']
        }
        
        color = colors.get(status_type, LRD_GAMER_THEME['primary'])
        self.status_label.setText(f"● {message}")
        self.status_label.setStyleSheet(f"""
            color: {color};
            font-weight: bold;
            padding-right: 15px;
        """)
        self.status_indicator.setText(f"● {message.upper()}")
        self.status_indicator.setStyleSheet(f"""
            font-size: 11px;
            font-weight: bold;
            color: {color};
            background-color: {LRD_GAMER_THEME['bg_light']};
            padding: 3px 8px;
            border-radius: 10px;
            border: 1px solid {color};
        """)
    
    # ==================== HELP & ABOUT ====================
    
    def show_documentation(self):
        doc_text = """
╔══════════════════════════════════════════════════════════╗
║                  LRD GAMER CODE EDITOR                   ║
║                   DOCUMENTATION v3.0                     ║
╚══════════════════════════════════════════════════════════╝

🎮 FEATURES:
• Ultra-fast code editor with Matrix theme
• Multi-language support (Python, JS, Java, C++, etc.)
• Gamer-style terminal with full typing support
• Real-time syntax highlighting
• File explorer with project support
• Code execution with one click (F5)
• Auto-save every 3 minutes
• Customizable interface

⚡ KEYBOARD SHORTCUTS:
• Ctrl+N: New file
• Ctrl+O: Open file
• Ctrl+S: Save file
• Ctrl+Shift+S: Save As
• Ctrl+W: Close tab
• Ctrl+Tab: Next tab
• Ctrl+Shift+Tab: Previous tab
• F5: Run code
• Ctrl+B: Toggle sidebar
• Ctrl+`: Toggle terminal
• Ctrl+Z: Undo
• Ctrl+Y: Redo
• Ctrl+C: Copy
• Ctrl+V: Paste

💻 TERMINAL FEATURES:
• Type directly in terminal
• Command history (Up/Down arrows)
• Auto-completion for files
• Syntax highlighting
• Run code directly from editor

🚀 GETTING STARTED:
1. Create new file (Ctrl+N)
2. Write your code
3. Save file (Ctrl+S)
4. Run code (F5)
5. Use terminal for advanced commands

🔧 SUPPORTED LANGUAGES:
• Python (.py)
• JavaScript (.js)
• HTML/CSS (.html/.css)
• Java (.java)
• C/C++ (.c/.cpp)
• PHP (.php)
• Bash (.sh)
        """
        QMessageBox.information(self, "Documentation", doc_text)
    
    def show_about(self):
        about_text = """
╔══════════════════════════════════════════════════════════╗
║  ██╗     ██████╗ ██████╗     ███████╗ ██████╗ ██████╗   ║
║  ██║     ██╔══██╗██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗  ║
║  ██║     ██████╔╝██║  ██║    █████╗  ██║   ██║██████╔╝  ║
║  ██║     ██╔══██╗██║  ██║    ██╔══╝  ██║   ██║██╔══██╗  ║
║  ███████╗██║  ██║██████╔╝    ██║     ╚██████╔╝██║  ██║  ║
║  ╚══════╝╚═╝  ╚═╝╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝  ║
║                    GAMER CODE EDITOR v3.0                 ║
╚══════════════════════════════════════════════════════════╝

[MATRIX MODE: ACTIVE]
[HACKER PROTOCOL: ENABLED]
[SYSTEMS: ONLINE]

👨‍💻 DEVELOPED BY: LRD_SOUL (Lead Developer)
🏢 COMPANY: LRD-TECH
🌐 WEBSITE: https://lrd-tech.com
📧 EMAIL: inscreator728@gmail.com
🐙 GITHUB: github.com/inscreator728
📱 TELEGRAM: @lrd_soul
📸 INSTAGRAM: @lrd_soul

🎮 SPECIAL THANKS:
• The entire LRD Team
• Our beta testers
• The open-source community

⚡ FEATURES:
• Ultra-fast performance
• Gamer/Hacker theme
• Full terminal integration
• Multi-language support
• Real-time code execution
• Professional tools for gamers

🔐 SECURITY:
• Local execution only
• No data collection
• Open-source transparency

📅 VERSION: 3.0.0 (Gamer Edition)
📅 YEAR: 2024-2025

"Code like a gamer, hack like a pro"
© 2024-2025 LRD-TECH. All rights reserved.
        """
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("About LRD Gamer Code Editor")
        msg_box.setText(about_text)
        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {LRD_GAMER_THEME['bg_dark']};
                color: {LRD_GAMER_THEME['primary']};
                font-family: 'Courier New';
                font-size: 10px;
            }}
            QPushButton {{
                background-color: {LRD_GAMER_THEME['bg_light']};
                color: {LRD_GAMER_THEME['primary']};
                border: 1px solid {LRD_GAMER_THEME['primary']};
                padding: 5px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {LRD_GAMER_THEME['primary']};
                color: black;
            }}
        """)
        msg_box.exec()
    
    def closeEvent(self, event):
        # Check for unsaved changes
        unsaved = any(info['modified'] for info in self.open_files.values())
        
        if unsaved:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Save before exiting?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

# ==================== APPLICATION ====================

def main():
    # High DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    app.setApplicationName("LRD Gamer Code Editor v3.0")
    app.setOrganizationName("LRD-TECH")
    
    # Set application palette for better performance
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(LRD_GAMER_THEME['bg_main']))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(LRD_GAMER_THEME['primary']))
    palette.setColor(QPalette.ColorRole.Base, QColor(LRD_GAMER_THEME['bg_dark']))
    palette.setColor(QPalette.ColorRole.Text, QColor(LRD_GAMER_THEME['primary']))
    app.setPalette(palette)
    
    # Create and show main window
    window = LRDGamerCodeEditor()
    window.show()
    
    # Start application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
