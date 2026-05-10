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
#  THEME / DESIGN TOKENS
# ─────────────────────────────────────────────────────────
BG         = "#0d0d0f"
PANEL      = "#13131a"
SURFACE    = "#1a1a24"
SURFACE2   = "#1f1f2e"
BORDER     = "#2a2a3d"
BLUE       = "#3b82f6"
BLUE_DIM   = "#1a2a4a"
BLUE_GLOW  = "#60a5fa"
CYAN       = "#22d3ee"
WHITE      = "#f1f5f9"
GREY       = "#94a3b8"
GREY_DIM   = "#475569"
RED        = "#ef4444"
RED_DIM    = "#7f1d1d"
ORANGE     = "#f97316"
GREEN      = "#22c55e"
YELLOW     = "#eab308"

F_HEAD   = ("Segoe UI", 11, "bold")
F_BODY   = ("Segoe UI", 10)
F_SMALL  = ("Segoe UI", 8)
F_MONO   = ("Consolas", 11)
F_MONO_S = ("Consolas", 9)
F_CALC   = ("Consolas", 24, "bold")
F_CALC_S = ("Consolas", 13)
F_BTN    = ("Segoe UI", 9,  "bold")
F_NAV    = ("Segoe UI", 8,  "bold")

# ─────────────────────────────────────────────────────────
#  WIDGET HELPERS
# ─────────────────────────────────────────────────────────
def styled_entry(parent, font=None, **kw):
    return tk.Entry(parent, font=font or F_MONO,
                    bg=SURFACE, fg=WHITE, insertbackground=BLUE_GLOW,
                    relief="flat", highlightthickness=1,
                    highlightbackground=BORDER, highlightcolor=BLUE, **kw)

def styled_text(parent, height=8):
    t = tk.Text(parent, font=F_MONO, bg=SURFACE, fg=WHITE,
                relief="flat", highlightthickness=1,
                highlightbackground=BORDER, highlightcolor=BLUE,
                insertbackground=BLUE_GLOW, height=height,
                padx=12, pady=10, wrap="word",
                selectbackground=BLUE_DIM, selectforeground=WHITE)
    t.tag_config("heading", foreground=BLUE_GLOW, font=("Consolas",10,"bold"))
    t.tag_config("result",  foreground=GREEN,     font=("Consolas",12,"bold"))
    t.tag_config("muted",   foreground=GREY)
    t.tag_config("var",     foreground=CYAN)
    t.tag_config("warn",    foreground=YELLOW)
    t.tag_config("err",     foreground=RED)
    return t

def section_label(parent, text):
    f = tk.Frame(parent, bg=PANEL)
    f.pack(fill="x", pady=(14, 4))
    tk.Frame(f, bg=BLUE, width=3).pack(side="left", fill="y", padx=(0,8))
    tk.Label(f, text=text, font=F_HEAD, bg=PANEL, fg=WHITE).pack(side="left")

def hint_label(parent, text):
    tk.Label(parent, text=text, font=F_SMALL, bg=PANEL,
             fg=GREY_DIM, justify="left").pack(anchor="w", pady=(0,6))

