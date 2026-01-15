# lrd_code_editor_ultimate.py - Optimized Hacker Edition
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

# ==================== OPTIMIZED HACKER THEME ====================

HACKER_THEME = {
    # Solid Backgrounds (faster rendering)
    'bg_dark': '#0a0a0a',
    'bg_surface': '#121212',
    'bg_panel': '#1a1a1a',
    'bg_terminal': '#0a0a0a',
    'bg_editor': '#0f0f0f',
    
    # Primary Colors (Green Hacker Theme)
    'primary': '#00ff00',
    'primary_light': '#66ff66',
    'primary_dark': '#00cc00',
    
    # Secondary Colors (Cyan)
    'secondary': '#00ffff',
    'secondary_light': '#66ffff',
    'secondary_dark': '#00cccc',
    
    # Accent Colors
    'accent': '#ff00ff',
    'warning': '#ffff00',
    'error': '#ff0000',
    'success': '#00ff00',
    'info': '#0088ff',
    
    # Text Colors
    'text_primary': '#00ff00',
    'text_secondary': '#00ffff',
    'text_tertiary': '#888888',
    'text_editor': '#ffffff',
    
    # Syntax Highlighting (Terminal Style)
    'syntax_keyword': '#ff00ff',
    'syntax_builtin': '#ffff00',
    'syntax_string': '#00ffff',
    'syntax_comment': '#666666',
    'syntax_function': '#00ff00',
    'syntax_class': '#ff6600',
    'syntax_number': '#ffaa00',
    'syntax_operator': '#ff0000',
}

# ==================== OPTIMIZED STYLESHEET ====================

