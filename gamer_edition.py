# lrd_code_editor_ultimate_optimized.py
import sys
import os
import subprocess
import re
import webbrowser
from datetime import datetime

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ==================== GAMER THEME CONSTANTS ====================

GAMER_THEME = {
    # Backgrounds (Solid for performance)
    'bg_dark': '#0a0a0a',
    'bg_darker': '#080808',
    'bg_black': '#000000',
    'bg_surface': '#1a0d0d',
    'bg_surface_dark': '#100505',
    
    # Primary Colors (Reddish-Brown/JARVIS Theme)
    'primary': '#ff3300',  # Bright red-orange
    'primary_light': '#ff6633',
    'primary_dark': '#cc2900',
    'primary_glow': '#ff4400',
    
    # Secondary Colors (Hacker Green)
    'secondary': '#00ff00',
    'secondary_light': '#66ff66',
    'secondary_dark': '#00cc00',
    'secondary_glow': '#00ff44',
    
    # Accent Colors
    'accent': '#ff0066',
    'accent_light': '#ff66aa',
    'warning': '#ffaa00',
    'info': '#ff6600',
    'error': '#ff3333',
    
    # Text Colors
    'text_primary': '#ff3300',
    'text_secondary': '#ff6666',
    'text_tertiary': '#ff9966',
    'text_editor': '#00ff00',
    'text_terminal': '#00ff88',
    
    # UI Elements
    'border': '#ff3300',
    'border_light': '#ff6633',
    'border_dark': '#cc2900',
    
    # Selection & Highlight
    'selection': '#331100',
    'selection_light': '#552200',
    'highlight': '#331100',
    
    # Line Numbers
    'line_bg': '#1a0808',
    'line_fg': '#ff3300',
    
    # Status Colors
    'status_ready': '#00ff00',
    'status_modified': '#ffaa00',
    'status_error': '#ff3333',
    'status_warning': '#ffaa00',
    
    # Syntax Highlighting (Hacker Theme)
    'syntax_keyword': '#ff0066',
    'syntax_builtin': '#ff6600',
    'syntax_string': '#ffaa00',
    'syntax_comment': '#666666',
    'syntax_function': '#ff3300',
    'syntax_class': '#ff3399',
    'syntax_number': '#ff9900',
    'syntax_operator': '#ff6666',
    'syntax_tag': '#ff3366',
    'syntax_attribute': '#ff9900',
    'syntax_variable': '#ff6633',
}

# ==================== OPTIMIZED STYLESHEET ====================

