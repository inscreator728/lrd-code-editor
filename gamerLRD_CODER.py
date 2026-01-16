# lrd_code_editor_ultimate_optimized.py
import sys
import os
import subprocess
import re
import webbrowser
import threading
import queue
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ==================== MODERN GAMER THEME CONSTANTS ====================

MODERN_GAMER_THEME = {
    # Modern Backgrounds with subtle gradients
    'bg_dark': '#0c0c0c',
    'bg_darker': '#090909',
    'bg_black': '#000000',
    'bg_surface': '#1a1010',
    'bg_surface_dark': '#120909',
    'bg_card': '#1a0f0f',
    
    # Primary Colors (Modern Reddish-Brown/JARVIS Theme)
    'primary': '#ff3d00',  # Brighter modern red-orange
    'primary_light': '#ff6d40',
    'primary_dark': '#d32f00',
    'primary_glow': '#ff5500',
    'primary_gradient': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff3d00, stop:1 #ff6d40)',
    
    # Secondary Colors (Modern Hacker Green)
    'secondary': '#00ff88',
    'secondary_light': '#66ffaa',
    'secondary_dark': '#00cc66',
    'secondary_glow': '#00ff99',
    'secondary_gradient': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00ff88, stop:1 #66ffaa)',
    
    # Accent Colors
    'accent': '#ff4081',
    'accent_light': '#ff79b0',
    'warning': '#ffb300',
    'info': '#ff8a00',
    'error': '#ff5252',
    'success': '#00e676',
    
    # Text Colors
    'text_primary': '#ff6d40',
    'text_secondary': '#ff8a65',
    'text_tertiary': '#ffa07a',
    'text_editor': '#00ff88',
    'text_terminal': '#00ffaa',
    'text_disabled': '#666666',
    
    # UI Elements
    'border': '#ff3d00',
    'border_light': '#ff6d40',
    'border_dark': '#d32f00',
    'border_gradient': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff3d00, stop:1 #ff6d40)',
    
    # Selection & Highlight
    'selection': '#441a1a',
    'selection_light': '#662626',
    'highlight': '#331a1a',
    'hover': '#2a1a1a',
    
    # Line Numbers
    'line_bg': '#1a0d0d',
    'line_fg': '#ff6d40',
    
    # Status Colors
    'status_ready': '#00ff88',
    'status_modified': '#ffb300',
    'status_error': '#ff5252',
    'status_warning': '#ffb300',
    'status_running': '#00b0ff',
    
    # Syntax Highlighting (Modern Hacker Theme)
    'syntax_keyword': '#ff4081',
    'syntax_builtin': '#ff8a00',
    'syntax_string': '#ffb300',
    'syntax_comment': '#888888',
    'syntax_function': '#ff6d40',
    'syntax_class': '#ff4081',
    'syntax_number': '#ff9800',
    'syntax_operator': '#ff8a65',
    'syntax_tag': '#ff4081',
    'syntax_attribute': '#ff9800',
    'syntax_variable': '#ff6d40',
    'syntax_import': '#00e5ff',
}

# ==================== MODERN OPTIMIZED STYLESHEET ====================

MODERN_GAMER_STYLESHEET = f"""
    /* Main Window - Modern Glass Effect */
    QMainWindow {{
        background-color: {MODERN_GAMER_THEME['bg_dark']};
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 8px;
    }}
    
    /* Menu Bar - Modern Gradient */
    QMenuBar {{
        background-color: {MODERN_GAMER_THEME['bg_surface_dark']};
        background: {MODERN_GAMER_THEME['primary_gradient']};
        color: #ffffff;
        border-bottom: 2px solid {MODERN_GAMER_THEME['border']};
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-family: 'Segoe UI', 'Consolas', monospace;
        font-weight: bold;
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 8px 15px;
        border-radius: 3px;
        margin: 2px;
    }}
    
    QMenuBar::item:selected {{
        background-color: rgba(255, 255, 255, 0.2);
        color: #ffffff;
    }}
    
    /* Modern Menus */
    QMenu {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        color: {MODERN_GAMER_THEME['text_primary']};
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 5px;
        padding: 5px;
    }}
    
    QMenu::item {{
        padding: 8px 30px 8px 20px;
        border-radius: 3px;
        margin: 2px;
    }}
    
    QMenu::item:selected {{
        background-color: {MODERN_GAMER_THEME['selection']};
        color: #ffffff;
    }}
    
    QMenu::separator {{
        height: 1px;
        background-color: {MODERN_GAMER_THEME['border']};
        margin: 5px 10px;
    }}
    
    /* Status Bar - Modern */
    QStatusBar {{
        background-color: {MODERN_GAMER_THEME['bg_surface_dark']};
        color: {MODERN_GAMER_THEME['text_secondary']};
        border-top: 1px solid {MODERN_GAMER_THEME['border']};
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
        font-family: 'Segoe UI', 'Consolas', monospace;
    }}
    
    /* Modern Buttons */
    QPushButton {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        color: {MODERN_GAMER_THEME['text_primary']};
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 6px;
        padding: 8px 15px;
        font-weight: bold;
        font-family: 'Segoe UI', 'Consolas', monospace;
        font-size: 12px;
    }}
    
    QPushButton:hover {{
        background-color: {MODERN_GAMER_THEME['selection']};
        border: 2px solid {MODERN_GAMER_THEME['primary_light']};
        color: #ffffff;
    }}
    
    QPushButton:pressed {{
        background-color: {MODERN_GAMER_THEME['primary_dark']};
        border: 2px solid {MODERN_GAMER_THEME['primary']};
        color: #ffffff;
    }}
    
    /* Modern ComboBox */
    QComboBox {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        color: {MODERN_GAMER_THEME['text_primary']};
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 6px;
        padding: 6px 10px;
        font-family: 'Segoe UI', 'Consolas', monospace;
        min-height: 25px;
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 25px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {MODERN_GAMER_THEME['primary']};
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        color: {MODERN_GAMER_THEME['text_primary']};
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 5px;
        selection-background-color: {MODERN_GAMER_THEME['selection']};
        selection-color: #ffffff;
        outline: none;
    }}
    
    /* Modern LineEdit */
    QLineEdit {{
        background-color: {MODERN_GAMER_THEME['bg_darker']};
        color: {MODERN_GAMER_THEME['text_editor']};
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 6px;
        padding: 8px 12px;
        font-family: 'Segoe UI', 'Consolas', monospace;
        font-size: 13px;
        selection-background-color: {MODERN_GAMER_THEME['selection']};
        selection-color: #ffffff;
    }}
    
    QLineEdit:focus {{
        border: 2px solid {MODERN_GAMER_THEME['secondary']};
        background-color: {MODERN_GAMER_THEME['bg_black']};
    }}
    
    /* Modern Tab Widget */
    QTabWidget::pane {{
        background-color: {MODERN_GAMER_THEME['bg_dark']};
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 5px;
        top: -1px;
    }}
    
    QTabBar::tab {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        color: {MODERN_GAMER_THEME['text_secondary']};
        padding: 10px 20px;
        border: 1px solid {MODERN_GAMER_THEME['border']};
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-family: 'Segoe UI', 'Consolas', monospace;
        font-weight: bold;
        margin-right: 2px;
        font-size: 12px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {MODERN_GAMER_THEME['bg_dark']};
        color: {MODERN_GAMER_THEME['primary']};
        border-top: 3px solid {MODERN_GAMER_THEME['primary']};
        font-size: 13px;
    }}
    
    QTabBar::tab:hover {{
        background-color: {MODERN_GAMER_THEME['selection_light']};
        color: #ffffff;
    }}
    
    /* Modern Dock Widget */
    QDockWidget {{
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 5px;
        titlebar-close-icon: url(close.png);
        titlebar-normal-icon: url(float.png);
    }}
    
    QDockWidget::title {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        background: {MODERN_GAMER_THEME['primary_gradient']};
        color: #ffffff;
        padding: 8px 15px;
        font-weight: bold;
        font-family: 'Segoe UI', 'Consolas', monospace;
        border-bottom: 1px solid {MODERN_GAMER_THEME['border']};
        text-align: center;
    }}
    
    /* Modern ScrollBar */
    QScrollBar:vertical {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        width: 14px;
        border-radius: 7px;
        margin: 2px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {MODERN_GAMER_THEME['primary']};
        border-radius: 7px;
        min-height: 25px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {MODERN_GAMER_THEME['primary_light']};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        border: none;
        background: none;
    }}
    
    QScrollBar:horizontal {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        height: 14px;
        border-radius: 7px;
        margin: 2px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {MODERN_GAMER_THEME['primary']};
        border-radius: 7px;
        min-width: 25px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {MODERN_GAMER_THEME['primary_light']};
    }}
    
    /* Modern TreeView (File Explorer) */
    QTreeView {{
        background-color: {MODERN_GAMER_THEME['bg_dark']};
        color: {MODERN_GAMER_THEME['text_primary']};
        border: none;
        font-family: 'Segoe UI', 'Consolas', monospace;
        font-size: 12px;
        outline: none;
    }}
    
    QTreeView::item {{
        height: 28px;
        padding: 4px 8px;
        border-radius: 3px;
    }}
    
    QTreeView::item:selected {{
        background-color: {MODERN_GAMER_THEME['selection']};
        color: #ffffff;
        font-weight: bold;
    }}
    
    QTreeView::item:hover {{
        background-color: {MODERN_GAMER_THEME['hover']};
    }}
    
    /* Modern Labels */
    QLabel {{
        background-color: transparent;
        font-family: 'Segoe UI', 'Consolas', monospace;
    }}
    
    /* Modern Text Edit */
    QTextEdit {{
        background-color: {MODERN_GAMER_THEME['bg_darker']};
        color: {MODERN_GAMER_THEME['text_editor']};
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 5px;
        font-family: 'Segoe UI', 'Consolas', monospace;
        font-size: 13px;
        padding: 5px;
        selection-background-color: {MODERN_GAMER_THEME['selection']};
        selection-color: #ffffff;
    }}
    
    /* Modern Checkbox */
    QCheckBox {{
        color: {MODERN_GAMER_THEME['text_primary']};
        font-family: 'Segoe UI', 'Consolas', monospace;
        spacing: 8px;
    }}
    
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 3px;
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {MODERN_GAMER_THEME['primary']};
        border: 1px solid {MODERN_GAMER_THEME['primary_light']};
        image: url(check.png);
    }}
    
    QCheckBox::indicator:unchecked {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        border: 1px solid {MODERN_GAMER_THEME['border']};
    }}
    
    /* Modern ToolTip */
    QToolTip {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        color: {MODERN_GAMER_THEME['text_primary']};
        border: 1px solid {MODERN_GAMER_THEME['border']};
        border-radius: 3px;
        padding: 5px;
        font-family: 'Segoe UI', 'Consolas', monospace;
    }}
    
    /* Modern Progress Bar */
    QProgressBar {{
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 5px;
        text-align: center;
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        color: {MODERN_GAMER_THEME['text_primary']};
        font-family: 'Segoe UI', 'Consolas', monospace;
    }}
    
    QProgressBar::chunk {{
        background-color: {MODERN_GAMER_THEME['primary']};
        border-radius: 3px;
    }}
    
    /* Modern Group Box */
    QGroupBox {{
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 5px;
        margin-top: 10px;
        font-family: 'Segoe UI', 'Consolas', monospace;
        font-weight: bold;
        color: {MODERN_GAMER_THEME['text_primary']};
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }}
    
    /* Modern Radio Button */
    QRadioButton {{
        color: {MODERN_GAMER_THEME['text_primary']};
        font-family: 'Segoe UI', 'Consolas', monospace;
        spacing: 8px;
    }}
    
    QRadioButton::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 9px;
    }}
    
    QRadioButton::indicator:checked {{
        background-color: {MODERN_GAMER_THEME['primary']};
        border: 4px solid {MODERN_GAMER_THEME['bg_surface']};
    }}
    
    QRadioButton::indicator:unchecked {{
        background-color: {MODERN_GAMER_THEME['bg_surface']};
        border: 2px solid {MODERN_GAMER_THEME['border']};
    }}
    
    /* Splitter */
    QSplitter::handle {{
        background-color: {MODERN_GAMER_THEME['border']};
        width: 4px;
        border-radius: 2px;
    }}
    
    QSplitter::handle:hover {{
        background-color: {MODERN_GAMER_THEME['primary_light']};
    }}
    
    /* Dialog */
    QDialog {{
        background-color: {MODERN_GAMER_THEME['bg_dark']};
        border: 2px solid {MODERN_GAMER_THEME['border']};
        border-radius: 8px;
    }}
"""

