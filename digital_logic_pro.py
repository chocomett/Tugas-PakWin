"""
╔══════════════════════════════════════════════════════╗
║         DIGITAL LOGIC SUITE  –  v2.0                ║
║  Gabungan 5 tools untuk mata kuliah Kerkom / Logika  ║
╚══════════════════════════════════════════════════════╝

DEPENDENCIES (auto-install saat pertama kali dijalankan):
  pip install schemdraw matplotlib Pillow

Jalankan:
  python digital_logic_suite.py
"""

import sys, subprocess, importlib, os, math, threading

# ─────────────────────────────────────────────────────────
#  AUTO INSTALLER
# ─────────────────────────────────────────────────────────
REQUIRED = {
    "schemdraw": "schemdraw",
    "matplotlib": "matplotlib",
    "PIL":        "Pillow",
}

def check_and_install():
    missing = []
    for mod, pkg in REQUIRED.items():
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append((mod, pkg))

    if not missing:
        return True

    print("╔══════════════════════════════════════════════╗")
    print("║  Library yang dibutuhkan belum terinstall:   ║")
    for m, p in missing:
        print(f"║    • {p:<40}║")
    print("╠══════════════════════════════════════════════╣")
    print("║  Menginstall otomatis sekarang...            ║")
    print("╚══════════════════════════════════════════════╝")
    all_ok = True
    for _, pkg in missing:
        print(f"\n  → pip install {pkg}")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ✗ Gagal install {pkg}:\n{result.stderr}")
            all_ok = False
        else:
            print(f"  ✓ {pkg} berhasil diinstall")
    if all_ok:
        print("\n  ✓ Semua library berhasil diinstall.")
        print("  Restart program untuk memuat library baru.\n")
    else:
        print("\n  ✗ Beberapa library gagal diinstall.")
        print("  Install manual: pip install schemdraw matplotlib Pillow\n")
    return False

if not check_and_install():
    sys.exit(0)

import tkinter as tk
from tkinter import messagebox, ttk

# ─────────────────────────────────────────────────────────
#  THEME SYSTEM — DARK & LIGHT MODE
# ─────────────────────────────────────────────────────────

DARK_THEME = {
    "BG":         "#08080c",
    "PANEL":      "#0f0f18",
    "SURFACE":    "#161622",
    "SURFACE2":   "#1c1c2e",
    "SURFACE3":   "#222236",
    "BORDER":     "#2e2e4a",
    "BORDER_HI":  "#4a4a7a",
    "BLUE":       "#4f8ef7",
    "BLUE_DIM":   "#15233d",
    "BLUE_MID":   "#2a4a80",
    "BLUE_GLOW":  "#7eb8ff",
    "BLUE_DEEP":  "#0a1628",
    "CYAN":       "#00e5ff",
    "CYAN_DIM":   "#003d4d",
    "WHITE":      "#eef2ff",
    "GREY":       "#8892b0",
    "GREY_DIM":   "#3d4466",
    "RED":        "#ff4d6a",
    "RED_DIM":    "#3d0a14",
    "RED_MID":    "#7a1525",
    "ORANGE":     "#ff8c42",
    "ORANGE_DIM": "#3d1f0a",
    "GREEN":      "#39e07a",
    "GREEN_DIM":  "#0a2e1a",
    "YELLOW":     "#ffe033",
    "YELLOW_DIM": "#2e2500",
    "PURPLE":     "#a78bfa",
    "PURPLE_DIM": "#1e1040",
    "NAV_ACTIVE_BG": "#1a2a4a",
    "NAV_ACTIVE_FG": "#7eb8ff",
}

LIGHT_THEME = {
    "BG":         "#f5f7fa",
    "PANEL":      "#ffffff",
    "SURFACE":    "#f0f4ff",
    "SURFACE2":   "#e8edf8",
    "SURFACE3":   "#dce3f5",
    "BORDER":     "#c4cde0",
    "BORDER_HI":  "#6b8dd6",
    "BLUE":       "#2563eb",
    "BLUE_DIM":   "#e0eaff",
    "BLUE_MID":   "#bfcffd",
    "BLUE_GLOW":  "#1a4dcc",
    "BLUE_DEEP":  "#edf2ff",
    "CYAN":       "#0369a1",
    "CYAN_DIM":   "#e0f2fe",
    "WHITE":      "#111827",
    "GREY":       "#374151",
    "GREY_DIM":   "#6b7280",
    "RED":        "#dc2626",
    "RED_DIM":    "#fee2e2",
    "RED_MID":    "#ef4444",
    "ORANGE":     "#c2410c",
    "ORANGE_DIM": "#fff7ed",
    "GREEN":      "#15803d",
    "GREEN_DIM":  "#dcfce7",
    "YELLOW":     "#92400e",
    "YELLOW_DIM": "#fffbeb",
    "PURPLE":     "#6d28d9",
    "PURPLE_DIM": "#ede9fe",
    "NAV_ACTIVE_BG": "#dbeafe",
    "NAV_ACTIVE_FG": "#1d4ed8",
}

_current_theme = DARK_THEME

def _t(key):
    return _current_theme[key]

# Dynamic theme accessors — used throughout the code
def _bg():         return _current_theme["BG"]
def _panel():      return _current_theme["PANEL"]
def _surface():    return _current_theme["SURFACE"]
def _surface2():   return _current_theme["SURFACE2"]
def _surface3():   return _current_theme["SURFACE3"]

# Shorthand globals — reassigned on theme switch via apply_theme()
BG         = _current_theme["BG"]
PANEL      = _current_theme["PANEL"]
SURFACE    = _current_theme["SURFACE"]
SURFACE2   = _current_theme["SURFACE2"]
SURFACE3   = _current_theme["SURFACE3"]
BORDER     = _current_theme["BORDER"]
BORDER_HI  = _current_theme["BORDER_HI"]
BLUE       = _current_theme["BLUE"]
BLUE_DIM   = _current_theme["BLUE_DIM"]
BLUE_MID   = _current_theme["BLUE_MID"]
BLUE_GLOW  = _current_theme["BLUE_GLOW"]
BLUE_DEEP  = _current_theme["BLUE_DEEP"]
CYAN       = _current_theme["CYAN"]
CYAN_DIM   = _current_theme["CYAN_DIM"]
WHITE      = _current_theme["WHITE"]
GREY       = _current_theme["GREY"]
GREY_DIM   = _current_theme["GREY_DIM"]
RED        = _current_theme["RED"]
RED_DIM    = _current_theme["RED_DIM"]
RED_MID    = _current_theme["RED_MID"]
ORANGE     = _current_theme["ORANGE"]
ORANGE_DIM = _current_theme["ORANGE_DIM"]
GREEN      = _current_theme["GREEN"]
GREEN_DIM  = _current_theme["GREEN_DIM"]
YELLOW     = _current_theme["YELLOW"]
YELLOW_DIM = _current_theme["YELLOW_DIM"]
PURPLE     = _current_theme["PURPLE"]
PURPLE_DIM = _current_theme["PURPLE_DIM"]
NAV_ACTIVE_BG  = _current_theme["NAV_ACTIVE_BG"]
NAV_ACTIVE_FG  = _current_theme["NAV_ACTIVE_FG"]

F_HEAD   = ("Segoe UI", 12, "bold")
F_BODY   = ("Segoe UI", 11)
F_SMALL  = ("Segoe UI", 9)
F_MONO   = ("Consolas", 12)
F_MONO_S = ("Consolas", 10)
F_CALC   = ("Consolas", 26, "bold")
F_CALC_S = ("Consolas", 14)
F_BTN    = ("Segoe UI", 10, "bold")
F_NAV    = ("Segoe UI", 9,  "bold")

# ─────────────────────────────────────────────────────────
#  WIDGET HELPERS  v3 — MEGAH EDITION
# ─────────────────────────────────────────────────────────

