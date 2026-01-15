# lrd_code_editor_pro.py
import sys
import os
import subprocess
import json
import re
import threading
import time
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ==================== CONSTANTS & THEME ====================

LRD_THEME = {
    # Dark Theme Colors
    'background': '#0a0a0a',
    'surface': '#1a0d0d',
    'surface_light': '#2d1a1a',
    'surface_lighter': '#3a2626',
    
    # Primary Colors
    'primary': '#ff3333',
    'primary_light': '#ff6666',
    'primary_dark': '#cc0000',
    
    # Secondary Colors
    'secondary': '#00ff88',
    'secondary_light': '#66ffaa',
    'secondary_dark': '#00cc66',
    
    # Accent Colors
    'accent': '#ff0066',
    'accent_light': '#ff66aa',
    'warning': '#ffaa00',
    'warning_light': '#ffcc66',
    
    # Text Colors
    'text_primary': '#ff3333',
    'text_secondary': '#ff6666',
    'text_tertiary': '#ff9999',
    'text_disabled': '#666666',
    
    # Editor Colors
    'editor_bg': '#0d0d0d',
    'editor_fg': '#00ff88',
    'editor_cursor': '#ff0066',
    'editor_selection': '#4d1a1a',
    
    # Line Numbers
    'line_bg': '#1a0808',
    'line_fg': '#ff4444',
    
    # Terminal Colors
    'terminal_bg': '#0a0a0a',
    'terminal_fg': '#00ff88',
    'terminal_prompt': '#ff3333',
    
    # Status Colors
    'status_ready': '#00ff88',
    'status_modified': '#ffaa00',
    'status_error': '#ff3333',
    'status_info': '#ff6666',
    
    # Syntax Highlighting
    'syntax_keyword': '#ff3366',
    'syntax_builtin': '#ff6633',
    'syntax_string': '#ffaa00',
    'syntax_comment': '#666666',
    'syntax_function': '#ff0066',
    'syntax_class': '#ff3399',
    'syntax_number': '#ff9900',
    'syntax_operator': '#ff6666',
    'syntax_tag': '#ff3366',
    'syntax_attribute': '#ff9900',
    'syntax_variable': '#ff6633',
}

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
        # Create text formats
        formats = {
            'keyword': self.create_format(LRD_THEME['syntax_keyword'], bold=True),
            'builtin': self.create_format(LRD_THEME['syntax_builtin']),
            'string': self.create_format(LRD_THEME['syntax_string']),
            'comment': self.create_format(LRD_THEME['syntax_comment'], italic=True),
            'function': self.create_format(LRD_THEME['syntax_function'], bold=True),
            'class': self.create_format(LRD_THEME['syntax_class'], bold=True),
            'number': self.create_format(LRD_THEME['syntax_number']),
            'operator': self.create_format(LRD_THEME['syntax_operator']),
            'tag': self.create_format(LRD_THEME['syntax_tag'], bold=True),
            'attribute': self.create_format(LRD_THEME['syntax_attribute']),
            'variable': self.create_format(LRD_THEME['syntax_variable']),
        }
        
        # Python rules
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
            
            # Function definitions
            self.rules.append((r'\bdef\s+(\w+)', formats['function']))
            
            # Class definitions
            self.rules.append((r'\bclass\s+(\w+)', formats['class']))
            
            # Comments
            self.rules.append((r'#.*', formats['comment']))
            
            # Strings
            self.rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', formats['string']))
            self.rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", formats['string']))
            
            # Numbers
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # HTML rules
        elif self.language == 'html':
            self.rules.append((r'</?\w+', formats['tag']))
            self.rules.append((r'\b\w+\s*=', formats['attribute']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r'<!--.*-->', formats['comment']))
        
        # CSS rules
        elif self.language == 'css':
            self.rules.append((r'\b[\w-]+\s*:', formats['attribute']))
            self.rules.append((r'/\*.*\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # JavaScript rules
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
            
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'/\*[\s\S]*?\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'[^']*'", formats['string']))
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

# ==================== CODE EDITOR ====================

class LRDCodeEditor(QPlainTextEdit):
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
        font = QFont("Consolas", 12)
        self.setFont(font)
        self.setTabStopDistance(40)
        
        # Colors
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {LRD_THEME['editor_bg']};
                color: {LRD_THEME['editor_fg']};
                selection-background-color: {LRD_THEME['editor_selection']};
                selection-color: #ffffff;
                border: none;
                padding: 10px;
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
        painter.fillRect(event.rect(), QColor(LRD_THEME['line_bg']))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(LRD_THEME['line_fg']))
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
            line_color = QColor(LRD_THEME['surface_light'])
            line_color.setAlpha(50)
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

# ==================== TERMINAL ====================

class LRDTerminal(QTextEdit):
    command_executed = pyqtSignal(str, str)  # command, output
    
    def __init__(self):
        super().__init__()
        self.setup_terminal()
        self.command_history = []
        self.history_index = -1
        self.current_dir = os.getcwd()
        
        # Show welcome message
        self.append_welcome()
    
    def setup_terminal(self):
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 10))
        
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {LRD_THEME['terminal_bg']};
                color: {LRD_THEME['terminal_fg']};
                border: none;
                padding: 10px;
            }}
        """)
    
    def append_welcome(self):
        self.append(f"◢◤ LRD TERMINAL ◥◣")
        self.append(f"Directory: {self.current_dir}")
        self.append("Type 'help' for available commands\n")
    
    def execute_command(self, command: str):
        if not command.strip():
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Show command
        self.append(f"<span style='color:{LRD_THEME['terminal_prompt']}'>$</span> {command}")
        
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
        
        # Run external command
        self.run_external_command(command)
    
    def handle_cd(self, command: str):
        path = command[3:].strip()
        try:
            if not path:
                return
            
            if path == "..":
                os.chdir("..")
            else:
                if os.path.isdir(path):
                    os.chdir(path)
                else:
                    # Try relative path
                    new_path = os.path.join(self.current_dir, path)
                    if os.path.isdir(new_path):
                        os.chdir(new_path)
                    else:
                        self.append(f"<span style='color:{LRD_THEME['status_error']}'>Error: Directory not found: {path}</span>")
                        return
            
            self.current_dir = os.getcwd()
            self.append(f"Changed directory to: {self.current_dir}")
        except Exception as e:
            self.append(f"<span style='color:{LRD_THEME['status_error']}'>Error: {str(e)}</span>")
    
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
                self.append(result.stdout)
            if result.stderr:
                self.append(f"<span style='color:{LRD_THEME['status_error']}'>Error: {result.stderr}</span>")
            
            if result.returncode != 0:
                self.append(f"<span style='color:{LRD_THEME['status_warning']}'>Process exited with code: {result.returncode}</span>")
        
        except subprocess.TimeoutExpired:
            self.append(f"<span style='color:{LRD_THEME['status_warning']}'>Command timed out after 30 seconds</span>")
        except Exception as e:
            self.append(f"<span style='color:{LRD_THEME['status_error']}'>Error: {str(e)}</span>")
        
        # Scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
    
    def show_help(self):
        help_text = """