def action_btn(parent, text, cmd, color=BLUE):
    b = tk.Button(parent, text=text, font=F_BTN,
                  bg=color, fg=WHITE,
                  activebackground=BLUE_GLOW if color==BLUE else color,
                  activeforeground=BG if color==BLUE else WHITE,
                  relief="flat", cursor="hand2", command=cmd, pady=8)
    lighter = _lighten(color)
    b.bind("<Enter>", lambda e: b.config(bg=lighter))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def _lighten(hex_color, amount=40):
    try:
        r=int(hex_color[1:3],16); g=int(hex_color[3:5],16); b=int(hex_color[5:7],16)
        r=min(255,r+amount); g=min(255,g+amount); b=min(255,b+amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    except: return hex_color

def info_box(parent, title, body):
    box = tk.Frame(parent, bg=BLUE_DIM, padx=12, pady=10)
    box.pack(fill="x", pady=(0,12))
    tk.Label(box, text="ℹ  "+title, font=("Segoe UI",8,"bold"),
             bg=BLUE_DIM, fg=BLUE_GLOW).pack(anchor="w")
    tk.Label(box, text=body, font=F_SMALL, bg=BLUE_DIM, fg=GREY,
             justify="left", wraplength=700).pack(anchor="w", pady=(3,0))

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
                          bg=SURFACE, fg=GREY, relief="flat", cursor="hand2", padx=10, pady=4,
                          command=lambda b=bits: self._set_ws(b))
            b.pack(side="left", padx=2)
            self.ws_btns[bits] = b
        self._set_ws(64, init=True)

        # ── Multi-base display ─────────────────────────────
        disp = tk.Frame(self, bg=SURFACE2, highlightthickness=1, highlightbackground=BORDER)
        disp.pack(fill="x", pady=(0,6))
        self.disp_vars = {}
        self.disp_lbls = {}
        specs = [
            ("HEX","hex", CYAN,    F_CALC_S),
            ("DEC","dec", WHITE,   F_CALC),
            ("OCT","oct", GREY,    F_CALC_S),
            ("BIN","bin", BLUE_GLOW, ("Consolas",9)),
        ]
        for lbl, key, clr, fnt in specs:
            row = tk.Frame(disp, bg=SURFACE2); row.pack(fill="x", padx=14, pady=2)
            tk.Label(row, text=lbl, font=("Consolas",8,"bold"),
                     bg=SURFACE2, fg=BLUE, width=4, anchor="w").pack(side="left")
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
                          bg=SURFACE, fg=GREY, relief="flat", cursor="hand2", padx=14, pady=5,
                          command=lambda m=m: self._set_mode(m))
            b.pack(side="left", padx=2)
            self.mode_btns[m] = b
        self._set_mode("DEC", init=True)

        # ── Keypad ─────────────────────────────────────────
        pad = tk.Frame(self, bg=PANEL); pad.pack(fill="x")

        # [text, col, row, colspan, bg_color]
        keys = [
            # row 0 – bitwise & special
            ("AND",0,0,1,BLUE_DIM),("OR", 1,0,1,BLUE_DIM),("XOR",2,0,1,BLUE_DIM),("NOT",3,0,1,BLUE_DIM),
            ("<<", 4,0,1,BLUE_DIM),(">>",5,0,1,BLUE_DIM),("MOD",6,0,1,BLUE_DIM),("CLR",7,0,1,RED_DIM),
            # row 1 – hex digits + parens
            ("A",  0,1,1,SURFACE2),("B", 1,1,1,SURFACE2),("C", 2,1,1,SURFACE2),("D", 3,1,1,SURFACE2),
            ("E",  4,1,1,SURFACE2),("F", 5,1,1,SURFACE2),("(",6,1,1,SURFACE), (")",7,1,1,SURFACE),
            # row 2
            ("7",  0,2,1,SURFACE), ("8", 1,2,1,SURFACE), ("9", 2,2,1,SURFACE), ("÷",3,2,1,ORANGE),
            ("MS", 4,2,1,GREY_DIM),("MR",5,2,1,GREY_DIM),("M+",6,2,1,GREY_DIM),("⌫",7,2,1,RED_DIM),
            # row 3
            ("4",  0,3,1,SURFACE), ("5", 1,3,1,SURFACE), ("6", 2,3,1,SURFACE), ("×",3,3,1,ORANGE),
            ("±",  4,3,1,SURFACE2),("1/x",5,3,1,SURFACE2),("x²",6,3,1,SURFACE2),("√",7,3,1,SURFACE2),
            # row 4
            ("1",  0,4,1,SURFACE), ("2", 1,4,1,SURFACE), ("3", 2,4,1,SURFACE), ("−",3,4,1,ORANGE),
            # row 5
            ("0",  0,5,2,SURFACE), (".",2,5,1,SURFACE),   ("+",3,5,1,ORANGE),
            ("=",  4,5,4,BLUE),
        ]
        self.key_btns = {}
        self.key_colors = {}
        for (lbl,c,r,cs,color) in keys:
            b = tk.Button(pad, text=lbl, font=("Segoe UI",9,"bold"),
                          bg=color, fg=WHITE, relief="flat", cursor="hand2",
                          command=lambda l=lbl: self._key(l))
            b.grid(row=r, column=c, columnspan=cs,
                   sticky="nsew", padx=2, pady=2, ipady=9)
            lighter = _lighten(color, 30)
            b.bind("<Enter>", lambda e,b=b,lc=lighter: b.config(bg=lc) if b.cget("state")=="normal" else None)
            b.bind("<Leave>", lambda e,b=b,oc=color:   b.config(bg=oc) if b.cget("state")=="normal" else None)
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
            btn.config(bg=BLUE if b2==bits else SURFACE,
                       fg=WHITE if b2==bits else GREY)
        if not init: self._refresh()

    def _set_mode(self, m, init=False):
        self.mode = m
        for m2, btn in self.mode_btns.items():
            btn.config(bg=BLUE if m2==m else SURFACE,
                       fg=WHITE if m2==m else GREY)
        
        if hasattr(self, 'disp_lbls'):
            key_map = {"HEX": "hex", "DEC": "dec", "OCT": "oct", "BIN": "bin"}
            active_key = key_map[m]
            default_colors = {"hex": CYAN, "dec": WHITE, "oct": GREY, "bin": BLUE_GLOW}
            for k, lbl in self.disp_lbls.items():
                if k == active_key:
                    lbl.config(font=F_CALC, fg=WHITE)
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
                        btn.config(state="disabled", bg=PANEL, fg=BORDER)
                        
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
        img_outer=tk.Frame(self,bg=SURFACE,highlightthickness=1,highlightbackground=BORDER)
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
            schemdraw.theme('dark')
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
        outer=tk.Frame(self,bg=SURFACE,highlightthickness=1,highlightbackground=BORDER)
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
        
        f = tk.Frame(self, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER, padx=14, pady=14)
        f.pack(fill="x", pady=10)
        
        self.enc_vars = [tk.IntVar() for _ in range(8)]
        for i in range(7, -1, -1):
            chk = tk.Checkbutton(f, text=f"I{i}", variable=self.enc_vars[i], font=F_MONO,
                                 bg=SURFACE, fg=WHITE, selectcolor=SURFACE2, activebackground=SURFACE, activeforeground=CYAN)
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
]