GAMER_STYLESHEET = f"""
    /* Main Window - Solid for Performance */
    QMainWindow {{
        background-color: {GAMER_THEME['bg_dark']};
        border: 2px solid {GAMER_THEME['border']};
    }}
    
    /* Menu Bar */
    QMenuBar {{
        background-color: {GAMER_THEME['bg_surface_dark']};
        color: {GAMER_THEME['text_primary']};
        border-bottom: 2px solid {GAMER_THEME['border']};
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 5px 10px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {GAMER_THEME['selection']};
        color: #ffffff;
    }}
    
    /* Menus */
    QMenu {{
        background-color: {GAMER_THEME['bg_surface']};
        color: {GAMER_THEME['text_primary']};
        border: 2px solid {GAMER_THEME['border']};
    }}
    
    QMenu::item {{
        padding: 5px 25px;
    }}
    
    QMenu::item:selected {{
        background-color: {GAMER_THEME['selection']};
        color: #ffffff;
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: {GAMER_THEME['bg_surface_dark']};
        color: {GAMER_THEME['text_secondary']};
        border-top: 1px solid {GAMER_THEME['border']};
    }}
    
    /* Buttons - Gamer Style */
    QPushButton {{
        background-color: {GAMER_THEME['bg_surface']};
        color: {GAMER_THEME['text_primary']};
        border: 2px solid {GAMER_THEME['border']};
        border-radius: 3px;
        padding: 5px 10px;
        font-weight: bold;
        font-family: 'Consolas', monospace;
    }}
    
    QPushButton:hover {{
        background-color: {GAMER_THEME['selection']};
        border: 2px solid {GAMER_THEME['primary_light']};
        color: #ffffff;
    }}
    
    QPushButton:pressed {{
        background-color: {GAMER_THEME['primary_dark']};
        border: 2px solid {GAMER_THEME['primary']};
        color: #ffffff;
    }}
    
    /* ComboBox */
    QComboBox {{
        background-color: {GAMER_THEME['bg_surface']};
        color: {GAMER_THEME['text_primary']};
        border: 2px solid {GAMER_THEME['border']};
        border-radius: 3px;
        padding: 5px;
        font-family: 'Consolas', monospace;
    }}
    
    QComboBox::drop-down {{
        border: none;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {GAMER_THEME['primary']};
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {GAMER_THEME['bg_surface']};
        color: {GAMER_THEME['text_primary']};
        border: 2px solid {GAMER_THEME['border']};
        selection-background-color: {GAMER_THEME['selection']};
        selection-color: #ffffff;
    }}
    
    /* LineEdit */
    QLineEdit {{
        background-color: {GAMER_THEME['bg_darker']};
        color: {GAMER_THEME['text_editor']};
        border: 2px solid {GAMER_THEME['border']};
        border-radius: 3px;
        padding: 5px;
        font-family: 'Consolas', monospace;
        font-size: 12px;
    }}
    
    QLineEdit:focus {{
        border: 2px solid {GAMER_THEME['secondary']};
        background-color: {GAMER_THEME['bg_black']};
    }}
    
    /* Tab Widget */
    QTabWidget::pane {{
        background-color: {GAMER_THEME['bg_dark']};
        border: 2px solid {GAMER_THEME['border']};
    }}
    
    QTabBar::tab {{
        background-color: {GAMER_THEME['bg_surface']};
        color: {GAMER_THEME['text_secondary']};
        padding: 8px 15px;
        border: 1px solid {GAMER_THEME['border']};
        border-bottom: none;
        font-family: 'Consolas', monospace;
        font-weight: bold;
    }}
    
    QTabBar::tab:selected {{
        background-color: {GAMER_THEME['bg_dark']};
        color: {GAMER_THEME['primary']};
        border-top: 2px solid {GAMER_THEME['primary']};
    }}
    
    QTabBar::tab:hover {{
        background-color: {GAMER_THEME['selection_light']};
    }}
    
    /* Dock Widget */
    QDockWidget {{
        border: 2px solid {GAMER_THEME['border']};
    }}
    
    QDockWidget::title {{
        background-color: {GAMER_THEME['bg_surface']};
        color: {GAMER_THEME['primary']};
        padding: 5px 10px;
        font-weight: bold;
        border-bottom: 1px solid {GAMER_THEME['border']};
    }}
    
    /* ScrollBar */
    QScrollBar:vertical {{
        background-color: {GAMER_THEME['bg_surface']};
        width: 12px;
        border-radius: 0px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {GAMER_THEME['primary']};
        border-radius: 0px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {GAMER_THEME['primary_light']};
    }}
    
    QScrollBar:horizontal {{
        background-color: {GAMER_THEME['bg_surface']};
        height: 12px;
        border-radius: 0px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {GAMER_THEME['primary']};
        border-radius: 0px;
        min-width: 20px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {GAMER_THEME['primary_light']};
    }}
    
    /* TreeView (File Explorer) */
    QTreeView {{
        background-color: {GAMER_THEME['bg_dark']};
        color: {GAMER_THEME['text_primary']};
        border: none;
        font-family: 'Consolas', monospace;
        font-size: 11px;
    }}
    
    QTreeView::item {{
        height: 22px;
        padding: 2px;
    }}
    
    QTreeView::item:selected {{
        background-color: {GAMER_THEME['selection']};
        color: #ffffff;
    }}
    
    QTreeView::item:hover {{
        background-color: {GAMER_THEME['highlight']};
    }}
    
    /* Labels */
    QLabel {{
        background-color: transparent;
        font-family: 'Consolas', monospace;
    }}
    
    /* Text Edit */
    QTextEdit {{
        background-color: {GAMER_THEME['bg_darker']};
        color: {GAMER_THEME['text_editor']};
        border: 2px solid {GAMER_THEME['border']};
        font-family: 'Consolas', monospace;
        font-size: 12px;
    }}
    
    /* Checkbox */
    QCheckBox {{
        color: {GAMER_THEME['text_primary']};
        font-family: 'Consolas', monospace;
    }}
    
    QCheckBox::indicator {{
        width: 13px;
        height: 13px;
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {GAMER_THEME['primary']};
        border: 1px solid {GAMER_THEME['primary_light']};
    }}
    
    QCheckBox::indicator:unchecked {{
        background-color: {GAMER_THEME['bg_surface']};
        border: 1px solid {GAMER_THEME['border']};
    }}
"""