STYLESHEET = f"""
    /* Main Window - Solid for speed */
    QMainWindow {{
        background-color: {HACKER_THEME['bg_dark']};
        border: 2px solid {HACKER_THEME['primary']};
    }}
    
    /* Menu Bar */
    QMenuBar {{
        background-color: {HACKER_THEME['bg_panel']};
        color: {HACKER_THEME['text_primary']};
        border-bottom: 2px solid {HACKER_THEME['primary']};
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 5px 10px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {HACKER_THEME['primary']};
        color: {HACKER_THEME['bg_dark']};
    }}
    
    /* Menus */
    QMenu {{
        background-color: {HACKER_THEME['bg_panel']};
        color: {HACKER_THEME['text_primary']};
        border: 2px solid {HACKER_THEME['primary']};
    }}
    
    QMenu::item {{
        padding: 5px 20px;
    }}
    
    QMenu::item:selected {{
        background-color: {HACKER_THEME['primary']};
        color: {HACKER_THEME['bg_dark']};
    }}
    
    /* Buttons - Gamer Style */
    QPushButton {{
        background-color: {HACKER_THEME['bg_panel']};
        color: {HACKER_THEME['text_primary']};
        border: 2px solid {HACKER_THEME['primary']};
        border-radius: 3px;
        padding: 8px 16px;
        font-weight: bold;
        font-family: 'Courier New';
    }}
    
    QPushButton:hover {{
        background-color: {HACKER_THEME['primary']};
        color: {HACKER_THEME['bg_dark']};
        border: 2px solid {HACKER_THEME['secondary']};
    }}
    
    QPushButton:pressed {{
        background-color: {HACKER_THEME['secondary']};
        color: {HACKER_THEME['bg_dark']};
    }}
    
    /* LineEdit */
    QLineEdit {{
        background-color: {HACKER_THEME['bg_panel']};
        color: {HACKER_THEME['text_editor']};
        border: 2px solid {HACKER_THEME['primary']};
        font-family: 'Consolas';
        font-size: 12px;
        padding: 8px;
    }}
    
    /* Tab Widget */
    QTabWidget::pane {{
        background-color: {HACKER_THEME['bg_dark']};
        border: 2px solid {HACKER_THEME['primary']};
    }}
    
    QTabBar::tab {{
        background-color: {HACKER_THEME['bg_panel']};
        color: {HACKER_THEME['text_secondary']};
        padding: 8px 16px;
        border: 1px solid {HACKER_THEME['primary']};
        font-family: 'Courier New';
        font-weight: bold;
    }}
    
    QTabBar::tab:selected {{
        background-color: {HACKER_THEME['primary']};
        color: {HACKER_THEME['bg_dark']};
        border-bottom: 2px solid {HACKER_THEME['primary']};
    }}
    
    /* TreeView */
    QTreeView {{
        background-color: {HACKER_THEME['bg_panel']};
        color: {HACKER_THEME['text_primary']};
        border: 1px solid {HACKER_THEME['primary']};
        font-family: 'Consolas';
        font-size: 11px;
    }}
    
    QTreeView::item:selected {{
        background-color: {HACKER_THEME['primary']};
        color: {HACKER_THEME['bg_dark']};
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
            'keyword': self.create_format(HACKER_THEME['syntax_keyword'], bold=True),
            'builtin': self.create_format(HACKER_THEME['syntax_builtin']),
            'string': self.create_format(HACKER_THEME['syntax_string']),
            'comment': self.create_format(HACKER_THEME['syntax_comment'], italic=True),
            'function': self.create_format(HACKER_THEME['syntax_function']),
            'class': self.create_format(HACKER_THEME['syntax_class']),
            'number': self.create_format(HACKER_THEME['syntax_number']),
        }
        
        # Python (optimized patterns)
        if self.language == 'python':
            keywords = [
                'and', 'as', 'assert', 'break', 'class', 'continue',
                'def', 'del', 'elif', 'else', 'except', 'False',
                'finally', 'for', 'from', 'global', 'if', 'import',
                'in', 'is', 'lambda', 'None', 'nonlocal', 'not',
                'or', 'pass', 'raise', 'return', 'True', 'try',
                'while', 'with', 'yield'
            ]
            self.rules.append((r'\b(' + '|'.join(keywords) + r')\b', formats['keyword']))
            
            builtins = [
                'print', 'len', 'range', 'str', 'int', 'float', 'list',
                'dict', 'set', 'tuple', 'open', 'input', 'type'
            ]
            self.rules.append((r'\b(' + '|'.join(builtins) + r')\b', formats['builtin']))
            
            self.rules.append((r'\bdef\s+(\w+)', formats['function']))
            self.rules.append((r'\bclass\s+(\w+)', formats['class']))
            self.rules.append((r'#.*', formats['comment']))
            self.rules.append((r'".*?"', formats['string']))
            self.rules.append((r"'.*?'", formats['string']))
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
                self.setFormat(match.start(), match.end() - match.start(), fmt)

# ==================== FAST CODE EDITOR ====================

class FastEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)
        self.highlighter = FastHighlighter(self.document())
        
        # Setup editor
        self.setup_editor()
        
        # Initial update
        self.update_line_number_area_width()
    
    def setup_editor(self):
        # Font
        font = QFont("Consolas", 11)
        self.setFont(font)
        self.setTabStopDistance(40)
        
        # Colors
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {HACKER_THEME['bg_editor']};
                color: {HACKER_THEME['text_editor']};
                selection-background-color: {HACKER_THEME['primary']};
                selection-color: {HACKER_THEME['bg_dark']};
                border: 2px solid {HACKER_THEME['primary']};
                font-family: 'Consolas';
            }}
        """)
    
    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 20 + self.fontMetrics().horizontalAdvance('9') * digits
    
    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), width, cr.height()))
    
    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(HACKER_THEME['bg_panel']))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QColor(HACKER_THEME['text_primary']))
                painter.drawText(0, top, self.line_number_area.width() - 5, 
                                self.fontMetrics().height(),
                                Qt.AlignmentFlag.AlignRight, str(block_number + 1))
            
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

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