# ==================== THREAD POOL FOR ASYNC OPERATIONS ====================

class ThreadManager(QObject):
    """Manages threads for non-blocking operations"""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.running_tasks = {}
        self.task_counter = 0
    
    def run_command(self, command, cwd=None, task_name="Command"):
        """Run a command in a separate thread"""
        task_id = self.task_counter
        self.task_counter += 1
        
        def worker():
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=cwd,
                    timeout=60
                )
                
                if result.stdout:
                    self.output_signal.emit(result.stdout)
                if result.stderr:
                    self.error_signal.emit(result.stderr)
                
                self.finished_signal.emit(f"{task_name} completed")
                
            except subprocess.TimeoutExpired:
                self.error_signal.emit(f"{task_name} timed out after 60 seconds")
            except Exception as e:
                self.error_signal.emit(f"Error in {task_name}: {str(e)}")
            finally:
                if task_id in self.running_tasks:
                    del self.running_tasks[task_id]
        
        # Run in thread pool
        future = self.thread_pool.submit(worker)
        self.running_tasks[task_id] = future
        
        return task_id
    
    def stop_all(self):
        """Stop all running tasks"""
        for future in self.running_tasks.values():
            future.cancel()
        self.running_tasks.clear()

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
            'keyword': self.create_format(MODERN_GAMER_THEME['syntax_keyword'], bold=True),
            'builtin': self.create_format(MODERN_GAMER_THEME['syntax_builtin']),
            'string': self.create_format(MODERN_GAMER_THEME['syntax_string']),
            'comment': self.create_format(MODERN_GAMER_THEME['syntax_comment'], italic=True),
            'function': self.create_format(MODERN_GAMER_THEME['syntax_function'], bold=True),
            'class': self.create_format(MODERN_GAMER_THEME['syntax_class'], bold=True),
            'number': self.create_format(MODERN_GAMER_THEME['syntax_number']),
            'operator': self.create_format(MODERN_GAMER_THEME['syntax_operator']),
            'tag': self.create_format(MODERN_GAMER_THEME['syntax_tag'], bold=True),
            'attribute': self.create_format(MODERN_GAMER_THEME['syntax_attribute']),
            'variable': self.create_format(MODERN_GAMER_THEME['syntax_variable']),
            'import': self.create_format(MODERN_GAMER_THEME['syntax_import']),
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
            self.rules.append((r'\bimport\s+\w+', formats['import']))
            self.rules.append((r'\bfrom\s+\w+', formats['import']))
        
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
            self.rules.append((r'\bimport\s+[\w.]+;', formats['import']))
        
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
            self.rules.append((r'#include\s+[<"][^>"]*[>"]', formats['import']))
        
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
        fmt.setFontFamily("'Segoe UI', 'Consolas', monospace")
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
        # Font - Modern monospaced
        font = QFont("'Segoe UI', 'Consolas', monospace", 13)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        self.setTabStopDistance(40)
        
        # Colors and styling
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {MODERN_GAMER_THEME['bg_darker']};
                color: {MODERN_GAMER_THEME['text_editor']};
                selection-background-color: {MODERN_GAMER_THEME['selection']};
                selection-color: #ffffff;
                border: 2px solid {MODERN_GAMER_THEME['border']};
                border-radius: 5px;
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 13px;
                padding: 10px;
            }}
        """)
        
        # Cursor
        self.setCursorWidth(3)
        self.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
    
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
        return 15 + self.fontMetrics().horizontalAdvance('9') * digits
    
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
        painter.fillRect(event.rect(), QColor(MODERN_GAMER_THEME['line_bg']))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(MODERN_GAMER_THEME['line_fg']))
                painter.setFont(QFont("'Segoe UI', 'Consolas', monospace", 12))
                painter.drawText(0, top, self.line_number_area.width() - 8, 
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
            line_color = QColor(MODERN_GAMER_THEME['selection_light'])
            line_color.setAlpha(80)
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
    output_received = pyqtSignal(str)
    error_received = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_terminal()
        self.command_history = []
        self.history_index = -1
        self.current_dir = os.getcwd()
        self.compiler_paths = self.detect_compilers()
        self.thread_manager = ThreadManager()
        
        # Connect thread manager signals
        self.thread_manager.output_signal.connect(self.append_output)
        self.thread_manager.error_signal.connect(self.append_error)
        self.thread_manager.finished_signal.connect(self.append_finished)
        
        # Show welcome message
        self.append_welcome()
    
    def setup_terminal(self):
        # Make it read-only for output, but we'll handle input separately
        self.setReadOnly(True)
        self.setFont(QFont("'Segoe UI', 'Consolas', monospace", 12))
        
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {MODERN_GAMER_THEME['bg_black']};
                color: {MODERN_GAMER_THEME['text_terminal']};
                border: 2px solid {MODERN_GAMER_THEME['border']};
                border-radius: 5px;
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }}
        """)
    
    def detect_compilers(self):
        """Detect available compilers and interpreters"""
        compilers = {}
        
        # Python
        for cmd in ['python3', 'python']:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, check=True, timeout=2)
                compilers['python'] = cmd
                break
            except:
                pass
        
        # Node.js
        try:
            subprocess.run(['node', '--version'], capture_output=True, check=True, timeout=2)
            compilers['node'] = 'node'
        except:
            pass
        
        # PHP
        try:
            subprocess.run(['php', '--version'], capture_output=True, check=True, timeout=2)
            compilers['php'] = 'php'
        except:
            pass
        
        # Java
        try:
            subprocess.run(['java', '-version'], capture_output=True, check=True, timeout=2)
            compilers['java'] = 'java'
            compilers['javac'] = 'javac'
        except:
            pass
        
        # GCC/G++
        for cmd in ['gcc', 'g++']:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, check=True, timeout=2)
                compilers[cmd] = cmd
            except:
                pass
        
        # PowerShell (Windows)
        try:
            subprocess.run(['powershell', '-Command', 'echo test'], capture_output=True, check=True, timeout=2)
            compilers['powershell'] = 'powershell'
        except:
            pass
        
        return compilers
    
    def append_welcome(self):
        self.append(f"<span style='color:{MODERN_GAMER_THEME['primary']}; font-weight:bold; font-size:14px;'>◢◤ LRD ADVANCED TERMINAL v4.0 ◥◣</span>")
        self.append(f"<span style='color:{MODERN_GAMER_THEME['secondary']}'>Directory:</span> {self.current_dir}")
        self.append(f"<span style='color:{MODERN_GAMER_THEME['secondary']}'>Type 'help' for commands, 'clear' to clear terminal</span>")
        
        # Show detected compilers
        if self.compiler_paths:
            compilers_list = ', '.join(self.compiler_paths.keys())
            self.append(f"<span style='color:{MODERN_GAMER_THEME['secondary']}'>Available compilers:</span> {compilers_list}")
        
        self.append(f"<span style='color:{MODERN_GAMER_THEME['text_secondary']}'>Terminal is ALWAYS typeable - No file needs to be open!</span>")
        self.append("")
    
    def execute_command(self, command: str):
        if not command.strip():
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Show command
        self.append(f"<span style='color:{MODERN_GAMER_THEME['primary']}; font-weight:bold'>$</span> <span style='color:{MODERN_GAMER_THEME['text_editor']}'>{command}</span>")
        
        # Special commands
        if command.lower() == 'clear':
            self.clear()
            self.append_welcome()
            return
        
        if command.lower() == 'help':
            self.show_help()
            return
        
        if command.lower() == 'history':
            self.show_history()
            return
        
        if command.lower().startswith('cd '):
            self.handle_cd(command)
            return
        
        if command.lower() == 'pwd':
            self.append(f"<span style='color:{MODERN_GAMER_THEME['secondary']}'>{self.current_dir}</span>")
            return
        
        if command.lower() in ['ls', 'dir']:
            self.handle_ls()
            return
        
        # Run command in thread
        self.thread_manager.run_command(command, self.current_dir, f"Command: {command}")
    
    def handle_cd(self, command: str):
        path = command[3:].strip()
        try:
            if not path:
                return
            
            if path == "..":
                os.chdir("..")
            elif path == "~":
                os.chdir(os.path.expanduser("~"))
            elif os.path.isdir(path):
                os.chdir(path)
            else:
                # Try relative path
                new_path = os.path.join(self.current_dir, path)
                if os.path.isdir(new_path):
                    os.chdir(new_path)
                else:
                    self.append(f"<span style='color:{MODERN_GAMER_THEME['error']}'>Error: Directory '{path}' not found</span>")
                    return
            
            self.current_dir = os.getcwd()
            self.append(f"<span style='color:{MODERN_GAMER_THEME['success']}'>Directory changed to:</span> {self.current_dir}")
        except Exception as e:
            self.append(f"<span style='color:{MODERN_GAMER_THEME['error']}'>Error: {str(e)}</span>")
    
    def handle_ls(self):
        try:
            items = os.listdir(self.current_dir)
            files = []
            dirs = []
            
            for item in items:
                if os.path.isdir(os.path.join(self.current_dir, item)):
                    dirs.append(f"<span style='color:{MODERN_GAMER_THEME['primary']}'>📁 {item}/</span>")
                else:
                    ext = os.path.splitext(item)[1].lower()
                    if ext in ['.py', '.js', '.java', '.cpp', '.c', '.php', '.html', '.css', '.sh']:
                        files.append(f"<span style='color:{MODERN_GAMER_THEME['secondary']}'>📄 {item}</span>")
                    else:
                        files.append(f"<span style='color:{MODERN_GAMER_THEME['text_secondary']}'>📄 {item}</span>")
            
            # Display directories first
            if dirs:
                self.append("<br>".join(dirs))
            if files:
                self.append("<br>".join(files))
            
            self.append(f"<span style='color:{MODERN_GAMER_THEME['text_tertiary']}'>{len(dirs)} directories, {len(files)} files</span>")
            
        except Exception as e:
            self.append(f"<span style='color:{MODERN_GAMER_THEME['error']}'>Error: {str(e)}</span>")
    
    def show_help(self):
        help_text = f"""
<span style='color:{MODERN_GAMER_THEME['primary']}; font-size:14px;'>◢ LRD TERMINAL HELP ◣</span><br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}; font-weight:bold'>Basic Commands:</span><br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>cd [dir]</span>          - Change directory<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>ls / dir</span>         - List files<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>pwd</span>              - Show current directory<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>clear</span>            - Clear terminal<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>history</span>          - Show command history<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>help</span>             - Show this help<br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}; font-weight:bold'>Code Execution:</span><br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>python script.py</span>  - Run Python<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>node script.js</span>    - Run JavaScript<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>php script.php</span>    - Run PHP<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>javac Main.java</span>   - Compile Java<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>java Main</span>         - Run Java<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>gcc program.c</span>     - Compile C<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>g++ program.cpp</span>   - Compile C++<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>./program</span>        - Run executable<br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}; font-weight:bold'>File Operations:</span><br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>mkdir folder</span>      - Create directory<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>rm file</span>          - Remove file<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>cp src dst</span>        - Copy file<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>mv src dst</span>        - Move/rename<br>
  <span style='color:{MODERN_GAMER_THEME['text_editor']}'>cat file</span>         - View file content<br>
"""
        self.append(help_text)
    
    def show_history(self):
        if not self.command_history:
            self.append(f"<span style='color:{MODERN_GAMER_THEME['text_tertiary']}'>No command history</span>")
            return
        
        self.append(f"<span style='color:{MODERN_GAMER_THEME['secondary']}; font-weight:bold'>Command History:</span>")
        for i, cmd in enumerate(self.command_history[-10:]):  # Show last 10 commands
            self.append(f"  <span style='color:{MODERN_GAMER_THEME['text_primary']}'>{len(self.command_history)-10+i if len(self.command_history) > 10 else i}:</span> {cmd}")
    
    def get_previous_command(self):
        if self.history_index > 0:
            self.history_index -= 1
            return self.command_history[self.history_index]
        elif self.command_history:
            self.history_index = 0
            return self.command_history[0]
        return ""
    
    def get_next_command(self):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            return self.command_history[self.history_index]
        elif self.command_history:
            self.history_index = len(self.command_history) - 1
            return self.command_history[-1]
        return ""
    
    def append_output(self, text):
        self.append(f"<span style='color:{MODERN_GAMER_THEME['text_editor']}'>{text}</span>")
    
    def append_error(self, text):
        self.append(f"<span style='color:{MODERN_GAMER_THEME['error']}'>{text}</span>")
    
    def append_finished(self, text):
        self.append(f"<span style='color:{MODERN_GAMER_THEME['success']}'>{text}</span>")
    
    def append(self, text: str):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)
        
        if "<" in text and ">" in text and ("span" in text or "br" in text):
            self.insertHtml(text + "<br>")
        else:
            # Escape HTML and add as plain text
            plain_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            self.insertHtml(f"<span style='color:{MODERN_GAMER_THEME['text_editor']}'>{plain_text}</span><br>")
        
        # Scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