def _lighten(hex_color, amount=40):
    try:
        r=int(hex_color[1:3],16); g=int(hex_color[3:5],16); b=int(hex_color[5:7],16)
        r=min(255,r+amount); g=min(255,g+amount); b=min(255,b+amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    except: return hex_color

def _darken(hex_color, amount=25):
    try:
        r=int(hex_color[1:3],16); g=int(hex_color[3:5],16); b=int(hex_color[5:7],16)
        r=max(0,r-amount); g=max(0,g-amount); b=max(0,b-amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    except: return hex_color

def styled_entry(parent, font=None, **kw):
    e = tk.Entry(parent, font=font or F_MONO,
                 bg=SURFACE, fg=WHITE, insertbackground=CYAN,
                 relief="flat", highlightthickness=2,
                 highlightbackground=BORDER, highlightcolor=CYAN, **kw)
    def _on_focus_in(ev):
        e.config(highlightbackground=BLUE, bg=SURFACE3)
    def _on_focus_out(ev):
        e.config(highlightbackground=BORDER, bg=SURFACE)
    def _on_enter(ev):
        if e["state"] != "disabled":
            e.config(highlightbackground=BORDER_HI)
    def _on_leave(ev):
        if e["state"] != "disabled":
            if e is not e.focus_get():
                e.config(highlightbackground=BORDER)
    e.bind("<FocusIn>",  _on_focus_in)
    e.bind("<FocusOut>", _on_focus_out)
    e.bind("<Enter>",    _on_enter)
    e.bind("<Leave>",    _on_leave)
    return e

def styled_text(parent, height=8):
    t = tk.Text(parent, font=F_MONO, bg=SURFACE, fg=WHITE,
                relief="flat", highlightthickness=2,
                highlightbackground=BORDER, highlightcolor=CYAN,
                insertbackground=CYAN, height=height,
                padx=12, pady=10, wrap="word",
                selectbackground=BLUE_MID, selectforeground=WHITE)
    t.tag_config("heading", foreground=BLUE_GLOW, font=("Consolas",10,"bold"))
    t.tag_config("result",  foreground=GREEN,     font=("Consolas",12,"bold"))
    t.tag_config("muted",   foreground=GREY)
    t.tag_config("var",     foreground=CYAN)
    t.tag_config("warn",    foreground=YELLOW)
    t.tag_config("err",     foreground=RED)
    t.bind("<Enter>", lambda e: t.config(highlightbackground=BORDER_HI))
    t.bind("<Leave>", lambda e: t.config(highlightbackground=BORDER))
    return t

def section_label(parent, text):
    f = tk.Frame(parent, bg=PANEL)
    f.pack(fill="x", pady=(14, 4))
    # thicker glow bar on left
    bar = tk.Frame(f, bg=BLUE, width=4)
    bar.pack(side="left", fill="y", padx=(0, 10))
    lbl = tk.Label(f, text=text, font=F_HEAD, bg=PANEL, fg=WHITE)
    lbl.pack(side="left")
    # animated: bar brightens on hover
    def _enter(e): bar.config(bg=CYAN)
    def _leave(e): bar.config(bg=BLUE)
    for w in (f, lbl, bar):
        w.bind("<Enter>", _enter)
        w.bind("<Leave>", _leave)

def hint_label(parent, text):
    tk.Label(parent, text=text, font=F_SMALL, bg=PANEL,
             fg=GREY_DIM, justify="left").pack(anchor="w", pady=(0,6))

def action_btn(parent, text, cmd, color=BLUE):
    """Premium action button with glow hover, press-down effect."""
    press_color  = _darken(color, 30)
    hover_color  = _lighten(color, 30)
    glow_border  = _lighten(color, 60)

    b = tk.Button(parent, text=text, font=F_BTN,
                  bg=color, fg=WHITE,
                  activebackground=press_color,
                  activeforeground=WHITE,
                  relief="flat", cursor="hand2",
                  command=cmd, pady=8,
                  padx=14,
                  highlightthickness=2,
                  highlightbackground=_darken(color, 15),
                  highlightcolor=glow_border,
                  bd=0)

    def _enter(e):
        b.config(bg=hover_color,
                 highlightbackground=glow_border,
                 fg=BG if color not in (RED_DIM, GREY_DIM, BLUE_DIM, ORANGE_DIM, GREEN_DIM) else WHITE)
    def _leave(e):
        b.config(bg=color,
                 highlightbackground=_darken(color, 15),
                 fg=WHITE)
    def _press(e):   b.config(bg=press_color, relief="sunken")
    def _release(e): b.config(bg=hover_color, relief="flat")

    b.bind("<Enter>",          _enter)
    b.bind("<Leave>",          _leave)
    b.bind("<ButtonPress-1>",  _press)
    b.bind("<ButtonRelease-1>",_release)
    return b

def info_box(parent, title, body):
    """Glowing info card with left accent bar."""
    outer = tk.Frame(parent, bg=BLUE_MID, padx=1, pady=1)
    outer.pack(fill="x", pady=(0,14))
    inner = tk.Frame(outer, bg=BLUE_DEEP, padx=0, pady=0)
    inner.pack(fill="both", expand=True)

    left_bar = tk.Frame(inner, bg=BLUE, width=4)
    left_bar.pack(side="left", fill="y")
    content = tk.Frame(inner, bg=BLUE_DEEP, padx=14, pady=10)
    content.pack(side="left", fill="both", expand=True)

    tk.Label(content, text="⬡  "+title, font=("Segoe UI", 8, "bold"),
             bg=BLUE_DEEP, fg=CYAN).pack(anchor="w")
    tk.Label(content, text=body, font=F_SMALL, bg=BLUE_DEEP, fg=GREY,
             justify="left", wraplength=700).pack(anchor="w", pady=(4,0))

    def _enter(e):
        outer.config(bg=BLUE)
        left_bar.config(bg=CYAN)
    def _leave(e):
        outer.config(bg=BLUE_MID)
        left_bar.config(bg=BLUE)
    for w in (outer, inner, content, left_bar):
        w.bind("<Enter>", _enter)
        w.bind("<Leave>", _leave)

# ─────────────────────────────────────────────────────────
#  PAGE BASE
# ─────────────────────────────────────────────────────────
class Page(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL, padx=24, pady=16)

# ─────────────────────────────────────────────────────────
#  PAGE 1 — PROGRAMMER CALCULATOR
# ─────────────────────────────────────────────────────────
class PageCalc(Page):
    def __init__(self, parent):
        super().__init__(parent)
        self.value      = 0
        self.pending_a  = None
        self.pending_op = None
        self.new_input  = True
        self.mode       = "DEC"
        self.word_size  = 64
        self._mem       = 0
        self._expr_hist = ""
        self._build()

    def _build(self):
        info_box(self, "PROGRAMMER CALCULATOR",
                 "Kalkulator lengkap mode programmer.\n"
                 "• 4 basis tampil sekaligus: HEX, DEC, OCT, BIN\n"
                 "• Operasi bitwise: AND (&) · OR (|) · XOR (^) · NOT (~) · LSHIFT (<<) · RSHIFT (>>)\n"
                 "• Word Size: BYTE=8bit · WORD=16bit · DWORD=32bit · QWORD=64bit (batasi nilai)\n"
                 "• Memori: MS=simpan · MR=recall · M+=tambah ke memori\n"
                 "• Keyboard: ketik angka/operator langsung, Enter=hitung, Del=clear, Backspace=hapus digit")

        # ── Word Size pills ────────────────────────────────
        wsf = tk.Frame(self, bg=PANEL); wsf.pack(fill="x", pady=(0,6))
        tk.Label(wsf, text="WORD SIZE", font=F_SMALL, bg=PANEL, fg=GREY).pack(side="left", padx=(0,8))
        self.ws_btns = {}
        for label, bits in [("QWORD 64",64),("DWORD 32",32),("WORD 16",16),("BYTE 8",8)]:
            b = tk.Button(wsf, text=label, font=("Consolas",8,"bold"),
                          bg=SURFACE2, fg=GREY, relief="flat", cursor="hand2", padx=10, pady=4,
                          highlightthickness=1, highlightbackground=BORDER, bd=0,
                          command=lambda b=bits: self._set_ws(b))
            b.pack(side="left", padx=2)
            b.bind("<Enter>", lambda e, w=b: w.config(bg=SURFACE3, fg=WHITE, highlightbackground=BORDER_HI) if w.cget("bg") != BLUE else None)
            b.bind("<Leave>", lambda e, w=b: w.config(bg=SURFACE2, fg=GREY, highlightbackground=BORDER) if w.cget("bg") != BLUE else None)
            self.ws_btns[bits] = b
        self._set_ws(64, init=True)

        # ── Multi-base display ─────────────────────────────
        disp = tk.Frame(self, bg=SURFACE2, highlightthickness=2, highlightbackground=BORDER)
        disp.pack(fill="x", pady=(0,6))
        disp.bind("<Enter>", lambda e: disp.config(highlightbackground=BLUE_MID))
        disp.bind("<Leave>", lambda e: disp.config(highlightbackground=BORDER))
        self.disp_vars = {}
        self.disp_lbls = {}
        specs = [
            ("HEX","hex", CYAN,      F_CALC_S),
            ("DEC","dec", WHITE,     F_CALC),
            ("OCT","oct", GREY,      F_CALC_S),
            ("BIN","bin", BLUE_GLOW, ("Consolas",9)),
        ]
        for lbl, key, clr, fnt in specs:
            row = tk.Frame(disp, bg=SURFACE2); row.pack(fill="x", padx=14, pady=2)
            tk.Label(row, text=lbl, font=("Consolas",8,"bold"),
                     bg=SURFACE2, fg=BLUE_GLOW, width=4, anchor="w").pack(side="left")
            var = tk.StringVar(value="0")
            self.disp_vars[key] = var
            l = tk.Label(row, textvariable=var, font=fnt,
                         bg=SURFACE2, fg=clr, anchor="e")
            l.pack(side="right", fill="x", expand=True)
            self.disp_lbls[key] = l

        # expression history bar
        self.expr_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.expr_var, font=("Consolas",9),
                 bg=PANEL, fg=GREY_DIM, anchor="e").pack(fill="x", pady=(0,2))

        # ── Mode (input base) ──────────────────────────────
        mf = tk.Frame(self, bg=PANEL); mf.pack(fill="x", pady=(0,8))
        tk.Label(mf, text="INPUT BASE", font=F_SMALL, bg=PANEL, fg=GREY).pack(side="left", padx=(0,8))
        self.mode_btns = {}
        for m in ["HEX","DEC","OCT","BIN"]:
            b = tk.Button(mf, text=m, font=("Consolas",8,"bold"),
                          bg=SURFACE2, fg=GREY, relief="flat", cursor="hand2", padx=14, pady=5,
                          highlightthickness=1, highlightbackground=BORDER, bd=0,
                          command=lambda m=m: self._set_mode(m))
            b.pack(side="left", padx=2)
            b.bind("<Enter>", lambda e, w=b: w.config(bg=SURFACE3, fg=WHITE, highlightbackground=BLUE) if w.cget("bg") != BLUE else None)
            b.bind("<Leave>", lambda e, w=b: w.config(bg=SURFACE2, fg=GREY, highlightbackground=BORDER) if w.cget("bg") != BLUE else None)
            self.mode_btns[m] = b
        self._set_mode("DEC", init=True)

        # ── Keypad ─────────────────────────────────────────
        pad = tk.Frame(self, bg=BG); pad.pack(fill="x")

        # [text, col, row, colspan, bg_color]
        keys = [
            # row 0 – bitwise & special
            ("AND",0,0,1,BLUE_MID),("OR", 1,0,1,BLUE_MID),("XOR",2,0,1,BLUE_MID),("NOT",3,0,1,BLUE_MID),
            ("<<", 4,0,1,BLUE_MID),(">>",5,0,1,BLUE_MID),("MOD",6,0,1,BLUE_MID),("CLR",7,0,1,RED_MID),
            # row 1 – hex digits + parens
            ("A",  0,1,1,SURFACE3),("B", 1,1,1,SURFACE3),("C", 2,1,1,SURFACE3),("D", 3,1,1,SURFACE3),
            ("E",  4,1,1,SURFACE3),("F", 5,1,1,SURFACE3),("(",6,1,1,SURFACE2), (")",7,1,1,SURFACE2),
            # row 2
            ("7",  0,2,1,SURFACE2), ("8", 1,2,1,SURFACE2), ("9", 2,2,1,SURFACE2), ("÷",3,2,1,ORANGE_DIM),
            ("MS", 4,2,1,GREY_DIM),("MR",5,2,1,GREY_DIM),("M+",6,2,1,GREY_DIM),("⌫",7,2,1,RED_MID),
            # row 3
            ("4",  0,3,1,SURFACE2), ("5", 1,3,1,SURFACE2), ("6", 2,3,1,SURFACE2), ("×",3,3,1,ORANGE_DIM),
            ("±",  4,3,1,SURFACE3),("1/x",5,3,1,SURFACE3),("x²",6,3,1,SURFACE3),("√",7,3,1,SURFACE3),
            # row 4
            ("1",  0,4,1,SURFACE2), ("2", 1,4,1,SURFACE2), ("3", 2,4,1,SURFACE2), ("−",3,4,1,ORANGE_DIM),
            # row 5
            ("0",  0,5,2,SURFACE2), (".",2,5,1,SURFACE2),   ("+",3,5,1,ORANGE_DIM),
            ("=",  4,5,4,BLUE),
        ]
        self.key_btns = {}
        self.key_colors = {}
        for (lbl,c,r,cs,color) in keys:
            hover_c = _lighten(color, 35)
            press_c = _darken(color, 20)
            b = tk.Button(pad, text=lbl, font=("Segoe UI",9,"bold"),
                          bg=color, fg=WHITE, relief="flat", cursor="hand2",
                          highlightthickness=1, highlightbackground=_lighten(color, 10), bd=0,
                          command=lambda l=lbl: self._key(l))
            b.grid(row=r, column=c, columnspan=cs,
                   sticky="nsew", padx=2, pady=2, ipady=9)
            b.bind("<Enter>",          lambda e,b=b,hc=hover_c,bc=color:  b.config(bg=hc,  highlightbackground=_lighten(bc,50)) if b.cget("state")=="normal" else None)
            b.bind("<Leave>",          lambda e,b=b,oc=color:              b.config(bg=oc,  highlightbackground=_lighten(oc,10)) if b.cget("state")=="normal" else None)
            b.bind("<ButtonPress-1>",  lambda e,b=b,pc=press_c:            b.config(bg=pc,  relief="sunken") if b.cget("state")=="normal" else None)
            b.bind("<ButtonRelease-1>",lambda e,b=b,hc=hover_c:            b.config(bg=hc,  relief="flat")   if b.cget("state")=="normal" else None)
            self.key_btns[lbl] = b
            self.key_colors[lbl] = color

        for i in range(8): pad.columnconfigure(i, weight=1)
        for i in range(6): pad.rowconfigure(i, weight=1)

        self._set_mode("DEC", init=True)
        self._refresh()

    def _mask(self): return (1 << self.word_size) - 1

    def _set_ws(self, bits, init=False):
        self.word_size = bits
        self.value &= self._mask()
        for b2, btn in self.ws_btns.items():
            btn.config(bg=BLUE if b2==bits else SURFACE2,
                       fg=WHITE if b2==bits else GREY,
                       highlightbackground=BLUE_GLOW if b2==bits else BORDER)
        if not init: self._refresh()

    def _set_mode(self, m, init=False):
        self.mode = m
        for m2, btn in self.mode_btns.items():
            btn.config(bg=BLUE if m2==m else SURFACE2,
                       fg=WHITE if m2==m else GREY,
                       highlightbackground=BLUE_GLOW if m2==m else BORDER)
        
        if hasattr(self, 'disp_lbls'):
            key_map = {"HEX": "hex", "DEC": "dec", "OCT": "oct", "BIN": "bin"}
            active_key = key_map[m]
            default_colors = {"hex": CYAN, "dec": WHITE, "oct": GREY, "bin": BLUE_GLOW}
            for k, lbl in self.disp_lbls.items():
                if k == active_key:
                    lbl.config(font=F_CALC, fg=CYAN)
                else:
                    lbl.config(font=("Consolas",9) if k=="bin" else F_CALC_S, fg=default_colors[k])
                    
        if hasattr(self, 'key_btns'):
            valid_map={"HEX":"0123456789ABCDEF", "DEC":"0123456789", "OCT":"01234567", "BIN":"01"}
            valid_chars = valid_map[m]
            for lbl, btn in self.key_btns.items():
                if lbl in "0123456789ABCDEF" and len(lbl)==1:
                    if lbl in valid_chars:
                        btn.config(state="normal", bg=self.key_colors[lbl], fg=WHITE)
                    else:
                        btn.config(state="disabled", bg=BG, fg=GREY_DIM)
                        
        if not init: self._refresh()

    def _refresh(self):
        v = self.value & self._mask()
        self.disp_vars["dec"].set(f"{v:,}")
        self.disp_vars["hex"].set(hex(v)[2:].upper() or "0")
        self.disp_vars["oct"].set(oct(v)[2:] or "0")
        b = format(v, f'0{self.word_size}b')
        groups = [b[i:i+4] for i in range(0, len(b), 4)]
        self.disp_vars["bin"].set("  ".join(groups))
        self.expr_var.set(self._expr_hist or " ")

    def _input_digit(self, d):
        base_map={"HEX":16,"DEC":10,"OCT":8,"BIN":2}
        valid_map={16:"0123456789abcdefABCDEF",10:"0123456789",8:"01234567",2:"01"}
        base = base_map[self.mode]
        if d.upper() not in valid_map[base].upper(): return
        if self.new_input:
            self._expr_hist += d.upper()
            cur = int(d, base)
            self.new_input = False
        else:
            old = self.value & self._mask()
            cur = old * base + int(d.upper(), base)
        self.value = cur & self._mask()
        self._refresh()

    def _key(self, lbl):
        if lbl.upper() in "0123456789ABCDEF" and len(lbl)==1:
            self._input_digit(lbl); return
        v = self.value & self._mask()
        op_map = {"−":"-","×":"*","÷":"//","MOD":"%",
                  "AND":"&","OR":"|","XOR":"^","<<":"<<",">>":">>","+":"+"}
        if lbl == "CLR":
            self.value=0; self._expr_hist=""; self.pending_op=None
            self.pending_a=None; self.new_input=True
        elif lbl == "⌫":
            base_map={"HEX":16,"DEC":10,"OCT":8,"BIN":2}
            self.value=(v//base_map[self.mode])&self._mask()
            if self._expr_hist: self._expr_hist=self._expr_hist[:-1]
        elif lbl == "=":
            self._compute()
            return
        elif lbl in op_map:
            self.pending_a  = v
            self.pending_op = op_map[lbl]
            self._expr_hist += f" {lbl} "
            self.new_input = True
        elif lbl == "NOT":
            self.value=(~v)&self._mask()
            self._expr_hist=f"~({self._expr_hist})"
        elif lbl == "±":
            self.value=(-v)&self._mask()
        elif lbl == "1/x":
            self.value=(1//v if v!=0 else 0)&self._mask()
        elif lbl == "x²":
            self.value=(v*v)&self._mask()
        elif lbl == "√":
            self.value=int(math.isqrt(abs(v)))&self._mask()
        elif lbl in ("(",")" ):
            self._expr_hist+=lbl
        elif lbl == "MS":
            self._mem=v
        elif lbl == "MR":
            self.value=self._mem&self._mask(); self.new_input=True
        elif lbl == "M+":
            self._mem=(self._mem+v)&self._mask()
        self._refresh()

    def _compute(self):
        if self.pending_a is not None and self.pending_op:
            b = self.value & self._mask()
            try:
                result = eval(f"{self.pending_a} {self.pending_op} {b}")
                self.value = int(result) & self._mask()
            except ZeroDivisionError:
                messagebox.showerror("Error","Pembagian dengan nol!")
                self.value = 0
            except Exception:
                self.value = 0
            self._expr_hist += f" = {self.value}"
            self.pending_a = None; self.pending_op = None
            self.new_input = True
        self._refresh()

    def _kb(self, event):
        mapping = {
            "+":"+","-":"−","*":"×","/":"÷","%":"MOD",
            "&":"AND","|":"OR","^":"XOR","~":"NOT",
        }
        k = event.char
        if k in "0123456789abcdefABCDEF":
            self._key(k.upper())
        elif k in mapping:
            self._key(mapping[k])
        elif event.keysym=="Return":     self._key("=")
        elif event.keysym=="BackSpace":  self._key("⌫")
        elif event.keysym=="Delete":     self._key("CLR")


# ─────────────────────────────────────────────────────────
#  PAGE 2 — SOP SIMPLIFIER (Quine-McCluskey)
# ─────────────────────────────────────────────────────────
def _qm_bin(n,bits): return format(n,f'0{bits}b')
def _qm_d1(a,b):    return sum(x!=y for x,y in zip(a,b))==1
def _qm_comb(a,b):  return ''.join('-' if x!=y else x for x,y in zip(a,b))

def qm_prime_implicants(minterms, nv):
    grp={}
    for m in minterms:
        b=_qm_bin(m,nv); c=b.count('1')
        grp.setdefault(c,set()).add(b)
    pis=set()
    while grp:
        ng,done={},set()
        for k in sorted(grp):
            if k+1 not in grp: continue
            for t1 in grp[k]:
                for t2 in grp[k+1]:
                    if _qm_d1(t1,t2):
                        ct=_qm_comb(t1,t2)
                        ng.setdefault(ct.count('1'),set()).add(ct)
                        done.update([t1,t2])
        for k in grp:
            for t in grp[k]:
                if t not in done: pis.add(t)
        grp=ng
    return pis

def qm_essential(pis,minterms,nv):
    chart={pi:[] for pi in pis}
    for pi in pis:
        for m in minterms:
            bm=_qm_bin(m,nv)
            if all(pi[i]=='-' or pi[i]==bm[i] for i in range(nv)):
                chart[pi].append(m)
    cnt={m:0 for m in minterms}
    for cv in chart.values():
        for m in cv: cnt[m]+=1
    epis,cov=set(),set()
    for m,c in cnt.items():
        if c==1:
            for pi,cm in chart.items():
                if m in cm: epis.add(pi); cov.update(cm)
    return epis,cov

def sop_fmt(imps):
    V="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res=[]
    for t in imps:
        s="".join(V[i] if c=='1' else V[i]+"'" if c=='0' else "" for i,c in enumerate(t))
        res.append(s or "1")
    return " + ".join(res) if res else "0"

class PageSOP(Page):
    def __init__(self, parent):
        super().__init__(parent)
        info_box(self,"SOP SIMPLIFIER – Quine-McCluskey",
                 "Menyederhanakan fungsi Boolean bentuk SOP (Sum of Products).\n"
                 "Algoritma Quine-McCluskey lebih akurat dari K-Map untuk variabel > 4.\n"
                 "• Prime Implicant (PI): term yang tidak bisa digabung/disederhanakan lagi.\n"
                 "• Essential PI (EPI): PI yang wajib ada karena satu-satunya yang cover suatu minterm.\n"
                 "• Hasil akhir F = bentuk SOP paling sederhana dari EPI.")
        row = tk.Frame(self,bg=PANEL); row.pack(fill="x",pady=(0,8))
        l=tk.Frame(row,bg=PANEL); l.pack(side="left",fill="x",expand=True,padx=(0,10))
        section_label(l,"JUMLAH VARIABEL")
        hint_label(l,"Angka 1–8")
        self.e_v=styled_entry(l); self.e_v.pack(fill="x",ipady=5)
        r=tk.Frame(row,bg=PANEL); r.pack(side="left",fill="x",expand=True)
        section_label(r,"MINTERMS")
        hint_label(r,"Pisah koma  ·  Contoh: 0, 1, 3, 5, 7")
        self.e_mt=styled_entry(r); self.e_mt.pack(fill="x",ipady=5)
        action_btn(self,"⚙  SEDERHANAKAN",self.solve).pack(fill="x",pady=12)
        self.txt=styled_text(self,height=14); self.txt.pack(fill="both",expand=True)

    def solve(self):
        try: nv=int(self.e_v.get().strip())
        except: messagebox.showerror("Error","Jumlah variabel harus angka!"); return
        try: mts=[int(x.strip()) for x in self.e_mt.get().split(",") if x.strip()]
        except: messagebox.showerror("Error","Minterms harus angka dipisah koma!"); return
        if not mts: messagebox.showerror("Error","Minterms tidak boleh kosong!"); return
        pis=qm_prime_implicants(mts,nv)
        epis,_=qm_essential(pis,mts,nv)
        self.txt.config(state="normal")
        self.txt.delete("1.0",tk.END)
        self.txt.insert(tk.END,"QUINE-McCLUSKEY SIMPLIFICATION\n","heading")
        self.txt.insert(tk.END,"─"*50+"\n","muted")
        self.txt.insert(tk.END,f"Variabel  : ","muted")
        self.txt.insert(tk.END,", ".join(chr(65+i) for i in range(nv))+"\n","var")
        self.txt.insert(tk.END,f"Minterms  : {mts}\n\n","muted")
        self.txt.insert(tk.END,"PRIME IMPLICANTS\n","heading")
        self.txt.insert(tk.END,f"  Biner    : {sorted(pis)}\n","muted")
        self.txt.insert(tk.END,f"  Variabel : ","muted"); self.txt.insert(tk.END,sop_fmt(pis)+"\n\n","var")
        self.txt.insert(tk.END,"ESSENTIAL PRIME IMPLICANTS\n","heading")
        self.txt.insert(tk.END,f"  Biner    : {sorted(epis)}\n","muted")
        self.txt.insert(tk.END,f"  Variabel : ","muted"); self.txt.insert(tk.END,sop_fmt(epis)+"\n\n","var")
        self.txt.insert(tk.END,"─"*50+"\n","muted")
        self.txt.insert(tk.END,"  F  =  ","heading"); self.txt.insert(tk.END,sop_fmt(epis)+"\n","result")
        self.txt.config(state="disabled")


# ─────────────────────────────────────────────────────────
#  PAGE 3 — BOOLEAN EQUATION GENERATOR
# ─────────────────────────────────────────────────────────
class PageEquation(Page):
    def __init__(self, parent):
        super().__init__(parent)
        info_box(self,"BOOLEAN EQUATION GENERATOR",
                 "Membangkitkan persamaan Boolean SOP dari kolom output Truth Table.\n"
                 "• Jumlah nilai harus 2ⁿ: 2=1var · 4=2var · 8=3var · 16=4var · 32=5var\n"
                 "• Program otomatis deteksi jumlah variabel dari banyaknya nilai input.\n"
                 "• Output: daftar minterm + ekspresi F = ... dalam bentuk SOP lengkap.\n"
                 "• Tip: gunakan hasil ini sebagai input SOP Simplifier untuk menyederhanakan.")
        section_label(self,"OUTPUT TRUTH TABLE")
        hint_label(self,"Nilai 0/1 dipisah spasi  ·  Jumlah harus 2ⁿ  ·  Contoh (3 var / 8 baris): 0 1 1 0 1 0 0 1")
        self.entry=styled_entry(self); self.entry.pack(fill="x",ipady=6,pady=(0,12))
        action_btn(self,"⚙  GENERATE EQUATION",self.generate).pack(fill="x",pady=(0,12))
        self.txt=styled_text(self,height=13); self.txt.pack(fill="both",expand=True)

    def generate(self):
        raw=self.entry.get().strip()
        if not raw: messagebox.showerror("Error","Input tidak boleh kosong!"); return
        try:
            data=[int(x) for x in (raw.split() if ' ' in raw else list(raw))]
        except: messagebox.showerror("Error","Hanya angka 0 atau 1!"); return
        if not all(x in [0,1] for x in data):
            messagebox.showerror("Error","Input hanya boleh 0 atau 1."); return
        total=len(data); nv_f=math.log2(total)
        if not nv_f.is_integer() or total<2:
            messagebox.showerror("Error",f"Jumlah data ({total}) harus pangkat 2."); return
        nv=int(nv_f); vars_=[chr(65+i) for i in range(nv)]
        minterms=[]
        for i,val in enumerate(data):
            if val==1:
                b=format(i,f'0{nv}b')
                minterms.append((i,"".join(v if bit=='1' else v+"'" for v,bit in zip(vars_,b))))
        self.txt.config(state="normal")
        self.txt.delete("1.0",tk.END)
        self.txt.insert(tk.END,"BOOLEAN EQUATION GENERATOR\n","heading")
        self.txt.insert(tk.END,"─"*50+"\n","muted")
        self.txt.insert(tk.END,f"Variabel : ","muted")
        self.txt.insert(tk.END,", ".join(vars_)+f"  ({nv} variabel, {total} baris)\n\n","var")
        self.txt.insert(tk.END,"MINTERMS (output = 1):\n","heading")
        for idx,t in minterms:
            self.txt.insert(tk.END,f"  m({idx:2d}) = ","muted"); self.txt.insert(tk.END,t+"\n","var")
        self.txt.insert(tk.END,"\n"+"─"*50+"\n","muted")
        self.txt.insert(tk.END,"F  =  ","heading")
        if minterms: self.txt.insert(tk.END," + ".join(t for _,t in minterms)+"\n","result")
        else: self.txt.insert(tk.END,"0  (fungsi selalu false)\n","result")
        self.txt.config(state="disabled")


# ─────────────────────────────────────────────────────────
#  PAGE 4 — GATE CIRCUIT GENERATOR
# ─────────────────────────────────────────────────────────
def parse_sop(expr):
    expr=expr.replace(" ","")
    terms=[]
    for term in expr.split("+"):
        factors,i=[],0
        while i<len(term):
            if i+1<len(term) and term[i+1]=="'":
                factors.append((term[i],True)); i+=2
            else:
                factors.append((term[i],False)); i+=1
        if factors: terms.append(factors)
    return terms

class PageGate(Page):
    def __init__(self, parent):
        super().__init__(parent)
        self.img_ref=None
        info_box(self,"GATE CIRCUIT GENERATOR",
                 "Menggambar rangkaian gerbang logika dari ekspresi SOP secara otomatis.\n"
                 "• Gunakan tanda ' (apostrof) setelah variabel untuk NOT  →  A' = NOT A\n"
                 "• Gunakan + untuk OR antar-term  ·  Gabung langsung untuk AND\n"
                 "• Gerbang yang digambar: NOT, AND (multi-input), OR (multi-input)\n"
                 "• Gambar ditampilkan langsung di sini dan disimpan sebagai circuit_output.png\n"
                 "• Library yang dibutuhkan: schemdraw, matplotlib, Pillow (auto-install)")
        section_label(self,"EKSPRESI SOP")
        hint_label(self,"Contoh: A'BC + AB'C + ABC'   atau   A'B + AB'")
        ef=tk.Frame(self,bg=PANEL); ef.pack(fill="x",pady=(0,10))
        self.entry=styled_entry(ef); self.entry.pack(side="left",fill="x",expand=True,ipady=6,padx=(0,8))
        self.entry.insert(0,"A'B+AB'")
        action_btn(ef,"⚙ GENERATE",self.generate,BLUE).pack(side="left")
        self.status_var=tk.StringVar(value="")
        tk.Label(self,textvariable=self.status_var,font=F_SMALL,bg=PANEL,fg=GREY).pack(anchor="w",pady=(0,6))
        # image canvas with scrollbars
        img_outer=tk.Frame(self,bg=SURFACE,highlightthickness=2,highlightbackground=BORDER_HI)
        img_outer.pack(fill="both",expand=True)
        self.c_img=tk.Canvas(img_outer,bg=SURFACE,highlightthickness=0)
        vsb=ttk.Scrollbar(img_outer,orient="vertical",command=self.c_img.yview)
        hsb=ttk.Scrollbar(img_outer,orient="horizontal",command=self.c_img.xview)
        self.c_img.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        vsb.pack(side="right",fill="y"); hsb.pack(side="bottom",fill="x")
        self.c_img.pack(fill="both",expand=True)
        self.c_img.create_text(20,20,text="[ Gambar rangkaian akan tampil di sini setelah Generate ]",
                               anchor="nw",fill=GREY_DIM,font=F_SMALL)

    def generate(self):
        expr=self.entry.get().strip()
        if not expr: messagebox.showerror("Error","Masukkan ekspresi!"); return
        self.status_var.set("  ⏳ Menggambar rangkaian..."); self.update()
        threading.Thread(target=self._thread,args=(expr,),daemon=True).start()

    def _thread(self,expr):
        try:
            import schemdraw, schemdraw.logic as logic
            import matplotlib; matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            from PIL import Image

            parsed=parse_sop(expr)
            
            # Evaluasi state tema dinamis
            if _current_theme == DARK_THEME:
                schemdraw.theme('dark')
            else:
                schemdraw.theme('default') # Stroke hitam untuk Light Mode
                
            d=schemdraw.Drawing(canvas='matplotlib')
            outs,y=[],0
            for term in parsed:
                if len(term)==1:
                    var,neg=term[0]
                    if neg:
                        d.add(logic.Line().at((0,y)).to((2.5,y)).label(var,loc='left'))
                        ng=d.add(logic.Not().at((2.5,y)).right()); outs.append(ng.out)
                    else:
                        ln=d.add(logic.Line().at((0,y)).to((4,y)).label(var,loc='left')); outs.append(ln.end)
                else:
                    ag=d.add(logic.And(inputs=len(term)).at((2,y)))
                    for i,(var,neg) in enumerate(term):
                        inp=getattr(ag,f'in{i+1}')
                        if neg:
                            d.add(logic.Not().at((0.5,inp[1])).to(inp))
                            d.add(logic.Line().at((0,inp[1])).to((0.5,inp[1])).label(var,loc='left'))
                        else:
                            d.add(logic.Line().at((0,inp[1])).to(inp).label(var,loc='left'))
                    outs.append(ag.out)
                y-=3
            if len(outs)>1:
                cy=-(len(parsed)-1)*1.5
                og=d.add(logic.Or(inputs=len(outs)).at((7,cy)))
                for i,op in enumerate(outs):
                    d.add(logic.Wire('|-').at(op).to(getattr(og,f'in{i+1}')))
                d.add(logic.Line().at(og.out).right().label("Output"))
            else:
                d.add(logic.Line().at(outs[0]).right().label("Output"))

            path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"circuit_output.png")
            d.save(path, transparent=True); plt.close("all")
            img=Image.open(path); img.thumbnail((850,550))
            self.after(0,lambda: self._show_img(img,path))
        except Exception as e:
            self.after(0,lambda: self._show_err(str(e)))

    def _show_img(self,img,path):
        from PIL import ImageTk
        photo=ImageTk.PhotoImage(img); self.img_ref=photo
        self.c_img.delete("all")
        self.c_img.create_image(8,8,image=photo,anchor="nw")
        self.c_img.configure(scrollregion=(0,0,img.width+16,img.height+16))
        self.status_var.set(f"  ✓ Gambar disimpan: circuit_output.png  ({img.width}×{img.height}px)")

    def _show_err(self,msg):
        self.status_var.set(f"  ✗ Error: {msg}")
        messagebox.showerror("Error Generator",msg)


# ─────────────────────────────────────────────────────────
#  PAGE 5 — TRUTH TABLE BUILDER
# ─────────────────────────────────────────────────────────
class PageTruthTable(Page):
    def __init__(self, parent, on_export=None):
        super().__init__(parent)
        self.on_export=on_export; self.nv=0
        self.out_vals=[]; self.cell_btns=[]
        info_box(self,"TRUTH TABLE BUILDER & ANALYZER",
                 "Buat dan edit tabel kebenaran interaktif secara visual.\n"
                 "• Klik sel kolom OUTPUT untuk toggle nilai 0 ↔ 1\n"
                 "• Analisis otomatis: minterms (output=1) dan maxterms (output=0)\n"
                 "• Tombol Export: kirim data ke Equation Generator untuk dibuat persamaan\n"
                 "• 1 var=2 baris · 2 var=4 · 3 var=8 · 4 var=16 · 5 var=32 baris")
        top=tk.Frame(self,bg=PANEL); top.pack(fill="x",pady=(0,10))
        section_label(top,"JUMLAH VARIABEL (1–5)")
        hint_label(top,"Masukkan angka, klik Generate, lalu klik sel Output untuk toggle 0/1")
        inp=tk.Frame(top,bg=PANEL); inp.pack(fill="x")
        self.e_nv=styled_entry(inp,width=5); self.e_nv.insert(0,"3"); self.e_nv.pack(side="left",ipady=5,padx=(0,8))
        action_btn(inp,"⚙  GENERATE TABLE",self.build,BLUE).pack(side="left")
        if on_export:
            action_btn(inp,"→ EXPORT TO EQUATION GEN",self.do_export,BLUE_DIM).pack(side="left",padx=(8,0))
        outer=tk.Frame(self,bg=SURFACE,highlightthickness=2,highlightbackground=BORDER_HI)
        outer.pack(fill="both",expand=True,pady=(10,0))
        canvas=tk.Canvas(outer,bg=SURFACE,highlightthickness=0)
        vsb=ttk.Scrollbar(outer,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set); vsb.pack(side="right",fill="y")
        canvas.pack(fill="both",expand=True)
        self.tbl=tk.Frame(canvas,bg=SURFACE)
        self.tbl.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0),window=self.tbl,anchor="nw")
        canvas.bind_all("<MouseWheel>",lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))
        self.info_lbl=tk.Label(self,text="",font=F_SMALL,bg=PANEL,fg=GREY,justify="left")
        self.info_lbl.pack(anchor="w",pady=(6,0))

    def build(self):
        try:
            nv=int(self.e_nv.get().strip())
            if not 1<=nv<=5: raise ValueError
        except: messagebox.showerror("Error","Variabel harus 1–5."); return
        self.nv=nv; rows=2**nv
        self.out_vals=[0]*rows; self.cell_btns=[]
        for w in self.tbl.winfo_children(): w.destroy()
        vars_=[chr(65+i) for i in range(nv)]
        hrow=tk.Frame(self.tbl,bg=BLUE_DIM); hrow.pack(fill="x")
        tk.Label(hrow,text="  #",font=("Consolas",9,"bold"),bg=BLUE_DIM,fg=BLUE_GLOW,width=5,anchor="w").pack(side="left")
        for v in vars_:
            tk.Label(hrow,text=v,font=("Consolas",9,"bold"),bg=BLUE_DIM,fg=WHITE,width=5).pack(side="left")
        tk.Label(hrow,text="OUTPUT",font=("Consolas",9,"bold"),bg=BLUE_DIM,fg=YELLOW,width=8).pack(side="left")
        for i in range(rows):
            bits=format(i,f'0{nv}b')
            bg=SURFACE if i%2==0 else SURFACE2
            rf=tk.Frame(self.tbl,bg=bg); rf.pack(fill="x")
            tk.Label(rf,text=f"  {i}",font=F_MONO_S,bg=bg,fg=GREY_DIM,width=5,anchor="w").pack(side="left")
            for bit in bits:
                tk.Label(rf,text=bit,font=F_MONO_S,
                         bg=bg,fg=BLUE_GLOW if bit=='1' else GREY,width=5).pack(side="left")
            btn=tk.Button(rf,text="0",font=("Consolas",9,"bold"),
                          bg=bg,fg=GREY,relief="flat",cursor="hand2",width=7,
                          command=lambda idx=i: self._toggle(idx))
            btn.pack(side="left"); self.cell_btns.append(btn)
        self._upd()

    def _toggle(self,idx):
        self.out_vals[idx]=1-self.out_vals[idx]; v=self.out_vals[idx]
        self.cell_btns[idx].config(text=str(v),fg=GREEN if v else GREY)
        self._upd()

    def _upd(self):
        mt=[i for i,v in enumerate(self.out_vals) if v==1]
        mx=[i for i,v in enumerate(self.out_vals) if v==0]
        self.info_lbl.config(text=f"  Minterms (output=1): {mt if mt else '—'}     Maxterms (output=0): {mx if mx else '—'}")

    def do_export(self):
        seq=" ".join(str(v) for v in self.out_vals)
        if self.on_export: self.on_export(seq)