<strong>Available Commands:</strong>
  • cd [dir]          - Change directory
  • ls / dir         - List files
  • python [file]    - Run Python script
  • node [file]      - Run JavaScript
  • clear            - Clear terminal
  • help             - Show this help

<strong>Examples:</strong>
  $ python script.py
  $ ls -la
  $ cd ..
  $ clear
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
        # Use HTML for colored text
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)
        
        # Check if text already has HTML
        if text.startswith("<") and text.endswith(">"):
            self.insertHtml(text + "<br>")
        else:
            super().append(text)

# ==================== FILE EXPLORER ====================

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
        self.setStyleSheet(f"""
            QTreeView {{
                background-color: {LRD_THEME['surface']};
                color: {LRD_THEME['text_primary']};
                border: none;
                outline: none;
            }}
            QTreeView::item {{
                height: 24px;
                padding: 2px;
            }}
            QTreeView::item:selected {{
                background-color: {LRD_THEME['editor_selection']};
                color: white;
            }}
            QTreeView::item:hover {{
                background-color: {LRD_THEME['surface_light']};
            }}
        """)
        
        # Set icon size
        self.setIconSize(QSize(16, 16))
    
    def set_root_path(self, path: str):
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))

# ==================== MAIN WINDOW ====================

class LRDCodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()
        self.apply_styles()
        
        # Setup timers
        self.setup_timers()
        
        # Create initial tab
        self.create_new_file()
    
    def setup_window(self):
        self.setWindowTitle("◢◤ LRD CODE EDITOR - PROFESSIONAL EDITION ◥◣")
        self.setGeometry(100, 50, 1600, 900)
        
        # Set window icon
        self.setWindowIcon(self.create_icon())
    
    def create_icon(self):
        # Create a simple icon if file doesn't exist
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(LRD_THEME['primary']))
        painter = QPainter(pixmap)
        painter.setPen(QColor(LRD_THEME['secondary']))
        painter.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "◢◤")
        painter.end()
        return QIcon(pixmap)
    
    def setup_variables(self):
        self.current_file = None
        self.open_files = {}  # editor -> file_info
        self.project_path = None
        self.font_size = 12
        self.current_language = 'python'
        self.theme = LRD_THEME
    
    def setup_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top bar
        self.create_top_bar(main_layout)
        
        # Main content (sidebar + editor)
        self.create_main_content(main_layout)
        
        # Terminal
        self.create_terminal(main_layout)
        
        # Status bar
        self.create_status_bar()
    
    def create_top_bar(self, parent_layout):
        top_bar = QWidget()
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet(f"background-color: {self.theme['surface']};")
        
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Logo/Title
        title = QLabel("◢◤ LRD CODE EDITOR ◥◣")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {self.theme['primary']};
            background: transparent;
        """)
        
        # Status indicator
        self.status_indicator = QLabel("● READY")
        self.status_indicator.setStyleSheet(f"""
            font-size: 12px;
            font-weight: bold;
            color: {self.theme['status_ready']};
            background: transparent;
            padding: 5px 10px;
            border-radius: 10px;
            border: 1px solid {self.theme['primary']};
        """)
        
        # Time display
        self.time_display = QLabel("00:00:00")
        self.time_display.setStyleSheet(f"""
            font-size: 14px;
            color: {self.theme['text_secondary']};
            background: transparent;
        """)
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status_indicator)
        layout.addSpacing(20)
        layout.addWidget(self.time_display)
        
        parent_layout.addWidget(top_bar)
    
    def create_main_content(self, parent_layout):
        # Create splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar
        self.create_sidebar()
        
        # Editor area
        self.create_editor_area()
        
        parent_layout.addWidget(self.main_splitter, 1)
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setMinimumWidth(250)
        sidebar.setMaximumWidth(400)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Explorer header
        explorer_header = QWidget()
        explorer_header.setFixedHeight(40)
        explorer_header.setStyleSheet(f"background-color: {self.theme['surface_light']};")
        
        header_layout = QHBoxLayout(explorer_header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        explorer_title = QLabel("◢ EXPLORER ◣")
        explorer_title.setStyleSheet(f"""
            color: {self.theme['primary']};
            font-weight: bold;
            font-size: 12px;
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
        btn.setFixedSize(30, 30)
        btn.setToolTip(tooltip)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['surface_lighter']};
                color: {self.theme['text_primary']};
                border: 1px solid {self.theme['primary']};
                border-radius: 3px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['primary']};
                color: white;
            }}
        """)
        return btn
    
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
        
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {self.theme['background']};
            }}
            QTabBar::tab {{
                background-color: {self.theme['surface']};
                color: {self.theme['text_secondary']};
                padding: 8px 15px;
                margin-right: 2px;
                border: 1px solid {self.theme['surface_light']};
                border-bottom: none;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background-color: {self.theme['background']};
                color: {self.theme['primary']};
            }}
            QTabBar::tab:hover {{
                background-color: {self.theme['surface_light']};
            }}
        """)
        
        layout.addWidget(self.tab_widget)
        
        self.main_splitter.addWidget(editor_area)
        self.main_splitter.setSizes([250, 1350])
    
    def create_editor_toolbar(self, parent_layout):
        toolbar = QWidget()
        toolbar.setFixedHeight(50)
        toolbar.setStyleSheet(f"background-color: {self.theme['surface']};")
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Action buttons
        actions = [
            ("◢ NEW", self.create_new_file, "Ctrl+N"),
            ("◢ OPEN", self.open_file_dialog, "Ctrl+O"),
            ("◢ SAVE", self.save_file, "Ctrl+S"),
            ("◢ SAVE AS", self.save_as, "Ctrl+Shift+S"),
            ("◢ RUN", self.run_current_file, "F5"),
        ]
        
        for text, callback, shortcut in actions:
            btn = self.create_toolbar_button(text, shortcut)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Language selector
        lang_label = QLabel("Language:")
        lang_label.setStyleSheet(f"color: {self.theme['text_secondary']};")
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Python", "JavaScript", "HTML", "CSS", "Java", "C++", "C", "PHP", "Bash"])
        self.language_combo.setCurrentText("Python")
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        self.language_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.theme['surface_light']};
                color: {self.theme['text_primary']};
                border: 1px solid {self.theme['primary']};
                padding: 5px;
                min-width: 120px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        
        layout.addWidget(lang_label)
        layout.addWidget(self.language_combo)
        
        parent_layout.addWidget(toolbar)
    
    def create_toolbar_button(self, text, shortcut):
        btn = QPushButton(f"{text} ({shortcut})")
        btn.setMinimumHeight(35)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['surface_light']};
                color: {self.theme['text_primary']};
                border: 1px solid {self.theme['primary']};
                border-radius: 3px;
                padding: 5px 15px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['primary']};
                color: white;
            }}
        """)
        return btn
    
    def create_terminal(self, parent_layout):
        # Terminal widget
        self.terminal = LRDTerminal()
        
        # Terminal input
        terminal_input = QWidget()
        terminal_input.setFixedHeight(50)
        terminal_input.setStyleSheet(f"background-color: {self.theme['surface']};")
        
        layout = QHBoxLayout(terminal_input)
        layout.setContentsMargins(10, 0, 10, 0)
        
        prompt = QLabel("$")
        prompt.setStyleSheet(f"""
            color: {self.theme['terminal_prompt']};
            font-weight: bold;
            font-size: 16px;
        """)
        prompt.setFixedWidth(20)
        
        self.terminal_input = QLineEdit()
        self.terminal_input.setPlaceholderText("Type command and press Enter...")
        self.terminal_input.returnPressed.connect(self.execute_terminal_command)
        self.terminal_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.theme['surface_light']};
                color: {self.theme['terminal_fg']};
                border: 1px solid {self.theme['primary']};
                padding: 8px;
                font-family: Consolas;
                font-size: 12px;
            }}
        """)
        
        run_btn = QPushButton("▶ RUN")
        run_btn.clicked.connect(self.execute_terminal_command)
        run_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['primary']};
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['primary_light']};
            }}
        """)
        
        clear_btn = QPushButton("🗑 CLEAR")
        clear_btn.clicked.connect(self.clear_terminal)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['surface_light']};
                color: {self.theme['text_primary']};
                border: 1px solid {self.theme['primary']};
                padding: 8px 20px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['surface_lighter']};
            }}
        """)
        
        layout.addWidget(prompt)
        layout.addWidget(self.terminal_input, 1)
        layout.addWidget(run_btn)
        layout.addWidget(clear_btn)
        
        # Terminal container
        terminal_container = QWidget()
        terminal_layout = QVBoxLayout(terminal_container)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        terminal_layout.setSpacing(0)
        
        terminal_layout.addWidget(self.terminal, 1)
        terminal_layout.addWidget(terminal_input)
        
        # Create dock widget
        self.terminal_dock = QDockWidget("◢ TERMINAL ◣", self)
        self.terminal_dock.setWidget(terminal_container)
        self.terminal_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                                       QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal_dock)
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status label
        self.status_label = QLabel("● READY")
        self.status_label.setStyleSheet(f"""
            color: {self.theme['status_ready']};
            font-weight: bold;
            padding-right: 20px;
        """)
        
        # Cursor position
        self.cursor_label = QLabel("Ln 1, Col 1")
        self.cursor_label.setStyleSheet(f"color: {self.theme['text_secondary']};")
        
        # File info
        self.file_label = QLabel("Untitled")
        self.file_label.setStyleSheet(f"color: {self.theme['text_secondary']};")
        
        # Language
        self.language_label = QLabel("Python")
        self.language_label.setStyleSheet(f"color: {self.theme['text_secondary']};")
        
        # Line count
        self.line_count_label = QLabel("Lines: 0")
        self.line_count_label.setStyleSheet(f"color: {self.theme['text_secondary']};")
        
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
        
        save_all_action = QAction("◢ Save All", self)
        save_all_action.triggered.connect(self.save_all)
        file_menu.addAction(save_all_action)
        
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
        
        edit_menu.addSeparator()
        
        find_action = QAction("◢ Find...", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.find_text)
        edit_menu.addAction(find_action)
        
        replace_action = QAction("◢ Replace...", self)
        replace_action.setShortcut("Ctrl+H")
        replace_action.triggered.connect(self.replace_text)
        edit_menu.addAction(replace_action)
        
        # View menu
        view_menu = menubar.addMenu("◢ View")
        
        toggle_sidebar = QAction("◢ Toggle Sidebar", self)
        toggle_sidebar.setShortcut("Ctrl+B")
        toggle_sidebar.triggered.connect(self.toggle_sidebar)
        view_menu.addAction(toggle_sidebar)
        
        toggle_terminal = QAction("◢ Toggle Terminal", self)
        toggle_terminal.setShortcut("Ctrl+`")
        toggle_terminal.triggered.connect(self.toggle_terminal)
        view_menu.addAction(toggle_terminal)
        
        view_menu.addSeparator()
        
        zoom_in = QAction("◢ Zoom In", self)
        zoom_in.setShortcut("Ctrl++")
        zoom_in.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in)
        
        zoom_out = QAction("◢ Zoom Out", self)
        zoom_out.setShortcut("Ctrl+-")
        zoom_out.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out)
        
        # Run menu
        run_menu = menubar.addMenu("◢ Run")
        
        run_action = QAction("◢ Run", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_current_file)
        run_menu.addAction(run_action)
        
        run_menu.addSeparator()
        
        # Help menu
        help_menu = menubar.addMenu("◢ Help")
        
        docs_action = QAction("◢ Documentation", self)
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)
        
        about_action = QAction("◢ About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_shortcuts(self):
        # Additional shortcuts
        QShortcut(QKeySequence("Ctrl+W"), self, self.close_current_tab)
        QShortcut(QKeySequence("Ctrl+Tab"), self, self.next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, self.previous_tab)
        QShortcut(QKeySequence("Ctrl+P"), self, self.open_file_dialog)
    
    def apply_styles(self):
        # Apply theme to the entire application
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.theme['background']};
            }}
            
            QMenuBar {{
                background-color: {self.theme['surface']};
                color: {self.theme['text_primary']};
                border-bottom: 1px solid {self.theme['primary']};
            }}
            
            QMenuBar::item {{
                padding: 5px 10px;
                background-color: transparent;
            }}
            
            QMenuBar::item:selected {{
                background-color: {self.theme['editor_selection']};
            }}
            
            QMenu {{
                background-color: {self.theme['surface']};
                color: {self.theme['text_primary']};
                border: 1px solid {self.theme['primary']};
            }}
            
            QMenu::item {{
                padding: 5px 20px;
            }}
            
            QMenu::item:selected {{
                background-color: {self.theme['editor_selection']};
            }}
            
            QStatusBar {{
                background-color: {self.theme['surface']};
                color: {self.theme['text_secondary']};
                border-top: 1px solid {self.theme['surface_light']};
            }}
            
            QDockWidget {{
                titlebar-close-icon: url(none);
                titlebar-normal-icon: url(none);
            }}
            
            QDockWidget::title {{
                background-color: {self.theme['surface']};
                color: {self.theme['primary']};
                padding: 5px;
                font-weight: bold;
            }}
        """)
    
    def setup_timers(self):
        # Clock timer
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()
    
    # ==================== EDITOR MANAGEMENT ====================
    
    def create_new_file(self):
        editor = LRDCodeEditor()
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
        self.update_status("New file created", "info")
        self.file_label.setText("Untitled")
        self.update_cursor_position(editor)
    
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
            editor = LRDCodeEditor()
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
            self.update_status(f"Opened: {filename}", "info")
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
    
    def save_all(self):
        for editor, info in self.open_files.items():
            if info['path'] and info['modified']:
                try:
                    with open(info['path'], 'w', encoding='utf-8') as f:
                        f.write(editor.toPlainText())
                    info['saved'] = True
                    info['modified'] = False
                except:
                    pass
        
        self.update_status("All files saved", "success")
    
    def close_tab(self, index):
        widget = self.tab_widget.widget(index)
        if isinstance(widget, LRDCodeEditor):
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
            if isinstance(widget, LRDCodeEditor):
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
    
    def find_text(self):
        editor = self.get_current_editor()
        if editor:
            text, ok = QInputDialog.getText(self, "Find", "Find text:")
            if ok and text:
                # Simple find implementation
                editor.moveCursor(QTextCursor.MoveOperation.Start)
                if editor.find(text):
                    # Highlight found text
                    extra_selections = []
                    selection = QTextEdit.ExtraSelection()
                    selection.format.setBackground(QColor(LRD_THEME['warning_light']))
                    selection.cursor = editor.textCursor()
                    extra_selections.append(selection)
                    editor.setExtraSelections(extra_selections)
    
    def replace_text(self):
        editor = self.get_current_editor()
        if editor:
            find, ok1 = QInputDialog.getText(self, "Replace", "Find:")
            if ok1:
                replace, ok2 = QInputDialog.getText(self, "Replace", "Replace with:")
                if ok2:
                    text = editor.toPlainText()
                    new_text = text.replace(find, replace)
                    editor.setPlainText(new_text)
    
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
            '.cpp': 'c++',
            '.c': 'c',
            '.php': 'php',
            '.sh': 'bash',
        }
        
        return language_map.get(ext, 'text')
    
    def set_editor_language(self, editor, language):
        if isinstance(editor, LRDCodeEditor):
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
            self.update_status(f"Project: {os.path.basename(folder)}", "info")
    
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
    
    def clear_terminal(self):
        self.terminal.clear()
        self.terminal.append_welcome()
    
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
        self.terminal.append(f"◢ Running {info['language']} file: {os.path.basename(info['path'])} ◣")
        self.terminal.append("=" * 50)
        
        # Run based on language
        try:
            if info['language'] == 'python':
                result = subprocess.run(
                    [sys.executable, info['path']],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=os.path.dirname(info['path'])
                )
            elif info['language'] == 'javascript':
                result = subprocess.run(
                    ['node', info['path']],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            elif info['language'] == 'html':
                # Open in browser
                webbrowser.open(f'file://{os.path.abspath(info["path"])}')
                self.terminal.append("◢ Opened in web browser ◣")
                return
            else:
                self.terminal.append(f"◢ Language {info['language']} execution not yet implemented ◣")
                return
            
            # Display results
            if result.stdout:
                self.terminal.append(result.stdout)
            if result.stderr:
                self.terminal.append(f"<span style='color:{LRD_THEME['status_error']}'>Error:</span>")
                self.terminal.append(result.stderr)
            
            self.terminal.append("=" * 50)
            self.terminal.append("◢ Execution completed ◣")
            self.update_status("Execution completed", "success")
            
        except subprocess.TimeoutExpired:
            self.terminal.append(f"<span style='color:{LRD_THEME['status_warning']}'>◢ Execution timed out after 30 seconds ◣</span>")
            self.update_status("Execution timed out", "warning")
        except Exception as e:
            self.terminal.append(f"<span style='color:{LRD_THEME['status_error']}'>◢ Error: {str(e)} ◣</span>")
            self.update_status("Execution failed", "error")
    
    # ==================== VIEW CONTROLS ====================
    
    def toggle_sidebar(self):
        sidebar = self.main_splitter.widget(0)
        sidebar.setVisible(not sidebar.isVisible())
    
    def toggle_terminal(self):
        self.terminal_dock.setVisible(not self.terminal_dock.isVisible())
    
    def zoom_in(self):
        self.font_size = min(24, self.font_size + 1)
        self.update_font_size()
    
    def zoom_out(self):
        self.font_size = max(8, self.font_size - 1)
        self.update_font_size()
    
    def update_font_size(self):
        for editor in self.open_files.keys():
            if isinstance(editor, LRDCodeEditor):
                font = editor.font()
                font.setPointSize(self.font_size)
                editor.setFont(font)
        self.update_status(f"Font size: {self.font_size}", "info")
    
    # ==================== UTILITIES ====================
    
    def get_current_editor(self):
        widget = self.tab_widget.currentWidget()
        if isinstance(widget, LRDCodeEditor):
            return widget
        return None
    
    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_display.setText(current_time)
    
    def update_status(self, message: str, status_type: str = "info"):
        colors = {
            'success': LRD_THEME['status_ready'],
            'error': LRD_THEME['status_error'],
            'warning': LRD_THEME['status_modified'],
            'info': LRD_THEME['status_info']
        }
        
        color = colors.get(status_type, LRD_THEME['status_info'])
        self.status_label.setText(f"● {message}")
        self.status_label.setStyleSheet(f"""
            color: {color};
            font-weight: bold;
            padding-right: 20px;
        """)
        self.status_indicator.setText(f"● {message}")
    
    # ==================== HELP & ABOUT ====================
    
    def show_documentation(self):
        QMessageBox.information(
            self,
            "Documentation",
            """◢◤ LRD CODE EDITOR - PROFESSIONAL EDITION ◥◣