# ==================== ENHANCED FILE EXPLORER ====================

class LRDFileExplorer(QTreeView):
    file_double_clicked = pyqtSignal(str)
    folder_opened = pyqtSignal(str)
    file_context_menu = pyqtSignal(str, QPoint)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_explorer()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.doubleClicked.connect(self.on_double_click)
    
    def setup_explorer(self):
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.model.setNameFilterDisables(False)
        self.model.setNameFilters(["*.py", "*.js", "*.html", "*.css", "*.java", "*.cpp", "*.c", "*.php", "*.sh", "*.txt"])
        self.setModel(self.model)
        
        # Hide unnecessary columns (size, type, modified date)
        for i in range(1, 4):
            self.hideColumn(i)
        
        self.setHeaderHidden(True)
        
        # Set custom icons
        self.setIconSize(QSize(22, 22))
        
        # Apply theme
        self.setStyleSheet(f"""
            QTreeView {{
                background-color: {MODERN_GAMER_THEME['bg_dark']};
                color: {MODERN_GAMER_THEME['text_primary']};
                border: 2px solid {MODERN_GAMER_THEME['border']};
                border-radius: 5px;
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 12px;
                outline: none;
            }}
            QTreeView::item {{
                height: 28px;
                padding: 4px 8px;
                border-radius: 3px;
            }}
            QTreeView::item:selected {{
                background-color: {MODERN_GAMER_THEME['selection']};
                color: #ffffff;
                font-weight: bold;
            }}
            QTreeView::item:hover {{
                background-color: {MODERN_GAMER_THEME['hover']};
            }}
        """)
    
    def set_root_path(self, path: str):
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))
    
    def show_context_menu(self, position):
        index = self.indexAt(position)
        menu = QMenu()
        
        if index.isValid():
            path = self.model.filePath(index)
            is_dir = os.path.isdir(path)
            
            # Open file
            if not is_dir:
                open_action = QAction("📄 Open File", self)
                open_action.triggered.connect(lambda: self.file_double_clicked.emit(path))
                menu.addAction(open_action)
                
                # Open with default app
                open_with_action = QAction("🔧 Open with Default App", self)
                open_with_action.triggered.connect(lambda: self.open_with_default_app(path))
                menu.addAction(open_with_action)
            
            # Open folder
            if is_dir:
                open_folder_action = QAction("📁 Open Folder", self)
                open_folder_action.triggered.connect(lambda: self.folder_opened.emit(path))
                menu.addAction(open_folder_action)
            
            menu.addSeparator()
            
            # Rename
            rename_action = QAction("✏️ Rename", self)
            rename_action.triggered.connect(lambda: self.rename_item(index))
            menu.addAction(rename_action)
            
            # Delete
            delete_action = QAction("🗑️ Delete", self)
            delete_action.triggered.connect(lambda: self.delete_item(index))
            menu.addAction(delete_action)
            
            menu.addSeparator()
            
            # Copy path
            copy_path_action = QAction("📋 Copy Path", self)
            copy_path_action.triggered.connect(lambda: self.copy_path(path))
            menu.addAction(copy_path_action)
        
        # Add create options
        create_menu = QMenu("➕ Create New", self)
        
        new_file_action = QAction("📄 New File", self)
        new_file_action.triggered.connect(lambda: self.create_new_file(position))
        create_menu.addAction(new_file_action)
        
        new_folder_action = QAction("📁 New Folder", self)
        new_folder_action.triggered.connect(lambda: self.create_new_folder(position))
        create_menu.addAction(new_folder_action)
        
        menu.addMenu(create_menu)
        
        menu.addSeparator()
        
        # Refresh
        refresh_action = QAction("🔄 Refresh", self)
        refresh_action.triggered.connect(self.refresh)
        menu.addAction(refresh_action)
        
        # Open in terminal
        open_terminal_action = QAction("💻 Open in Terminal", self)
        if index.isValid():
            path = self.model.filePath(index) if os.path.isdir(self.model.filePath(index)) else os.path.dirname(self.model.filePath(index))
        else:
            path = self.model.rootPath() if self.model.rootPath() else os.getcwd()
        open_terminal_action.triggered.connect(lambda: self.open_in_terminal(path))
        menu.addAction(open_terminal_action)
        
        # Show properties
        if index.isValid():
            menu.addSeparator()
            properties_action = QAction("📊 Properties", self)
            properties_action.triggered.connect(lambda: self.show_properties(path))
            menu.addAction(properties_action)
        
        menu.exec(self.viewport().mapToGlobal(position))
    
    def on_double_click(self, index):
        if index.isValid():
            path = self.model.filePath(index)
            if os.path.isdir(path):
                # Toggle expansion
                if self.isExpanded(index):
                    self.collapse(index)
                else:
                    self.expand(index)
            else:
                # Emit signal for file opening
                self.file_double_clicked.emit(path)
    
    def open_with_default_app(self, path):
        """Open file with default system application"""
        try:
            if sys.platform == 'win32':
                os.startfile(path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', path], check=True)
            else:
                subprocess.run(['xdg-open', path], check=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")
    
    def rename_item(self, index):
        self.edit(index)
    
    def delete_item(self, index):
        path = self.model.filePath(index)
        reply = QMessageBox.question(
            self,
            "Delete Item",
            f"Are you sure you want to delete '{os.path.basename(path)}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                import shutil
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete: {str(e)}")
    
    def copy_path(self, path):
        clipboard = QApplication.clipboard()
        clipboard.setText(path)
        QMessageBox.information(self, "Copied", "File path copied to clipboard")
    
    def create_new_file(self, position):
        index = self.indexAt(position)
        if index.isValid():
            path = self.model.filePath(index)
            if os.path.isdir(path):
                parent_dir = path
            else:
                parent_dir = os.path.dirname(path)
        else:
            parent_dir = self.model.rootPath() if self.model.rootPath() else os.getcwd()
        
        # Create new file dialog
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Create New File")
        dialog.setLabelText("Enter filename:")
        dialog.setTextValue("new_file.py")
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {MODERN_GAMER_THEME['bg_dark']};
                border: 2px solid {MODERN_GAMER_THEME['border']};
            }}
            QLabel {{
                color: {MODERN_GAMER_THEME['text_primary']};
            }}
            QLineEdit {{
                background-color: {MODERN_GAMER_THEME['bg_darker']};
                color: {MODERN_GAMER_THEME['text_editor']};
                border: 2px solid {MODERN_GAMER_THEME['border']};
            }}
        """)
        
        if dialog.exec():
            filename = dialog.textValue()
            if filename:
                file_path = os.path.join(parent_dir, filename)
                try:
                    with open(file_path, 'w') as f:
                        f.write("")
                    self.refresh()
                    # Select the new file
                    new_index = self.model.index(file_path)
                    self.setCurrentIndex(new_index)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create file: {str(e)}")
    
    def create_new_folder(self, position):
        index = self.indexAt(position)
        if index.isValid():
            path = self.model.filePath(index)
            if os.path.isdir(path):
                parent_dir = path
            else:
                parent_dir = os.path.dirname(path)
        else:
            parent_dir = self.model.rootPath() if self.model.rootPath() else os.getcwd()
        
        # Create new folder dialog
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Create New Folder")
        dialog.setLabelText("Enter folder name:")
        dialog.setTextValue("New Folder")
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {MODERN_GAMER_THEME['bg_dark']};
                border: 2px solid {MODERN_GAMER_THEME['border']};
            }}
            QLabel {{
                color: {MODERN_GAMER_THEME['text_primary']};
            }}
            QLineEdit {{
                background-color: {MODERN_GAMER_THEME['bg_darker']};
                color: {MODERN_GAMER_THEME['text_editor']};
                border: 2px solid {MODERN_GAMER_THEME['border']};
            }}
        """)
        
        if dialog.exec():
            foldername = dialog.textValue()
            if foldername:
                folder_path = os.path.join(parent_dir, foldername)
                try:
                    os.makedirs(folder_path, exist_ok=True)
                    self.refresh()
                    # Select the new folder
                    new_index = self.model.index(folder_path)
                    self.setCurrentIndex(new_index)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create folder: {str(e)}")
    
    def refresh(self):
        self.model.setRootPath(self.model.rootPath())
    
    def open_in_terminal(self, path):
        # This will be handled by the main window
        return path
    
    def show_properties(self, path):
        """Show file/folder properties"""
        try:
            stats = os.stat(path)
            size = stats.st_size
            modified = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            created = datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            
            is_dir = os.path.isdir(path)
            item_type = "Directory" if is_dir else "File"
            
            # Count files if directory
            if is_dir:
                file_count = sum(1 for _ in os.listdir(path))
                size_info = f"{file_count} items"
            else:
                # Convert size to human readable format
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size < 1024.0:
                        size_info = f"{size:.2f} {unit}"
                        break
                    size /= 1024.0
            
            properties_text = f"""
<span style='color:{MODERN_GAMER_THEME['primary']}; font-size:16px;'>📊 Properties</span><br><br>
<span style='color:{MODERN_GAMER_THEME['secondary']}'>Name:</span> {os.path.basename(path)}<br>
<span style='color:{MODERN_GAMER_THEME['secondary']}'>Type:</span> {item_type}<br>
<span style='color:{MODERN_GAMER_THEME['secondary']}'>Size:</span> {size_info}<br>
<span style='color:{MODERN_GAMER_THEME['secondary']}'>Location:</span> {os.path.dirname(path)}<br>
<span style='color:{MODERN_GAMER_THEME['secondary']}'>Created:</span> {created}<br>
<span style='color:{MODERN_GAMER_THEME['secondary']}'>Modified:</span> {modified}<br>
<span style='color:{MODERN_GAMER_THEME['secondary']}'>Permissions:</span> {oct(stats.st_mode)[-3:]}<br>
"""
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Properties")
            dialog.setFixedSize(400, 300)
            dialog.setStyleSheet(f"""
                QDialog {{
                    background-color: {MODERN_GAMER_THEME['bg_dark']};
                    border: 2px solid {MODERN_GAMER_THEME['border']};
                    border-radius: 8px;
                }}
            """)
            
            layout = QVBoxLayout(dialog)
            
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setHtml(properties_text)
            text_edit.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {MODERN_GAMER_THEME['bg_darker']};
                    color: {MODERN_GAMER_THEME['text_editor']};
                    border: 1px solid {MODERN_GAMER_THEME['border']};
                    border-radius: 5px;
                    font-family: 'Segoe UI', 'Consolas', monospace;
                    font-size: 12px;
                }}
            """)
            
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(dialog.close)
            close_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {MODERN_GAMER_THEME['bg_surface']};
                    color: {MODERN_GAMER_THEME['primary']};
                    border: 2px solid {MODERN_GAMER_THEME['border']};
                    border-radius: 5px;
                    padding: 8px;
                    font-weight: bold;
                    font-family: 'Segoe UI', 'Consolas', monospace;
                }}
                QPushButton:hover {{
                    background-color: {MODERN_GAMER_THEME['selection']};
                    border: 2px solid {MODERN_GAMER_THEME['primary_light']};
                    color: #ffffff;
                }}
            """)
            
            layout.addWidget(text_edit)
            layout.addWidget(close_btn)
            
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get properties: {str(e)}")