# ─────────────────────────────────────────────────────────
#  PAGE 6 — ALU 1-BIT
# ─────────────────────────────────────────────────────────
class PageALU(Page):
    def __init__(self, parent):
        super().__init__(parent)
        info_box(self, "ALU 1-BIT (ADDER & SUBTRACTOR)", 
                 "Menghitung penjumlahan dan pengurangan biner 1-bit.\n"
                 "• Adder menghasilkan Sum & Carry Out\n"
                 "• Subtractor menghasilkan Difference & Borrow Out")
        
        section_label(self, "INPUT BINER")
        hint_label(self, "Masukkan angka 0 atau 1 pada masing-masing kolom")
        
        row1 = tk.Frame(self, bg=PANEL); row1.pack(fill="x", pady=2)
        tk.Label(row1, text="Input A:", font=F_BODY, bg=PANEL, fg=GREY, width=15, anchor="w").pack(side="left")
        self.alu_a = styled_entry(row1, width=10); self.alu_a.pack(side="left")
        
        row2 = tk.Frame(self, bg=PANEL); row2.pack(fill="x", pady=2)
        tk.Label(row2, text="Input B:", font=F_BODY, bg=PANEL, fg=GREY, width=15, anchor="w").pack(side="left")
        self.alu_b = styled_entry(row2, width=10); self.alu_b.pack(side="left")
        
        row3 = tk.Frame(self, bg=PANEL); row3.pack(fill="x", pady=2)
        tk.Label(row3, text="Carry/Borrow In:", font=F_BODY, bg=PANEL, fg=GREY, width=15, anchor="w").pack(side="left")
        self.alu_cin = styled_entry(row3, width=10); self.alu_cin.pack(side="left")
        
        btn_f = tk.Frame(self, bg=PANEL); btn_f.pack(fill="x", pady=(16, 0))
        action_btn(btn_f, "➕ HITUNG ADDER", lambda: self.calc_alu("adder"), GREEN).pack(side="left", padx=(0, 10))
        action_btn(btn_f, "➖ HITUNG SUBTRACTOR", lambda: self.calc_alu("sub"), ORANGE).pack(side="left")
        
        section_label(self, "HASIL OUTPUT")
        self.res_var = tk.StringVar(value="...")
        tk.Label(self, textvariable=self.res_var, font=F_CALC_S, bg=PANEL, fg=CYAN, justify="left").pack(anchor="w")

    def calc_alu(self, mode):
        try:
            a, b, c = int(self.alu_a.get()), int(self.alu_b.get()), int(self.alu_cin.get())
            if not all(x in (0,1) for x in (a,b,c)): raise ValueError
            
            if mode == "adder":
                s = a ^ b ^ c
                cout = (a & b) | (b & c) | (a & c)
                self.res_var.set(f"∑ Sum (S) = {s}\nCarry Out (Cout) = {cout}")
            else:
                diff = a ^ b ^ c
                bout = (int(not a) & c) | (int(not a) & b) | (b & c)
                self.res_var.set(f"Δ Difference (D) = {diff}\nBorrow Out (Bout) = {bout}")
        except:
            messagebox.showerror("Error", "Input ALU harus berupa angka 0 atau 1!")