# ==================== OPTIMIZED SYNTAX HIGHLIGHTER ====================

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
            'keyword': self.create_format(GAMER_THEME['syntax_keyword'], bold=True),
            'builtin': self.create_format(GAMER_THEME['syntax_builtin']),
            'string': self.create_format(GAMER_THEME['syntax_string']),
            'comment': self.create_format(GAMER_THEME['syntax_comment'], italic=True),
            'function': self.create_format(GAMER_THEME['syntax_function'], bold=True),
            'class': self.create_format(GAMER_THEME['syntax_class'], bold=True),
            'number': self.create_format(GAMER_THEME['syntax_number']),
            'operator': self.create_format(GAMER_THEME['syntax_operator']),
            'tag': self.create_format(GAMER_THEME['syntax_tag'], bold=True),
            'attribute': self.create_format(GAMER_THEME['syntax_attribute']),
            'variable': self.create_format(GAMER_THEME['syntax_variable']),
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
            self.rules.append((r"'.*'", formats['string']))
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
            self.rules.append((r'\binterface\s+(\w+)', formats['class']))
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'/\*[\s\S]*?\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'.'", formats['string']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # PHP
        elif self.language == 'php':
            php_keywords = [
                'echo', 'print', 'if', 'else', 'elseif', 'while', 'do', 'for',
                'foreach', 'break', 'continue', 'switch', 'case', 'default',
                'function', 'return', 'class', 'interface', 'trait', 'namespace',
                'use', 'public', 'private', 'protected', 'static', 'abstract',
                'final', 'const', 'new', 'clone', 'instanceof', 'try', 'catch',
                'finally', 'throw', 'array', 'true', 'false', 'null', 'isset',
                'empty', 'include', 'require', 'include_once', 'require_once'
            ]
            for kw in php_keywords:
                self.rules.append((r'\b' + kw + r'\b', formats['keyword']))
            
            self.rules.append((r'\bfunction\s+(\w+)', formats['function']))
            self.rules.append((r'\bclass\s+(\w+)', formats['class']))
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'#.*', formats['comment']))
            self.rules.append((r'/\*[\s\S]*?\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'[^']*'", formats['string']))
            self.rules.append((r'\$\w+', formats['variable']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # C/C++
        elif self.language in ['c', 'cpp']:
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
            self.rules.append((r'\bstruct\s+(\w+)', formats['class']))
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'/\*[\s\S]*?\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'.'", formats['string']))
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
            self.rules.append((r"'.*'", formats['string']))
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

# ==================== OPTIMIZED CODE EDITOR ====================

class LRDCustomEditor(QPlainTextEdit):
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
        # Font - Monospaced for coding
        font = QFont("Consolas", 12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        self.setTabStopDistance(40)
        
        # Colors
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {GAMER_THEME['bg_darker']};
                color: {GAMER_THEME['text_editor']};
                selection-background-color: {GAMER_THEME['selection']};
                selection-color: #ffffff;
                border: 2px solid {GAMER_THEME['border']};
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 5px;
            }}
        """)
        
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
        painter.fillRect(event.rect(), QColor(GAMER_THEME['line_bg']))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(GAMER_THEME['line_fg']))
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
            line_color = QColor(GAMER_THEME['selection_light'])
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

# ==================== ADVANCED TERMINAL (FULLY TYPEABLE) ====================

class LRDTerminal(QTextEdit):
    command_executed = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.setup_terminal()
        self.command_history = []
        self.history_index = -1
        self.current_dir = os.getcwd()
        self.compiler_paths = self.detect_compilers()
        
        # Show welcome message
        self.append_welcome()
    
    def setup_terminal(self):
        # Make it read-only for output, but we'll handle input separately
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 11))
        
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {GAMER_THEME['bg_black']};
                color: {GAMER_THEME['text_terminal']};
                border: 2px solid {GAMER_THEME['border']};
                font-family: 'Consolas', monospace;
                font-size: 11px;
                padding: 5px;
            }}
        """)
    
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
        
        # Java
        try:
            subprocess.run(['java', '-version'], capture_output=True, check=True)
            compilers['java'] = 'java'
            compilers['javac'] = 'javac'
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
        self.append(f"<span style='color:{GAMER_THEME['primary']}; font-weight:bold'>◢◤ LRD ADVANCED TERMINAL v3.0 ◥◣</span>")
        self.append(f"<span style='color:{GAMER_THEME['secondary']}'>Directory:</span> {self.current_dir}")
        self.append(f"<span style='color:{GAMER_THEME['secondary']}'>Type 'help' for commands</span>")
        
        # Show detected compilers
        if self.compiler_paths:
            self.append(f"<span style='color:{GAMER_THEME['secondary']}'>Compilers:</span> {', '.join(self.compiler_paths.keys())}")
        self.append("")
    
    def execute_command(self, command: str):
        if not command.strip():
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Show command
        self.append(f"<span style='color:{GAMER_THEME['primary']}'>$</span> {command}")
        
        # Special commands
        if command.lower() == 'clear':
            self.clear()
            self.append_welcome()
            return
        
        if command.lower() == 'help':
            self.show_help()
            return
        
        if command.lower().startswith('cd '):
            self.handle_cd(command)
            return
        
        # Run command
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
                    self.append(f"<span style='color:{GAMER_THEME['error']}'>Error: Directory not found</span>")
                    return
            
            self.current_dir = os.getcwd()
            self.append(f"<span style='color:{GAMER_THEME['secondary']}'>Changed to:</span> {self.current_dir}")
        except Exception as e:
            self.append(f"<span style='color:{GAMER_THEME['error']}'>Error: {str(e)}</span>")
    
    def run_external_command(self, command: str):
        try:
            # Run command with timeout
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
                self.append(result.stdout)
            if result.stderr:
                self.append(f"<span style='color:{GAMER_THEME['warning']}'>Error:</span> {result.stderr}")
            
            if result.returncode != 0:
                self.append(f"<span style='color:{GAMER_THEME['warning']}'>Exit code: {result.returncode}</span>")
        
        except subprocess.TimeoutExpired:
            self.append(f"<span style='color:{GAMER_THEME['warning']}'>Command timed out</span>")
        except Exception as e:
            self.append(f"<span style='color:{GAMER_THEME['error']}'>Error: {str(e)}</span>")
        
        # Scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
    
    def show_help(self):
        help_text = f"""
<span style='color:{GAMER_THEME['primary']}'>◢ LRD TERMINAL HELP ◣</span>

<span style='color:{GAMER_THEME['secondary']}'>Basic Commands:</span>
  cd [dir]          - Change directory
  ls / dir         - List files
  clear            - Clear terminal
  help             - Show this help

<span style='color:{GAMER_THEME['secondary']}'>Code Execution:</span>
  python script.py  - Run Python
  node script.js    - Run JavaScript
  php script.php    - Run PHP
  javac Main.java   - Compile Java
  java Main         - Run Java
  gcc program.c     - Compile C
  ./program        - Run executable
"""
        self.append(help_text)
    
    def get_previous_command(self):
        if self.history_index > 0:
            self.history_index -= 1
            return self.command_history[self.history_index]
        return ""
    
    def get_next_command(self):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            return self.command_history[self.history_index]
        return ""
    
    def append(self, text: str):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)
        
        if text.startswith("<") and text.endswith(">"):
            self.insertHtml(text + "<br>")
        else:
            super().append(text)

# ==================== CUSTOM FILE EXPLORER ====================

class LRDFileExplorer(QTreeView):
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
        
        # Set custom icons for better gaming look
        self.setIconSize(QSize(20, 20))
        
        # Apply theme
        self.setStyleSheet(f"""
            QTreeView {{
                background-color: {GAMER_THEME['bg_dark']};
                color: {GAMER_THEME['text_primary']};
                border: 2px solid {GAMER_THEME['border']};
                font-family: 'Consolas', monospace;
                font-size: 11px;
                outline: none;
            }}
            QTreeView::item {{
                height: 24px;
                padding: 2px;
            }}
            QTreeView::item:selected {{
                background-color: {GAMER_THEME['selection']};
                color: #ffffff;
            }}
            QTreeView::item:hover {{
                background-color: {GAMER_THEME['highlight']};
            }}
        """)
    
    def set_root_path(self, path: str):
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))

