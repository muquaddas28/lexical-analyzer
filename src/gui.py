import re
import tkinter as tk
from collections import Counter
from tkinter import filedialog, messagebox, ttk

from lexer import LexicalAnalyzer


class LexerGUI:
    BG = "#c5dff0"
    PANEL = "#7c6bb0"
    PANEL_DARK = "#69579c"
    SURFACE = "#d6eef0"
    HEADER_BG = "#9fd8cf"
    HEADER_FG = "#174e63"
    INPUT_BG = "#f8fcfc"
    ACCENT = "#7a6baa"
    ACCENT_LT = "#f3efff"
    SUCCESS = "#3a9a8c"
    DANGER = "#b85c5c"
    ERROR_HDR = "#9b5d76"
    ERROR_BG = "#f7e6eb"
    ERROR_BORDER = "#d8a6b6"
    ERROR_TEXT = "#7a243d"
    TEXT = "#1a3545"
    BLUE = "#2d7888"
    BLUE_LT = "#3d93a5"
    GREEN_LT = "#4dbfb0"
    ROW_ODD = "#eaf5f3"
    ROW_EVEN = "#f5fbfa"
    BORDER = "#8aa8bf"
    LN_BG = "#ede8f8"
    LN_FG = "#9980cc"

    SYN_KW = "#7a1ea0"
    SYN_STR = "#2e7d32"
    SYN_CMT = "#757575"
    SYN_NUM = "#e65100"
    SYN_OP = "#1565c0"

    def __init__(self, root):
        self.root = root
        self.root.title("CS3510 - Lexical Analyzer")
        self.root.geometry("1320x820")
        self.root.minsize(1050, 680)
        self.root.configure(bg=self.BG)
        self.lexer = LexicalAnalyzer()
        self._apply_styles()
        self._build_ui()

    def _apply_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Tree.Treeview",
            background=self.INPUT_BG,
            fieldbackground=self.INPUT_BG,
            foreground=self.TEXT,
            rowheight=24,
            font=("Consolas", 10),
            borderwidth=0,
            relief="flat",
        )
        style.configure(
            "Tree.Treeview.Heading",
            background=self.HEADER_BG,
            foreground=self.HEADER_FG,
            font=("Helvetica", 10, "bold"),
            relief="flat",
            borderwidth=0,
        )
        style.map(
            "Tree.Treeview",
            background=[("selected", self.ACCENT)],
            foreground=[("selected", "#ffffff")],
        )
        style.map(
            "Tree.Treeview.Heading",
            background=[("active", self.BLUE_LT)],
            foreground=[("active", "#ffffff")],
        )

        style.configure("TNotebook", background=self.BG, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=self.SURFACE,
            foreground=self.TEXT,
            font=("Helvetica", 9, "bold"),
            padding=[12, 5],
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.ACCENT)],
            foreground=[("selected", "#ffffff")],
        )

        style.configure(
            "Custom.Vertical.TScrollbar",
            background=self.SURFACE,
            troughcolor=self.BG,
            arrowcolor=self.ACCENT,
            borderwidth=0,
            width=10,
        )

    def _build_ui(self):
        self._header()
        tk.Frame(self.root, bg=self.ACCENT, height=2).pack(fill=tk.X)

        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        left = tk.Frame(body, bg=self.PANEL, bd=0)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 7))

        right = tk.Frame(body, bg=self.BG)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(7, 0))
        right.configure(width=760)
        right.pack_propagate(False)

        self._left_panel(left)
        self._right_panel(right)
        self._stats_bar()
        self._error_panel()

    def _header(self):
        header = tk.Frame(self.root, bg=self.PANEL, pady=14)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="COMPILER CONSTRUCTION",
            font=("Helvetica", 9, "bold"),
            fg="#ddd5f5",
            bg=self.PANEL,
        ).pack()
        tk.Label(
            header,
            text="Lexical Analyzer",
            font=("Helvetica", 22, "bold"),
            fg="#ffffff",
            bg=self.PANEL,
        ).pack()
        tk.Label(
            header,
            text="CS3510 - Phase 1: Tokenization | Symbol Table | Error Detection",
            font=("Helvetica", 9),
            fg="#e0d8f8",
            bg=self.PANEL,
        ).pack()

    def _left_panel(self, parent):
        self._section_title(parent, "SOURCE CODE INPUT")

        border = tk.Frame(parent, bg=self.ACCENT, padx=1, pady=1)
        border.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 10))

        inner = tk.Frame(border, bg=self.INPUT_BG)
        inner.pack(fill=tk.BOTH, expand=True)

        editor_row = tk.Frame(inner, bg=self.INPUT_BG)

        self.line_nums = tk.Text(
            editor_row,
            width=4,
            bg=self.LN_BG,
            fg=self.LN_FG,
            font=("Consolas", 11),
            state=tk.DISABLED,
            relief="flat",
            bd=0,
            cursor="arrow",
            takefocus=False,
            padx=6,
            pady=4,
        )
        self.line_nums.pack(side=tk.LEFT, fill=tk.Y)

        tk.Frame(editor_row, bg=self.ACCENT_LT, width=1).pack(side=tk.LEFT, fill=tk.Y)

        self._vsb = ttk.Scrollbar(
            editor_row,
            orient="vertical",
            style="Custom.Vertical.TScrollbar",
            command=self._code_yview,
        )
        self._vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.code_text = tk.Text(
            editor_row,
            font=("Consolas", 11),
            wrap=tk.NONE,
            bg=self.INPUT_BG,
            fg=self.TEXT,
            insertbackground=self.ACCENT_LT,
            selectbackground=self.ACCENT,
            selectforeground="#fff",
            relief="flat",
            bd=8,
            pady=4,
            yscrollcommand=self._code_yscroll,
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)

        self.code_text.tag_config("hl_kw", foreground=self.SYN_KW, font=("Consolas", 11, "bold"))
        self.code_text.tag_config("hl_str", foreground=self.SYN_STR)
        self.code_text.tag_config("hl_cmt", foreground=self.SYN_CMT, font=("Consolas", 11, "italic"))
        self.code_text.tag_config("hl_num", foreground=self.SYN_NUM)
        self.code_text.tag_config("hl_op", foreground=self.SYN_OP)

        xscroll = ttk.Scrollbar(inner, orient="horizontal", command=self.code_text.xview)
        self.code_text.configure(xscrollcommand=xscroll.set)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        editor_row.pack(fill=tk.BOTH, expand=True)

        self.code_text.bind("<KeyRelease>", self._update_line_numbers)
        self.code_text.bind("<<Paste>>", self._update_line_numbers)

        btn_row = tk.Frame(parent, bg=self.PANEL)
        btn_row.pack(fill=tk.X, padx=12, pady=(0, 14))
        self._btn(btn_row, "Load File", self.load_file, self.BLUE, self.BLUE_LT).pack(side=tk.LEFT)
        self._btn(btn_row, "Clear", self.clear_all, "#374151", "#4b5563").pack(side=tk.LEFT, padx=(8, 0))
        self._btn(btn_row, "Analyze >", self.analyze_code, self.SUCCESS, self.GREEN_LT).pack(side=tk.RIGHT)

    def _code_yview(self, *args):
        self.code_text.yview(*args)
        self.line_nums.yview(*args)

    def _code_yscroll(self, first, last):
        self._vsb.set(first, last)
        self.line_nums.yview_moveto(first)

    def _update_line_numbers(self, event=None):
        end = int(self.code_text.index("end-1c").split(".")[0])
        self.line_nums.config(state=tk.NORMAL)
        self.line_nums.delete("1.0", tk.END)
        self.line_nums.insert("1.0", "\n".join(str(i) for i in range(1, end + 1)))
        self.line_nums.config(state=tk.DISABLED)

    def _right_panel(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        tab_tok = tk.Frame(self.notebook, bg=self.INPUT_BG)
        tab_sym = tk.Frame(self.notebook, bg=self.INPUT_BG)
        tab_stat = tk.Frame(self.notebook, bg=self.INPUT_BG)

        self.notebook.add(tab_tok, text="  Token Stream  ")
        self.notebook.add(tab_sym, text="  Symbol Table  ")
        self.notebook.add(tab_stat, text="  Statistics  ")

        self._build_token_tab(tab_tok)
        self._build_symbol_tab(tab_sym)
        self._build_stats_tab(tab_stat)

    def _tab_toolbar(self, parent, title, button_text=None, button_cmd=None):
        bar = tk.Frame(parent, bg=self.INPUT_BG)
        bar.pack(fill=tk.X, padx=10, pady=(8, 6))
        tk.Label(bar, text=title, font=("Helvetica", 11, "bold"), fg=self.TEXT, bg=self.INPUT_BG).pack(side=tk.LEFT)
        if button_text and button_cmd:
            self._btn(bar, button_text, button_cmd, self.BLUE, self.BLUE_LT).pack(side=tk.RIGHT)

    def _table_container(self, parent):
        frame = tk.Frame(parent, bg=self.INPUT_BG, highlightbackground=self.BORDER, highlightthickness=1)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        return frame

    def _build_token_tab(self, parent):
        self._tab_toolbar(parent, "Token Stream", "Export CSV", self.export_tokens)
        cols = ("Type", "Lexeme", "Line", "Col")
        table_wrap = self._table_container(parent)
        self.token_table = ttk.Treeview(table_wrap, columns=cols, show="headings", style="Tree.Treeview")
        widths = {"Type": 150, "Lexeme": 240, "Line": 80, "Col": 80}
        anchors = {"Type": "center", "Lexeme": "center", "Line": "center", "Col": "center"}
        for c in cols:
            self.token_table.heading(c, text=c, anchor="center")
            self.token_table.column(c, width=widths[c], anchor=anchors[c])
        self.token_table.tag_configure("odd", background=self.ROW_ODD)
        self.token_table.tag_configure("even", background=self.ROW_EVEN)

        vsb = ttk.Scrollbar(table_wrap, orient="vertical", command=self.token_table.yview, style="Custom.Vertical.TScrollbar")
        self.token_table.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.token_table.pack(fill=tk.BOTH, expand=True)

    def _build_symbol_tab(self, parent):
        self._tab_toolbar(parent, "Symbol Table", "Export CSV", self.export_symbols)
        cols = ("Identifier", "Type", "Scope", "Line", "Col")
        table_wrap = self._table_container(parent)
        self.sym_table = ttk.Treeview(table_wrap, columns=cols, show="headings", style="Tree.Treeview")
        widths = {"Identifier": 230, "Type": 100, "Scope": 140, "Line": 80, "Col": 80}
        anchors = {"Identifier": "center", "Type": "center", "Scope": "center", "Line": "center", "Col": "center"}
        for c in cols:
            self.sym_table.heading(c, text=c, anchor="center")
            self.sym_table.column(c, width=widths[c], anchor=anchors[c])
        self.sym_table.tag_configure("odd", background=self.ROW_ODD)
        self.sym_table.tag_configure("even", background=self.ROW_EVEN)

        vsb = ttk.Scrollbar(table_wrap, orient="vertical", command=self.sym_table.yview, style="Custom.Vertical.TScrollbar")
        self.sym_table.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.sym_table.pack(fill=tk.BOTH, expand=True)

    def _build_stats_tab(self, parent):
        self._tab_toolbar(parent, "Statistics")

        summary = tk.Frame(parent, bg=self.SURFACE, highlightbackground=self.BORDER, highlightthickness=1)
        summary.pack(fill=tk.X, padx=10, pady=(0, 8))
        tk.Label(
            summary,
            text="Token Type Breakdown",
            font=("Helvetica", 11, "bold"),
            fg=self.HEADER_FG,
            bg=self.SURFACE,
        ).pack(anchor="w", padx=12, pady=(10, 2))
        self.stats_summary = tk.Label(
            summary,
            text="Run analysis to see statistics.",
            font=("Helvetica", 10),
            fg=self.TEXT,
            bg=self.SURFACE,
        )
        self.stats_summary.pack(anchor="w", padx=12, pady=(0, 10))

        cols = ("Token Type", "Count", "% of Total")
        table_wrap = self._table_container(parent)
        self.stats_table = ttk.Treeview(
            table_wrap,
            columns=cols,
            show="headings",
            style="Tree.Treeview",
            height=8,
        )
        widths = {"Token Type": 220, "Count": 100, "% of Total": 120}
        anchors = {"Token Type": "center", "Count": "center", "% of Total": "center"}
        for c in cols:
            self.stats_table.heading(c, text=c, anchor="center")
            self.stats_table.column(c, width=widths[c], anchor=anchors[c])
        self.stats_table.tag_configure("odd", background=self.ROW_ODD)
        self.stats_table.tag_configure("even", background=self.ROW_EVEN)

        vsb = ttk.Scrollbar(table_wrap, orient="vertical", command=self.stats_table.yview, style="Custom.Vertical.TScrollbar")
        self.stats_table.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.stats_table.pack(fill=tk.BOTH, expand=True)

    def _stats_bar(self):
        title_bar = tk.Frame(self.root, bg=self.ERROR_HDR)
        title_bar.pack(fill=tk.X, padx=14, pady=(0, 0))
        tk.Label(
            title_bar,
            text="Lexical Error Detection Log",
            font=("Helvetica", 12, "bold"),
            fg="#fff8fb",
            bg=self.ERROR_HDR,
        ).pack(side=tk.LEFT, padx=20, pady=6)

        bar = tk.Frame(self.root, bg=self.ERROR_HDR, pady=10)
        bar.pack(fill=tk.X, padx=14)

        self.lbl_tokens = self._stat(bar, "Tokens: -", boxed=False)
        self.lbl_identifiers = self._stat(bar, "Identifiers: -", boxed=False)
        self.lbl_errors = self._stat(bar, "Errors: -", boxed=False)
        self.lbl_tokens.pack(side=tk.LEFT, padx=(14, 28))
        self.lbl_identifiers.pack(side=tk.LEFT, padx=(0, 28))
        self.lbl_errors.pack(side=tk.LEFT)

        self.lbl_status = tk.Label(
            bar,
            text="Ready",
            font=("Helvetica", 11, "bold"),
            fg="#ffffff",
            bg=self.PANEL_DARK,
        )
        self.lbl_status.pack(side=tk.RIGHT, padx=14)

    def _error_panel(self):
        outer = tk.Frame(
            self.root,
            bg=self.ERROR_BG,
            highlightbackground=self.ERROR_BORDER,
            highlightthickness=1,
        )
        outer.pack(fill=tk.X, padx=14, pady=(0, 14), ipady=4)

        self.error_log = tk.Text(
            outer,
            font=("Consolas", 12),
            bg=self.ERROR_BG,
            fg=self.ERROR_TEXT,
            height=7,
            state=tk.DISABLED,
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
        )
        self.error_log.pack(fill=tk.X, pady=(2, 10))

    def _section_title(self, parent, text):
        row = tk.Frame(parent, bg=parent["bg"])
        row.pack(fill=tk.X, padx=12, pady=(10, 4))
        tk.Label(row, text=text, font=("Helvetica", 8, "bold"), fg=self.ACCENT_LT, bg=parent["bg"]).pack(side=tk.LEFT)
        tk.Frame(row, bg=self.ACCENT_LT, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0), pady=5)

    def _stat(self, parent, text, boxed=True):
        bg = self.PANEL_DARK if boxed else self.ERROR_HDR
        return tk.Label(parent, text=text, font=("Consolas", 11, "bold"), fg="#ffffff", bg=bg)

    def _btn(self, parent, text, cmd, color, hover):
        button = tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=color,
            fg="#fff",
            font=("Helvetica", 10, "bold"),
            padx=14,
            pady=7,
            relief="flat",
            cursor="hand2",
            bd=0,
            activebackground=hover,
            activeforeground="#fff",
        )
        button.bind("<Enter>", lambda _: button.config(bg=hover))
        button.bind("<Leave>", lambda _: button.config(bg=color))
        return button

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text / Source Files", "*.txt *.c *.cpp *.java *.py *.h")])
        if path:
            with open(path, "r", encoding="utf-8", errors="replace") as file:
                content = file.read()
            self.code_text.delete("1.0", tk.END)
            self.code_text.insert(tk.END, content)
            self._update_line_numbers()
            short = path.replace("\\", "/").split("/")[-1]
            self.lbl_status.config(text=f"Loaded: {short}", fg=self.BLUE_LT)

    def clear_all(self):
        self.code_text.delete("1.0", tk.END)
        self._update_line_numbers()
        self._clear_highlights()

        self.error_log.config(state=tk.NORMAL)
        self.error_log.delete("1.0", tk.END)
        self.error_log.config(state=tk.DISABLED)

        for item in self.token_table.get_children():
            self.token_table.delete(item)
        for item in self.sym_table.get_children():
            self.sym_table.delete(item)
        for item in self.stats_table.get_children():
            self.stats_table.delete(item)

        self.lbl_tokens.config(text="Tokens: -", fg="#ffffff")
        self.lbl_identifiers.config(text="Identifiers: -", fg="#ffffff")
        self.lbl_errors.config(text="Errors: -", fg="#ffffff")
        self.lbl_status.config(text="Cleared", fg="#ffffff")
        self.stats_summary.config(text="Run analysis to see statistics.")

    def analyze_code(self):
        for item in self.token_table.get_children():
            self.token_table.delete(item)
        for item in self.sym_table.get_children():
            self.sym_table.delete(item)
        for item in self.stats_table.get_children():
            self.stats_table.delete(item)

        source = self.code_text.get("1.0", tk.END)
        if not source.strip():
            messagebox.showwarning("Empty Input", "Please type or load source code first.")
            return

        tokens, symbols, errors = self.lexer.tokenize(source)

        for i, (token_type, token_value, token_line, token_col) in enumerate(tokens):
            tag = "odd" if i % 2 == 0 else "even"
            self.token_table.insert("", tk.END, values=(token_type, token_value, token_line, token_col), tags=(tag,))

        for i, (name, info) in enumerate(sorted(symbols.items())):
            tag = "odd" if i % 2 == 0 else "even"
            self.sym_table.insert(
                "",
                tk.END,
                values=(name, info["type"], info["scope"], info["line"], info["col"]),
                tags=(tag,),
            )

        counts = Counter(token[0] for token in tokens)
        total = len(tokens)
        for i, (token_type, count) in enumerate(sorted(counts.items(), key=lambda item: -item[1])):
            pct = f"{count / total * 100:.1f}%" if total else "0%"
            tag = "odd" if i % 2 == 0 else "even"
            self.stats_table.insert("", tk.END, values=(token_type, count, pct), tags=(tag,))
        self.stats_summary.config(
            text=f"Total tokens: {total}   |   Unique types: {len(counts)}   |   Identifiers: {len(symbols)}"
        )

        self.error_log.config(state=tk.NORMAL)
        self.error_log.delete("1.0", tk.END)
        if errors:
            for err in errors:
                self.error_log.insert(tk.END, f"  {err}\n")
            self.lbl_errors.config(text=f"Errors: {len(errors)}", fg=self.DANGER)
            self.lbl_status.config(text="Errors detected", fg=self.DANGER)
        else:
            self.error_log.insert(tk.END, "  Lexical analysis successful - 0 errors detected.")
            self.lbl_errors.config(text="Errors: 0", fg=self.SUCCESS)
            self.lbl_status.config(text="Analysis complete", fg=self.SUCCESS)
        self.error_log.config(state=tk.DISABLED)

        self.lbl_tokens.config(text=f"Tokens: {total}", fg="#ffffff")
        self.lbl_identifiers.config(text=f"Identifiers: {len(symbols)}", fg="#ffffff")

        self._apply_highlighting(source)

    def _clear_highlights(self):
        for tag in ("hl_kw", "hl_str", "hl_cmt", "hl_num", "hl_op"):
            self.code_text.tag_remove(tag, "1.0", tk.END)

    def _apply_highlighting(self, source):
        self._clear_highlights()
        rules = [
            ("hl_cmt", r"/\*[\s\S]*?\*/|//[^\n]*"),
            ("hl_str", r'"[^"\n]*"'),
            (
                "hl_kw",
                r"\b(?:int|float|char|double|if|else|while|for|return|void|break|continue|switch|case|default|do|struct|bool|string|const|long|short|unsigned|signed|NULL|true|false)\b",
            ),
            ("hl_num", r"\b0[xX][0-9a-fA-F]+\b|\b\d+(?:\.\d+)?\b"),
            ("hl_op", r"&&|\|\||!|<<|>>|[&|^~]|==|!=|<=|>=|[+\-*/%<>=]"),
        ]
        for tag, pattern in rules:
            for match in re.finditer(pattern, source):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.code_text.tag_add(tag, start, end)

    def export_tokens(self):
        rows = [self.token_table.item(child)["values"] for child in self.token_table.get_children()]
        if not rows:
            messagebox.showinfo("Export", "No tokens to export. Run analysis first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv"), ("Text", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write("Token Type,Lexeme,Line,Column\n")
                for row in rows:
                    file.write(",".join(str(value) for value in row) + "\n")
            messagebox.showinfo("Exported", f"Token stream saved to:\n{path}")

    def export_symbols(self):
        rows = [self.sym_table.item(child)["values"] for child in self.sym_table.get_children()]
        if not rows:
            messagebox.showinfo("Export", "No symbol table to export. Run analysis first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv"), ("Text", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write("Identifier,Type,Scope,Line,Column\n")
                for row in rows:
                    file.write(",".join(str(value) for value in row) + "\n")
            messagebox.showinfo("Exported", f"Symbol table saved to:\n{path}")