class AdvancedTerminal(QTextEdit):
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
        self.setReadOnly(True)
        font = QFont("Consolas", 10)
        font.setBold(True)
        self.setFont(font)
        
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {HACKER_THEME['bg_terminal']};
                color: {HACKER_THEME['text_primary']};
                border: 2px solid {HACKER_THEME['primary']};
                font-family: 'Consolas';
                font-weight: bold;
            }}
        """)
    
    def detect_compilers(self):
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
            subprocess.run(['javac', '-version'], capture_output=True, check=True)
            compilers['javac'] = 'javac'
            compilers['java'] = 'java'
        except:
            pass
        
        # Node.js
        try:
            subprocess.run(['node', '--version'], capture_output=True, check=True)
            compilers['node'] = 'node'
        except:
            pass
        
        return compilers
    
    def append_welcome(self):
        self.append(f"<span style='color:{HACKER_THEME['primary']}; font-weight:bold'>◢◤ LRD HACKER TERMINAL v3.0 ◥◣</span>")
        self.append(f"<span style='color:{HACKER_THEME['secondary']}'>Directory: {self.current_dir}</span>")
        self.append("<span style='color:#ffff00'>Type commands below. Type 'help' for assistance.</span>\n")
    
    def execute_command(self, command: str):
        if not command.strip():
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Show command
        self.append(f"<span style='color:{HACKER_THEME['primary']}'>$</span> <span style='color:{HACKER_THEME['text_editor']}'>{command}</span>")
        
        # Special commands
        cmd_lower = command.lower()
        
        if cmd_lower == 'clear':
            self.clear()
            self.append_welcome()
            return
        
        if cmd_lower == 'help':
            self.show_help()
            return
        
        if cmd_lower == 'compilers':
            self.show_compilers()
            return
        
        if cmd_lower.startswith('cd '):
            self.handle_cd(command)
            return
        
        # Execute command
        self.run_command(command)
    
    def run_command(self, command):
        try:
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
                self.append(f"<span style='color:{HACKER_THEME['text_editor']}'>{result.stdout}</span>")
            if result.stderr:
                self.append(f"<span style='color:{HACKER_THEME['error']}'>{result.stderr}</span>")
            
            if result.returncode != 0:
                self.append(f"<span style='color:{HACKER_THEME['warning']}'>Exit code: {result.returncode}</span>")
        
        except subprocess.TimeoutExpired:
            self.append(f"<span style='color:{HACKER_THEME['warning']}'>Command timed out</span>")
        except Exception as e:
            self.append(f"<span style='color:{HACKER_THEME['error']}'>Error: {str(e)}</span>")
    
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
                    new_path = os.path.join(self.current_dir, path)
                    if os.path.isdir(new_path):
                        os.chdir(new_path)
                    else:
                        self.append(f"<span style='color:{HACKER_THEME['error']}'>Directory not found: {path}</span>")
                        return
            
            self.current_dir = os.getcwd()
            self.append(f"<span style='color:{HACKER_THEME['success']}'>Changed to: {self.current_dir}</span>")
        except Exception as e:
            self.append(f"<span style='color:{HACKER_THEME['error']}'>Error: {str(e)}</span>")
    
    def show_help(self):
        help_text = f"""
<span style='color:{HACKER_THEME['primary']}'>◢ LRD TERMINAL COMMANDS ◣</span>

<span style='color:{HACKER_THEME['secondary']}'>System:</span>
  cd [dir]    - Change directory
  ls / dir    - List files
  clear       - Clear terminal
  help        - Show this help

<span style='color:{HACKER_THEME['secondary']}'>Execution:</span>
  python file.py    - Run Python
  node file.js      - Run JavaScript
  javac Main.java   - Compile Java
  java Main         - Run Java