# ─────────────────────────────────────────────────────────
#  PAGE 7 — ARITMATIKA BINER N-BIT
# ─────────────────────────────────────────────────────────
class PageArith(Page):
    def __init__(self, parent):
        super().__init__(parent)
        info_box(self, "ARITMATIKA BINER N-BIT", 
                 "Kalkulator untuk menjumlahkan, mengurangkan, dan mengalikan bilangan biner.")
                 
        section_label(self, "OPERASI BINER")
        row = tk.Frame(self, bg=PANEL); row.pack(fill="x", pady=5)
        
        self.bin1 = styled_entry(row, width=15); self.bin1.pack(side="left", padx=(0, 10))
        
        self.op_var = tk.StringVar(value="+")
        op_menu = ttk.Combobox(row, textvariable=self.op_var, values=["+", "-", "*"], width=5, state="readonly", font=F_MONO)
        op_menu.pack(side="left", padx=10)
        
        self.bin2 = styled_entry(row, width=15); self.bin2.pack(side="left", padx=10)
        
        action_btn(self, "⚙ HITUNG", self.calc_binary, BLUE).pack(anchor="w", pady=16)
        
        section_label(self, "HASIL")
        self.res_var = tk.StringVar(value="...")
        tk.Label(self, textvariable=self.res_var, font=F_CALC_S, bg=PANEL, fg=GREEN, justify="left").pack(anchor="w")

    def calc_binary(self):
        try:
            val1 = int(self.bin1.get(), 2)
            val2 = int(self.bin2.get(), 2)
            op = self.op_var.get()
            
            if op == "+": res = val1 + val2
            elif op == "-": res = val1 - val2
            elif op == "*": res = val1 * val2
            
            if res < 0:
                bin_res = "-" + bin(res)[3:]
            else:
                bin_res = bin(res)[2:]
                
            self.res_var.set(f"Biner   : {bin_res}\nDesimal : {res}")
        except:
            messagebox.showerror("Error", "Input harus berupa bilangan biner yang valid!")