# ==================== MAIN WINDOW ====================

class LRDCodeEditor(QMainWindow):
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
        QTimer.singleShot(100, self.focus_editor)
    
    def setup_window(self):
        self.setWindowTitle("◢◤ LRD CODE EDITOR - GAMER EDITION ◥◣")
        self.setGeometry(100, 50, 1600, 900)
        
        # Set window icon
        self.set_window_icon()
        
        # Apply theme
        self.setStyleSheet(GAMER_STYLESHEET)
    
    def set_window_icon(self):
        # Try to load tlogo.png from the same directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "tlogo.png")
        
        if os.path.exists(icon_path):
            try:
                self.setWindowIcon(QIcon(icon_path))
                return
            except:
                pass
        
        # Fallback to generated icon
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw LRD gaming logo
        painter.setPen(QPen(QColor(GAMER_THEME['primary']), 3))
        painter.setBrush(QColor(GAMER_THEME['primary']))
        painter.drawRect(10, 10, 44, 44)
        
        painter.setPen(QPen(QColor(GAMER_THEME['secondary']), 2))
        painter.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "LRD")
        
        painter.end()
        self.setWindowIcon(QIcon(pixmap))
    
    def setup_variables(self):
        self.current_file = None
        self.open_files = {}
        self.project_path = None
        self.font_size = 12
        self.current_language = 'python'
        self.theme = GAMER_THEME
    
    def setup_ui(self):
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
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
            QWidget {{
                background-color: {self.theme['bg_surface_dark']};
                border-bottom: 3px solid {self.theme['border']};
            }}
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Logo
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "tlogo.png")
            if os.path.exists(icon_path):
                logo_label = QLabel()
                pixmap = QPixmap(icon_path).scaled(30, 30, 
                                                   Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(pixmap)
                layout.addWidget(logo_label)
        except:
            pass
        
        # Title
        title = QLabel("◢◤ LRD CODE EDITOR - GAMER EDITION ◥◣")
        title.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {self.theme['primary']};
            font-family: 'Consolas', monospace;
        """)
        
        layout.addWidget(title)
        layout.addStretch()
        
        # Status indicator
        self.status_indicator = QLabel("● READY")
        self.status_indicator.setStyleSheet(f"""
            font-size: 11px;
            font-weight: bold;
            color: {self.theme['status_ready']};
            background: {self.theme['bg_surface']};
            padding: 3px 8px;
            border: 1px solid {self.theme['border']};
            font-family: 'Consolas', monospace;
        """)
        
        # Time display
        self.time_display = QLabel("")
        self.time_display.setStyleSheet(f"""
            font-size: 12px;
            color: {self.theme['text_secondary']};
            background: {self.theme['bg_surface']};
            padding: 3px 8px;
            border: 1px solid {self.theme['border']};
            font-family: 'Consolas', monospace;
        """)
        
        layout.addWidget(self.status_indicator)
        layout.addSpacing(10)
        layout.addWidget(self.time_display)
        
        parent_layout.addWidget(title_bar)
    
    def create_main_content(self, parent_layout):
        # Create splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setStyleSheet("QSplitter::handle { background-color: #333333; }")
        
        # Sidebar
        self.create_sidebar()
        
        # Editor area
        self.create_editor_area()
        
        parent_layout.addWidget(self.main_splitter, 1)
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setMinimumWidth(250)
        sidebar.setMaximumWidth(350)
        sidebar.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg_dark']};
                border-right: 2px solid {self.theme['border']};
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
                background-color: {self.theme['bg_surface_dark']};
                border-bottom: 2px solid {self.theme['border']};
            }}
        """)
        
        header_layout = QHBoxLayout(explorer_header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        explorer_title = QLabel("◢ EXPLORER ◣")
        explorer_title.setStyleSheet(f"""
            color: {self.theme['primary']};
            font-weight: bold;
            font-size: 12px;
            font-family: 'Consolas', monospace;
        """)
        
        # Buttons
        open_btn = self.create_sidebar_button("📁", "Open Folder")
        open_btn.clicked.connect(self.open_folder)
        
        refresh_btn = self.create_sidebar_button("🔄", "Refresh")
        refresh_btn.clicked.connect(self.refresh_explorer)
        
        header_layout.addWidget(explorer_title)
        header_layout.addStretch()
        header_layout.addWidget(open_btn)
        header_layout.addWidget(refresh_btn)
        
        # File explorer
        self.file_explorer = LRDFileExplorer()
        self.file_explorer.doubleClicked.connect(self.on_file_double_clicked)
        
        layout.addWidget(explorer_header)
        layout.addWidget(self.file_explorer)
        
        self.main_splitter.addWidget(sidebar)
    
    def create_sidebar_button(self, text, tooltip):
        btn = QPushButton(text)
        btn.setFixedSize(28, 28)
        btn.setToolTip(tooltip)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['bg_surface']};
                color: {self.theme['text_primary']};
                border: 1px solid {self.theme['border']};
                font-size: 12px;
                font-family: 'Consolas', monospace;
            }}
            QPushButton:hover {{
                background-color: {self.theme['selection']};
                border: 1px solid {self.theme['primary_light']};
            }}
        """)
        return btn
    
    def create_editor_area(self):
        editor_area = QWidget()
        editor_area.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg_dark']};
            }}
        """)
        
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
        self.main_splitter.setSizes([250, 1350])
    
    def create_editor_toolbar(self, parent_layout):
        toolbar = QWidget()
        toolbar.setFixedHeight(45)
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg_surface_dark']};
                border-bottom: 2px solid {self.theme['border']};
            }}
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Action buttons
        actions = [
            ("◢ NEW", self.create_new_file, "Ctrl+N"),
            ("◢ OPEN", self.open_file_dialog, "Ctrl+O"),
            ("◢ SAVE", self.save_file, "Ctrl+S"),
            ("◢ RUN", self.run_current_file, "F5"),
        ]
        
        for text, callback, shortcut in actions:
            btn = self.create_toolbar_button(text, shortcut)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Language selector
        lang_label = QLabel("LANG:")
        lang_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Consolas', monospace;")
        
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
    
    def create_toolbar_button(self, text, shortcut):
        btn = QPushButton(f"{text}")
        btn.setMinimumHeight(32)
        btn.setToolTip(shortcut)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['bg_surface']};
                color: {self.theme['text_primary']};
                border: 2px solid {self.theme['border']};
                padding: 5px 12px;
                font-weight: bold;
                min-width: 70px;
                font-family: 'Consolas', monospace;
            }}
            QPushButton:hover {{
                background-color: {self.theme['selection']};
                border: 2px solid {self.theme['primary_light']};
            }}
        """)
        return btn
    
    def create_terminal(self, parent_layout):
        # Terminal widget
        self.terminal = LRDTerminal()
        
        # Terminal input (FULLY TYPEABLE)
        terminal_input = QWidget()
        terminal_input.setFixedHeight(40)
        terminal_input.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg_surface_dark']};
                border-top: 2px solid {self.theme['border']};
            }}
        """)
        
        layout = QHBoxLayout(terminal_input)
        layout.setContentsMargins(10, 0, 10, 0)
        
        prompt = QLabel("$")
        prompt.setStyleSheet(f"""
            color: {self.theme['primary']};
            font-weight: bold;
            font-size: 14px;
            font-family: 'Consolas', monospace;
        """)
        prompt.setFixedWidth(20)
        
        self.terminal_input = QLineEdit()
        self.terminal_input.setPlaceholderText("Type command and press Enter (Up/Down for history)...")
        self.terminal_input.returnPressed.connect(self.execute_terminal_command)
        
        # Connect key events for history navigation
        self.terminal_input.keyPressEvent = self.terminal_keyPressEvent
        
        layout.addWidget(prompt)
        layout.addWidget(self.terminal_input, 1)
        
        # Terminal container
        terminal_container = QWidget()
        terminal_container.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg_dark']};
            }}
        """)
        
        terminal_layout = QVBoxLayout(terminal_container)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        terminal_layout.setSpacing(0)
        
        terminal_layout.addWidget(self.terminal, 1)
        terminal_layout.addWidget(terminal_input)
        
        # Create dock widget
        self.terminal_dock = QDockWidget("◢ TERMINAL ◣", self)
        self.terminal_dock.setWidget(terminal_container)
        self.terminal_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable | 
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal_dock)
        self.terminal_dock.setVisible(True)
    
    def terminal_keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            history_cmd = self.terminal.get_previous_command()
            if history_cmd:
                self.terminal_input.setText(history_cmd)
        elif event.key() == Qt.Key.Key_Down:
            history_cmd = self.terminal.get_next_command()
            self.terminal_input.setText(history_cmd)
        else:
            # Call parent class method for normal key handling
            super(QLineEdit, self.terminal_input).keyPressEvent(event)
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status label
        self.status_label = QLabel("● READY")
        self.status_label.setStyleSheet(f"""
            color: {self.theme['status_ready']};
            font-weight: bold;
            padding-right: 20px;
            font-family: 'Consolas', monospace;
        """)
        
        # Cursor position
        self.cursor_label = QLabel("Ln 1, Col 1")
        self.cursor_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Consolas', monospace;")
        
        # File info
        self.file_label = QLabel("Untitled")
        self.file_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Consolas', monospace;")
        
        # Language
        self.language_label = QLabel("Python")
        self.language_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Consolas', monospace;")
        
        # Line count
        self.line_count_label = QLabel("Lines: 0")
        self.line_count_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Consolas', monospace;")
        
        # Add widgets
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.cursor_label)
        self.status_bar.addPermanentWidget(self.file_label)
        self.status_bar.addPermanentWidget(self.language_label)
        self.status_bar.addPermanentWidget(self.line_count_label)
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("◢ File")
        
        new_action = QAction("◢ New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.create_new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("◢ Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        open_folder_action = QAction("◢ Open Folder...", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("◢ Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("◢ Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("◢ Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("◢ Edit")
        
        undo_action = QAction("◢ Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("◢ Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("◢ Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("◢ Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("◢ Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        # Run menu
        run_menu = menubar.addMenu("◢ Run")
        
        run_action = QAction("◢ Run", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_current_file)
        run_menu.addAction(run_action)
        
        # Help menu
        help_menu = menubar.addMenu("◢ Help")
        
        docs_action = QAction("◢ Documentation", self)
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)
        
        about_action = QAction("◢ About LRD", self)
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
    
    # ==================== EDITOR MANAGEMENT ====================
    
    def create_new_file(self):
        editor = LRDCustomEditor()
        index = self.tab_widget.addTab(editor, "Untitled")
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
        self.update_status("New file created", "ready")
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
            editor = LRDCustomEditor()
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
                self.update_status(f"Saved as: {filename}", "ready")
                self.file_label.setText(filename)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
    
    def close_tab(self, index):
        widget = self.tab_widget.widget(index)
        if isinstance(widget, LRDCustomEditor):
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
            if isinstance(widget, LRDCustomEditor):
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
        if isinstance(editor, LRDCustomEditor):
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
    
    # ==================== TERMINAL ====================
    
    def execute_terminal_command(self):
        command = self.terminal_input.text().strip()
        if command:
            self.terminal.execute_command(command)
            self.terminal_input.clear()
    
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
        self.terminal.append(f"<span style='color:{GAMER_THEME['primary']}'>◢ Running {info['language']} file: {os.path.basename(info['path'])} ◣</span>")
        
        # Run based on language
        try:
            if info['language'] == 'python':
                cmd = self.terminal.compiler_paths.get('python', 'python')
                self.terminal.run_external_command(f'{cmd} "{info["path"]}"')
                
            elif info['language'] == 'javascript':
                if 'node' in self.terminal.compiler_paths:
                    self.terminal.run_external_command(f'node "{info["path"]}"')
                else:
                    self.terminal.append(f"<span style='color:{GAMER_THEME['error']}'>Error: Node.js not found</span>")
                    
            elif info['language'] == 'java':
                # Compile and run Java
                compile_cmd = f'javac "{info["path"]}"'
                self.terminal.run_external_command(compile_cmd)
                class_name = os.path.splitext(os.path.basename(info['path']))[0]
                run_cmd = f'java -cp "{os.path.dirname(info["path"])}" {class_name}'
                self.terminal.run_external_command(run_cmd)
                
            elif info['language'] == 'c':
                # Compile C
                output_name = os.path.splitext(info['path'])[0]
                compile_cmd = f'gcc "{info["path"]}" -o "{output_name}"'
                self.terminal.run_external_command(compile_cmd)
                run_cmd = f'"{output_name}"'
                self.terminal.run_external_command(run_cmd)
                
            elif info['language'] == 'cpp':
                # Compile C++
                output_name = os.path.splitext(info['path'])[0]
                compile_cmd = f'g++ "{info["path"]}" -o "{output_name}"'
                self.terminal.run_external_command(compile_cmd)
                run_cmd = f'"{output_name}"'
                self.terminal.run_external_command(run_cmd)
                
            elif info['language'] == 'php':
                if 'php' in self.terminal.compiler_paths:
                    self.terminal.run_external_command(f'php "{info["path"]}"')
                else:
                    self.terminal.append(f"<span style='color:{GAMER_THEME['error']}'>Error: PHP not found</span>")
                    
            elif info['language'] == 'html':
                webbrowser.open(f'file://{os.path.abspath(info["path"])}')
                self.terminal.append(f"<span style='color:{GAMER_THEME['secondary']}'>◢ Opened in browser ◣</span>")
                return
                
            elif info['language'] == 'bash':
                self.terminal.run_external_command(f'bash "{info["path"]}"')
                
            else:
                self.terminal.append(f"<span style='color:{GAMER_THEME['warning']}'>Language not supported</span>")
                return
            
            self.terminal.append(f"<span style='color:{GAMER_THEME['secondary']}'>◢ Execution completed ◣</span>")
            self.update_status("Execution completed", "ready")
            
        except Exception as e:
            self.terminal.append(f"<span style='color:{GAMER_THEME['error']}'>◢ Error: {str(e)} ◣</span>")
            self.update_status("Execution failed", "error")
    
    # ==================== UTILITIES ====================
    
    def get_current_editor(self):
        widget = self.tab_widget.currentWidget()
        if isinstance(widget, LRDCustomEditor):
            return widget
        return None
    
    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_display.setText(current_time)
    
    def update_status(self, message: str, status_type: str = "ready"):
        colors = {
            'ready': GAMER_THEME['status_ready'],
            'error': GAMER_THEME['status_error'],
            'warning': GAMER_THEME['status_warning'],
            'modified': GAMER_THEME['status_modified']
        }
        
        color = colors.get(status_type, GAMER_THEME['status_ready'])
        self.status_label.setText(f"● {message}")
        self.status_label.setStyleSheet(f"""
            color: {color};
            font-weight: bold;
            padding-right: 20px;
            font-family: 'Consolas', monospace;
        """)
        self.status_indicator.setText(f"● {message}")
        self.status_indicator.setStyleSheet(f"""
            font-size: 11px;
            font-weight: bold;
            color: {color};
            background: {GAMER_THEME['bg_surface']};
            padding: 3px 8px;
            border: 1px solid {color};
            font-family: 'Consolas', monospace;
        """)
    
    # ==================== HELP & ABOUT ====================
    
    def show_documentation(self):
        QMessageBox.information(
            self,
            "Documentation",
            """◢◤ LRD CODE EDITOR - GAMER EDITION ◥◣

