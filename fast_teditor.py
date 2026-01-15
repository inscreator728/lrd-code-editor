# lrd_code_editor_optimized.py
import sys
import os
import subprocess
import re
import webbrowser
from datetime import datetime

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ==================== SIMPLE THEME ====================

LRD_THEME = {
    # Backgrounds
    'bg_primary': '#0a0a0a',
    'bg_secondary': '#1a0d0d',
    'bg_tertiary': '#2d1a1a',
    'bg_editor': '#0d0d0d',
    'bg_terminal': '#0a0a0a',
    
    # Primary Colors (Red Theme)
    'primary': '#ff3333',
    'primary_light': '#ff6666',
    'primary_dark': '#cc0000',
    
    # Secondary Colors (Green)
    'secondary': '#00ff88',
    'secondary_light': '#66ffaa',
    'secondary_dark': '#00cc66',
    
    # Text Colors
    'text_primary': '#ff3333',
    'text_secondary': '#ff6666',
    'text_tertiary': '#ff9999',
    'text_editor': '#00ff88',
    
    # Syntax Highlighting
    'syntax_keyword': '#ff3366',
    'syntax_builtin': '#ff6633',
    'syntax_string': '#ffaa00',
    'syntax_comment': '#666666',
    'syntax_function': '#ff0066',
    'syntax_class': '#ff3399',
    'syntax_number': '#ff9900',
    'syntax_operator': '#ff6666',
}

# ==================== SIMPLE STYLESHEET ====================

SIMPLE_STYLESHEET = f"""
    QMainWindow {{
        background-color: {LRD_THEME['bg_primary']};
        border: 1px solid {LRD_THEME['primary_dark']};
    }}
    
    QMenuBar {{
        background-color: {LRD_THEME['bg_secondary']};
        color: {LRD_THEME['text_primary']};
        border-bottom: 1px solid {LRD_THEME['primary']};
    }}
    
    QMenuBar::item:selected {{
        background-color: {LRD_THEME['primary']};
        color: white;
    }}
    
    QStatusBar {{
        background-color: {LRD_THEME['bg_secondary']};
        color: {LRD_THEME['text_secondary']};
        border-top: 1px solid {LRD_THEME['primary']};
    }}
    
    QPushButton {{
        background-color: {LRD_THEME['bg_tertiary']};
        color: {LRD_THEME['text_primary']};
        border: 1px solid {LRD_THEME['primary']};
        border-radius: 3px;
        padding: 5px 10px;
    }}
    
    QPushButton:hover {{
        background-color: {LRD_THEME['primary']};
        color: white;
    }}
    
    QComboBox {{
        background-color: {LRD_THEME['bg_tertiary']};
        color: {LRD_THEME['text_primary']};
        border: 1px solid {LRD_THEME['primary']};
        border-radius: 3px;
        padding: 3px;
    }}
    
    QLineEdit {{
        background-color: {LRD_THEME['bg_tertiary']};
        color: {LRD_THEME['text_editor']};
        border: 1px solid {LRD_THEME['primary']};
        border-radius: 3px;
        padding: 5px;
        font-family: Consolas;
    }}
    
    QTabBar::tab {{
        background-color: {LRD_THEME['bg_secondary']};
        color: {LRD_THEME['text_secondary']};
        padding: 6px 12px;
        border: 1px solid {LRD_THEME['primary']};
    }}
    
    QTabBar::tab:selected {{
        background-color: {LRD_THEME['primary']};
        color: white;
    }}
    
    QTreeView {{
        background-color: transparent;
        color: {LRD_THEME['text_primary']};
        border: none;
    }}
    
    QTreeView::item:selected {{
        background-color: {LRD_THEME['primary']};
        color: white;
    }}
    
    QScrollBar:vertical {{
        background-color: {LRD_THEME['bg_tertiary']};
        width: 12px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {LRD_THEME['primary']};
    }}
"""

# ==================== FAST SYNTAX HIGHLIGHTER ====================