# ─────────────────────────────────────────────────────────
#  PAGE 8 — PRIORITY ENCODER 8-TO-3
# ─────────────────────────────────────────────────────────
class PageEncoder(Page):
    def __init__(self, parent):
        super().__init__(parent)
        info_box(self, "PRIORITY ENCODER 8-TO-3", 
                 "Pilih jalur input yang aktif (I7 hingga I0). Priority Encoder akan memproses "
                 "jalur dengan indeks tertinggi menjadi output biner 3-bit.")
                 
        section_label(self, "INPUT JALUR (CHECKBOX)")
        hint_label(self, "I7 memiliki prioritas tertinggi")
        
        f = tk.Frame(self, bg=SURFACE2, highlightthickness=2, highlightbackground=BORDER, padx=14, pady=14)
        f.pack(fill="x", pady=10)
        f.bind("<Enter>", lambda e: f.config(highlightbackground=BLUE_MID))
        f.bind("<Leave>", lambda e: f.config(highlightbackground=BORDER))
        
        self.enc_vars = [tk.IntVar() for _ in range(8)]
        for i in range(7, -1, -1):
            chk = tk.Checkbutton(f, text=f"I{i}", variable=self.enc_vars[i], font=F_MONO,
                                 bg=SURFACE2, fg=WHITE, selectcolor=BLUE_DIM, activebackground=SURFACE3, activeforeground=CYAN)
            chk.pack(side="left", expand=True)

        action_btn(self, "⚙ ENCODE", self.calc_encoder, BLUE_DIM).pack(anchor="w", pady=16)
        
        section_label(self, "OUTPUT BINER (A2 A1 A0)")
        self.res_var = tk.StringVar(value="-")
        tk.Label(self, textvariable=self.res_var, font=F_CALC, bg=PANEL, fg=BLUE_GLOW).pack(anchor="w")

    def calc_encoder(self):
        output = "000"
        for i in range(7, -1, -1):
            if self.enc_vars[i].get() == 1:
                output = format(i, '03b')
                break
        if all(v.get() == 0 for v in self.enc_vars):
            self.res_var.set("IDLE (Semua 0)")
        else:
            self.res_var.set(output)

# ─────────────────────────────────────────────────────────
#  PAGE 9 — DECODER 3-TO-8
# ─────────────────────────────────────────────────────────
class PageDecoder(Page):
    def __init__(self, parent):
        super().__init__(parent)
        info_box(self, "DECODER 3-TO-8", 
                 "Menerjemahkan input 3-bit biner menjadi 8 jalur output (hanya 1 jalur yang bernilai 1).")
                 
        section_label(self, "INPUT 3-BIT")
        hint_label(self, "Masukkan tepat 3 digit biner (misal: 101)")
        
        row = tk.Frame(self, bg=PANEL); row.pack(fill="x", pady=5)
        self.dec_entry = styled_entry(row, width=10); self.dec_entry.pack(side="left", padx=(0, 10))
        action_btn(row, "⚙ DECODE", self.calc_decoder, BLUE_DIM).pack(side="left")
        
        section_label(self, "OUTPUT JALUR (Y0 - Y7)")
        self.res_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.res_var, font=F_MONO, bg=PANEL, fg=CYAN, justify="left").pack(anchor="w", pady=10)

    def calc_decoder(self):
        val = self.dec_entry.get().strip()
        if len(val) != 3 or not all(c in '01' for c in val):
            messagebox.showerror("Error", "Input harus 3 digit biner!")
            return
            
        decimal_val = int(val, 2)
        res_text = ""
        for i in range(8):
            active = "1 (AKTIF)" if i == decimal_val else "0"
            res_text += f"Y{i} = {active}\n"
        self.res_var.set(res_text)