class App:
    def __init__(self, root):
        self.root=root
        root.title("Digital Logic Suite  ·  v2.0")
        root.geometry("1020x720"); root.configure(bg=BG)
        root.minsize(880,620)
        self._build()

    def _build(self):
        # ── Sidebar Container ─────────────────────────────
        sb_outer=tk.Frame(self.root,bg=PANEL,width=168)
        sb_outer.pack(side="left",fill="y"); sb_outer.pack_propagate(False)
        
        # Bottom Pinned Text
        tk.Label(sb_outer,text="Kerkom  ·  Logika Digital",font=("Segoe UI",6),bg=PANEL,fg=GREY_DIM).pack(side="bottom",pady=(0,10))
        tk.Frame(sb_outer,bg=BORDER,height=1).pack(fill="x",padx=14,side="bottom",pady=6)
        
        # Scrollable Canvas
        sb_canvas = tk.Canvas(sb_outer, bg=PANEL, highlightthickness=0)
        sb_vsb = ttk.Scrollbar(sb_outer, orient="vertical", command=sb_canvas.yview)
        sb_canvas.configure(yscrollcommand=sb_vsb.set)
        
        sb_vsb.pack(side="right", fill="y")
        sb_canvas.pack(side="left", fill="both", expand=True)
        
        sb = tk.Frame(sb_canvas, bg=PANEL)
        sb.bind("<Configure>", lambda e: sb_canvas.configure(scrollregion=sb_canvas.bbox("all")))
        sb_canvas.create_window((0,0), window=sb, anchor="nw", width=150)
        
        def _scroll_sb(e):
            sb_canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        sb_outer.bind("<Enter>", lambda e: sb_canvas.bind_all("<MouseWheel>", _scroll_sb))
        sb_outer.bind("<Leave>", lambda e: sb_canvas.unbind_all("<MouseWheel>"))

        # Logo
        lf=tk.Frame(sb,bg=PANEL); lf.pack(fill="x",pady=(22,8))
        tk.Label(lf,text="DL",font=("Consolas",30,"bold"),bg=PANEL,fg=BLUE).pack()
        tk.Label(lf,text="SUITE",font=("Segoe UI",7,"bold"),bg=PANEL,fg=GREY).pack()
        tk.Label(lf,text="Digital Logic v2.0",font=("Segoe UI",7),bg=PANEL,fg=GREY_DIM).pack(pady=(0,12))
        tk.Frame(sb,bg=BORDER,height=1).pack(fill="x",padx=14,pady=(0,8))

        self.nav_items=[]
        for i,(key,label,num) in enumerate(NAV):
            frm=tk.Frame(sb,bg=PANEL); frm.pack(fill="x",padx=8,pady=1)
            nl=tk.Label(frm,text=num,font=("Consolas",7),bg=PANEL,fg=GREY_DIM,anchor="w")
            nl.pack(anchor="w",padx=10,pady=(5,0))
            btn=tk.Button(frm,text=label,font=("Segoe UI",8,"bold"),
                          bg=PANEL,fg=GREY,activebackground=SURFACE2,activeforeground=WHITE,
                          relief="flat",cursor="hand2",pady=7,justify="left",anchor="w",padx=12,
                          command=lambda idx=i: self.show(idx))
            btn.pack(fill="x")
            self.nav_items.append((frm,nl,btn))

        # ── Right ─────────────────────────────────────────
        right=tk.Frame(self.root,bg=BG); right.pack(side="right",fill="both",expand=True)

        # Topbar
        topbar=tk.Frame(right,bg=PANEL,height=50); topbar.pack(fill="x"); topbar.pack_propagate(False)
        tk.Frame(topbar,bg=BLUE,height=2).pack(fill="x",side="bottom")
        lrow=tk.Frame(topbar,bg=PANEL); lrow.pack(side="left",fill="y",padx=20)
        self.tb_num=tk.StringVar(value=""); self.tb_ttl=tk.StringVar(value="")
        tk.Label(lrow,textvariable=self.tb_num,font=("Consolas",11,"bold"),bg=PANEL,fg=BLUE).pack(side="left",padx=(0,10))
        tk.Label(lrow,textvariable=self.tb_ttl,font=("Segoe UI",11,"bold"),bg=PANEL,fg=WHITE).pack(side="left")

        # Pages
        self.container=tk.Frame(right,bg=PANEL); self.container.pack(fill="both",expand=True)
        self.pages=[]
        p0=PageCalc(self.container)
        p1=PageSOP(self.container)
        p2=PageEquation(self.container)
        p3=PageGate(self.container)
        p4=PageTruthTable(self.container,on_export=self._export_to_eq)
        p5=PageALU(self.container)
        p6=PageArith(self.container)
        p7=PageEncoder(self.container)
        p8=PageDecoder(self.container)
        for p in [p0,p1,p2,p3,p4,p5,p6,p7,p8]:
            p.place(relx=0,rely=0,relwidth=1,relheight=1)
            self.pages.append(p)

        # bind keyboard to calc
        self.root.bind("<Key>", p0._kb)
        self.show(0)

    def _export_to_eq(self,seq):
        p=self.pages[2]; p.entry.delete(0,tk.END); p.entry.insert(0,seq)
        self.show(2)
        messagebox.showinfo("Export Berhasil",
            "Data Truth Table berhasil dikirim ke Equation Generator!\nKlik 'Generate Equation' untuk melihat hasil.")

    def show(self,idx):
        key,label,num=NAV[idx]
        self.tb_num.set(f"/{num}"); self.tb_ttl.set(label.replace("\n"," "))
        for i,(frm,nl,btn) in enumerate(self.nav_items):
            if i==idx:
                frm.config(bg=BLUE_DIM); btn.config(bg=BLUE_DIM,fg=WHITE); nl.config(bg=BLUE_DIM,fg=BLUE_GLOW)
            else:
                frm.config(bg=PANEL); btn.config(bg=PANEL,fg=GREY); nl.config(bg=PANEL,fg=GREY_DIM)
        self.pages[idx].lift()


if __name__ == "__main__":
    root=tk.Tk()
    try: root.iconbitmap(default="")
    except: pass
    App(root)
    root.mainloop()