<span style='color:{HACKER_THEME['secondary']}'>Examples:</span>
  $ python script.py
  $ cd Documents
  $ ls -la
        """
        self.append(help_text)
    
    def show_compilers(self):
        if not self.compiler_paths:
            self.append(f"<span style='color:{HACKER_THEME['error']}'>No compilers detected</span>")
            return
        
        self.append(f"<span style='color:{HACKER_THEME['primary']}'>Detected Compilers:</span>")
        for lang, cmd in self.compiler_paths.items():
            self.append(f"  <span style='color:{HACKER_THEME['secondary']}'>{lang}:</span> {cmd}")
    
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
        self.insertHtml(text + "<br>")
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

# ==================== FILE EXPLORER ====================

class FileExplorer(QTreeView):
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
                background-color: {HACKER_THEME['bg_panel']};
                color: {HACKER_THEME['text_primary']};
                border: 2px solid {HACKER_THEME['primary']};
                font-family: 'Consolas';
                font-size: 11px;
            }}
            QTreeView::item:selected {{
                background-color: {HACKER_THEME['primary']};
                color: {HACKER_THEME['bg_dark']};
            }}
        """)
        
        # Set icon size
        self.setIconSize(QSize(20, 20))
    
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
        
        # Create initial tab
        self.create_new_file()
        
        # Setup timers
        self.setup_timers()
        
        # Focus on editor
        QTimer.singleShot(100, self.focus_editor)
    
    def setup_window(self):
        self.setWindowTitle("◢◤ LRD CODE EDITOR - HACKER EDITION v3.0 ◥◣")
        self.setGeometry(100, 50, 1400, 800)
        
        # Set window icon from tlogo.png
        self.set_window_icon()
        
        # Remove frame for cleaner look
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        
        # Apply stylesheet
        self.setStyleSheet(STYLESHEET)
    
    def set_window_icon(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "tlogo.png")
        
        if os.path.exists(icon_path):
            try:
                app = QApplication.instance()
                app.setWindowIcon(QIcon(icon_path))
                self.setWindowIcon(QIcon(icon_path))
            except:
                # Fallback icon
                pixmap = QPixmap(64, 64)
                pixmap.fill(QColor(HACKER_THEME['primary']))
                painter = QPainter(pixmap)
                painter.setPen(QPen(QColor(HACKER_THEME['bg_dark']), 3))
                painter.setFont(QFont("Arial", 24, QFont.Weight.Bold))
                painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "LRD")
                painter.end()
                self.setWindowIcon(QIcon(pixmap))
    
    def setup_variables(self):
        self.open_files = {}
        self.project_path = None
        self.font_size = 11
    
    def setup_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
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
                background-color: {HACKER_THEME['bg_panel']};
                border: 2px solid {HACKER_THEME['primary']};
                border-bottom: none;
            }}
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Logo/Title
        title_label = QLabel("◢◤ LRD CODE EDITOR - HACKER EDITION v3.0 ◥◣")
        title_label.setStyleSheet(f"""
            color: {HACKER_THEME['text_primary']};
            font-weight: bold;
            font-size: 14px;
            font-family: 'Courier New';
        """)
        
        # Window controls
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(5)
        
        # Control buttons
        min_btn = self.create_control_button("─")
        min_btn.clicked.connect(self.showMinimized)
        
        max_btn = self.create_control_button("□")
        max_btn.clicked.connect(self.toggle_maximize)
        self.max_btn = max_btn
        
        close_btn = self.create_control_button("✕")
        close_btn.clicked.connect(self.close)
        
        controls_layout.addWidget(min_btn)
        controls_layout.addWidget(max_btn)
        controls_layout.addWidget(close_btn)
        
        layout.addWidget(title_label)
        layout.addStretch()
        
        # Time display
        self.time_label = QLabel()
        self.time_label.setStyleSheet(f"""
            color: {HACKER_THEME['secondary']};
            font-family: 'Courier New';
            font-weight: bold;
        """)
        
        layout.addWidget(self.time_label)
        layout.addSpacing(10)
        layout.addWidget(controls_widget)
        
        parent_layout.addWidget(title_bar)
    
    def create_control_button(self, text):
        btn = QPushButton(text)
        btn.setFixedSize(30, 30)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {HACKER_THEME['bg_panel']};
                color: {HACKER_THEME['text_primary']};
                border: 1px solid {HACKER_THEME['primary']};
                border-radius: 3px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {HACKER_THEME['primary']};
                color: {HACKER_THEME['bg_dark']};
            }}
        """)
        return btn
    
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.max_btn.setText("□")
        else:
            self.showMaximized()
            self.max_btn.setText("🗗")
    
    def create_main_content(self, parent_layout):
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar
        sidebar = self.create_sidebar()
        splitter.addWidget(sidebar)
        
        # Editor area
        editor_area = self.create_editor_area()
        splitter.addWidget(editor_area)
        
        splitter.setSizes([200, 1200])
        parent_layout.addWidget(splitter, 1)
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setMinimumWidth(180)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Explorer header
        header = QWidget()
        header.setFixedHeight(35)
        header.setStyleSheet(f"""
            QWidget {{
                background-color: {HACKER_THEME['bg_panel']};
                border-bottom: 2px solid {HACKER_THEME['primary']};
            }}
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        title = QLabel("◢ FILES ◣")
        title.setStyleSheet(f"""
            color: {HACKER_THEME['text_primary']};
            font-weight: bold;
            font-family: 'Courier New';
        """)
        
        open_btn = QPushButton("📁")
        open_btn.setFixedSize(25, 25)
        open_btn.setToolTip("Open Folder")
        open_btn.clicked.connect(self.open_folder)
        open_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {HACKER_THEME['text_primary']};
                border: none;
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: {HACKER_THEME['secondary']};
            }}
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(open_btn)
        
        # File explorer
        self.file_explorer = FileExplorer()
        self.file_explorer.doubleClicked.connect(self.on_file_double_clicked)
        
        layout.addWidget(header)
        layout.addWidget(self.file_explorer)
        
        return sidebar
    
    def create_editor_area(self):
        editor_area = QWidget()
        
        layout = QVBoxLayout(editor_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Editor toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(40)
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: {HACKER_THEME['bg_panel']};
                border-bottom: 2px solid {HACKER_THEME['primary']};
            }}
        """)
        
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 0, 10, 0)
        
        # Toolbar buttons
        actions = [
            ("◢ NEW", self.create_new_file, "New file"),
            ("◢ OPEN", self.open_file_dialog, "Open file"),
            ("◢ SAVE", self.save_file, "Save file"),
            ("◢ RUN", self.run_current_file, "Run code"),
        ]
        
        for text, callback, tooltip in actions:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {HACKER_THEME['text_primary']};
                    border: none;
                    font-weight: bold;
                    font-family: 'Courier New';
                    padding: 5px 10px;
                }}
                QPushButton:hover {{
                    background-color: {HACKER_THEME['primary']};
                    color: {HACKER_THEME['bg_dark']};
                }}
            """)
            toolbar_layout.addWidget(btn)
        
        toolbar_layout.addStretch()
        
        # Language selector
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Python", "JavaScript", "HTML", "Java", "C++", "C", "PHP"])
        self.language_combo.setCurrentText("Python")
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        self.language_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {HACKER_THEME['bg_panel']};
                color: {HACKER_THEME['text_primary']};
                border: 1px solid {HACKER_THEME['primary']};
                font-family: 'Courier New';
                min-width: 100px;
                padding: 3px;
            }}
        """)
        
        toolbar_layout.addWidget(self.language_combo)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        layout.addWidget(toolbar)
        layout.addWidget(self.tab_widget)
        
        return editor_area
    
    def create_terminal(self, parent_layout):
        terminal_widget = QWidget()
        terminal_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {HACKER_THEME['bg_panel']};
                border: 2px solid {HACKER_THEME['primary']};
                border-top: none;
            }}
        """)
        
        layout = QVBoxLayout(terminal_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Terminal header
        terminal_header = QWidget()
        terminal_header.setFixedHeight(30)
        terminal_header.setStyleSheet(f"""
            QWidget {{
                background-color: {HACKER_THEME['bg_panel']};
                border-bottom: 1px solid {HACKER_THEME['primary']};
            }}
        """)
        
        header_layout = QHBoxLayout(terminal_header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        title = QLabel("◢ TERMINAL ◣")
        title.setStyleSheet(f"""
            color: {HACKER_THEME['text_primary']};
            font-weight: bold;
            font-family: 'Courier New';
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Terminal widget
        self.terminal = AdvancedTerminal()
        
        # Terminal input
        input_widget = QWidget()
        input_widget.setFixedHeight(40)
        input_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {HACKER_THEME['bg_panel']};
                border-top: 1px solid {HACKER_THEME['primary']};
            }}
        """)
        
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(10, 0, 10, 0)
        
        prompt = QLabel("$")
        prompt.setStyleSheet(f"""
            color: {HACKER_THEME['primary']};
            font-weight: bold;
            font-family: 'Consolas';
            font-size: 14px;
        """)
        prompt.setFixedWidth(20)
        
        self.terminal_input = QLineEdit()
        self.terminal_input.setPlaceholderText("Type command (Up/Down for history)...")
        self.terminal_input.returnPressed.connect(self.execute_terminal_command)
        self.terminal_input.keyPressEvent = self.terminal_keyPressEvent
        
        run_btn = QPushButton("▶")
        run_btn.setFixedSize(30, 30)
        run_btn.clicked.connect(self.execute_terminal_command)
        run_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {HACKER_THEME['primary']};
                color: {HACKER_THEME['bg_dark']};
                border: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {HACKER_THEME['secondary']};
            }}
        """)
        
        input_layout.addWidget(prompt)
        input_layout.addWidget(self.terminal_input, 1)
        input_layout.addWidget(run_btn)
        
        layout.addWidget(terminal_header)
        layout.addWidget(self.terminal, 1)
        layout.addWidget(input_widget)
        
        parent_layout.addWidget(terminal_widget)
    
    def terminal_keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            cmd = self.terminal.get_previous_command()
            if cmd:
                self.terminal_input.setText(cmd)
        elif event.key() == Qt.Key.Key_Down:
            cmd = self.terminal.get_next_command()
            self.terminal_input.setText(cmd)
        else:
            super(QLineEdit, self.terminal_input).keyPressEvent(event)
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status label
        self.status_label = QLabel("● READY")
        self.status_label.setStyleSheet(f"""
            color: {HACKER_THEME['success']};
            font-weight: bold;
            font-family: 'Courier New';
            padding-right: 20px;
        """)
        
        # Cursor position
        self.cursor_label = QLabel("Ln 1, Col 1")
        self.cursor_label.setStyleSheet(f"color: {HACKER_THEME['text_secondary']};")
        
        # File info
        self.file_label = QLabel("Untitled")
        self.file_label.setStyleSheet(f"color: {HACKER_THEME['text_primary']};")
        
        # Language
        self.language_label = QLabel("Python")
        self.language_label.setStyleSheet(f"color: {HACKER_THEME['text_secondary']};")
        
        # Add widgets
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.cursor_label)
        self.status_bar.addPermanentWidget(self.file_label)
        self.status_bar.addPermanentWidget(self.language_label)
    
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
        
        save_action = QAction("◢ Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("◢ Exit", self)
        exit_action.setShortcut("Ctrl+Q")
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
        
        run_action = QAction("◢ Run Code", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_current_file)
        run_menu.addAction(run_action)
        
        # Help menu
        help_menu = menubar.addMenu("◢ Help")
        
        about_action = QAction("◢ About LRD", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+W"), self, self.close_current_tab)
        QShortcut(QKeySequence("Ctrl+Tab"), self, self.next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, self.previous_tab)
    
    def setup_timers(self):
        # Update clock
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()
    
    # ==================== EDITOR MANAGEMENT ====================
    
    def create_new_file(self):
        editor = FastEditor()
        index = self.tab_widget.addTab(editor, "Untitled")
        self.tab_widget.setCurrentIndex(index)
        
        self.open_files[editor] = {
            'path': None,
            'language': 'python'
        }
        
        editor.cursorPositionChanged.connect(lambda: self.update_cursor_position(editor))
        editor.textChanged.connect(lambda: self.on_text_changed(editor))
        
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
            "All Files (*.*);;Python Files (*.py);;JavaScript Files (*.js);;HTML Files (*.html);;Java Files (*.java)"
        )
        
        if file_path:
            self.open_file(file_path)
    
    def open_file(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            editor = FastEditor()
            editor.setPlainText(content)
            
            filename = os.path.basename(file_path)
            index = self.tab_widget.addTab(editor, filename)
            self.tab_widget.setCurrentIndex(index)
            
            self.open_files[editor] = {
                'path': file_path,
                'language': self.detect_language(file_path)
            }
            
            editor.cursorPositionChanged.connect(lambda: self.update_cursor_position(editor))
            editor.textChanged.connect(lambda: self.on_text_changed(editor))
            
            self.set_editor_language(editor, self.open_files[editor]['language'])
            
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
            try:
                with open(info['path'], 'w', encoding='utf-8') as f:
                    f.write(editor.toPlainText())
                
                self.update_status(f"Saved: {os.path.basename(info['path'])}", "success")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
        else:
            self.save_as()
    
    def save_as(self):
        editor = self.get_current_editor()
        if not editor:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save As",
            "",
            "Python Files (*.py);;JavaScript Files (*.js);;HTML Files (*.html);;Java Files (*.java)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(editor.toPlainText())
                
                info = self.open_files.get(editor)
                if info:
                    info['path'] = file_path
                    info['language'] = self.detect_language(file_path)
                
                filename = os.path.basename(file_path)
                index = self.tab_widget.indexOf(editor)
                self.tab_widget.setTabText(index, filename)
                self.set_editor_language(editor, info['language'])
                
                self.update_status(f"Saved as: {filename}", "success")
                self.file_label.setText(filename)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
    
    def close_tab(self, index):
        widget = self.tab_widget.widget(index)
        if isinstance(widget, FastEditor):
            self.open_files.pop(widget, None)
        
        self.tab_widget.removeTab(index)
        
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
            if isinstance(widget, FastEditor):
                info = self.open_files.get(widget)
                if info:
                    if info['path']:
                        self.file_label.setText(os.path.basename(info['path']))
                    else:
                        self.file_label.setText("Untitled")
                    
                    self.language_label.setText(info['language'].capitalize())
                    self.language_combo.setCurrentText(info['language'].capitalize())
                    self.update_cursor_position(widget)
                    widget.setFocus()
    
    # ==================== TEXT OPERATIONS ====================
    
    def on_text_changed(self, editor):
        info = self.open_files.get(editor)
        if info:
            index = self.tab_widget.indexOf(editor)
            filename = os.path.basename(info['path']) if info['path'] else "Untitled"
            self.tab_widget.setTabText(index, f"*{filename}")
    
    def update_cursor_position(self, editor=None):
        if not editor:
            editor = self.get_current_editor()
        
        if editor:
            cursor = editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            self.cursor_label.setText(f"Ln {line}, Col {col}")
    
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
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.php': 'php',
        }
        
        return language_map.get(ext, 'text')
    
    def set_editor_language(self, editor, language):
        if isinstance(editor, FastEditor):
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
            self.terminal_input.setFocus()
    
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
        self.terminal.append(f"<span style='color:{HACKER_THEME['primary']}'>◢ Running {info['language']} file: {os.path.basename(info['path'])} ◣</span>")
        
        try:
            if info['language'] == 'python':
                cmd = self.terminal.compiler_paths.get('python', 'python')
                self.terminal.run_command(f"{cmd} \"{info['path']}\"")
            elif info['language'] == 'javascript':
                self.terminal.run_command(f"node \"{info['path']}\"")
            elif info['language'] == 'java':
                self.terminal.run_command(f"javac \"{info['path']}\" && java -cp \"{os.path.dirname(info['path'])}\" \"{os.path.splitext(os.path.basename(info['path']))[0]}\"")
            elif info['language'] == 'html':
                webbrowser.open(f'file://{os.path.abspath(info["path"])}')
                self.terminal.append(f"<span style='color:{HACKER_THEME['success']}'>Opened in browser</span>")
            else:
                self.terminal.append(f"<span style='color:{HACKER_THEME['warning']}'>Language not supported for execution</span>")
            
            self.update_status("Execution completed", "success")
            
        except Exception as e:
            self.terminal.append(f"<span style='color:{HACKER_THEME['error']}'>Error: {str(e)}</span>")
            self.update_status("Execution failed", "error")
    
    # ==================== UTILITIES ====================
    
    def get_current_editor(self):
        widget = self.tab_widget.currentWidget()
        if isinstance(widget, FastEditor):
            return widget
        return None
    
    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(f"🕒 {current_time}")
    
    def update_status(self, message: str, status_type: str = "info"):
        colors = {
            'success': HACKER_THEME['success'],
            'error': HACKER_THEME['error'],
            'warning': HACKER_THEME['warning'],
            'info': HACKER_THEME['info']
        }
        
        color = colors.get(status_type, HACKER_THEME['info'])
        self.status_label.setText(f"● {message}")
        self.status_label.setStyleSheet(f"""
            color: {color};
            font-weight: bold;
            font-family: 'Courier New';
            padding-right: 20px;
        """)
    
    # ==================== MOUSE EVENTS FOR DRAGGING ====================
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    # ==================== HACKER THEMED ABOUT ====================
    
    def show_about(self):
        about_text = f"""