# ─────────────────────────────────────────────────────────
#  PAGE 10 — HEX TO 7-SEGMENT DISPLAY
# ─────────────────────────────────────────────────────────
class PageHexTo7Seg(Page):
    """
    Konversi digit Hexadecimal (0–F) ke tampilan 7-Segment.
    Segmen: a (atas), b (kanan atas), c (kanan bawah),
            d (bawah), e (kiri bawah), f (kiri atas), g (tengah)

    Encoding aktif-HIGH (1 = nyala):
       a  b  c  d  e  f  g
    """
    # Segment map: key → (a,b,c,d,e,f,g)
    SEG_MAP = {
        '0': (1,1,1,1,1,1,0),
        '1': (0,1,1,0,0,0,0),
        '2': (1,1,0,1,1,0,1),
        '3': (1,1,1,1,0,0,1),
        '4': (0,1,1,0,0,1,1),
        '5': (1,0,1,1,0,1,1),
        '6': (1,0,1,1,1,1,1),
        '7': (1,1,1,0,0,0,0),
        '8': (1,1,1,1,1,1,1),
        '9': (1,1,1,1,0,1,1),
        'A': (1,1,1,0,1,1,1),
        'B': (0,0,1,1,1,1,1),
        'C': (1,0,0,1,1,1,0),
        'D': (0,1,1,1,1,0,1),
        'E': (1,0,0,1,1,1,1),
        'F': (1,0,0,0,1,1,1),
    }

    def __init__(self, parent):
        super().__init__(parent)
        info_box(self, "HEX TO 7-SEGMENT DISPLAY",
                 "Konversi digit Hexadecimal (0–F) menjadi output 7-Segment.\n"
                 "• Masukkan 1–4 digit hex untuk melihat tampilan multi-digit\n"
                 "• Segmen: a=atas · b=kanan-atas · c=kanan-bawah · d=bawah · e=kiri-bawah · f=kiri-atas · g=tengah\n"
                 "• Encoding aktif-HIGH: 1=nyala (kuning) · 0=mati (gelap)")
        self._build()

    def _build(self):
        # ── Input row ──────────────────────────────────────
        section_label(self, "INPUT HEX DIGIT(S)")
        hint_label(self, "Masukkan 1–4 digit hex (0–9, A–F), contoh: 2A, F0, 1B3C")

        inp_row = tk.Frame(self, bg=PANEL); inp_row.pack(fill="x", pady=(0, 10))
        self.hex_entry = styled_entry(inp_row, width=12)
        self.hex_entry.pack(side="left", ipady=6, padx=(0, 10))
        self.hex_entry.bind("<Return>", lambda e: self._convert())

        action_btn(inp_row, "▶  KONVERSI", self._convert, BLUE).pack(side="left", padx=(0, 8))
        action_btn(inp_row, "✕  CLEAR",    self._clear,   RED_DIM).pack(side="left")

        # ── HEX pad (quick-input) ──────────────────────────
        section_label(self, "QUICK INPUT PAD")
        pad_outer = tk.Frame(self, bg=SURFACE, highlightthickness=1,
                             highlightbackground=BORDER, padx=10, pady=10)
        pad_outer.pack(anchor="w", pady=(0, 14))

        hex_chars = list("0123456789ABCDEF")
        for idx, ch in enumerate(hex_chars):
            b = tk.Button(pad_outer, text=ch, font=("Consolas", 9, "bold"),
                          bg=SURFACE2, fg=WHITE, relief="flat", cursor="hand2",
                          padx=10, pady=6,
                          command=lambda c=ch: self._append_char(c))
            lighter = _lighten(SURFACE2, 30)
            b.bind("<Enter>", lambda e, b=b: b.config(bg=lighter))
            b.bind("<Leave>", lambda e, b=b: b.config(bg=SURFACE2))
            b.grid(row=idx // 8, column=idx % 8, padx=2, pady=2)

        # ── Canvas area for 7-segment display ─────────────
        section_label(self, "TAMPILAN 7-SEGMENT")
        self.canvas_frame = tk.Frame(self, bg=SURFACE, highlightthickness=1,
                                     highlightbackground=BORDER)
        self.canvas_frame.pack(fill="x", pady=(0, 12))

        self.seg_canvas = tk.Canvas(self.canvas_frame, bg=SURFACE,
                                    highlightthickness=0, height=160)
        self.seg_canvas.pack(fill="x", padx=14, pady=14)

        # ── Segment table ──────────────────────────────────
        section_label(self, "TABEL SEGMENT (a b c d e f g)")
        self.table_frame = tk.Frame(self, bg=PANEL)
        self.table_frame.pack(fill="x", pady=(0, 8))
        self._draw_table_header()

        # initial hint
        self._status_lbl = tk.Label(self, text="← Masukkan digit hex lalu klik KONVERSI",
                                    font=F_SMALL, bg=PANEL, fg=GREY_DIM)
        self._status_lbl.pack(anchor="w")

    # ── helpers ───────────────────────────────────────────
    def _append_char(self, c):
        cur = self.hex_entry.get()
        if len(cur) < 4:
            self.hex_entry.insert(tk.END, c)

    def _clear(self):
        self.hex_entry.delete(0, tk.END)
        self.seg_canvas.delete("all")
        for w in self.table_frame.winfo_children():
            if hasattr(w, '_is_data_row'):
                w.destroy()
        self._draw_table_header()
        self._status_lbl.config(text="← Masukkan digit hex lalu klik KONVERSI", fg=GREY_DIM)

    def _draw_table_header(self):
        # remove old header if any
        for w in self.table_frame.winfo_children():
            w.destroy()
        cols = ["DIGIT", "a", "b", "c", "d", "e", "f", "g", "BINARY (abcdefg)", "HEX CODE"]
        hrow = tk.Frame(self.table_frame, bg=BLUE_DIM)
        hrow.pack(fill="x")
        widths = [7, 4, 4, 4, 4, 4, 4, 4, 20, 12]
        for i, (col, w) in enumerate(zip(cols, widths)):
            fg = BLUE_GLOW if i == 0 else (YELLOW if i <= 7 else WHITE)
            tk.Label(hrow, text=col, font=("Consolas", 8, "bold"),
                     bg=BLUE_DIM, fg=fg, width=w, anchor="center").pack(side="left")

    def _convert(self):
        raw = self.hex_entry.get().strip().upper()
        if not raw:
            messagebox.showerror("Error", "Input tidak boleh kosong!")
            return
        if not all(c in "0123456789ABCDEF" for c in raw):
            messagebox.showerror("Error", "Input hanya boleh karakter hex: 0–9, A–F")
            return
        if len(raw) > 4:
            messagebox.showerror("Error", "Maksimal 4 digit hex!")
            return

        # clear old table data rows
        self._draw_table_header()
        self._status_lbl.config(text="")

        # draw segments on canvas
        self.seg_canvas.delete("all")
        self._draw_digits(raw)

        # draw table rows
        for i, ch in enumerate(raw):
            segs = self.SEG_MAP[ch]
            bg = SURFACE if i % 2 == 0 else SURFACE2
            drow = tk.Frame(self.table_frame, bg=bg)
            drow._is_data_row = True
            drow.pack(fill="x")

            widths = [7, 4, 4, 4, 4, 4, 4, 4, 20, 12]
            # digit
            tk.Label(drow, text=ch, font=("Consolas", 9, "bold"),
                     bg=bg, fg=CYAN, width=widths[0], anchor="center").pack(side="left")
            # segment bits
            for j, bit in enumerate(segs):
                fg = GREEN if bit else GREY_DIM
                tk.Label(drow, text=str(bit), font=("Consolas", 9, "bold"),
                         bg=bg, fg=fg, width=widths[j+1], anchor="center").pack(side="left")
            # binary string
            bin_str = "".join(str(s) for s in segs)
            hex_code = f"0x{int(bin_str, 2):02X}"
            tk.Label(drow, text=bin_str, font=("Consolas", 9),
                     bg=bg, fg=BLUE_GLOW, width=widths[8], anchor="center").pack(side="left")
            tk.Label(drow, text=hex_code, font=("Consolas", 9, "bold"),
                     bg=bg, fg=ORANGE, width=widths[9], anchor="center").pack(side="left")

        self._status_lbl.config(
            text=f"  ✓ {len(raw)} digit dikonversi — segmen aktif ditampilkan kuning",
            fg=GREEN)

    # ── 7-segment canvas drawing ──────────────────────────
    def _draw_digits(self, digits):
        """Draw one or more 7-segment digit displays on the canvas."""
        # Dimensions of one digit cell
        W  = 80    # cell width
        H  = 130   # cell height
        PAD_X = 20 # left margin
        GAP   = 18 # gap between digits

        total_w = PAD_X * 2 + len(digits) * W + (len(digits) - 1) * GAP
        # make canvas wide enough
        self.seg_canvas.config(width=max(total_w, 300), height=H + 30)

        SEG_ON  = "#eab308"   # YELLOW – lit
        SEG_OFF = "#1f1f2e"   # SURFACE2 – dim
        BG_DIGIT = "#0d0d0f"  # BG

        for di, ch in enumerate(digits):
            ox = PAD_X + di * (W + GAP)
            oy = 15
            segs = self.SEG_MAP[ch]  # (a,b,c,d,e,f,g)

            # background rect
            self.seg_canvas.create_rectangle(
                ox, oy, ox + W, oy + H,
                fill="#13131a", outline=BORDER, width=1)

            # digit label below
            self.seg_canvas.create_text(
                ox + W // 2, oy + H + 10,
                text=ch, fill=CYAN,
                font=("Consolas", 9, "bold"))

            T  = 8    # segment thickness
            M  = 6    # margin from cell edge
            MH = 4    # half-thickness for join

            # Segment layout (all coords relative to ox, oy):
            # a – top horizontal
            # b – top-right vertical
            # c – bottom-right vertical
            # d – bottom horizontal
            # e – bottom-left vertical
            # f – top-left vertical
            # g – middle horizontal

            mid_y = oy + H // 2

            def seg(idx, points, color_on):
                color = color_on if segs[idx] else SEG_OFF
                self.seg_canvas.create_polygon(
                    *points, fill=color, outline="")

            def h_seg(x1, y, x2, col):
                """Draw a horizontal segment as a hexagon."""
                pts = [
                    x1 + MH, y,
                    x2 - MH, y,
                    x2,      y + MH,
                    x2 - MH, y + T,
                    x1 + MH, y + T,
                    x1,      y + MH,
                ]
                self.seg_canvas.create_polygon(*pts, fill=col, outline="")

            def v_seg(x, y1, y2, col):
                """Draw a vertical segment as a hexagon."""
                pts = [
                    x,      y1 + MH,
                    x + MH, y1,
                    x + T,  y1 + MH,
                    x + T,  y2 - MH,
                    x + MH, y2,
                    x,      y2 - MH,
                ]
                self.seg_canvas.create_polygon(*pts, fill=col, outline="")

            # a – top
            h_seg(ox + M,     oy + M,
                  ox + W - M, SEG_ON if segs[0] else SEG_OFF)

            # b – top-right
            v_seg(ox + W - M - T, oy + M + T,
                  mid_y - MH,
                  SEG_ON if segs[1] else SEG_OFF)

            # c – bottom-right
            v_seg(ox + W - M - T, mid_y + T + MH,
                  oy + H - M - T,
                  SEG_ON if segs[2] else SEG_OFF)

            # d – bottom
            h_seg(ox + M,     oy + H - M - T,
                  ox + W - M, SEG_ON if segs[3] else SEG_OFF)

            # e – bottom-left
            v_seg(ox + M, mid_y + T + MH,
                  oy + H - M - T,
                  SEG_ON if segs[4] else SEG_OFF)

            # f – top-left
            v_seg(ox + M, oy + M + T,
                  mid_y - MH,
                  SEG_ON if segs[5] else SEG_OFF)

            # g – middle
            h_seg(ox + M,     mid_y,
                  ox + W - M, SEG_ON if segs[6] else SEG_OFF)




# ─────────────────────────────────────────────────────────
#  PAGE 11 — FULL ADDER 4-BIT
# ─────────────────────────────────────────────────────────
class PageFullAdder4bit(Page):
    """
    Simulasi Full Adder 4-bit ripple-carry.
    Menampilkan setiap tahap 1-bit adder secara visual,
    termasuk carry propagation, serta hasil akhir 5-bit.
    """
    def __init__(self, parent):
        super().__init__(parent)
        info_box(self, "FULL ADDER 4-BIT (RIPPLE CARRY)",
                 "Simulasi penjumlahan 2 bilangan biner 4-bit dengan Full Adder Ripple Carry.\n"
                 "• Setiap bit dijumlahkan satu per satu dari LSB (bit-0) ke MSB (bit-3)\n"
                 "• Carry out setiap tahap menjadi Carry in tahap berikutnya\n"
                 "• Hasil akhir bisa 5-bit jika terjadi overflow (Cout dari bit-3 = 1)\n"
                 "• Rumus per bit: Sum = A ⊕ B ⊕ Cin  |  Cout = (A·B) + (B·Cin) + (A·Cin)")
        self._build()

    def _build(self):
        # ── Input Area ────────────────────────────────────
        section_label(self, "INPUT BINER 4-BIT")
        hint_label(self, "Masukkan tepat 4 digit biner (0/1) untuk A dan B  ·  Contoh: A=1011  B=0110")

        inp_row = tk.Frame(self, bg=PANEL); inp_row.pack(fill="x", pady=(0, 8))

        tk.Label(inp_row, text="A (4-bit):", font=F_BODY, bg=PANEL, fg=GREY, width=12, anchor="w").pack(side="left")
        self.entry_a = styled_entry(inp_row, width=10)
        self.entry_a.insert(0, "1011")
        self.entry_a.pack(side="left", ipady=5, padx=(0, 20))

        tk.Label(inp_row, text="B (4-bit):", font=F_BODY, bg=PANEL, fg=GREY, width=12, anchor="w").pack(side="left")
        self.entry_b = styled_entry(inp_row, width=10)
        self.entry_b.insert(0, "0110")
        self.entry_b.pack(side="left", ipady=5, padx=(0, 20))

        tk.Label(inp_row, text="Cin (awal):", font=F_BODY, bg=PANEL, fg=GREY, width=12, anchor="w").pack(side="left")
        self.entry_cin = styled_entry(inp_row, width=5)
        self.entry_cin.insert(0, "0")
        self.entry_cin.pack(side="left", ipady=5, padx=(0, 20))

        action_btn(self, "⚙  HITUNG FULL ADDER 4-BIT", self._calc, BLUE).pack(anchor="w", pady=(10, 14))

        # ── Step-by-step visual table ──────────────────────
        section_label(self, "PROSES PER-BIT (LSB → MSB)")

        tbl_outer = tk.Frame(self, bg=SURFACE, highlightthickness=2, highlightbackground=BORDER_HI)
        tbl_outer.pack(fill="x", pady=(0, 14))

        # Header
        hrow = tk.Frame(tbl_outer, bg=BLUE_DIM); hrow.pack(fill="x")
        cols  = ["BIT", "A", "B", "Cin", "Sum", "Cout", "Ekspresi"]
        widths= [6,      5,   5,   6,     6,     7,      45]
        for col, w in zip(cols, widths):
            tk.Label(hrow, text=col, font=("Consolas",9,"bold"),
                     bg=BLUE_DIM, fg=BLUE_GLOW, width=w, anchor="center").pack(side="left", padx=2, pady=5)

        self.step_frame = tk.Frame(tbl_outer, bg=SURFACE)
        self.step_frame.pack(fill="x")

        # ── Result display ─────────────────────────────────
        section_label(self, "HASIL AKHIR")

        res_outer = tk.Frame(self, bg=BLUE_MID, padx=1, pady=1)
        res_outer.pack(fill="x", pady=(0, 10))
        res_inner = tk.Frame(res_outer, bg=BLUE_DEEP, padx=20, pady=16)
        res_inner.pack(fill="both", expand=True)

        # Row: labels
        lrow = tk.Frame(res_inner, bg=BLUE_DEEP); lrow.pack(anchor="w", pady=(0,6))
        self.res_labels = {}
        for key, text in [("A","A"), ("B","B"), ("Cin","Cin"), ("sum5","A+B+Cin"), ("dec","Desimal"), ("hex","Hex"), ("overflow","Status")]:
            r = tk.Frame(lrow, bg=BLUE_DEEP); r.pack(side="left", padx=14)
            tk.Label(r, text=text, font=("Consolas",8), bg=BLUE_DEEP, fg=GREY).pack()
            var = tk.StringVar(value="—")
            lbl = tk.Label(r, textvariable=var, font=("Consolas",15,"bold"), bg=BLUE_DEEP, fg=BLUE_GLOW)
            lbl.pack()
            self.res_labels[key] = (var, lbl)

        # ── Circuit diagram canvas ────────────────────────
        section_label(self, "DIAGRAM RIPPLE CARRY")
        hint_label(self, "Blok FA = Full Adder 1-bit · Carry mengalir dari kiri (FA0) ke kanan (FA3)")

        self.diag_canvas = tk.Canvas(self, bg=SURFACE, height=160,
                                     highlightthickness=2, highlightbackground=BORDER)
        self.diag_canvas.pack(fill="x", pady=(0, 4))
        self._draw_empty_diagram()

    def _draw_empty_diagram(self):
        self.diag_canvas.delete("all")
        self.diag_canvas.create_text(20, 80, text="← Klik  ⚙ HITUNG  untuk menampilkan diagram ripple carry",
                                     anchor="w", fill=GREY_DIM, font=F_SMALL)

    def _calc(self):
        a_str   = self.entry_a.get().strip()
        b_str   = self.entry_b.get().strip()
        cin_str = self.entry_cin.get().strip()

        # Validate
        if len(a_str) != 4 or not all(c in "01" for c in a_str):
            messagebox.showerror("Error", "Input A harus tepat 4 digit biner (0/1)!"); return
        if len(b_str) != 4 or not all(c in "01" for c in b_str):
            messagebox.showerror("Error", "Input B harus tepat 4 digit biner (0/1)!"); return
        if cin_str not in ("0","1"):
            messagebox.showerror("Error", "Cin awal harus 0 atau 1!"); return

        # Bits: index 0 = LSB, 3 = MSB  (reverse string)
        a_bits   = [int(c) for c in reversed(a_str)]
        b_bits   = [int(c) for c in reversed(b_str)]
        cin_init = int(cin_str)

        steps = []  # list of (bit_idx, a, b, cin, sum_, cout, expr)
        carry = cin_init
        sum_bits = []

        for i in range(4):
            a = a_bits[i]; b = b_bits[i]; cin = carry
            s   = a ^ b ^ cin
            cout = (a & b) | (b & cin) | (a & cin)
            expr = f"S={a}⊕{b}⊕{cin}={s}  Cout=({a}·{b})+(·{cin})=({a&b}|{b&cin}|{a&cin})={cout}"
            steps.append((i, a, b, cin, s, cout, expr))
            sum_bits.append(s)
            carry = cout

        final_cout = carry
        # Rebuild sum string MSB first
        sum5_bits = [final_cout] + list(reversed(sum_bits))  # 5 bits, MSB first
        sum5_str  = "".join(str(b) for b in sum5_bits)
        sum_dec   = int(sum5_str, 2)
        a_dec     = int(a_str, 2)
        b_dec     = int(b_str, 2)
        overflow  = "OVERFLOW! (Cout=1)" if final_cout else "OK (Cout=0)"
        overflow_color = RED if final_cout else GREEN

        # Update step table
        for w in self.step_frame.winfo_children():
            w.destroy()

        for (bit, a, b, cin, s, cout, expr) in steps:
            bg = SURFACE if bit % 2 == 0 else SURFACE2
            row = tk.Frame(self.step_frame, bg=bg); row.pack(fill="x")
            vals = [f"bit-{bit}", str(a), str(b), str(cin), str(s), str(cout), expr]
            widths = [6, 5, 5, 6, 6, 7, 45]
            colors = [GREY, CYAN, ORANGE, YELLOW, GREEN, RED, GREY]
            for val, w, clr in zip(vals, widths, colors):
                tk.Label(row, text=val, font=("Consolas",9),
                         bg=bg, fg=clr, width=w, anchor="center").pack(side="left", padx=2, pady=4)

        # Update result labels
        data = {
            "A":    (a_str,               CYAN),
            "B":    (b_str,               ORANGE),
            "Cin":  (cin_str,             YELLOW),
            "sum5": (sum5_str,            GREEN),
            "dec":  (f"{sum_dec}",        WHITE),
            "hex":  (f"0x{sum_dec:02X}",  BLUE_GLOW),
            "overflow": (overflow,        overflow_color),
        }
        for key, (val, clr) in data.items():
            var, lbl = self.res_labels[key]
            var.set(val); lbl.config(fg=clr)

        # Draw ripple carry diagram
        self._draw_diagram(a_bits, b_bits, steps, final_cout)

    def _draw_diagram(self, a_bits, b_bits, steps, final_cout):
        """Draw 4 FA blocks with carry wires."""
        c = self.diag_canvas
        c.delete("all")

        W, H   = 110, 90
        PAD_X  = 30
        GAP    = 40
        TOP_Y  = 30

        # Color mapping
        fg_text = WHITE     # canvas text — always use theme-aware color
        # But canvas doesn't use tkinter theme so use fixed readable colors
        # based on is_dark flag held in App... canvas is standalone, use hex directly
        # We'll check _current_theme
        is_dark = (_current_theme is DARK_THEME)
        BG_C    = "#161622" if is_dark else "#f0f4ff"
        TEXT_C  = "#eef2ff" if is_dark else "#111827"
        GREY_C  = "#8892b0" if is_dark else "#6b7280"
        WIRE_C  = "#4f8ef7" if is_dark else "#2563eb"
        CARRY_C = "#ff8c42" if is_dark else "#c2410c"
        SUM_C   = "#39e07a" if is_dark else "#15803d"
        A_C     = "#00e5ff" if is_dark else "#0369a1"
        B_C     = "#ff8c42" if is_dark else "#c2410c"
        BOX_BG  = "#1c1c2e" if is_dark else "#ffffff"
        BOX_BD  = "#4f8ef7" if is_dark else "#2563eb"

        c.config(bg=BG_C)

        total_w = PAD_X * 2 + 4 * W + 3 * GAP + 60
        c.config(width=max(total_w, 600))

        for i, (bit, a, b, cin_v, s, cout, _) in enumerate(steps):
            ox = PAD_X + i * (W + GAP)
            oy = TOP_Y

            # FA box
            c.create_rectangle(ox, oy, ox+W, oy+H, fill=BOX_BG, outline=BOX_BD, width=2)
            c.create_text(ox+W//2, oy+18, text=f"FA{bit}", font=("Consolas",10,"bold"), fill=BOX_BD)
            c.create_text(ox+W//2, oy+38, text=f"A={a}  B={b}", font=("Consolas",8), fill=TEXT_C)
            c.create_text(ox+W//2, oy+52, text=f"Cin={cin_v}", font=("Consolas",8), fill=CARRY_C)
            c.create_text(ox+W//2, oy+70, text=f"Sum={s}", font=("Consolas",9,"bold"), fill=SUM_C)

            # A input arrow (top-left)
            c.create_line(ox+20, oy-20, ox+20, oy, fill=A_C, arrow=tk.LAST, width=2)
            c.create_text(ox+20, oy-26, text=f"A{bit}={a}", font=("Consolas",7), fill=A_C)

            # B input arrow (top-right)
            c.create_line(ox+W-20, oy-20, ox+W-20, oy, fill=B_C, arrow=tk.LAST, width=2)
            c.create_text(ox+W-20, oy-26, text=f"B{bit}={b}", font=("Consolas",7), fill=B_C)

            # Sum output (bottom)
            c.create_line(ox+W//2, oy+H, ox+W//2, oy+H+20, fill=SUM_C, arrow=tk.LAST, width=2)
            c.create_text(ox+W//2, oy+H+28, text=f"S{bit}={s}", font=("Consolas",8,"bold"), fill=SUM_C)

            # Carry wire — connect to next FA or show final
            if i < 3:
                nx = ox + W + GAP
                cy_wire = oy + H // 2
                c.create_line(ox+W, cy_wire, nx, cy_wire, fill=CARRY_C, arrow=tk.LAST, width=2)
                c.create_text(ox+W+GAP//2, cy_wire-10, text=f"C{cout}", font=("Consolas",8), fill=CARRY_C)
            else:
                # Final carry out
                end_x = ox + W + 40
                cy_wire = oy + H // 2
                c.create_line(ox+W, cy_wire, end_x, cy_wire, fill=CARRY_C, arrow=tk.LAST, width=2)
                cout_clr = "#ff4d6a" if final_cout else SUM_C
                c.create_text(end_x+4, cy_wire, text=f"Cout={final_cout}", font=("Consolas",8,"bold"),
                              fill=cout_clr, anchor="w")

        # Cin initial arrow (left of FA0)
        c.create_line(PAD_X-30, TOP_Y+H//2, PAD_X, TOP_Y+H//2, fill=CARRY_C, arrow=tk.LAST, width=2)
        c.create_text(PAD_X-32, TOP_Y+H//2-10, text=f"Cin", font=("Consolas",7), fill=CARRY_C, anchor="e")


# ─────────────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────────────
NAV = [
    ("CALC",  "Programmer\nCalculator", "01"),
    ("SOP",   "SOP\nSimplifier",        "02"),
    ("EQ",    "Equation\nGenerator",    "03"),
    ("GATE",  "Gate\nCircuit",          "04"),
    ("TABLE", "Truth\nTable",           "05"),
    ("ALU",   "ALU 1-Bit\nSimulator",   "06"),
    ("ARITH", "Binary\nArithmetic",     "07"),
    ("ENC",   "Priority\nEncoder",      "08"),
    ("DEC",   "3-to-8\nDecoder",        "09"),
    ("7SEG",  "Hex to\n7-Segment",      "10"),
    ("FA4",   "Full Adder\n4-Bit",      "11"),
]

class App:
    def __init__(self, root):
        self.root = root
        root.title("Digital Logic Suite  ·  v2.0  MEGAH")
        root.geometry("1100x740"); root.configure(bg=BG)
        root.minsize(920, 640)
        self._is_dark = True
        self._active_idx = 0
        self.pages = []
        self.nav_items = []
        self.nav_refs = []
        self._apply_ttk_theme()
        self._build_ui()

    def _apply_ttk_theme(self):
        """Apply dark theme to all ttk widgets."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # ── Scrollbar ──────────────────────────────────────
        style.configure("Vertical.TScrollbar",
                        troughcolor=PANEL, background=GREY_DIM,
                        arrowcolor=BLUE_GLOW, bordercolor=BORDER,
                        lightcolor=SURFACE2, darkcolor=BG, relief="flat")
        style.map("Vertical.TScrollbar",
                  background=[("active", BLUE), ("pressed", BLUE_GLOW)])

        # ── Combobox ───────────────────────────────────────
        style.configure("TCombobox",
                        fieldbackground=SURFACE2, background=SURFACE2,
                        foreground=WHITE, arrowcolor=BLUE_GLOW,
                        selectbackground=BLUE_MID, selectforeground=WHITE,
                        bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
                        relief="flat", padding=4)
        style.map("TCombobox",
                  fieldbackground=[("readonly", SURFACE2), ("active", SURFACE3)],
                  foreground=[("readonly", WHITE)],
                  background=[("active", SURFACE3), ("pressed", BLUE_MID)],
                  bordercolor=[("active", BLUE), ("focus", CYAN)])

    def _build_ui(self):
        global BG, PANEL, SURFACE, SURFACE2, SURFACE3, BORDER, BORDER_HI
        global BLUE, BLUE_DIM, BLUE_MID, BLUE_GLOW, BLUE_DEEP
        global CYAN, CYAN_DIM, WHITE, GREY, GREY_DIM
        global RED, RED_DIM, RED_MID, ORANGE, ORANGE_DIM
        global GREEN, GREEN_DIM, YELLOW, YELLOW_DIM
        global PURPLE, PURPLE_DIM, NAV_ACTIVE_BG, NAV_ACTIVE_FG

        self.root.configure(bg=BG)
        self.sb_outer=tk.Frame(self.root, bg=PANEL, width=200)
        self.sb_outer.pack(side="left", fill="y")
        self.sb_outer.pack_propagate(False)

        # ── Right accent border on sidebar ────────────────
        self.sb_border = tk.Frame(self.root, bg=BORDER, width=1)
        self.sb_border.pack(side="left", fill="y")

        # ── Logo & Version — STATIC ───────────────────────
        lf = tk.Frame(self.sb_outer, bg=PANEL)
        lf.pack(fill="x", pady=(18, 0))
        self.logo_ring = tk.Frame(lf, bg=BLUE_MID, padx=2, pady=2)
        self.logo_ring.pack()
        self.logo_inner = tk.Frame(self.logo_ring, bg=PANEL, padx=10, pady=6)
        self.logo_inner.pack()
        self.dl_lbl = tk.Label(self.logo_inner, text="DL", font=("Consolas",30,"bold"), bg=PANEL, fg=BLUE)
        self.dl_lbl.pack()
        self.suite_lbl = tk.Label(lf, text="SUITE", font=("Segoe UI",8,"bold"), bg=PANEL, fg=BLUE_GLOW)
        self.suite_lbl.pack(pady=(4,0))
        self.ver_lbl = tk.Label(lf, text="Digital Logic v2.0", font=("Segoe UI",8), bg=PANEL, fg=GREY_DIM)
        self.ver_lbl.pack(pady=(2,10))

        def _logo_in(e):
            self.logo_ring.config(bg=BLUE)
            self.dl_lbl.config(fg=CYAN)
        def _logo_out(e):
            self.logo_ring.config(bg=BLUE_MID)
            self.dl_lbl.config(fg=BLUE)
        for w in (self.logo_ring, self.logo_inner, self.dl_lbl, lf):
            w.bind("<Enter>", _logo_in)
            w.bind("<Leave>", _logo_out)

        # divider
        self.logo_div = tk.Frame(self.sb_outer, bg=BLUE_MID, height=1)
        self.logo_div.pack(fill="x", padx=10, pady=(0,4))

        # ── Bottom Pinned Area ────────────────────────────
        self.bot_lbl = tk.Label(self.sb_outer, text="Kerkom  ·  Logika Digital",
                                font=("Segoe UI",7), bg=PANEL, fg=GREY_DIM)
        self.bot_lbl.pack(side="bottom", pady=(0,10))
        self.bot_div = tk.Frame(self.sb_outer, bg=BORDER, height=1)
        self.bot_div.pack(fill="x", padx=14, side="bottom", pady=6)

        # ── Nav Menu — NON-SCROLLABLE ─────────────────────
        self.sb = tk.Frame(self.sb_outer, bg=PANEL)
        self.sb.pack(fill="both", expand=True)

        self.nav_items = []
        self.nav_refs  = []   # keep refs for theme update
        for i, (key, label, num) in enumerate(NAV):
            frm = tk.Frame(self.sb, bg=PANEL, padx=0, pady=0)
            frm.pack(fill="x", padx=6, pady=1)

            accent = tk.Frame(frm, bg=PANEL, width=4)
            accent.pack(side="left", fill="y")

            inner = tk.Frame(frm, bg=PANEL)
            inner.pack(side="left", fill="both", expand=True)

            nl = tk.Label(inner, text=num, font=("Consolas",8), bg=PANEL, fg=GREY_DIM, anchor="w")
            nl.pack(anchor="w", padx=8, pady=(5,0))
            btn = tk.Button(inner, text=label, font=("Segoe UI",9,"bold"),
                            bg=PANEL, fg=GREY,
                            activebackground=SURFACE2, activeforeground=WHITE,
                            relief="flat", cursor="hand2", pady=7,
                            justify="left", anchor="w", padx=8,
                            command=lambda idx=i: self.show(idx))
            btn.pack(fill="x")

            def _nav_enter(e, f=frm, a=accent, n=nl, b=btn, inn=inner, idx=i):
                if idx != getattr(self, '_active_idx', 0):
                    f.config(bg=SURFACE2); a.config(bg=BLUE_MID)
                    n.config(bg=SURFACE2); b.config(bg=SURFACE2, fg=WHITE)
                    inn.config(bg=SURFACE2)
            def _nav_leave(e, f=frm, a=accent, n=nl, b=btn, inn=inner, idx=i):
                if idx != getattr(self, '_active_idx', 0):
                    f.config(bg=PANEL); a.config(bg=PANEL)
                    n.config(bg=PANEL); b.config(bg=PANEL, fg=GREY)
                    inn.config(bg=PANEL)
            for w in (frm, inner, btn, nl):
                w.bind("<Enter>", _nav_enter)
                w.bind("<Leave>", _nav_leave)

            self.nav_items.append((frm, nl, btn, accent, inner))
            self.nav_refs.append((frm, nl, btn, accent, inner))

        # ── Right ─────────────────────────────────────────
        self.right = tk.Frame(self.root, bg=BG)
        self.right.pack(side="right", fill="both", expand=True)

        # Topbar
        self.topbar = tk.Frame(self.right, bg=PANEL, height=56)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.topbar_accent = tk.Frame(self.topbar, bg=PANEL)
        self.topbar_accent.pack(fill="x", side="bottom")
        self.topbar_line1 = tk.Frame(self.topbar_accent, bg=BLUE, height=2)
        self.topbar_line1.pack(fill="x")
        self.topbar_line2 = tk.Frame(self.topbar_accent, bg=BLUE_MID, height=1)
        self.topbar_line2.pack(fill="x")

        lrow = tk.Frame(self.topbar, bg=PANEL)
        lrow.pack(side="left", fill="y", padx=20)
        self.tb_num = tk.StringVar(value="")
        self.tb_ttl = tk.StringVar(value="")
        self.tb_num_lbl = tk.Label(lrow, textvariable=self.tb_num,
                                   font=("Consolas",13,"bold"), bg=PANEL, fg=CYAN)
        self.tb_num_lbl.pack(side="left", padx=(0,10))
        self.tb_ttl_lbl = tk.Label(lrow, textvariable=self.tb_ttl,
                                   font=("Segoe UI",13,"bold"), bg=PANEL, fg=WHITE)
        self.tb_ttl_lbl.pack(side="left")

        # Right side of topbar — toggle + badge
        rrow = tk.Frame(self.topbar, bg=PANEL)
        rrow.pack(side="right", fill="y", padx=16)

        # Dark/Light toggle button
        toggle_text = "☀  Light Mode" if self._is_dark else "🌙  Dark Mode"
        self.toggle_btn = tk.Button(rrow, text=toggle_text,
                                    font=("Segoe UI",9,"bold"),
                                    bg=BLUE_DIM, fg=BLUE_GLOW,
                                    activebackground=BLUE_MID, activeforeground=WHITE,
                                    relief="flat", cursor="hand2",
                                    padx=12, pady=4,
                                    highlightthickness=1, highlightbackground=BLUE_MID, bd=0,
                                    command=self._toggle_theme)
        self.toggle_btn.pack(side="right", anchor="center", pady=14, padx=(8,0))
        self.toggle_btn.bind("<Enter>", lambda e: self.toggle_btn.config(bg=BLUE_MID))
        self.toggle_btn.bind("<Leave>", lambda e: self.toggle_btn.config(bg=BLUE_DIM))

        self.badge_frame = tk.Frame(rrow, bg=BLUE_DIM, padx=8, pady=3)
        self.badge_frame.pack(side="right", anchor="center", pady=14)
        self.badge_lbl = tk.Label(self.badge_frame, text="v2.0  MEGAH",
                                  font=("Consolas",8,"bold"), bg=BLUE_DIM, fg=BLUE_GLOW)
        self.badge_lbl.pack()

        # Pages
        self.container = tk.Frame(self.right, bg=BG)
        self.container.pack(fill="both", expand=True)
        self.pages = []
        self.nav_items = []
        self.nav_refs  = []
        p0 = PageCalc(self.container)
        p1 = PageSOP(self.container)
        p2 = PageEquation(self.container)
        p3 = PageGate(self.container)
        p4 = PageTruthTable(self.container, on_export=self._export_to_eq)
        p5 = PageALU(self.container)
        p6 = PageArith(self.container)
        p7 = PageEncoder(self.container)
        p8 = PageDecoder(self.container)
        p9 = PageHexTo7Seg(self.container)
        p10= PageFullAdder4bit(self.container)
        for p in [p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]:
            p.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.pages.append(p)

        self.root.bind("<Key>", p0._kb)
        self.show(self._active_idx)

    def _toggle_theme(self):
        global _current_theme
        global BG, PANEL, SURFACE, SURFACE2, SURFACE3, BORDER, BORDER_HI
        global BLUE, BLUE_DIM, BLUE_MID, BLUE_GLOW, BLUE_DEEP
        global CYAN, CYAN_DIM, WHITE, GREY, GREY_DIM
        global RED, RED_DIM, RED_MID, ORANGE, ORANGE_DIM
        global GREEN, GREEN_DIM, YELLOW, YELLOW_DIM
        global PURPLE, PURPLE_DIM, NAV_ACTIVE_BG, NAV_ACTIVE_FG

        self._is_dark = not self._is_dark
        _current_theme = DARK_THEME if self._is_dark else LIGHT_THEME
        BG=_current_theme["BG"]; PANEL=_current_theme["PANEL"]
        SURFACE=_current_theme["SURFACE"]; SURFACE2=_current_theme["SURFACE2"]
        SURFACE3=_current_theme["SURFACE3"]; BORDER=_current_theme["BORDER"]
        BORDER_HI=_current_theme["BORDER_HI"]; BLUE=_current_theme["BLUE"]
        BLUE_DIM=_current_theme["BLUE_DIM"]; BLUE_MID=_current_theme["BLUE_MID"]
        BLUE_GLOW=_current_theme["BLUE_GLOW"]; BLUE_DEEP=_current_theme["BLUE_DEEP"]
        CYAN=_current_theme["CYAN"]; CYAN_DIM=_current_theme["CYAN_DIM"]
        WHITE=_current_theme["WHITE"]; GREY=_current_theme["GREY"]
        GREY_DIM=_current_theme["GREY_DIM"]; RED=_current_theme["RED"]
        RED_DIM=_current_theme["RED_DIM"]; RED_MID=_current_theme["RED_MID"]
        ORANGE=_current_theme["ORANGE"]; ORANGE_DIM=_current_theme["ORANGE_DIM"]
        GREEN=_current_theme["GREEN"]; GREEN_DIM=_current_theme["GREEN_DIM"]
        YELLOW=_current_theme["YELLOW"]; YELLOW_DIM=_current_theme["YELLOW_DIM"]
        PURPLE=_current_theme["PURPLE"]; PURPLE_DIM=_current_theme["PURPLE_DIM"]
        NAV_ACTIVE_BG=_current_theme["NAV_ACTIVE_BG"]
        NAV_ACTIVE_FG=_current_theme["NAV_ACTIVE_FG"]

        # ── Rebuild everything from scratch ───────────────
        # Destroy all existing pages + sidebar + right panel
        for p in self.pages:
            p.destroy()

        self.sb_outer.destroy()
        self.sb_border.destroy()
        self.right.destroy()

        # Re-apply ttk theme with new colors
        self._apply_ttk_theme()

        # Rebuild all UI with new theme colors
        self._build_ui()

    def _export_to_eq(self,seq):
        p=self.pages[2]; p.entry.delete(0,tk.END); p.entry.insert(0,seq)
        self.show(2)
        messagebox.showinfo("Export Berhasil",
            "Data Truth Table berhasil dikirim ke Equation Generator!\nKlik 'Generate Equation' untuk melihat hasil.")

    def show(self, idx):
        self._active_idx = idx
        key, label, num = NAV[idx]
        self.tb_num.set(f"/{num}")
        self.tb_ttl.set(label.replace("\n", " "))
        for i, (frm, nl, btn, accent, inner) in enumerate(self.nav_items):
            if i == idx:
                frm.config(bg=NAV_ACTIVE_BG)
                inner.config(bg=NAV_ACTIVE_BG)
                btn.config(bg=NAV_ACTIVE_BG, fg=WHITE)
                nl.config(bg=NAV_ACTIVE_BG, fg=CYAN)
                accent.config(bg=CYAN)
            else:
                frm.config(bg=PANEL)
                inner.config(bg=PANEL)
                btn.config(bg=PANEL, fg=GREY)
                nl.config(bg=PANEL, fg=GREY_DIM)
                accent.config(bg=PANEL)
        self.pages[idx].lift()


if __name__ == "__main__":
    root=tk.Tk()
    try: root.iconbitmap(default="")
    except: pass
    App(root)
    root.mainloop()