◢ Features:
• High-performance code editor
• Multi-language support
• Integrated terminal
• File explorer
• Syntax highlighting
• Code execution

◢ Supported Languages:
• Python, JavaScript, HTML, CSS
• Java, C++, C, PHP, Bash

◢ Keyboard Shortcuts:
• Ctrl+N: New file
• Ctrl+O: Open file
• Ctrl+S: Save file
• Ctrl+W: Close tab
• Ctrl+Tab: Next tab
• F5: Run code
• Ctrl+Z: Undo
• Ctrl+Y: Redo

◢ Getting Started:
1. Create new file (Ctrl+N)
2. Write your code
3. Save file (Ctrl+S)
4. Run code (F5)
5. Use terminal for commands
            """
        )
    
    def show_about(self):
        # Create hacker-themed about dialog
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("◢◤ ABOUT LRD ◥◣")
        about_dialog.setFixedSize(600, 500)
        about_dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {GAMER_THEME['bg_black']};
                border: 3px solid {GAMER_THEME['primary']};
            }}
        """)
        
        layout = QVBoxLayout(about_dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("◢◤ LRD TEAM - GAMER EDITION ◥◣")
        title.setStyleSheet(f"""
            color: {GAMER_THEME['primary']};
            font-size: 20px;
            font-weight: bold;
            font-family: 'Consolas', monospace;
            text-align: center;
            padding: 10px;
            border-bottom: 2px solid {GAMER_THEME['secondary']};
        """)
        
        # Logo
        logo_label = QLabel()
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "tlogo.png")
            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path).scaled(100, 100, 
                                                   Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(pixmap)
                logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        except:
            pass
        
        # Hacker-themed text
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {GAMER_THEME['bg_black']};
                color: {GAMER_THEME['secondary']};
                border: 2px solid {GAMER_THEME['primary']};
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }}
        """)
        
        hacker_text = f"""