<pre style='color:{HACKER_THEME['primary']}; font-family: Courier New; font-size: 10pt;'>
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██╗     ██████╗ ██████╗     ██████╗ ██████╗ ██████╗ ███████╗               ║
║  ██║     ██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗██╔════╝               ║
║  ██║     ██████╔╝██║  ██║    ██║  ██║██████╔╝██████╔╝█████╗                 ║
║  ██║     ██╔══██╗██║  ██║    ██║  ██║██╔══██╗██╔══██╗██╔══╝                 ║
║  ███████╗██║  ██║██████╔╝    ██████╔╝██║  ██║██║  ██║███████╗               ║
║  ╚══════╝╚═╝  ╚═╝╚═════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝               ║
║                                                                              ║
║  ◢◤ LRD CODE EDITOR - HACKER EDITION v3.0 ◥◣                               ║
║  =========================================================================  ║
║                                                                              ║
║  <span style='color:{HACKER_THEME['secondary']}'>[SYSTEM INFO]</span>                                                 ║
║  Version: 3.0.0 | Build: 2024.12 | Status: <span style='color:#00ff00'>ACTIVE</span>                          ║
║  Platform: {sys.platform} | Python: {sys.version.split()[0]}                     ║
║                                                                              ║
║  <span style='color:{HACKER_THEME['secondary']}'>[DEVELOPMENT TEAM]</span>                                           ║
║  • Lead Developer: LRD_SOUL                                                 ║
║  • Security Lead: LRD_GUARDIAN                                              ║
║  • AI Specialist: LRD_NEURAL                                                ║
║  • Frontend: LRD_VISION                                                     ║
║                                                                              ║
║  <span style='color:{HACKER_THEME['secondary']}'>[CONTACT & SOCIAL]</span>                                           ║
║  🔐 Email: <span style='color:#ffff00'>inscreator728@gmail.com</span>                                   ║
║  🌐 GitHub: <span style='color:#00ffff'>github.com/inscreator728</span>                                 ║
║  📱 Telegram: <span style='color:#ff00ff'>@lrd_soul</span>                                            ║
║  📸 Instagram: <span style='color:#ff6600'>@lrd_soul</span>                                             ║
║  💼 LinkedIn: <span style='color:#0088ff'>LRD-TECH</span>                                               ║
║                                                                              ║
║  <span style='color:{HACKER_THEME['secondary']}'>[PROJECTS]</span>                                                   ║
║  • LRD-Security Suite v2.5                                                  ║
║  • NeuralAI Framework v1.8                                                  ║
║  • QuantumCoder IDE v3.2                                                    ║
║  • CyberShield Firewall v4.1                                                ║
║                                                                              ║
║  <span style='color:{HACKER_THEME['secondary']}'>[FEATURES]</span>                                                   ║
║  ✓ Multi-language Code Editor                                               ║
║  ✓ Integrated Terminal with Auto-compilation                                ║
║  ✓ Real-time Syntax Highlighting                                            ║
║  ✓ File Explorer with Project Support                                       ║
║  ✓ Code Execution for 8+ Languages                                          ║
║  ✓ Hacker-themed UI with Custom Icons                                       ║
║  ✓ Fast Performance & Low Memory Usage                                      ║
║                                                                              ║
║  <span style='color:{HACKER_THEME['secondary']}'>[SYSTEM COMMANDS]</span>                                            ║
║  $ python script.py      # Execute Python                                   ║
║  $ node app.js           # Run JavaScript                                   ║
║  $ javac Main.java       # Compile Java                                     ║
║  $ clear                 # Clear Terminal                                   ║
║  $ help                  # Show Commands                                    ║
║                                                                              ║
║  <span style='color:{HACKER_THEME['accent']}'>[SECURITY NOTICE]</span>                                              ║
║  This software is protected under LRD-TECH Security Protocol v2.0.          ║
║  Unauthorized distribution or modification is strictly prohibited.          ║
║                                                                              ║
║  © 2024-2025 LRD-TECH | All Systems Operational | [ACCESS GRANTED]          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
</pre>
"""
        
        dialog = QDialog(self)
        dialog.setWindowTitle("◢◤ LRD SYSTEM INFORMATION ◥◣")
        dialog.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(about_text)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {HACKER_THEME['bg_dark']};
                color: {HACKER_THEME['text_primary']};
                border: 2px solid {HACKER_THEME['primary']};
                font-family: 'Courier New';
                font-size: 9pt;
            }}
        """)
        
        layout.addWidget(text_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        dialog.exec()
    
    def closeEvent(self, event):
        # Auto-save if needed
        unsaved = False
        for editor, info in self.open_files.items():
            if info['path']:
                try:
                    with open(info['path'], 'w', encoding='utf-8') as f:
                        f.write(editor.toPlainText())
                except:
                    pass
        
        event.accept()

# ==================== APPLICATION ====================

def main():
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("LRD Code Editor - Hacker Edition")
    app.setOrganizationName("LRD-TECH")
    
    # Set icon
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "tlogo.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Create and show window
    window = LRDCodeEditor()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