◢ Features:
• Multi-language code editing (Python, JavaScript, HTML, CSS, Java, C++, C, PHP, Bash)
• Advanced syntax highlighting
• Integrated terminal with command history
• File explorer with project support
• Multiple tab support
• Find and replace
• Code execution (Python, JavaScript, HTML)
• VS Code-like interface with LRD theme
• Zoom in/out
• Auto-save detection
• Line numbers
• Status bar with cursor position

◢ Keyboard Shortcuts:
• Ctrl+N: New file
• Ctrl+O: Open file
• Ctrl+S: Save file
• Ctrl+Shift+S: Save As
• Ctrl+W: Close tab
• Ctrl+Tab: Next tab
• Ctrl+Shift+Tab: Previous tab
• F5: Run code
• Ctrl+F: Find
• Ctrl+H: Replace
• Ctrl+Z: Undo
• Ctrl+Y: Redo
• Ctrl+B: Toggle sidebar
• Ctrl+`: Toggle terminal
• Ctrl++: Zoom in
• Ctrl+-: Zoom out

◢ Getting Started:
1. Create a new file (Ctrl+N)
2. Write your code
3. Save the file (Ctrl+S)
4. Run the code (F5)
5. Use terminal for commands
            """
        )
    
    def show_about(self):
        QMessageBox.about(
            self,
            "About LRD Code Editor",
            """◢◤ LRD CODE EDITOR - PROFESSIONAL EDITION ◥◣
Version 2.0.0

A professional code editor with advanced features
and VS Code-like interface with LRD holographic theme.

◢ Developer: LRD_SOUL
◢ Email: inscreator728@gmail.com
◢ GitHub: inscreator728
◢ Telegram: @lrd_soul
◢ Instagram: @lrd_soul

◢ Company: LRD-TECH
◢ Year: 2024-2025

© All rights reserved.
            """
        )
    
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
                self.save_all()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

# ==================== APPLICATION ====================

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    app.setApplicationName("LRD Code Editor")
    app.setOrganizationName("LRD-TECH")
    
    # Create and show main window
    window = LRDCodeEditorWindow()
    window.show()
    
    # Start application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