<span style='color:{GAMER_THEME['primary']}; font-size: 14px;'>◢◤ SYSTEM INITIALIZED ◥◣</span><br><br>

<span style='color:{GAMER_THEME['secondary']}'>[+] LRD DEVELOPMENT TEAM</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Founder & Lead Developer: LRD_SOUL</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • UI/UX Designer: LRD_DESIGN</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Security Expert: LRD_SEC</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Backend Developer: LRD_BACK</span><br><br>

<span style='color:{GAMER_THEME['secondary']}'>[+] CONTACT INFORMATION</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Email: inscreator728@gmail.com</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • GitHub: github.com/inscreator728</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Telegram: @lrd_soul</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Instagram: @lrd_soul</span><br><br>

<span style='color:{GAMER_THEME['secondary']}'>[+] COMPANY DETAILS</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Organization: LRD-TECH</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Founded: 2024</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Specialization: Gaming Tools & Development</span><br><br>

<span style='color:{GAMER_THEME['secondary']}'>[+] SOFTWARE SPECS</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Version: Gamer Edition 3.0</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Build: 2024.12.01</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Theme: JARVIS Red-Black</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   • Performance: Optimized</span><br><br>

<span style='color:{GAMER_THEME['secondary']}'>[+] MISSION STATEMENT</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   Creating professional gaming tools with</span><br>
<span style='color:{GAMER_THEME['text_editor']}'>   superior performance and hacker aesthetics.</span><br><br>