# ==================== MAIN WINDOW ====================

class LRDCodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread_manager = ThreadManager()
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
        self.setWindowTitle("◢◤ LRD CODE EDITOR - MODERN GAMER EDITION ◥◣")
        self.setGeometry(100, 50, 1600, 900)
        
        # Set window icon
        self.set_window_icon()
        
        # Apply modern theme
        self.setStyleSheet(MODERN_GAMER_STYLESHEET)
        
        # Enable transparency for modern look
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    
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
        
        # Draw modern LRD gaming logo
        painter.setPen(QPen(QColor(MODERN_GAMER_THEME['primary']), 3))
        painter.setBrush(QColor(MODERN_GAMER_THEME['primary']))
        painter.drawRoundedRect(10, 10, 44, 44, 10, 10)
        
        painter.setPen(QPen(QColor(MODERN_GAMER_THEME['secondary']), 2))
        painter.setFont(QFont("'Segoe UI', 'Consolas', monospace", 16, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "LRD")
        
        painter.end()
        self.setWindowIcon(QIcon(pixmap))
    
    def setup_variables(self):
        self.current_file = None
        self.open_files = {}
        self.project_path = None
        self.font_size = 13
        self.current_language = 'python'
        self.theme = MODERN_GAMER_THEME
        self.is_running = False
        self.current_process = None
    
    def setup_ui(self):
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
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
        title_bar.setFixedHeight(45)
        title_bar.setStyleSheet(f"""
            QWidget {{
                background: {self.theme['primary_gradient']};
                border: 2px solid {self.theme['border']};
                border-radius: 8px;
                border-bottom-left-radius: 0;
                border-bottom-right-radius: 0;
            }}
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Logo
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "tlogo.png")
            if os.path.exists(icon_path):
                logo_label = QLabel()
                pixmap = QPixmap(icon_path).scaled(32, 32, 
                                                   Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(pixmap)
                layout.addWidget(logo_label)
        except:
            pass
        
        # Title
        title = QLabel("◢◤ LRD CODE EDITOR - MODERN GAMER EDITION ◥◣")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: #ffffff;
            font-family: 'Segoe UI', 'Consolas', monospace;
            padding-left: 10px;
        """)
        
        layout.addWidget(title)
        layout.addStretch()
        
        # Status indicator
        self.status_indicator = QLabel("● READY")
        self.status_indicator.setStyleSheet(f"""
            font-size: 12px;
            font-weight: bold;
            color: {self.theme['status_ready']};
            background: rgba(0, 0, 0, 0.3);
            padding: 5px 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            font-family: 'Segoe UI', 'Consolas', monospace;
        """)
        
        # Time display
        self.time_display = QLabel("")
        self.time_display.setStyleSheet(f"""
            font-size: 13px;
            color: #ffffff;
            background: rgba(0, 0, 0, 0.3);
            padding: 5px 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            font-family: 'Segoe UI', 'Consolas', monospace;
        """)
        
        layout.addWidget(self.status_indicator)
        layout.addSpacing(10)
        layout.addWidget(self.time_display)
        
        parent_layout.addWidget(title_bar)
    
    def create_main_content(self, parent_layout):
        # Create splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #444444;
                width: 3px;
                border-radius: 1px;
            }
            QSplitter::handle:hover {
                background-color: #666666;
            }
        """)
        
        # Sidebar
        self.create_sidebar()
        
        # Editor area
        self.create_editor_area()
        
        parent_layout.addWidget(self.main_splitter, 1)
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setMinimumWidth(280)
        sidebar.setMaximumWidth(400)
        sidebar.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg_dark']};
                border: 2px solid {self.theme['border']};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Explorer header with icons
        explorer_header = QWidget()
        explorer_header.setFixedHeight(45)
        explorer_header.setStyleSheet(f"""
            QWidget {{
                background: {self.theme['primary_gradient']};
                border-bottom: 2px solid {self.theme['border']};
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
        """)
        
        header_layout = QHBoxLayout(explorer_header)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        explorer_title = QLabel("📁 EXPLORER")
        explorer_title.setStyleSheet(f"""
            color: #ffffff;
            font-weight: bold;
            font-size: 14px;
            font-family: 'Segoe UI', 'Consolas', monospace;
        """)
        
        # Buttons with icons
        buttons = [
            ("📄", "New File", self.create_new_file_from_explorer),
            ("📁", "New Folder", self.create_new_folder_from_explorer),
            ("📂", "Open Folder (Ctrl+E)", self.open_folder),
            ("🔄", "Refresh", self.refresh_explorer),
            ("⚙️", "Settings", self.show_explorer_settings),
        ]
        
        header_layout.addWidget(explorer_title)
        header_layout.addStretch()
        
        for icon, tooltip, callback in buttons:
            btn = self.create_sidebar_button(icon, tooltip)
            btn.clicked.connect(callback)
            header_layout.addWidget(btn)
        
        # File explorer
        self.file_explorer = LRDFileExplorer()
        self.file_explorer.file_double_clicked.connect(self.open_file)
        self.file_explorer.folder_opened.connect(self.open_folder_path)
        
        layout.addWidget(explorer_header)
        layout.addWidget(self.file_explorer)
        
        self.main_splitter.addWidget(sidebar)
    
    def create_sidebar_button(self, icon, tooltip):
        btn = QPushButton(icon)
        btn.setFixedSize(32, 32)
        btn.setToolTip(tooltip)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 0, 0, 0.3);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                font-size: 14px;
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }}
            QPushButton:pressed {{
                background-color: rgba(255, 255, 255, 0.1);
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
        self.tab_widget.setMovable(True)
        
        layout.addWidget(self.tab_widget)
        
        self.main_splitter.addWidget(editor_area)
        self.main_splitter.setSizes([280, 1320])
    
    def create_editor_toolbar(self, parent_layout):
        toolbar = QWidget()
        toolbar.setFixedHeight(50)
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg_surface_dark']};
                border-bottom: 2px solid {self.theme['border']};
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Action buttons with icons
        actions = [
            ("📝 NEW", self.create_new_file, "Ctrl+N"),
            ("📂 OPEN", self.open_file_dialog, "Ctrl+O"),
            ("💾 SAVE", self.save_file, "Ctrl+S"),
            ("💾💾 SAVE ALL", self.save_all_files, "Ctrl+Shift+S"),
            ("▶️ RUN", self.run_current_file_async, "F5"),
            ("⏹️ STOP", self.stop_running_program, "Ctrl+."),
        ]
        
        for text, callback, shortcut in actions:
            btn = self.create_toolbar_button(f"{text}", shortcut)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Language selector
        lang_label = QLabel("📝 LANGUAGE:")
        lang_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Segoe UI', 'Consolas', monospace; font-size: 12px;")
        
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "Python", "JavaScript", "HTML", "CSS", 
            "Java", "C++", "C", "PHP", "Bash", "Text"
        ])
        self.language_combo.setCurrentText("Python")
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        self.language_combo.setMinimumWidth(120)
        
        layout.addWidget(lang_label)
        layout.addWidget(self.language_combo)
        layout.addSpacing(20)
        
        # Font size
        font_label = QLabel("🔤 FONT:")
        font_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Segoe UI', 'Consolas', monospace; font-size: 12px;")
        
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["10", "11", "12", "13", "14", "15", "16", "18", "20"])
        self.font_size_combo.setCurrentText("13")
        self.font_size_combo.currentTextChanged.connect(self.on_font_size_changed)
        self.font_size_combo.setMinimumWidth(60)
        
        layout.addWidget(font_label)
        layout.addWidget(self.font_size_combo)
        
        parent_layout.addWidget(toolbar)
    
    def create_toolbar_button(self, text, shortcut):
        btn = QPushButton(f"{text}")
        btn.setMinimumHeight(36)
        btn.setToolTip(shortcut)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['bg_surface']};
                color: {self.theme['text_primary']};
                border: 2px solid {self.theme['border']};
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
                min-width: 90px;
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['selection']};
                border: 2px solid {self.theme['primary_light']};
                color: #ffffff;
            }}
            QPushButton:pressed {{
                background-color: {self.theme['primary_dark']};
                border: 2px solid {self.theme['primary']};
                transform: translateY(1px);
            }}
        """)
        return btn
    
    def create_terminal(self, parent_layout):
        # Terminal widget
        self.terminal = LRDTerminal()
        
        # Terminal input (ALWAYS TYPEABLE)
        terminal_input = QWidget()
        terminal_input.setFixedHeight(45)
        terminal_input.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg_surface_dark']};
                border-top: 2px solid {self.theme['border']};
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(terminal_input)
        layout.setContentsMargins(15, 0, 15, 0)
        
        prompt = QLabel("💻 $")
        prompt.setStyleSheet(f"""
            color: {self.theme['primary']};
            font-weight: bold;
            font-size: 16px;
            font-family: 'Segoe UI', 'Consolas', monospace;
        """)
        prompt.setFixedWidth(30)
        
        self.terminal_input = QLineEdit()
        self.terminal_input.setPlaceholderText("Type any command and press Enter (Up/Down for history)... Terminal is ALWAYS typeable!")
        self.terminal_input.returnPressed.connect(self.execute_terminal_command)
        
        # Connect key events for history navigation
        self.terminal_input.keyPressEvent = self.terminal_keyPressEvent
        
        # Buttons
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.setFixedWidth(80)
        clear_btn.clicked.connect(lambda: self.terminal.execute_command("clear"))
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['bg_surface']};
                color: {self.theme['text_primary']};
                border: 2px solid {self.theme['border']};
                border-radius: 6px;
                padding: 5px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
            QPushButton:hover {{
                background-color: {self.theme['selection']};
                border: 2px solid {self.theme['primary_light']};
                color: #ffffff;
            }}
        """)
        
        kill_btn = QPushButton("⏹️ Stop")
        kill_btn.setFixedWidth(80)
        kill_btn.clicked.connect(self.stop_terminal_process)
        kill_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['error']};
                color: #ffffff;
                border: 2px solid {self.theme['border']};
                border-radius: 6px;
                padding: 5px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
            QPushButton:hover {{
                background-color: #ff3333;
                border: 2px solid {self.theme['primary_light']};
            }}
        """)
        
        layout.addWidget(prompt)
        layout.addWidget(self.terminal_input, 1)
        layout.addWidget(clear_btn)
        layout.addWidget(kill_btn)
        
        # Terminal container
        terminal_container = QWidget()
        terminal_container.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg_dark']};
                border-radius: 8px;
            }}
        """)
        
        terminal_layout = QVBoxLayout(terminal_container)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        terminal_layout.setSpacing(0)
        
        terminal_layout.addWidget(self.terminal, 1)
        terminal_layout.addWidget(terminal_input)
        
        # Create dock widget
        self.terminal_dock = QDockWidget("💻 TERMINAL", self)
        self.terminal_dock.setWidget(terminal_container)
        self.terminal_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable | 
            QDockWidget.DockWidgetFeature.DockWidgetFloatable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
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
            font-family: 'Segoe UI', 'Consolas', monospace;
            font-size: 12px;
        """)
        
        # Cursor position
        self.cursor_label = QLabel("📏 Ln 1, Col 1")
        self.cursor_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Segoe UI', 'Consolas', monospace; font-size: 11px;")
        
        # File info
        self.file_label = QLabel("📄 Untitled")
        self.file_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Segoe UI', 'Consolas', monospace; font-size: 11px;")
        
        # Language
        self.language_label = QLabel("🐍 Python")
        self.language_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Segoe UI', 'Consolas', monospace; font-size: 11px;")
        
        # Line count
        self.line_count_label = QLabel("📊 Lines: 0")
        self.line_count_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Segoe UI', 'Consolas', monospace; font-size: 11px;")
        
        # Encoding
        self.encoding_label = QLabel("🔤 UTF-8")
        self.encoding_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-family: 'Segoe UI', 'Consolas', monospace; font-size: 11px;")
        
        # Add widgets
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.cursor_label)
        self.status_bar.addPermanentWidget(self.file_label)
        self.status_bar.addPermanentWidget(self.language_label)
        self.status_bar.addPermanentWidget(self.line_count_label)
        self.status_bar.addPermanentWidget(self.encoding_label)
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        
        new_action = QAction("📝 New File", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.create_new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("📂 Open File...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        open_folder_action = QAction("📁 Open Folder...", self)
        open_folder_action.setShortcut("Ctrl+E")
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("💾 Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("💾 Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)
        
        save_all_action = QAction("💾💾 Save All", self)
        save_all_action.setShortcut("Ctrl+Alt+S")
        save_all_action.triggered.connect(self.save_all_files)
        file_menu.addAction(save_all_action)
        
        file_menu.addSeparator()
        
        close_action = QAction("❌ Close Tab", self)
        close_action.setShortcut("Ctrl+W")
        close_action.triggered.connect(self.close_current_tab)
        file_menu.addAction(close_action)
        
        close_all_action = QAction("❌ Close All", self)
        close_all_action.triggered.connect(self.close_all_tabs)
        file_menu.addAction(close_all_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("🚪 Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("✏️ Edit")
        
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
        
        paste_action = QAction("📝 Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        select_all_action = QAction("📄 Select All", self)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self.select_all)
        edit_menu.addAction(select_all_action)
        
        edit_menu.addSeparator()
        
        find_action = QAction("🔍 Find...", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.find_text)
        edit_menu.addAction(find_action)
        
        replace_action = QAction("🔄 Replace...", self)
        replace_action.setShortcut("Ctrl+H")
        replace_action.triggered.connect(self.replace_text)
        edit_menu.addAction(replace_action)
        
        # Run menu
        run_menu = menubar.addMenu("▶️ Run")
        
        run_action = QAction("▶️ Run Current File", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_current_file_async)
        run_menu.addAction(run_action)
        
        run_selection_action = QAction("▶️ Run Selection", self)
        run_selection_action.setShortcut("F6")
        run_selection_action.triggered.connect(self.run_selection_async)
        run_menu.addAction(run_selection_action)
        
        stop_action = QAction("⏹️ Stop Execution", self)
        stop_action.setShortcut("Ctrl+.")
        stop_action.triggered.connect(self.stop_running_program)
        run_menu.addAction(stop_action)
        
        # View menu
        view_menu = menubar.addMenu("👁️ View")
        
        toggle_sidebar_action = QAction("📁 Toggle Sidebar", self)
        toggle_sidebar_action.setShortcut("Ctrl+B")
        toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        view_menu.addAction(toggle_sidebar_action)
        
        toggle_terminal_action = QAction("💻 Toggle Terminal", self)
        toggle_terminal_action.setShortcut("Ctrl+`")
        toggle_terminal_action.triggered.connect(self.toggle_terminal)
        view_menu.addAction(toggle_terminal_action)
        
        view_menu.addSeparator()
        
        increase_font_action = QAction("🔤 Increase Font Size", self)
        increase_font_action.setShortcut("Ctrl++")
        increase_font_action.triggered.connect(self.increase_font_size)
        view_menu.addAction(increase_font_action)
        
        decrease_font_action = QAction("🔤 Decrease Font Size", self)
        decrease_font_action.setShortcut("Ctrl+-")
        decrease_font_action.triggered.connect(self.decrease_font_size)
        view_menu.addAction(decrease_font_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("⚙️ Tools")
        
        format_code_action = QAction("✨ Format Code", self)
        format_code_action.setShortcut("Ctrl+Shift+F")
        format_code_action.triggered.connect(self.format_code)
        tools_menu.addAction(format_code_action)
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        
        docs_action = QAction("📚 Documentation", self)
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)
        
        shortcuts_action = QAction("⌨️ Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("ℹ️ About LRD", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_shortcuts(self):
        # Tab navigation
        QShortcut(QKeySequence("Ctrl+W"), self, self.close_current_tab)
        QShortcut(QKeySequence("Ctrl+Tab"), self, self.next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, self.previous_tab)
        QShortcut(QKeySequence("Ctrl+PageUp"), self, self.previous_tab)
        QShortcut(QKeySequence("Ctrl+PageDown"), self, self.next_tab)
        
        # File operations
        QShortcut(QKeySequence("Ctrl+E"), self, self.open_folder)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        
        # Editor operations
        QShortcut(QKeySequence("Ctrl+F"), self, self.find_text)
        QShortcut(QKeySequence("Ctrl+H"), self, self.replace_text)
        QShortcut(QKeySequence("Ctrl+D"), self, self.duplicate_line)
        QShortcut(QKeySequence("Ctrl+/"), self, self.toggle_comment)
        QShortcut(QKeySequence("Ctrl+Shift+F"), self, self.format_code)
        
        # Run shortcuts
        QShortcut(QKeySequence("F5"), self, self.run_current_file_async)
        QShortcut(QKeySequence("F6"), self, self.run_selection_async)
        QShortcut(QKeySequence("Ctrl+."), self, self.stop_running_program)
        
        # View shortcuts
        QShortcut(QKeySequence("Ctrl+B"), self, self.toggle_sidebar)
        QShortcut(QKeySequence("Ctrl+`"), self, self.toggle_terminal)
        QShortcut(QKeySequence("Ctrl++"), self, self.increase_font_size)
        QShortcut(QKeySequence("Ctrl+-"), self, self.decrease_font_size)
    
    def setup_timers(self):
        # Clock timer
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()
    
    # ==================== ENHANCED FILE EXPLORER FUNCTIONS ====================
    
    def create_new_file_from_explorer(self):
        # Get current directory from explorer
        current_dir = self.file_explorer.model.rootPath() if self.file_explorer.model.rootPath() else os.getcwd()
        
        # Create new file dialog
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Create New File")
        dialog.setLabelText("Enter filename:")
        dialog.setTextValue("new_file.py")
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {self.theme['bg_dark']};
                border: 2px solid {self.theme['border']};
                border-radius: 8px;
            }}
            QLabel {{
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
            QLineEdit {{
                background-color: {self.theme['bg_darker']};
                color: {self.theme['text_editor']};
                border: 2px solid {self.theme['border']};
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
        """)
        
        if dialog.exec():
            filename = dialog.textValue()
            if filename:
                file_path = os.path.join(current_dir, filename)
                try:
                    with open(file_path, 'w') as f:
                        f.write("")
                    
                    # Refresh explorer
                    self.file_explorer.refresh()
                    
                    # Open the new file
                    self.open_file(file_path)
                    
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create file: {str(e)}")
    
    def create_new_folder_from_explorer(self):
        # Get current directory from explorer
        current_dir = self.file_explorer.model.rootPath() if self.file_explorer.model.rootPath() else os.getcwd()
        
        # Create new folder dialog
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Create New Folder")
        dialog.setLabelText("Enter folder name:")
        dialog.setTextValue("New Folder")
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {self.theme['bg_dark']};
                border: 2px solid {self.theme['border']};
                border-radius: 8px;
            }}
            QLabel {{
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
            QLineEdit {{
                background-color: {self.theme['bg_darker']};
                color: {self.theme['text_editor']};
                border: 2px solid {self.theme['border']};
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
        """)
        
        if dialog.exec():
            foldername = dialog.textValue()
            if foldername:
                folder_path = os.path.join(current_dir, foldername)
                try:
                    os.makedirs(folder_path, exist_ok=True)
                    
                    # Refresh explorer
                    self.file_explorer.refresh()
                    
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create folder: {str(e)}")
    
    def open_folder_path(self, path):
        """Open a specific folder path"""
        if os.path.isdir(path):
            self.project_path = path
            self.file_explorer.set_root_path(path)
            self.update_status(f"Opened folder: {os.path.basename(path)}", "ready")
    
    def show_explorer_settings(self):
        """Show explorer settings dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Explorer Settings")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {self.theme['bg_dark']};
                border: 2px solid {self.theme['border']};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(dialog)
        
        # Settings options
        show_hidden = QCheckBox("Show hidden files")
        show_hidden.setChecked(False)
        show_hidden.setStyleSheet(f"""
            QCheckBox {{
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }}
        """)
        
        show_icons = QCheckBox("Show file icons")
        show_icons.setChecked(True)
        show_icons.setStyleSheet(f"""
            QCheckBox {{
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }}
        """)
        
        auto_refresh = QCheckBox("Auto-refresh explorer")
        auto_refresh.setChecked(True)
        auto_refresh.setStyleSheet(f"""
            QCheckBox {{
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }}
        """)
        
        # Buttons
        button_box = QDialogButtonBox()
        apply_button = button_box.addButton("Apply", QDialogButtonBox.ButtonRole.ApplyRole)
        cancel_button = button_box.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
        
        layout.addWidget(show_hidden)
        layout.addWidget(show_icons)
        layout.addWidget(auto_refresh)
        layout.addStretch()
        layout.addWidget(button_box)
        
        def apply_settings():
            # Apply settings logic here
            self.file_explorer.model.setFilter(
                QDir.Filter.AllEntries | 
                (QDir.Filter.Hidden if show_hidden.isChecked() else QDir.Filter.NoFilter)
            )
            dialog.accept()
        
        apply_button.clicked.connect(apply_settings)
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    # ==================== EDITOR MANAGEMENT ====================
    
    def create_new_file(self):
        editor = LRDCustomEditor()
        index = self.tab_widget.addTab(editor, "📄 Untitled")
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
        self.file_label.setText("📄 Untitled")
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
            "Bash Files (*.sh);;"
            "Text Files (*.txt)"
        )
        
        if file_path:
            self.open_file(file_path)
    
    def open_file(self, file_path: str):
        # Check if file is already open
        for editor, info in self.open_files.items():
            if info['path'] == file_path:
                index = self.tab_widget.indexOf(editor)
                self.tab_widget.setCurrentIndex(index)
                return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create editor
            editor = LRDCustomEditor()
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
            self.file_label.setText(f"📄 {filename}")
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
    
    def save_all_files(self):
        for editor, info in self.open_files.items():
            if info['modified'] and info['path']:
                try:
                    with open(info['path'], 'w', encoding='utf-8') as f:
                        f.write(editor.toPlainText())
                    info['saved'] = True
                    info['modified'] = False
                    self.update_tab_title(editor)
                except:
                    pass
        
        self.update_status("All files saved", "ready")
    
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
            "Bash Files (*.sh);;"
            "Text Files (*.txt)"
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
                self.tab_widget.setTabText(index, f"📄 {filename}")
                self.set_editor_language(editor, info['language'])
                
                # Update status
                self.update_status(f"Saved as: {filename}", "ready")
                self.file_label.setText(f"📄 {filename}")
                
                # Refresh explorer if in same directory
                if self.project_path and file_path.startswith(self.project_path):
                    self.file_explorer.refresh()
                
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
    
    def close_all_tabs(self):
        while self.tab_widget.count() > 0:
            self.close_tab(0)
    
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
                        self.file_label.setText(f"📄 {os.path.basename(info['path'])}")
                    else:
                        self.file_label.setText("📄 Untitled")
                    
                    # Update language
                    self.language_label.setText(f"🐍 {info['language'].capitalize()}")
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
                self.tab_widget.setTabText(index, f"*📄 {filename}")
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
            self.cursor_label.setText(f"📏 Ln {line}, Col {col}")
            
            # Update line count
            self.update_line_count(editor)
    
    def update_line_count(self, editor):
        if editor:
            line_count = editor.document().blockCount()
            self.line_count_label.setText(f"📊 Lines: {line_count}")
    
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
    
    def select_all(self):
        editor = self.get_current_editor()
        if editor:
            editor.selectAll()
    
    def find_text(self):
        editor = self.get_current_editor()
        if not editor:
            return
        
        # Create find dialog
        find_dialog = QDialog(self)
        find_dialog.setWindowTitle("Find")
        find_dialog.setFixedSize(400, 200)
        find_dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {self.theme['bg_dark']};
                border: 2px solid {self.theme['border']};
                border-radius: 8px;
            }}
            QLabel {{
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
            QLineEdit {{
                background-color: {self.theme['bg_darker']};
                color: {self.theme['text_editor']};
                border: 2px solid {self.theme['border']};
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
            QCheckBox {{
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
        """)
        
        layout = QVBoxLayout(find_dialog)
        
        # Find input
        find_input = QLineEdit()
        find_input.setPlaceholderText("Enter text to find...")
        
        # Options
        case_sensitive = QCheckBox("Case sensitive")
        whole_words = QCheckBox("Whole words only")
        
        # Buttons
        button_box = QDialogButtonBox()
        find_button = button_box.addButton("Find", QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_button = button_box.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
        
        layout.addWidget(QLabel("Find:"))
        layout.addWidget(find_input)
        layout.addWidget(case_sensitive)
        layout.addWidget(whole_words)
        layout.addWidget(button_box)
        
        def find():
            text = find_input.text()
            if not text:
                return
            
            cursor = editor.textCursor()
            flags = QTextDocument.FindFlag(0)
            if case_sensitive.isChecked():
                flags |= QTextDocument.FindFlag.FindCaseSensitively
            if whole_words.isChecked():
                flags |= QTextDocument.FindFlag.FindWholeWords
            
            found = editor.find(text, flags)
            if not found:
                QMessageBox.information(self, "Find", f"Text '{text}' not found.")
        
        find_input.returnPressed.connect(find)
        find_button.clicked.connect(find)
        cancel_button.clicked.connect(find_dialog.close)
        
        find_dialog.exec()
    
    def replace_text(self):
        editor = self.get_current_editor()
        if not editor:
            return
        
        # Create replace dialog
        replace_dialog = QDialog(self)
        replace_dialog.setWindowTitle("Find and Replace")
        replace_dialog.setFixedSize(400, 250)
        replace_dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {self.theme['bg_dark']};
                border: 2px solid {self.theme['border']};
                border-radius: 8px;
            }}
            QLabel {{
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
            QLineEdit {{
                background-color: {self.theme['bg_darker']};
                color: {self.theme['text_editor']};
                border: 2px solid {self.theme['border']};
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
            QCheckBox {{
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', 'Consolas', monospace;
            }}
        """)
        
        layout = QVBoxLayout(replace_dialog)
        
        # Find input
        find_input = QLineEdit()
        find_input.setPlaceholderText("Text to find...")
        
        # Replace input
        replace_input = QLineEdit()
        replace_input.setPlaceholderText("Replace with...")
        
        # Options
        case_sensitive = QCheckBox("Case sensitive")
        whole_words = QCheckBox("Whole words only")
        
        # Buttons
        button_box = QDialogButtonBox()
        find_button = button_box.addButton("Find", QDialogButtonBox.ButtonRole.ActionRole)
        replace_button = button_box.addButton("Replace", QDialogButtonBox.ButtonRole.ActionRole)
        replace_all_button = button_box.addButton("Replace All", QDialogButtonBox.ButtonRole.ActionRole)
        cancel_button = button_box.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
        
        layout.addWidget(QLabel("Find:"))
        layout.addWidget(find_input)
        layout.addWidget(QLabel("Replace with:"))
        layout.addWidget(replace_input)
        layout.addWidget(case_sensitive)
        layout.addWidget(whole_words)
        layout.addWidget(button_box)
        
        def find():
            text = find_input.text()
            if not text:
                return
            
            cursor = editor.textCursor()
            flags = QTextDocument.FindFlag(0)
            if case_sensitive.isChecked():
                flags |= QTextDocument.FindFlag.FindCaseSensitively
            if whole_words.isChecked():
                flags |= QTextDocument.FindFlag.FindWholeWords
            
            found = editor.find(text, flags)
            if not found:
                QMessageBox.information(self, "Find", f"Text '{text}' not found.")
        
        def replace():
            text = find_input.text()
            if not text:
                return
            
            cursor = editor.textCursor()
            if cursor.hasSelection() and cursor.selectedText() == text:
                cursor.insertText(replace_input.text())
            
            # Find next
            find()
        
        def replace_all():
            text = find_input.text()
            if not text:
                return
            
            replace_text = replace_input.text()
            
            # Get all text
            all_text = editor.toPlainText()
            
            flags = 0
            if case_sensitive.isChecked():
                flags = re.IGNORECASE
            
            count = 0
            if whole_words.isChecked():
                pattern = r'\b' + re.escape(text) + r'\b'
                new_text, count = re.subn(pattern, replace_text, all_text, flags=flags)
            else:
                new_text, count = re.subn(re.escape(text), replace_text, all_text, flags=flags)
            
            if count > 0:
                editor.setPlainText(new_text)
                QMessageBox.information(self, "Replace All", f"Replaced {count} occurrences.")
            else:
                QMessageBox.information(self, "Replace All", "No occurrences found.")
        
        find_input.returnPressed.connect(find)
        find_button.clicked.connect(find)
        replace_button.clicked.connect(replace)
        replace_all_button.clicked.connect(replace_all)
        cancel_button.clicked.connect(replace_dialog.close)
        
        replace_dialog.exec()
    
    def duplicate_line(self):
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            text = cursor.selectedText()
            cursor.insertText(text + "\n" + text)
    
    def toggle_comment(self):
        editor = self.get_current_editor()
        if not editor:
            return
        
        info = self.open_files.get(editor)
        if not info:
            return
        
        cursor = editor.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        start_line = cursor.blockNumber()
        
        cursor.setPosition(end)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        end_line = cursor.blockNumber()
        
        # Get comment style based on language
        comment_style = "#"
        if info['language'] in ['javascript', 'java', 'c', 'cpp']:
            comment_style = "//"
        elif info['language'] == 'html':
            comment_style = "<!--"
        elif info['language'] == 'css':
            comment_style = "/*"
        
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        
        # Check if first line is commented
        first_line = cursor.block().text()
        is_commented = first_line.lstrip().startswith(comment_style)
        
        cursor.beginEditBlock()
        
        for i in range(start_line, end_line + 1):
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
            line_text = cursor.block().text()
            
            if is_commented:
                # Uncomment
                if line_text.lstrip().startswith(comment_style):
                    # Find the comment
                    uncommented = line_text.replace(comment_style, "", 1)
                    cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
                    cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
                    cursor.insertText(uncommented)
            else:
                # Comment
                indent = len(line_text) - len(line_text.lstrip())
                commented = line_text[:indent] + comment_style + " " + line_text[indent:]
                cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
                cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
                cursor.insertText(commented)
            
            cursor.movePosition(QTextCursor.MoveOperation.Down)
        
        cursor.endEditBlock()
    
    def format_code(self):
        """Format code (basic indentation)"""
        editor = self.get_current_editor()
        if not editor:
            return
        
        cursor = editor.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        
        if start == end:
            # Format entire document
            text = editor.toPlainText()
            lines = text.split('\n')
            formatted_lines = []
            
            for line in lines:
                stripped = line.lstrip()
                indent = len(line) - len(stripped)
                formatted_lines.append(line)
            
            editor.setPlainText('\n'.join(formatted_lines))
        else:
            # Format selected text
            cursor.beginEditBlock()
            
            start_line = editor.document().findBlock(start).blockNumber()
            end_line = editor.document().findBlock(end).blockNumber()
            
            for i in range(start_line, end_line + 1):
                block = editor.document().findBlockByNumber(i)
                cursor.setPosition(block.position())
                cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
                text = cursor.selectedText()
                cursor.removeSelectedText()
                cursor.insertText(text.lstrip())
            
            cursor.endEditBlock()
        
        self.update_status("Code formatted", "ready")
    
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
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.c': 'c',
            '.php': 'php',
            '.sh': 'bash',
            '.bash': 'bash',
            '.txt': 'text',
        }
        
        return language_map.get(ext, 'text')
    
    def set_editor_language(self, editor, language):
        if isinstance(editor, LRDCustomEditor):
            editor.highlighter.set_language(language)
            # Update language label with icon
            icons = {
                'python': '🐍',
                'javascript': '📜',
                'html': '🌐',
                'css': '🎨',
                'java': '☕',
                'cpp': '⚡',
                'c': '🔧',
                'php': '🐘',
                'bash': '💻',
                'text': '📄'
            }
            icon = icons.get(language, '📄')
            self.language_label.setText(f"{icon} {language.capitalize()}")
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
            
            # Change terminal directory
            self.terminal.current_dir = folder
            self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['success']}'>Terminal directory changed to: {folder}</span>")
    
    def refresh_explorer(self):
        if self.project_path:
            self.file_explorer.set_root_path(self.project_path)
    
    # ==================== TERMINAL ====================
    
    def execute_terminal_command(self):
        command = self.terminal_input.text().strip()
        if command:
            self.terminal.execute_command(command)
            self.terminal_input.clear()
    
    def stop_terminal_process(self):
        """Stop the currently running terminal process"""
        self.terminal.thread_manager.stop_all()
        self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['warning']}'>All processes stopped</span>")
        self.update_status("Processes stopped", "warning")
    
    # ==================== ASYNC CODE EXECUTION ====================
    
    def run_current_file_async(self):
        """Run current file asynchronously"""
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
        self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['primary']}; font-weight:bold'>◢ Running {info['language']} file: {os.path.basename(info['path'])} ◣</span>")
        self.terminal.append("")
        
        # Run based on language asynchronously
        self.is_running = True
        self.update_status(f"Running {info['language']} file...", "running")
        
        # Create command based on language
        cmd = ""
        if info['language'] == 'python':
            python_cmd = self.terminal.compiler_paths.get('python', 'python')
            cmd = f'{python_cmd} "{info["path"]}"'
        elif info['language'] == 'javascript':
            if 'node' in self.terminal.compiler_paths:
                cmd = f'node "{info["path"]}"'
            else:
                self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['error']}'>Error: Node.js not found</span>")
                return
        elif info['language'] == 'java':
            # Compile and run Java
            compile_cmd = f'javac "{info["path"]}"'
            class_name = os.path.splitext(os.path.basename(info['path']))[0]
            run_cmd = f'java -cp "{os.path.dirname(info["path"])}" {class_name}'
            cmd = f'{compile_cmd} && {run_cmd}'
        elif info['language'] == 'c':
            # Compile C
            output_name = os.path.splitext(info['path'])[0]
            compile_cmd = f'gcc "{info["path"]}" -o "{output_name}"'
            run_cmd = f'"{output_name}"'
            cmd = f'{compile_cmd} && {run_cmd}'
        elif info['language'] == 'cpp':
            # Compile C++
            output_name = os.path.splitext(info['path'])[0]
            compile_cmd = f'g++ "{info["path"]}" -o "{output_name}"'
            run_cmd = f'"{output_name}"'
            cmd = f'{compile_cmd} && {run_cmd}'
        elif info['language'] == 'php':
            if 'php' in self.terminal.compiler_paths:
                cmd = f'php "{info["path"]}"'
            else:
                self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['error']}'>Error: PHP not found</span>")
                return
        elif info['language'] == 'html':
            webbrowser.open(f'file://{os.path.abspath(info["path"])}')
            self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['secondary']}'>◢ Opened in browser ◣</span>")
            return
        elif info['language'] == 'bash':
            cmd = f'bash "{info["path"]}"'
        else:
            self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['warning']}'>Language not supported for execution</span>")
            return
        
        # Run command in thread
        if cmd:
            self.terminal.thread_manager.run_command(cmd, os.path.dirname(info['path']), f"Running {info['language']} file")
    
    def run_selection_async(self):
        """Run selected code asynchronously"""
        editor = self.get_current_editor()
        if not editor:
            return
        
        cursor = editor.textCursor()
        selected_text = cursor.selectedText()
        
        if not selected_text:
            QMessageBox.warning(self, "Warning", "No text selected to run.")
            return
        
        # Clear terminal and show running message
        self.terminal.clear()
        self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['primary']}; font-weight:bold'>◢ Running selected code ◣</span>")
        self.terminal.append("")
        
        # Get current language
        info = self.open_files.get(editor)
        language = info['language'] if info else 'python'
        
        # Create temporary file with selected text
        import tempfile
        temp_ext = {
            'python': '.py',
            'javascript': '.js',
            'java': '.java',
            'c': '.c',
            'cpp': '.cpp',
            'php': '.php',
            'bash': '.sh',
            'html': '.html',
            'css': '.css'
        }.get(language, '.txt')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix=temp_ext, delete=False) as f:
            f.write(selected_text)
            temp_file = f.name
        
        # Create command based on language
        cmd = ""
        if language == 'python':
            python_cmd = self.terminal.compiler_paths.get('python', 'python')
            cmd = f'{python_cmd} "{temp_file}"'
        elif language == 'javascript':
            if 'node' in self.terminal.compiler_paths:
                cmd = f'node "{temp_file}"'
            else:
                self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['error']}'>Error: Node.js not found</span>")
                return
        elif language == 'php':
            if 'php' in self.terminal.compiler_paths:
                cmd = f'php "{temp_file}"'
            else:
                self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['error']}'>Error: PHP not found</span>")
                return
        else:
            self.terminal.append(f"<span style='color:{MODERN_GAMER_THEME['warning']}'>Language not supported for execution</span>")
            return
        
        # Run command in thread
        if cmd:
            self.is_running = True
            self.update_status("Running selected code...", "running")
            self.terminal.thread_manager.run_command(cmd, os.getcwd(), "Running selected code")
    
    def stop_running_program(self):
        """Stop the currently running program"""
        self.stop_terminal_process()
        self.is_running = False
        self.update_status("Execution stopped", "warning")
    
    # ==================== VIEW FUNCTIONS ====================
    
    def toggle_sidebar(self):
        sidebar = self.main_splitter.widget(0)
        if sidebar.isVisible():
            sidebar.hide()
        else:
            sidebar.show()
    
    def toggle_terminal(self):
        if self.terminal_dock.isVisible():
            self.terminal_dock.hide()
        else:
            self.terminal_dock.show()
    
    def increase_font_size(self):
        editor = self.get_current_editor()
        if editor:
            font = editor.font()
            size = font.pointSize()
            font.setPointSize(size + 1)
            editor.setFont(font)
            self.font_size_combo.setCurrentText(str(size + 1))
    
    def decrease_font_size(self):
        editor = self.get_current_editor()
        if editor:
            font = editor.font()
            size = font.pointSize()
            if size > 8:
                font.setPointSize(size - 1)
                editor.setFont(font)
                self.font_size_combo.setCurrentText(str(size - 1))
    
    def on_font_size_changed(self, size):
        editor = self.get_current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(int(size))
            editor.setFont(font)
    
    # ==================== UTILITIES ====================
    
    def get_current_editor(self):
        widget = self.tab_widget.currentWidget()
        if isinstance(widget, LRDCustomEditor):
            return widget
        return None
    
    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.time_display.setText(f"🕒 {current_date} {current_time}")
    
    def update_status(self, message: str, status_type: str = "ready"):
        colors = {
            'ready': MODERN_GAMER_THEME['status_ready'],
            'error': MODERN_GAMER_THEME['status_error'],
            'warning': MODERN_GAMER_THEME['status_warning'],
            'modified': MODERN_GAMER_THEME['status_modified'],
            'running': MODERN_GAMER_THEME['status_running']
        }
        
        icons = {
            'ready': '●',
            'error': '⚠',
            'warning': '⚠',
            'modified': '✎',
            'running': '▶'
        }
        
        color = colors.get(status_type, MODERN_GAMER_THEME['status_ready'])
        icon = icons.get(status_type, '●')
        self.status_label.setText(f"{icon} {message}")
        self.status_label.setStyleSheet(f"""
            color: {color};
            font-weight: bold;
            padding-right: 20px;
            font-family: 'Segoe UI', 'Consolas', monospace;
            font-size: 12px;
        """)
        self.status_indicator.setText(f"{icon} {message}")
        self.status_indicator.setStyleSheet(f"""
            font-size: 12px;
            font-weight: bold;
            color: {color};
            background: rgba(0, 0, 0, 0.3);
            padding: 5px 12px;
            border: 1px solid {color};
            border-radius: 4px;
            font-family: 'Segoe UI', 'Consolas', monospace;
        """)
    
    # ==================== HELP & ABOUT ====================
    
    def show_documentation(self):
        QMessageBox.information(
            self,
            "Documentation",
            """◢◤ LRD CODE EDITOR - MODERN GAMER EDITION ◥◣

◢ Features:
• High-performance modern code editor
• Multi-language support with syntax highlighting
• Integrated fully typeable terminal
• Advanced file explorer with VSCode-like features
• Code execution for multiple languages
• Modern UI with gaming aesthetics
• Multi-threaded execution (won't hang)
• Open files with default applications

◢ Enhanced File Explorer:
• Right-click context menu with icons
• Create new files and folders
• Rename and delete items
• Open with default app
• Copy file paths
• Show properties
• Double-click to open files/folders

◢ Terminal Features:
• ALWAYS typeable - no file needs to be open
• Command history (Up/Down arrows)
• Syntax colored output
• Built-in commands: cd, ls, clear, help, history
• Auto-detects compilers/interpreters
• Multi-threaded execution

◢ Performance Optimizations:
• Thread pool for async operations
• Non-blocking UI during execution
• Optimized for older processors
• Smooth scrolling and rendering

◢ Keyboard Shortcuts:
• Ctrl+N: New file
• Ctrl+O: Open file
• Ctrl+E: Open folder
• Ctrl+S: Save file
• Ctrl+Shift+S: Save all files
• Ctrl+W: Close tab
• Ctrl+Tab: Next tab
• Ctrl+Shift+Tab: Previous tab
• F5: Run current file (async)
• F6: Run selection (async)
• Ctrl+.: Stop execution
• Ctrl+F: Find
• Ctrl+H: Replace
• Ctrl+B: Toggle sidebar
• Ctrl+`: Toggle terminal

◢ Getting Started:
1. Open folder (Ctrl+E) to use file explorer
2. Create new files/folders from explorer
3. Write your code with syntax highlighting
4. Save file (Ctrl+S)
5. Run code (F5) or selection (F6) - async!
6. Use terminal for any system commands
            """
        )
    
    def show_shortcuts(self):
        shortcuts_text = f"""
<span style='color:{MODERN_GAMER_THEME['primary']}; font-size:16px; font-weight:bold'>⌨️ KEYBOARD SHORTCUTS</span><br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}'>📁 File Operations:</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+N</span> - New File<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+O</span> - Open File<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+E</span> - Open Folder<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+S</span> - Save File<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+Shift+S</span> - Save All Files<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+W</span> - Close Tab<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+Q</span> - Exit<br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}'>📑 Tab Navigation:</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+Tab</span> - Next Tab<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+Shift+Tab</span> - Previous Tab<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+PageUp</span> - Previous Tab<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+PageDown</span> - Next Tab<br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}'>✏️ Edit Operations:</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+Z</span> - Undo<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+Y</span> - Redo<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+X</span> - Cut<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+C</span> - Copy<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+V</span> - Paste<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+A</span> - Select All<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+F</span> - Find<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+H</span> - Replace<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+D</span> - Duplicate Line<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+/</span> - Toggle Comment<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+Shift+F</span> - Format Code<br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}'>▶️ Run Operations:</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>F5</span> - Run Current File (Async)<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>F6</span> - Run Selection (Async)<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+.</span> - Stop Execution<br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}'>👁️ View Operations:</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+B</span> - Toggle Sidebar<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+`</span> - Toggle Terminal<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl++</span> - Increase Font<br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>Ctrl+-</span> - Decrease Font<br>
"""
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Keyboard Shortcuts")
        dialog.setFixedSize(500, 600)
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {MODERN_GAMER_THEME['bg_dark']};
                border: 3px solid {MODERN_GAMER_THEME['primary']};
                border-radius: 10px;
            }}
        """)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(shortcuts_text)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {MODERN_GAMER_THEME['bg_darker']};
                color: {MODERN_GAMER_THEME['text_editor']};
                border: 2px solid {MODERN_GAMER_THEME['border']};
                border-radius: 5px;
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }}
        """)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {MODERN_GAMER_THEME['bg_surface']};
                color: {MODERN_GAMER_THEME['primary']};
                border: 2px solid {MODERN_GAMER_THEME['border']};
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {MODERN_GAMER_THEME['selection']};
                border: 2px solid {MODERN_GAMER_THEME['primary_light']};
                color: #ffffff;
            }}
        """)
        
        layout.addWidget(text_edit, 1)
        layout.addWidget(close_btn)
        
        dialog.exec()
    
    def show_about(self):
        # Create hacker-themed about dialog
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("◢◤ ABOUT LRD ◥◣")
        about_dialog.setFixedSize(700, 600)
        about_dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {MODERN_GAMER_THEME['bg_black']};
                border: 3px solid {MODERN_GAMER_THEME['primary']};
                border-radius: 10px;
            }}
        """)
        
        layout = QVBoxLayout(about_dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("◢◤ LRD TEAM - MODERN GAMER EDITION ◥◣")
        title.setStyleSheet(f"""
            color: {MODERN_GAMER_THEME['primary']};
            font-size: 22px;
            font-weight: bold;
            font-family: 'Segoe UI', 'Consolas', monospace;
            text-align: center;
            padding: 15px;
            border-bottom: 2px solid {MODERN_GAMER_THEME['secondary']};
        """)
        
        # Logo
        logo_label = QLabel()
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "tlogo.png")
            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path).scaled(120, 120, 
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
                background-color: {MODERN_GAMER_THEME['bg_dark']};
                color: {MODERN_GAMER_THEME['secondary']};
                border: 2px solid {MODERN_GAMER_THEME['primary']};
                border-radius: 5px;
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 13px;
                padding: 15px;
            }}
        """)
        
        hacker_text = f"""
<span style='color:{MODERN_GAMER_THEME['primary']}; font-size: 16px;'>◢◤ SYSTEM INITIALIZED ◥◣</span><br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}'>[+] LRD DEVELOPMENT TEAM</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Founder & Lead Developer: LRD_SOUL</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • UI/UX Designer: LRD_DESIGN</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Security Expert: LRD_SEC</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Backend Developer: LRD_BACK</span><br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}'>[+] CONTACT INFORMATION</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Email: inscreator728@gmail.com</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • GitHub: github.com/inscreator728</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Telegram: @lrd_soul</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Instagram: @lrd_soul</span><br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}'>[+] COMPANY DETAILS</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Organization: LRD-TECH</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Founded: 2024</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Specialization: Gaming Tools & Development</span><br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}'>[+] SOFTWARE SPECS</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Version: Modern Gamer Edition 4.0</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Build: 2024.12.01</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Theme: Modern JARVIS Red-Black</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Performance: Multi-threaded Optimized</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Terminal: Always Typeable & Async</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Explorer: VSCode-like Features with Icons</span><br><br>

<span style='color:{MODERN_GAMER_THEME['secondary']}'>[+] NEW FEATURES</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Enhanced File Explorer with context menu & icons</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Create new files and folders</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Open with default applications</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Always typeable terminal</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Multi-threaded execution (won't hang)</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • Modern UI with gradients and icons</span><br>
<span style='color:{MODERN_GAMER_THEME['text_editor']}'>   • More keyboard shortcuts</span><br><br>

<span style='color:{MODERN_GAMER_THEME['primary']}'>◢◤ ACCESS GRANTED - WELCOME TO LRD ◥◣</span>
"""
        
        about_text.setHtml(hacker_text)
        
        # Close button
        close_btn = QPushButton("CLOSE SYSTEM")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {MODERN_GAMER_THEME['bg_surface']};
                color: {MODERN_GAMER_THEME['primary']};
                border: 2px solid {MODERN_GAMER_THEME['border']};
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Consolas', monospace;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {MODERN_GAMER_THEME['selection']};
                border: 2px solid {MODERN_GAMER_THEME['primary_light']};
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
                self.save_all_files()
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
    app.setApplicationName("LRD Code Editor - Modern Gamer Edition")
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
