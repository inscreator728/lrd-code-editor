import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, font, ttk
import re
import os
import subprocess
from datetime import datetime

class LRDCodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("LRD Code Editor")
        self.root.geometry("1400x900")
        
        # Color scheme - Holographic Hacker Theme
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a0d0d',
            'bg_light': '#2d1a1a',
            'primary': '#ff3333',
            'secondary': '#ff6600',
            'accent': '#ff0066',
            'text_primary': '#ff3333',
            'text_secondary': '#ff6666',
            'editor_bg': '#0d0d0d',
            'editor_text': '#00ff88',
            'line_num_bg': '#1a0808',
            'line_num_text': '#ff4444',
            'status_ready': '#00ff88',
            'status_modified': '#ffaa00',
            'status_error': '#ff0033',
            'selection': '#4d1a1a',
            'cursor': '#ff0066'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Try to load logo
        try:
            self.logo_image = tk.PhotoImage(file='tlogo.jpg')
            self.root.iconphoto(False, self.logo_image)
        except:
            pass
        
        self.filename = None
        self.current_language = 'python'
        self.setup_ui()
        self.setup_syntax()
        self.bind_events()
        
    def setup_ui(self):
        # Custom fonts
        self.editor_font = font.Font(family="Consolas", size=11)
        self.title_font = font.Font(family="Consolas", size=14, weight="bold")
        self.menu_font = font.Font(family="Consolas", size=9, weight="bold")
        
        # Top bar with logo
        top_bar = tk.Frame(self.root, bg=self.colors['bg_medium'], height=50)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Logo frame
        logo_frame = tk.Frame(top_bar, bg=self.colors['bg_medium'])
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        try:
            logo_img = tk.PhotoImage(file='tlogo.jpg')
            # Resize logo to fit
            logo_img = logo_img.subsample(3, 3)
            logo_label = tk.Label(logo_frame, image=logo_img, bg=self.colors['bg_medium'])
            logo_label.image = logo_img
            logo_label.pack(side=tk.LEFT, pady=5)
        except:
            pass
        
        # Title
        title = tk.Label(top_bar, text="◢◤ LRD CODE EDITOR ◥◣", 
                        font=self.title_font, 
                        fg=self.colors['primary'], 
                        bg=self.colors['bg_medium'])
        title.pack(side=tk.LEFT, padx=20, pady=8)
        
        # Status indicators
        status_frame = tk.Frame(top_bar, bg=self.colors['bg_medium'])
        status_frame.pack(side=tk.RIGHT, padx=20)
        
        self.status_label = tk.Label(status_frame, text="● READY", 
                                     font=("Consolas", 10, "bold"), 
                                     fg=self.colors['status_ready'], 
                                     bg=self.colors['bg_medium'])
        self.status_label.pack()
        
        self.time_label = tk.Label(status_frame, text="", 
                                   font=("Consolas", 8), 
                                   fg=self.colors['text_secondary'], 
                                   bg=self.colors['bg_medium'])
        self.time_label.pack()
        self.update_time()
        
        # Menu bar
        menu_bar = tk.Frame(self.root, bg=self.colors['bg_light'], height=40)
        menu_bar.pack(fill=tk.X)
        menu_bar.pack_propagate(False)
        
        menu_items = [
            ("◢ NEW", self.new_file),
            ("◢ OPEN", self.open_file),
            ("◢ SAVE", self.save_file),
            ("◢ SAVE AS", self.save_as),
            ("◢ RUN", self.run_code),
            ("◢ ABOUT", self.show_about),
            ("◢ EXIT", self.exit_app)
        ]
        
        for text, cmd in menu_items:
            btn = tk.Button(menu_bar, text=text, command=cmd,
                          font=self.menu_font,
                          fg=self.colors['text_primary'], 
                          bg=self.colors['bg_light'],
                          activeforeground=self.colors['primary'],
                          activebackground=self.colors['bg_medium'],
                          bd=0, padx=15, pady=8,
                          cursor="hand2")
            btn.pack(side=tk.LEFT, padx=3)
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg=self.colors['secondary'], bg=self.colors['bg_medium']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(fg=self.colors['text_primary'], bg=self.colors['bg_light']))
        
        # Language selector
        lang_frame = tk.Frame(menu_bar, bg=self.colors['bg_light'])
        lang_frame.pack(side=tk.RIGHT, padx=15)
        
        tk.Label(lang_frame, text="LANG:", font=("Consolas", 8, "bold"),
                fg=self.colors['text_secondary'], bg=self.colors['bg_light']).pack(side=tk.LEFT, padx=5)
        
        self.lang_var = tk.StringVar(value="Python")
        lang_menu = ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                                values=["Python", "Java", "PHP", "JavaScript", "HTML", "CSS", "C++", "C"],
                                width=10, state="readonly", font=("Consolas", 8))
        lang_menu.pack(side=tk.LEFT)
        lang_menu.bind("<<ComboboxSelected>>", self.on_language_change)
        
        # Main editor container
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Editor frame
        editor_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Line numbers
        self.line_numbers = tk.Text(editor_frame, width=6, 
                                   font=self.editor_font,
                                   bg=self.colors['line_num_bg'], 
                                   fg=self.colors['line_num_text'],
                                   state=tk.DISABLED,
                                   bd=0, padx=8, pady=10,
                                   selectbackground=self.colors['selection'],
                                   cursor="arrow")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Text editor with custom scrollbar
        editor_container = tk.Frame(editor_frame, bg=self.colors['editor_bg'])
        editor_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.text_editor = scrolledtext.ScrolledText(
            editor_container,
            font=self.editor_font,
            bg=self.colors['editor_bg'],
            fg=self.colors['editor_text'],
            insertbackground=self.colors['cursor'],
            selectbackground=self.colors['selection'],
            selectforeground="#ffffff",
            bd=0,
            padx=15,
            pady=10,
            wrap=tk.NONE,
            undo=True,
            maxundo=-1
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Bottom status bar
        bottom_bar = tk.Frame(self.root, bg=self.colors['bg_medium'], height=35)
        bottom_bar.pack(fill=tk.X)
        bottom_bar.pack_propagate(False)
        
        self.file_info = tk.Label(bottom_bar, text="◢ [UNTITLED] ◣", 
                                 font=("Consolas", 9, "bold"),
                                 fg=self.colors['text_primary'], 
                                 bg=self.colors['bg_medium'])
        self.file_info.pack(side=tk.LEFT, padx=20, pady=5)
        
        self.cursor_info = tk.Label(bottom_bar, text="Ln: 1 │ Col: 0", 
                                   font=("Consolas", 9),
                                   fg=self.colors['text_secondary'], 
                                   bg=self.colors['bg_medium'])
        self.cursor_info.pack(side=tk.LEFT, padx=10)
        
        self.char_count = tk.Label(bottom_bar, text="Characters: 0", 
                                  font=("Consolas", 9),
                                  fg=self.colors['text_secondary'], 
                                  bg=self.colors['bg_medium'])
        self.char_count.pack(side=tk.RIGHT, padx=20)
        
        self.encoding_label = tk.Label(bottom_bar, text="UTF-8", 
                                      font=("Consolas", 9),
                                      fg=self.colors['text_secondary'], 
                                      bg=self.colors['bg_medium'])
        self.encoding_label.pack(side=tk.RIGHT, padx=10)
        
    def setup_syntax(self):
        # Syntax highlighting tags
        self.text_editor.tag_configure("keyword", foreground="#ff3366")
        self.text_editor.tag_configure("builtin", foreground="#ff6633")
        self.text_editor.tag_configure("string", foreground="#ffaa00")
        self.text_editor.tag_configure("comment", foreground="#666666")
        self.text_editor.tag_configure("function", foreground="#ff0066")
        self.text_editor.tag_configure("number", foreground="#ff9900")
        self.text_editor.tag_configure("class", foreground="#ff3399")
        self.text_editor.tag_configure("operator", foreground="#ff6666")
        self.text_editor.tag_configure("tag", foreground="#ff3366")
        self.text_editor.tag_configure("attribute", foreground="#ff9900")
        
        # Language-specific patterns
        self.syntax_patterns = {
            'python': {
                'keywords': r'\b(def|class|import|from|if|elif|else|for|while|try|except|finally|with|as|return|break|continue|pass|raise|yield|lambda|and|or|not|in|is|None|True|False|async|await|global|nonlocal|assert|del)\b',
                'builtins': r'\b(print|len|range|str|int|float|list|dict|set|tuple|open|input|type|isinstance|enumerate|zip|map|filter|sorted|sum|min|max|abs|round|all|any|dir|help|super|property|staticmethod|classmethod)\b',
                'comments': r'#.*$',
                'strings': r'(["\'])(?:(?=(\\?))\2.)*?\1|"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'',
                'numbers': r'\b\d+\.?\d*\b'
            },
            'java': {
                'keywords': r'\b(public|private|protected|static|final|abstract|class|interface|extends|implements|import|package|new|return|if|else|for|while|do|switch|case|break|continue|try|catch|finally|throw|throws|void|int|double|float|boolean|char|String|this|super|null|true|false)\b',
                'builtins': r'\b(System|Math|String|Integer|Double|Boolean|ArrayList|HashMap|List|Set|Map|Exception|Thread|Object)\b',
                'comments': r'//.*$|/\*[\s\S]*?\*/',
                'strings': r'"(?:[^"\\]|\\.)*"',
                'numbers': r'\b\d+\.?\d*[fFdDlL]?\b'
            },
            'php': {
                'keywords': r'\b(function|class|public|private|protected|static|final|abstract|interface|extends|implements|namespace|use|new|return|if|else|elseif|for|foreach|while|do|switch|case|break|continue|try|catch|finally|throw|echo|print|isset|empty|array|true|false|null|const|var|global|require|include|require_once|include_once)\b',
                'builtins': r'\b(strlen|strpos|substr|str_replace|explode|implode|array_push|array_pop|count|in_array|array_merge|json_encode|json_decode|file_get_contents|file_put_contents|preg_match|preg_replace|mysqli_connect|PDO)\b',
                'comments': r'//.*$|/\*[\s\S]*?\*/|#.*$',
                'strings': r'(["\'])(?:(?=(\\?))\2.)*?\1',
                'numbers': r'\b\d+\.?\d*\b',
                'variables': r'\$\w+'
            },
            'javascript': {
                'keywords': r'\b(function|class|const|let|var|if|else|for|while|do|switch|case|break|continue|return|try|catch|finally|throw|new|this|super|extends|import|export|default|async|await|yield|typeof|instanceof|in|of|null|undefined|true|false)\b',
                'builtins': r'\b(console|document|window|Array|Object|String|Number|Boolean|Date|Math|JSON|Promise|setTimeout|setInterval|addEventListener|querySelector|getElementById)\b',
                'comments': r'//.*$|/\*[\s\S]*?\*/',
                'strings': r'(["\'])(?:(?=(\\?))\2.)*?\1|`[\s\S]*?`',
                'numbers': r'\b\d+\.?\d*\b'
            },
            'html': {
                'tags': r'</?[a-zA-Z][\w]*(?:\s|>|/>)',
                'attributes': r'\b[\w-]+(?==)',
                'strings': r'(["\'])(?:(?=(\\?))\2.)*?\1',
                'comments': r'<!--[\s\S]*?-->'
            },
            'css': {
                'keywords': r'\b(background|color|font|margin|padding|border|width|height|display|position|float|clear|text-align|line-height|opacity|transition|transform|animation)\b',
                'comments': r'/\*[\s\S]*?\*/',
                'strings': r'(["\'])(?:(?=(\\?))\2.)*?\1',
                'numbers': r'\b\d+\.?\d*(?:px|em|rem|%|vh|vw)?\b'
            }
        }
        
    def bind_events(self):
        self.text_editor.bind("<KeyRelease>", self.on_key_release)
        self.text_editor.bind("<Button-1>", self.update_cursor_info)
        self.text_editor.bind("<Control-s>", lambda e: self.save_file())
        self.text_editor.bind("<Control-o>", lambda e: self.open_file())
        self.text_editor.bind("<Control-n>", lambda e: self.new_file())
        self.text_editor.bind("<Control-r>", lambda e: self.run_code())
        self.text_editor.bind("<Control-z>", lambda e: self.text_editor.edit_undo())
        self.text_editor.bind("<Control-y>", lambda e: self.text_editor.edit_redo())
        
    def highlight_syntax(self):
        lang = self.current_language.lower()
        if lang not in self.syntax_patterns:
            lang = 'python'
            
        content = self.text_editor.get("1.0", tk.END)
        
        # Remove old tags
        for tag in ["keyword", "builtin", "string", "comment", "function", "number", "class", "operator", "tag", "attribute", "variable"]:
            self.text_editor.tag_remove(tag, "1.0", tk.END)
        
        patterns = self.syntax_patterns[lang]
        
        # Highlight comments first (so they override other patterns)
        if 'comments' in patterns:
            for match in re.finditer(patterns['comments'], content, re.MULTILINE):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_editor.tag_add("comment", start, end)
        
        # Highlight strings
        if 'strings' in patterns:
            for match in re.finditer(patterns['strings'], content, re.DOTALL):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_editor.tag_add("string", start, end)
        
        # Highlight keywords
        if 'keywords' in patterns:
            for match in re.finditer(patterns['keywords'], content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_editor.tag_add("keyword", start, end)
        
        # Highlight builtins
        if 'builtins' in patterns:
            for match in re.finditer(patterns['builtins'], content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_editor.tag_add("builtin", start, end)
        
        # Highlight numbers
        if 'numbers' in patterns:
            for match in re.finditer(patterns['numbers'], content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_editor.tag_add("number", start, end)
        
        # Language-specific highlighting
        if lang == 'python':
            # Function definitions
            for match in re.finditer(r'\bdef\s+(\w+)', content):
                start = f"1.0+{match.start(1)}c"
                end = f"1.0+{match.end(1)}c"
                self.text_editor.tag_add("function", start, end)
            
            # Class definitions
            for match in re.finditer(r'\bclass\s+(\w+)', content):
                start = f"1.0+{match.start(1)}c"
                end = f"1.0+{match.end(1)}c"
                self.text_editor.tag_add("class", start, end)
                
        elif lang == 'php' and 'variables' in patterns:
            for match in re.finditer(patterns['variables'], content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_editor.tag_add("builtin", start, end)
                
        elif lang == 'html':
            # Tags
            if 'tags' in patterns:
                for match in re.finditer(patterns['tags'], content):
                    start = f"1.0+{match.start()}c"
                    end = f"1.0+{match.end()}c"
                    self.text_editor.tag_add("tag", start, end)
            
            # Attributes
            if 'attributes' in patterns:
                for match in re.finditer(patterns['attributes'], content):
                    start = f"1.0+{match.start()}c"
                    end = f"1.0+{match.end()}c"
                    self.text_editor.tag_add("attribute", start, end)
    
    def update_line_numbers(self):
        line_count = self.text_editor.get("1.0", tk.END).count('\n')
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert("1.0", line_numbers_string)
        self.line_numbers.config(state=tk.DISABLED)
    
    def update_cursor_info(self, event=None):
        cursor_pos = self.text_editor.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        self.cursor_info.config(text=f"Ln: {line} │ Col: {col}")
        
        # Update character count
        content = self.text_editor.get("1.0", tk.END)
        char_count = len(content) - 1  # Subtract trailing newline
        self.char_count.config(text=f"Characters: {char_count}")
    
    def on_key_release(self, event):
        self.highlight_syntax()
        self.update_line_numbers()
        self.update_cursor_info()
        self.status_label.config(text="● MODIFIED", fg=self.colors['status_modified'])
    
    def on_language_change(self, event=None):
        lang_map = {
            'Python': 'python',
            'Java': 'java',
            'PHP': 'php',
            'JavaScript': 'javascript',
            'HTML': 'html',
            'CSS': 'css',
            'C++': 'cpp',
            'C': 'c'
        }
        self.current_language = lang_map.get(self.lang_var.get(), 'python')
        self.highlight_syntax()
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def new_file(self):
        if self.text_editor.get("1.0", tk.END).strip():
            if messagebox.askyesno("New File", "Create new file? Unsaved changes will be lost."):
                self.text_editor.delete("1.0", tk.END)
                self.filename = None
                self.file_info.config(text="◢ [UNTITLED] ◣")
                self.status_label.config(text="● NEW FILE", fg=self.colors['status_ready'])
        else:
            self.text_editor.delete("1.0", tk.END)
            self.filename = None
            self.file_info.config(text="◢ [UNTITLED] ◣")
            self.status_label.config(text="● NEW FILE", fg=self.colors['status_ready'])
    
    def open_file(self):
        file = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("Python Files", "*.py"),
                ("Java Files", "*.java"),
                ("PHP Files", "*.php"),
                ("JavaScript Files", "*.js"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("C++ Files", "*.cpp"),
                ("C Files", "*.c"),
                ("All Files", "*.*")
            ]
        )
        if file:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert("1.0", content)
                self.filename = file
                self.file_info.config(text=f"◢ [{os.path.basename(file)}] ◣")
                self.status_label.config(text="● LOADED", fg=self.colors['status_ready'])
                
                # Auto-detect language
                ext = os.path.splitext(file)[1].lower()
                lang_map = {
                    '.py': 'Python',
                    '.java': 'Java',
                    '.php': 'PHP',
                    '.js': 'JavaScript',
                    '.html': 'HTML',
                    '.css': 'CSS',
                    '.cpp': 'C++',
                    '.c': 'C'
                }
                if ext in lang_map:
                    self.lang_var.set(lang_map[ext])
                    self.on_language_change()
                
                self.highlight_syntax()
                self.update_line_numbers()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
    
    def save_file(self):
        if self.filename:
            try:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    f.write(self.text_editor.get("1.0", tk.END))
                self.status_label.config(text="● SAVED", fg=self.colors['status_ready'])
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
        else:
            self.save_as()
    
    def save_as(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Python Files", "*.py"),
                ("Java Files", "*.java"),
                ("PHP Files", "*.php"),
                ("JavaScript Files", "*.js"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("C++ Files", "*.cpp"),
                ("C Files", "*.c"),
                ("All Files", "*.*")
            ]
        )
        if file:
            try:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(self.text_editor.get("1.0", tk.END))
                self.filename = file
                self.file_info.config(text=f"◢ [{os.path.basename(file)}] ◣")
                self.status_label.config(text="● SAVED", fg=self.colors['status_ready'])
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
    
    def run_code(self):
        if not self.filename:
            messagebox.showwarning("Run", "Please save the file first!")
            return
        
        ext = os.path.splitext(self.filename)[1].lower()
        
        try:
            if ext == '.py':
                if os.name == 'nt':  # Windows
                    subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'python', self.filename])
                else:  # Linux/Mac
                    subprocess.Popen(['xterm', '-e', f'python3 {self.filename}'])
            elif ext == '.java':
                if os.name == 'nt':
                    subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'javac', self.filename, '&&', 'java', os.path.splitext(os.path.basename(self.filename))[0]])
                else:
                    subprocess.Popen(['xterm', '-e', f'javac {self.filename} && java {os.path.splitext(os.path.basename(self.filename))[0]}'])
            elif ext == '.php':
                if os.name == 'nt':
                    subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'php', self.filename])
                else:
                    subprocess.Popen(['xterm', '-e', f'php {self.filename}'])
            elif ext == '.js':
                if os.name == 'nt':
                    subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'node', self.filename])
                else:
                    subprocess.Popen(['xterm', '-e', f'node {self.filename}'])
            elif ext in ['.html', '.htm']:
                import webbrowser
                webbrowser.open(self.filename)
            elif ext in ['.cpp', '.c']:
                messagebox.showinfo("Run", "C/C++ files need to be compiled first.\nUse: gcc/g++ filename -o output")
            else:
                messagebox.showinfo("Run", f"Running {ext} files is not supported yet.")
            
            self.status_label.config(text="● EXECUTING", fg="#ffff00")
        except Exception as e:
            messagebox.showerror("Error", f"Could not run file: {str(e)}")
    
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About LRD Code Editor")
        about_window.geometry("600x500")
        about_window.configure(bg=self.colors['bg_dark'])
        about_window.resizable(False, False)
        
        # Center the window
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Header
        header = tk.Frame(about_window, bg=self.colors['bg_medium'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        try:
            logo_img = tk.PhotoImage(file='tlogo.jpg')
            logo_img = logo_img.subsample(4, 4)
            logo_label = tk.Label(header, image=logo_img, bg=self.colors['bg_medium'])
            logo_label.image = logo_img
            logo_label.pack(pady=10)
        except:
            pass
        
        tk.Label(header, text="LRD CODE EDITOR", 
                font=("Consolas", 18, "bold"),
                fg=self.colors['primary'],
                bg=self.colors['bg_medium']).pack()
        
        # Content
        content = tk.Frame(about_window, bg=self.colors['bg_dark'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        info = [
            ("Version:", "1.0.0"),
            ("", ""),
            ("Company:", "LRD-TECH"),
            ("", ""),
            ("Developer:", "LRD_SOUL"),
            ("Email:", "inscreator728@gmail.com"),
            ("GitHub:", "inscreator728"),
            ("", ""),
            ("Telegram:", "@lrd_soul"),
            ("Instagram:", "@lrd_soul"),
            ("", ""),
            ("Description:", "Multi-Language Code Editor"),
            ("", "with Advanced Syntax Highlighting"),
            ("", ""),
            ("Supported Languages:", "Python, Java, PHP,"),
            ("", "JavaScript, HTML, CSS, C++, C"),
            ("", ""),
            ("Features:", "• Real-time Syntax Highlighting"),
            ("", "• Multi-Language Support"),
            ("", "• Auto Line Numbering"),
            ("", "• Code Execution"),
            ("", "• File Management"),
            ("", "• Custom Themes"),
        ]
        
        for i, (label, value) in enumerate(info):
            row = tk.Frame(content, bg=self.colors['bg_dark'])
            row.pack(fill=tk.X, pady=2)
            
            if label:
                tk.Label(row, text=label, 
                        font=("Consolas", 10, "bold"),
                        fg=self.colors['text_primary'],
                        bg=self.colors['bg_dark'],
                        width=15,
                        anchor='w').pack(side=tk.LEFT)
                
                tk.Label(row, text=value, 
                        font=("Consolas", 10),
                        fg=self.colors['text_secondary'],
                        bg=self.colors['bg_dark'],
                        anchor='w').pack(side=tk.LEFT, padx=10)
            else:
                if value:
                    tk.Label(row, text=value, 
                            font=("Consolas", 10),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['bg_dark'],
                            anchor='w').pack(side=tk.LEFT, padx=(165, 0))
        
        # Footer
        footer = tk.Frame(about_window, bg=self.colors['bg_medium'], height=60)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        tk.Label(footer, text="© 2024-2025 LRD-TECH | All Rights Reserved", 
                font=("Consolas", 9),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_medium']).pack(pady=8)
        
        close_btn = tk.Button(footer, text="◢ CLOSE ◣", 
                             command=about_window.destroy,
                             font=("Consolas", 10, "bold"),
                             fg=self.colors['primary'],
                             bg=self.colors['bg_light'],
                             activeforeground="#ffffff",
                             activebackground=self.colors['primary'],
                             bd=0, padx=30, pady=8,
                             cursor="hand2")
        close_btn.pack()
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg=self.colors['primary'], fg="#ffffff"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg=self.colors['bg_light'], fg=self.colors['primary']))
    
    def exit_app(self):
        if messagebox.askyesno("Exit", "◢ Exit LRD Code Editor? ◣"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LRDCodeEditor(root)
    root.mainloop()