class LRDFastHighlighter(QSyntaxHighlighter):
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
            'keyword': self.create_format(LRD_THEME['syntax_keyword'], bold=True),
            'builtin': self.create_format(LRD_THEME['syntax_builtin']),
            'string': self.create_format(LRD_THEME['syntax_string']),
            'comment': self.create_format(LRD_THEME['syntax_comment']),
            'function': self.create_format(LRD_THEME['syntax_function']),
            'class': self.create_format(LRD_THEME['syntax_class']),
            'number': self.create_format(LRD_THEME['syntax_number']),
        }
        
        # Python - optimized patterns
        if self.language == 'python':
            keyword_pattern = r'\b(and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield|async|await)\b'
            self.rules.append((keyword_pattern, formats['keyword']))
            
            builtin_pattern = r'\b(print|len|range|str|int|float|list|dict|set|tuple|open|input|type|isinstance)\b'
            self.rules.append((builtin_pattern, formats['builtin']))
            
            self.rules.append((r'\bdef\s+\w+', formats['function']))
            self.rules.append((r'\bclass\s+\w+', formats['class']))
            self.rules.append((r'#.*', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'[^']*'", formats['string']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # JavaScript
        elif self.language == 'javascript':
            keyword_pattern = r'\b(function|class|const|let|var|if|else|for|while|return|try|catch|finally|throw|new|this|async|await|export|import)\b'
            self.rules.append((keyword_pattern, formats['keyword']))
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'[^']*'", formats['string']))
            self.rules.append((r'`[^`]*`', formats['string']))
            self.rules.append((r'\b\d+\b', formats['number']))
        
        # Java
        elif self.language == 'java':
            keyword_pattern = r'\b(public|private|protected|static|final|class|interface|extends|implements|import|package|new|return|if|else|for|while|try|catch|finally|throw|void|int|double|float|boolean|char|String|this)\b'
            self.rules.append((keyword_pattern, formats['keyword']))
            self.rules.append((r'//.*', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
        
        # HTML
        elif self.language == 'html':
            self.rules.append((r'</?\w+', formats['keyword']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r'<!--.*-->', formats['comment']))
        
        # CSS
        elif self.language == 'css':
            self.rules.append((r'/\*.*?\*/', formats['comment']))
            self.rules.append((r'"[^"]*"', formats['string']))
            self.rules.append((r"'.*?'", formats['string']))
    
    def create_format(self, color, bold=False):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Weight.Bold)
        return fmt
    
    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)

# ==================== FAST CODE EDITOR ====================

class LRDFastEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.highlighter = LRDFastHighlighter(self.document())
        self.setup_editor()
        
    def setup_editor(self):
        font = QFont("Consolas", 11)
        self.setFont(font)
        self.setTabStopDistance(40)
        
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {LRD_THEME['bg_editor']};
                color: {LRD_THEME['text_editor']};
                selection-background-color: {LRD_THEME['primary']};
                selection-color: white;
                border: 1px solid {LRD_THEME['primary']};
                font-family: Consolas;
            }}
        """)

# ==================== FULLY TYPABLE TERMINAL ====================

class LRDTypableTerminal(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setup_terminal()
        self.command_history = []
        self.history_index = -1
        self.current_dir = os.getcwd()
        self.compiler_paths = {}
        self.detect_compilers()
        
        # Show initial prompt
        self.append_text("LRD TERMINAL - Type commands directly\n")
        self.append_text(f"Directory: {self.current_dir}\n")
        self.append_text("Type 'help' for commands\n")
        self.append_text("\n> ")
        
        # Store cursor position for prompt
        self.prompt_position = self.textCursor().position()
    
    def setup_terminal(self):
        self.setFont(QFont("Consolas", 10))
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {LRD_THEME['bg_terminal']};
                color: {LRD_THEME['text_editor']};
                border: 1px solid {LRD_THEME['primary']};
                font-family: Consolas;
            }}
        """)
    
    def detect_compilers(self):
        """Quick compiler detection"""
        compilers = {}
        
        # Quick checks
        for cmd in ['python3', 'python']:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, timeout=1)
                compilers['python'] = cmd
                break
            except:
                pass
        
        for cmd in ['node', 'javac', 'gcc', 'g++', 'php']:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, timeout=1)
                compilers[cmd] = cmd
            except:
                pass
        
        self.compiler_paths = compilers
    
    def append_text(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)
        self.insertPlainText(text)
        self.ensureCursorVisible()
    
    def keyPressEvent(self, event):
        # Handle Enter key
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            cursor = self.textCursor()
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            command_line = cursor.selectedText()[2:]  # Remove "> " prompt
            
            if command_line.strip():
                self.execute_command(command_line.strip())
            
            self.append_text("\n> ")
            self.prompt_position = self.textCursor().position()
        
        # Handle Up/Down for history
        elif event.key() == Qt.Key.Key_Up:
            if self.history_index > 0:
                self.history_index -= 1
                self.replace_current_line(self.command_history[self.history_index])
        
        elif event.key() == Qt.Key.Key_Down:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.replace_current_line(self.command_history[self.history_index])
        
        # Handle Ctrl+C for interrupt
        elif event.key() == Qt.Key.Key_C and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.append_text("^C\n> ")
            self.prompt_position = self.textCursor().position()
        
        # Handle Ctrl+L for clear
        elif event.key() == Qt.Key.Key_L and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.clear()
            self.append_text("LRD TERMINAL (Cleared)\n")
            self.append_text(f"Directory: {self.current_dir}\n> ")
            self.prompt_position = self.textCursor().position()
        
        # Default behavior
        else:
            super().keyPressEvent(event)
    
    def replace_current_line(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText("> " + text)
    
    def execute_command(self, command):
        # Add to history
        if not self.command_history or self.command_history[-1] != command:
            self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Special commands
        if command.lower() == 'help':
            self.show_help()
            return
        
        if command.lower() == 'clear':
            self.clear()
            self.append_text("LRD TERMINAL\n")
            self.append_text(f"Directory: {self.current_dir}\n> ")
            self.prompt_position = self.textCursor().position()
            return
        
        if command.lower().startswith('cd '):
            self.handle_cd(command)
            return
        
        # Execute command
        self.run_command(command)
    
    def handle_cd(self, command):
        path = command[3:].strip()
        try:
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
                    self.append_text(f"Directory not found: {path}\n")
                    return
            
            self.current_dir = os.getcwd()
            self.append_text(f"Changed to: {self.current_dir}\n")
        except Exception as e:
            self.append_text(f"Error: {str(e)}\n")
    
    def run_command(self, command):
        try:
            # Check if it's a file to execute
            if command.endswith('.py') and 'python' in self.compiler_paths:
                self.run_python(command)
            elif command.endswith('.js') and 'node' in self.compiler_paths:
                self.run_node(command)
            elif command.endswith('.java') and 'javac' in self.compiler_paths:
                self.run_java(command)
            else:
                # Run as shell command
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=self.current_dir,
                    timeout=10
                )
                
                if result.stdout:
                    self.append_text(result.stdout)
                if result.stderr:
                    self.append_text(f"Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.append_text("Command timed out\n")
        except Exception as e:
            self.append_text(f"Error: {str(e)}\n")
    
    def run_python(self, filename):
        if 'python' in self.compiler_paths:
            result = subprocess.run(
                [self.compiler_paths['python'], filename],
                capture_output=True,
                text=True,
                cwd=self.current_dir
            )
            
            if result.stdout:
                self.append_text(result.stdout)
            if result.stderr:
                self.append_text(f"Python Error: {result.stderr}")
    
    def run_node(self, filename):
        if 'node' in self.compiler_paths:
            result = subprocess.run(
                ['node', filename],
                capture_output=True,
                text=True,
                cwd=self.current_dir
            )
            
            if result.stdout:
                self.append_text(result.stdout)
            if result.stderr:
                self.append_text(f"Node Error: {result.stderr}")
    
    def run_java(self, filename):
        if 'javac' in self.compiler_paths:
            # Compile
            compile_result = subprocess.run(
                ['javac', filename],
                capture_output=True,
                text=True,
                cwd=self.current_dir
            )
            
            if compile_result.returncode != 0:
                self.append_text(f"Compilation Error: {compile_result.stderr}")
                return
            
            # Run
            class_name = os.path.splitext(filename)[0]
            run_result = subprocess.run(
                ['java', class_name],
                capture_output=True,
                text=True,
                cwd=self.current_dir
            )
            
            if run_result.stdout:
                self.append_text(run_result.stdout)
            if run_result.stderr:
                self.append_text(f"Java Error: {run_result.stderr}")
    
    def show_help(self):
        help_text = """
LRD Terminal Commands:
• cd [dir]          - Change directory
• python file.py    - Run Python script
• node file.js      - Run JavaScript
• javac file.java   - Compile Java
• java Class        - Run Java class
• clear             - Clear terminal
• help              - Show this help

Keyboard Shortcuts:
• Ctrl+C           - Interrupt command
• Ctrl+L           - Clear terminal
• Up/Down arrows   - Command history

Just type commands and press Enter!
"""
        self.append_text(help_text)

# ==================== FAST FILE EXPLORER ====================

class LRDFastFileExplorer(QTreeView):
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
                background-color: transparent;
                color: {LRD_THEME['text_primary']};
                border: none;
            }}
            QTreeView::item:selected {{
                background-color: {LRD_THEME['primary']};
                color: white;
            }}
        """)
        
        # Set icon size
        self.setIconSize(QSize(16, 16))
    
    def set_root_path(self, path: str):
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))

# ==================== FAST MAIN WINDOW ====================

class LRDFastCodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()
        
        # Create initial tab
        self.create_new_file()
        
        # Focus on editor
        QTimer.singleShot(100, self.focus_editor)
    
    def setup_window(self):
        self.setWindowTitle("LRD CODE EDITOR - FAST")
        self.setGeometry(100, 50, 1400, 800)
        self.setStyleSheet(SIMPLE_STYLESHEET)
        
        # Set window icon
        self.set_window_icon()
    
    def set_window_icon(self):
        # Try to load tlogo.png
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "tlogo.png")
        
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            # Simple fallback icon
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(LRD_THEME['primary']))
            self.setWindowIcon(QIcon(pixmap))
    
    def setup_variables(self):
        self.open_files = {}
        self.project_path = None
        self.font_size = 11
        self.current_language = 'python'
    
    def setup_ui(self):
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Toolbar
        self.create_toolbar(main_layout)
        
        # Main splitter (sidebar + editor)
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar
        self.create_sidebar()
        
        # Editor area
        self.create_editor_area()
        
        main_layout.addWidget(self.main_splitter, 1)
        
        # Terminal
        self.create_terminal(main_layout)
        
        # Status bar
        self.create_status_bar()
    
    def create_toolbar(self, parent_layout):
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 2, 5, 2)
        toolbar_layout.setSpacing(5)
        
        # Quick action buttons
        actions = [
            ("New", self.create_new_file, "Ctrl+N"),
            ("Open", self.open_file_dialog, "Ctrl+O"),
            ("Save", self.save_file, "Ctrl+S"),
            ("Run", self.run_current_file, "F5"),
        ]
        
        for text, callback, shortcut in actions:
            btn = QPushButton(text)
            btn.setToolTip(shortcut)
            btn.clicked.connect(callback)
            btn.setMinimumHeight(30)
            toolbar_layout.addWidget(btn)
        
        toolbar_layout.addStretch()
        
        # Language selector
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Python", "JavaScript", "HTML", "CSS", "Java", "C++", "C", "PHP"])
        self.language_combo.setCurrentText("Python")
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        
        toolbar_layout.addWidget(QLabel("Language:"))
        toolbar_layout.addWidget(self.language_combo)
        
        parent_layout.addWidget(toolbar)
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setMinimumWidth(200)
        sidebar.setMaximumWidth(300)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Explorer header
        header = QWidget()
        header.setFixedHeight(30)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(5, 0, 5, 0)
        
        title = QLabel("EXPLORER")
        title.setStyleSheet(f"color: {LRD_THEME['primary']}; font-weight: bold;")
        
        open_btn = QPushButton("📁")
        open_btn.setFixedSize(25, 25)
        open_btn.setToolTip("Open Folder")
        open_btn.clicked.connect(self.open_folder)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(open_btn)
        
        # File explorer
        self.file_explorer = LRDFastFileExplorer()
        self.file_explorer.doubleClicked.connect(self.on_file_double_clicked)
        
        layout.addWidget(header)
        layout.addWidget(self.file_explorer)
        
        self.main_splitter.addWidget(sidebar)
    
    def create_editor_area(self):
        editor_area = QWidget()
        layout = QVBoxLayout(editor_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        layout.addWidget(self.tab_widget)
        
        self.main_splitter.addWidget(editor_area)
        self.main_splitter.setSizes([200, 1200])
    
    def create_terminal(self, parent_layout):
        self.terminal = LRDTypableTerminal()
        self.terminal.setMinimumHeight(150)
        parent_layout.addWidget(self.terminal)
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {LRD_THEME['secondary']};")
        
        # Cursor position
        self.cursor_label = QLabel("Ln 1, Col 1")
        
        # File info
        self.file_label = QLabel("Untitled")
        
        # Add widgets
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.cursor_label)
        self.status_bar.addPermanentWidget(self.file_label)
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.create_new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        open_folder_action = QAction("Open Folder...", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        # Run menu
        run_menu = menubar.addMenu("Run")
        
        run_action = QAction("Run", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_current_file)
        run_menu.addAction(run_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        zoom_in = QAction("Zoom In", self)
        zoom_in.setShortcut("Ctrl++")
        zoom_in.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in)
        
        zoom_out = QAction("Zoom Out", self)
        zoom_out.setShortcut("Ctrl+-")
        zoom_out.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out)
    
    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+W"), self, self.close_current_tab)
        QShortcut(QKeySequence("Ctrl+Tab"), self, self.next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, self.previous_tab)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
    
    # ==================== EDITOR MANAGEMENT ====================
    
    def create_new_file(self):
        editor = LRDFastEditor()
        index = self.tab_widget.addTab(editor, "Untitled")
        self.tab_widget.setCurrentIndex(index)
        
        self.open_files[editor] = {
            'path': None,
            'saved': False,
            'modified': False,
            'language': 'python'
        }
        
        editor.cursorPositionChanged.connect(lambda: self.update_cursor_position(editor))
        editor.textChanged.connect(lambda: self.on_text_changed(editor))
        
        self.status_label.setText("New file created")
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
            "HTML Files (*.html);;"
            "CSS Files (*.css);;"
            "Java Files (*.java);;"
            "C++ Files (*.cpp);;"
            "C Files (*.c);;"
            "PHP Files (*.php)"
        )
        
        if file_path:
            self.open_file(file_path)
    
    def open_file(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            editor = LRDFastEditor()
            editor.setPlainText(content)
            
            filename = os.path.basename(file_path)
            index = self.tab_widget.addTab(editor, filename)
            self.tab_widget.setCurrentIndex(index)
            
            language = self.detect_language(file_path)
            self.open_files[editor] = {
                'path': file_path,
                'saved': True,
                'modified': False,
                'language': language
            }
            
            editor.cursorPositionChanged.connect(lambda: self.update_cursor_position(editor))
            editor.textChanged.connect(lambda: self.on_text_changed(editor))
            
            self.set_editor_language(editor, language)
            
            self.status_label.setText(f"Opened: {filename}")
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
                
                info['saved'] = True
                info['modified'] = False
                
                self.status_label.setText(f"Saved: {os.path.basename(info['path'])}")
                self.update_tab_title(editor)
                
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
            "All Files (*.*);;"
            "Python Files (*.py);;"
            "JavaScript Files (*.js);;"
            "HTML Files (*.html);;"
            "CSS Files (*.css);;"
            "Java Files (*.java);;"
            "C++ Files (*.cpp);;"
            "C Files (*.c);;"
            "PHP Files (*.php)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(editor.toPlainText())
                
                info = self.open_files.get(editor)
                if info:
                    info['path'] = file_path
                    info['saved'] = True
                    info['modified'] = False
                    info['language'] = self.detect_language(file_path)
                
                filename = os.path.basename(file_path)
                index = self.tab_widget.indexOf(editor)
                self.tab_widget.setTabText(index, filename)
                self.set_editor_language(editor, info['language'])
                
                self.status_label.setText(f"Saved as: {filename}")
                self.file_label.setText(filename)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
    
    def close_tab(self, index):
        widget = self.tab_widget.widget(index)
        if isinstance(widget, LRDFastEditor):
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
            if isinstance(widget, LRDFastEditor):
                info = self.open_files.get(widget)
                if info:
                    if info['path']:
                        self.file_label.setText(os.path.basename(info['path']))
                    else:
                        self.file_label.setText("Untitled")
                    
                    self.language_combo.setCurrentText(info['language'].capitalize())
                    self.update_cursor_position(widget)
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
    
    def on_text_changed(self, editor):
        info = self.open_files.get(editor)
        if info:
            info['modified'] = True
            self.update_tab_title(editor)
    
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
        }
        
        return language_map.get(ext, 'text')
    
    def set_editor_language(self, editor, language):
        if isinstance(editor, LRDFastEditor):
            editor.highlighter.set_language(language)
            self.language_combo.setCurrentText(language.capitalize())
    
    def on_language_changed(self, language):
        editor = self.get_current_editor()
        if editor:
            lang_lower = language.lower()
            self.open_files[editor]['language'] = lang_lower
            self.set_editor_language(editor, lang_lower)
    
    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folder:
            self.project_path = folder
            self.file_explorer.set_root_path(folder)
            self.status_label.setText(f"Project: {os.path.basename(folder)}")
    
    def on_file_double_clicked(self, index):
        path = self.file_explorer.model.filePath(index)
        if os.path.isfile(path):
            self.open_file(path)
    
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
        self.terminal.append_text(f"Running {info['language']} file: {os.path.basename(info['path'])}\n")
        
        try:
            if info['language'] == 'python':
                if 'python' in self.terminal.compiler_paths:
                    result = subprocess.run(
                        [self.terminal.compiler_paths['python'], info['path']],
                        capture_output=True,
                        text=True,
                        cwd=os.path.dirname(info['path'])
                    )
                    
                    if result.stdout:
                        self.terminal.append_text(result.stdout)
                    if result.stderr:
                        self.terminal.append_text(f"Error: {result.stderr}")
                else:
                    self.terminal.append_text("Python not found\n")
                    
            elif info['language'] == 'javascript':
                if 'node' in self.terminal.compiler_paths:
                    result = subprocess.run(
                        ['node', info['path']],
                        capture_output=True,
                        text=True,
                        cwd=os.path.dirname(info['path'])
                    )
                    
                    if result.stdout:
                        self.terminal.append_text(result.stdout)
                    if result.stderr:
                        self.terminal.append_text(f"Error: {result.stderr}")
                else:
                    self.terminal.append_text("Node.js not found\n")
                    
            elif info['language'] == 'html':
                webbrowser.open(f'file://{os.path.abspath(info["path"])}')
                self.terminal.append_text("Opened in web browser\n")
                
            else:
                self.terminal.append_text(f"Language {info['language']} execution not supported\n")
                return
            
            self.terminal.append_text("\nExecution completed\n")
            self.status_label.setText("Execution completed")
            
        except Exception as e:
            self.terminal.append_text(f"Error: {str(e)}\n")
            self.status_label.setText("Execution failed")
    
    def zoom_in(self):
        self.font_size = min(20, self.font_size + 1)
        self.update_font_size()
    
    def zoom_out(self):
        self.font_size = max(8, self.font_size - 1)
        self.update_font_size()
    
    def update_font_size(self):
        for editor in self.open_files.keys():
            if isinstance(editor, LRDFastEditor):
                font = editor.font()
                font.setPointSize(self.font_size)
                editor.setFont(font)
        self.status_label.setText(f"Font size: {self.font_size}")
    
    def get_current_editor(self):
        widget = self.tab_widget.currentWidget()
        if isinstance(widget, LRDFastEditor):
            return widget
        return None
    
    def closeEvent(self, event):
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
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("LRD Fast Code Editor")
    
    window = LRDFastCodeEditor()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