<span style='color:{GAMER_THEME['primary']}'>◢◤ ACCESS GRANTED - WELCOME TO LRD ◥◣</span>
"""
        
        about_text.setHtml(hacker_text)
        
        # Close button
        close_btn = QPushButton("CLOSE SYSTEM")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {GAMER_THEME['bg_surface']};
                color: {GAMER_THEME['primary']};
                border: 2px solid {GAMER_THEME['border']};
                padding: 10px;
                font-weight: bold;
                font-family: 'Consolas', monospace;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {GAMER_THEME['selection']};
                border: 2px solid {GAMER_THEME['primary_light']};
                color: #ffffff;
            }}
        """)
        close_btn.clicked.connect(about_dialog.close)
        
        layout.addWidget(title)
        layout.addWidget(logo_label)
        layout.addWidget(about_text, 1)
        layout.addWidget(close_btn)
        
        about_dialog.exec()
    
    def closeEvent(self, event):
        # Check for unsaved changes
        unsaved = any(info.get('modified', False) for info in self.open_files.values())
        
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
                for editor, info in self.open_files.items():
                    if info['modified'] and info['path']:
                        try:
                            with open(info['path'], 'w', encoding='utf-8') as f:
                                f.write(editor.toPlainText())
                        except:
                            pass
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

# ==================== APPLICATION ====================

def main():
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    
    # Set application style and info
    app.setStyle("Fusion")
    app.setApplicationName("LRD Code Editor - Gamer Edition")
    app.setOrganizationName("LRD-TECH")
    
    # Set application icon
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "tlogo.png")
    
    if os.path.exists(icon_path):
        try:
            app.setWindowIcon(QIcon(icon_path))
        except:
            pass
    
    # Create and show main window
    window = LRDCodeEditor()
    window.show()
    
    # Start application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
