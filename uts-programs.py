import tkinter as tk
from tkinter import messagebox
import math
import os

# ─────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────
BG       = "#0f0f0f"
PANEL    = "#1a1a1a"
CARD     = "#222222"
BORDER   = "#2e2e2e"
ACCENT   = "#e8e8e8"
MUTED    = "#666666"
WHITE    = "#f0f0f0"
INPUT_BG = "#2a2a2a"
BTN_BG   = "#e8e8e8"
BTN_FG   = "#0f0f0f"

FONT_TITLE  = ("Courier New", 22, "bold")
FONT_HEAD   = ("Courier New", 13, "bold")
FONT_BODY   = ("Courier New", 11)
FONT_SMALL  = ("Courier New", 9)
FONT_MONO   = ("Courier New", 11)
FONT_BTN    = ("Courier New", 11, "bold")
FONT_NAV    = ("Courier New", 10, "bold")

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def make_entry(parent, **kw):
    e = tk.Entry(parent, font=FONT_MONO, bg=INPUT_BG, fg=WHITE,
                 insertbackground=WHITE, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT, **kw)
    return e

def make_button(parent, text, command):
    b = tk.Button(parent, text=text, font=FONT_BTN,
                  bg=BTN_BG, fg=BTN_FG,
                  activebackground=WHITE, activeforeground=BG,
                  relief="flat", cursor="hand2", command=command,
                  pady=8)
    return b

def make_label(parent, text, font=None, fg=None, **kw):
    return tk.Label(parent, text=text,
                    font=font or FONT_BODY,
                    bg=PANEL, fg=fg or WHITE,
                    **kw)

def make_text(parent, height=10):
    t = tk.Text(parent, font=FONT_MONO, bg=INPUT_BG, fg=WHITE,
                relief="flat", highlightthickness=1,
                highlightbackground=BORDER, highlightcolor=ACCENT,
                insertbackground=WHITE, height=height,
                padx=10, pady=10)
    return t

# ─────────────────────────────────────────────
#  PAGE BASE
# ─────────────────────────────────────────────
class Page(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL)

    def section(self, title):
        tk.Label(self, text=title, font=FONT_HEAD, bg=PANEL,
                 fg=ACCENT).pack(anchor="w", pady=(18, 4))

    def hint(self, text):
        tk.Label(self, text=text, font=FONT_SMALL, bg=PANEL,
                 fg=MUTED).pack(anchor="w", pady=(0, 6))

# ─────────────────────────────────────────────
#  1. BASE CONVERTER
# ─────────────────────────────────────────────
class PageBaseConverter(Page):
    def __init__(self, parent):
        super().__init__(parent)
        self.section("INPUT ANGKA")
        self.hint("Prefix: 0b biner · 0o oktal · 0x hex · tanpa prefix = desimal")
        self.entry_val = make_entry(self)
        self.entry_val.pack(fill="x", ipady=5, pady=(0, 10))

        self.section("TARGET BASIS (2–36)")
        self.entry_base = make_entry(self)
        self.entry_base.pack(fill="x", ipady=5, pady=(0, 14))

        make_button(self, "KONVERSI", self.convert).pack(fill="x", pady=(0, 16))

        self.result_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.result_var, font=FONT_MONO,
                 bg=CARD, fg=ACCENT, justify="left",
                 relief="flat", padx=14, pady=12,
                 wraplength=500).pack(fill="x")

    def convert(self):
        raw = self.entry_val.get().strip().lower()
        if not raw:
            messagebox.showerror("Error", "Input tidak boleh kosong!"); return

        if raw.startswith("0b"):   basis_asal, bersih = 2, raw[2:]
        elif raw.startswith("0o"): basis_asal, bersih = 8, raw[2:]
        elif raw.startswith("0x"): basis_asal, bersih = 16, raw[2:]
        else:                      basis_asal, bersih = 10, raw

        if not bersih:
            messagebox.showerror("Error", "Tidak ada angka setelah prefix."); return

        try:
            basis_tujuan = int(self.entry_base.get().strip())
            if not 2 <= basis_tujuan <= 36: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Basis tujuan harus angka antara 2–36."); return

        try:
            desimal = int(bersih, basis_asal)
            digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            hasil = ""
            tmp = desimal
            if tmp == 0: hasil = "0"
            else:
                while tmp:
                    hasil = digits[tmp % basis_tujuan] + hasil
                    tmp //= basis_tujuan
            self.result_var.set(
                f"  Basis asal  : {basis_asal}\n"
                f"  Desimal     : {desimal}\n"
                f"  Basis {basis_tujuan:<3}    : {hasil}"
            )
        except ValueError:
            messagebox.showerror("Error", f"Angka '{bersih}' tidak valid untuk basis {basis_asal}.")

# ─────────────────────────────────────────────
#  2. SOP SIMPLIFIER (Quine-McCluskey)
# ─────────────────────────────────────────────
def _int_to_binary(n, bits): return format(n, f'0{bits}b')
def _differ_by_one(t1, t2):  return sum(a!=b for a,b in zip(t1,t2)) == 1
def _combine(t1, t2):        return ''.join('-' if a!=b else a for a,b in zip(t1,t2))

def get_prime_implicants(minterms, num_vars):
    groups = {}
    for m in minterms:
        b = _int_to_binary(m, num_vars)
        c = b.count('1')
        groups.setdefault(c, set()).add(b)
    prime_implicants = set()
    while groups:
        new_groups, combined = {}, set()
        keys = sorted(groups)
        for i in range(len(keys)-1):
            k1, k2 = keys[i], keys[i+1]
            if k2-k1 != 1: continue
            for t1 in groups[k1]:
                for t2 in groups[k2]:
                    if _differ_by_one(t1, t2):
                        ct = _combine(t1, t2)
                        new_groups.setdefault(ct.count('1'), set()).add(ct)
                        combined.update([t1, t2])
        for k in groups:
            for t in groups[k]:
                if t not in combined: prime_implicants.add(t)
        groups = new_groups
    return prime_implicants

def get_essential_pis(pis, minterms, num_vars):
    chart = {pi: [] for pi in pis}
    for pi in pis:
        for m in minterms:
            bm = _int_to_binary(m, num_vars)
            if all(pi[i]=='-' or pi[i]==bm[i] for i in range(num_vars)):
                chart[pi].append(m)
    cnt = {m: 0 for m in minterms}
    for covered in chart.values():
        for m in covered: cnt[m] += 1
    epis, covered_global = set(), set()
    for m, c in cnt.items():
        if c == 1:
            for pi, cm in chart.items():
                if m in cm:
                    epis.add(pi)
                    covered_global.update(cm)
    return epis, covered_global

def format_sop(implicants):
    V = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    for term in implicants:
        s = "".join((V[i] if c=='1' else V[i]+"'" if c=='0' else "")
                    for i,c in enumerate(term))
        result.append(s or "1")
    return " + ".join(result) if result else "0"

class PageSOP(Page):
    def __init__(self, parent):
        super().__init__(parent)
        self.section("JUMLAH VARIABEL")
        self.entry_vars = make_entry(self)
        self.entry_vars.pack(fill="x", ipady=5, pady=(0, 10))

        self.section("MINTERMS")
        self.hint("Pisahkan dengan koma  ·  Contoh: 0, 1, 2, 5, 6, 7")
        self.entry_mt = make_entry(self)
        self.entry_mt.pack(fill="x", ipady=5, pady=(0, 14))

        make_button(self, "SEDERHANAKAN", self.solve).pack(fill="x", pady=(0, 14))
        self.txt = make_text(self, height=12)
        self.txt.pack(fill="both", expand=True)

    def solve(self):
        try: num_vars = int(self.entry_vars.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Jumlah variabel harus angka!"); return
        try:
            mts = [int(x.strip()) for x in self.entry_mt.get().split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("Error", "Minterms harus angka yang dipisahkan koma!"); return
        if not mts:
            messagebox.showerror("Error", "Minterms tidak boleh kosong!"); return

        pis  = get_prime_implicants(mts, num_vars)
        epis, _ = get_essential_pis(pis, mts, num_vars)

        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, f"Minterms        : {mts}\n\n")
        self.txt.insert(tk.END, f"Prime Implicants (biner):\n  {sorted(pis)}\n\n")
        self.txt.insert(tk.END, f"Prime Implicants :\n  {format_sop(pis)}\n\n")
        self.txt.insert(tk.END, f"Essential PI     :\n  {format_sop(epis)}\n\n")
        self.txt.insert(tk.END, f"─" * 40 + f"\n  F = {format_sop(epis)}\n")

# ─────────────────────────────────────────────
#  3. BOOLEAN EQUATION GENERATOR
# ─────────────────────────────────────────────
class PageEquation(Page):
    def __init__(self, parent):
        super().__init__(parent)
        self.section("TRUTH TABLE OUTPUT")
        self.hint("Nilai output dipisah spasi  ·  Contoh: 0 1 1 0 1 0 0 1")
        self.entry = make_entry(self)
        self.entry.pack(fill="x", ipady=5, pady=(0, 14))

        make_button(self, "GENERATE EQUATION", self.generate).pack(fill="x", pady=(0, 16))
        self.txt = make_text(self, height=10)
        self.txt.pack(fill="both", expand=True)

    def generate(self):
        raw = self.entry.get().strip()
        if not raw:
            messagebox.showerror("Error", "Input tidak boleh kosong!"); return
        try:
            data = [int(x) for x in (raw.split() if ' ' in raw else list(raw))]
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka 0 atau 1 saja!"); return
        if not all(x in [0,1] for x in data):
            messagebox.showerror("Error", "Input hanya boleh 0 atau 1."); return

        total = len(data)
        nv = math.log2(total)
        if not nv.is_integer() or total < 2:
            messagebox.showerror("Error", f"Jumlah data ({total}) harus pangkat 2 (2,4,8,16...)."); return

        nv = int(nv)
        vars_ = [chr(65+i) for i in range(nv)]
        minterms = []
        for i, val in enumerate(data):
            if val == 1:
                b = format(i, f'0{nv}b')
                minterms.append("".join(v if bit=='1' else v+"'" for v,bit in zip(vars_,b)))

        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, f"Variabel  : {', '.join(vars_)}\n")
        self.txt.insert(tk.END, f"Banyak var: {nv}\n\n")
        if not minterms:
            self.txt.insert(tk.END, "F = 0")
        else:
            self.txt.insert(tk.END, "F = " + " + ".join(minterms))

# ─────────────────────────────────────────────
#  4. LOGIC GATE CIRCUIT GENERATOR
# ─────────────────────────────────────────────
def parse_sop_expr(expr):
    expr = expr.replace(" ", "")
    terms = []
    for term in expr.split("+"):
        factors, i = [], 0
        while i < len(term):
            if i+1 < len(term) and term[i+1] == "'":
                factors.append((term[i], True)); i += 2
            else:
                factors.append((term[i], False)); i += 1
        terms.append(factors)
    return terms

class PageGateGenerator(Page):
    def __init__(self, parent):
        super().__init__(parent)
        self.section("EKSPRESI SOP")
        self.hint("Contoh: B+AC  atau  A'BC+AB'")
        self.entry = make_entry(self)
        self.entry.pack(fill="x", ipady=5, pady=(0, 14))

        make_button(self, "GENERATE CIRCUIT", self.generate).pack(fill="x", pady=(0, 14))
        self.txt = make_text(self, height=16)
        self.txt.pack(fill="both", expand=True)

    def generate(self):
        expr = self.entry.get().strip()
        if not expr:
            messagebox.showerror("Error", "Masukkan ekspresi logika!"); return

        # Try schemdraw if available, else fall back to ASCII diagram
        try:
            import schemdraw
            import schemdraw.logic as logic
            import schemdraw.elements as elm
            from PIL import Image, ImageTk
            self._schemdraw_draw(expr)
        except ImportError:
            self._ascii_draw(expr)

    def _schemdraw_draw(self, expr):
        import schemdraw
        import schemdraw.logic as logic
        schemdraw.theme('default')
        parsed = parse_sop_expr(expr)
        d = schemdraw.Drawing(canvas='matplotlib')
        and_outputs, y = [], 0
        for term in parsed:
            if len(term) == 1:
                var, neg = term[0]
                if neg:
                    d.add(logic.Line().at((0,y)).to((2.5,y)).label(var,loc='left'))
                    ng = d.add(logic.Not().at((2.5,y)).right())
                    and_outputs.append(ng.out)
                else:
                    ln = d.add(logic.Line().at((0,y)).to((4,y)).label(var,loc='left'))
                    and_outputs.append(ln.end)
            else:
                ag = d.add(logic.And(inputs=len(term)).at((2,y)))
                for i,(var,neg) in enumerate(term):
                    inp = getattr(ag, f'in{i+1}')
                    if neg:
                        ng = d.add(logic.Not().at((0.5,inp[1])).to(inp))
                        d.add(logic.Line().at((0,inp[1])).to((0.5,inp[1])).label(var,loc='left'))
                    else:
                        d.add(logic.Line().at((0,inp[1])).to(inp).label(var,loc='left'))
                and_outputs.append(ag.out)
            y -= 3
        if len(and_outputs) > 1:
            cy = -(len(parsed)-1)*1.5
            og = d.add(logic.Or(inputs=len(and_outputs)).at((7,cy)))
            for i, op in enumerate(and_outputs):
                d.add(logic.Wire('|-').at(op).to(getattr(og, f'in{i+1}')))
            d.add(logic.Line().at(og.out).right().label("Output"))
        else:
            d.add(logic.Line().at(and_outputs[0]).right().label("Output"))
        d.save("circuit.png")
        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, "Circuit berhasil di-generate!\nFile disimpan sebagai circuit.png\n\n")
        self.txt.insert(tk.END, f"Ekspresi  : {self.entry.get().strip()}\n")
        parsed_view = parse_sop_expr(self.entry.get().strip())
        self.txt.insert(tk.END, f"Terms     : {len(parsed_view)} term(s)\n")

    def _ascii_draw(self, expr):
        parsed = parse_sop_expr(expr)
        lines = []
        lines.append(f"  Ekspresi : {expr}")
        lines.append("  " + "─"*40)
        and_wires = []
        for idx, term in enumerate(parsed):
            inputs = [f"{v}'" if neg else v for v,neg in term]
            if len(inputs) == 1:
                gate_str = f"  {inputs[0]} ──────────────────── wire ──┐"
            else:
                gate_str = f"  [{' · '.join(inputs)}] ──[ AND ]──────────┐"
            lines.append(gate_str)
            and_wires.append(idx)

        if len(parsed) > 1:
            for _ in and_wires: lines.append("  " + " "*36 + "│")
            lines.append("  " + " "*36 + "├── [ OR ] ── OUTPUT")
        else:
            lines.append("  " + " "*36 + "└──────────────── OUTPUT")

        lines.append("")
        lines.append("  (Install schemdraw + Pillow untuk gambar rangkaian visual)")

        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, "\n".join(lines))

# ─────────────────────────────────────────────
#  5. TRUTH TABLE BUILDER
# ─────────────────────────────────────────────
class PageTruthTable(Page):
    def __init__(self, parent):
        super().__init__(parent)
        self.section("JUMLAH VARIABEL")
        self.hint("Masukkan jumlah variabel (1–5)")
        self.entry_v = make_entry(self)
        self.entry_v.insert(0, "3")
        self.entry_v.pack(fill="x", ipady=5, pady=(0, 10))

        make_button(self, "BUAT TRUTH TABLE", self.build).pack(fill="x", pady=(0, 14))
        self.txt = make_text(self, height=18)
        self.txt.pack(fill="both", expand=True)

    def build(self):
        try:
            nv = int(self.entry_v.get().strip())
            if not 1 <= nv <= 5: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Jumlah variabel antara 1–5."); return

        vars_ = [chr(65+i) for i in range(nv)]
        rows  = 2**nv
        header = "  ".join(f"{v:>2}" for v in vars_) + "   │  Output"
        sep    = "─" * (len(header)+4)

        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, f"  {header}\n  {sep}\n")
        for i in range(rows):
            bits = format(i, f'0{nv}b')
            row  = "  ".join(f"{int(b):>2}" for b in bits)
            self.txt.insert(tk.END, f"  {row}   │   ?\n")
        self.txt.insert(tk.END, f"\n  Total baris: {rows}\n")

# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
PAGES = [
    ("BASE\nCONVERTER",   "01", PageBaseConverter),
    ("SOP\nSIMPLIFIER",   "02", PageSOP),
    ("EQUATION\nGEN",     "03", PageEquation),
    ("GATE\nGENERATOR",   "04", PageGateGenerator),
    ("TRUTH\nTABLE",      "05", PageTruthTable),
]

class App:
    def __init__(self, root):
        self.root = root
        root.title("Digital Logic Suite")
        root.geometry("860x620")
        root.configure(bg=BG)
        root.resizable(False, False)

        # ── Sidebar ──────────────────────────────
        sidebar = tk.Frame(root, bg=BG, width=148)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="DL\nSUITE", font=("Courier New", 15, "bold"),
                 bg=BG, fg=WHITE, pady=0).pack(pady=(24, 4))
        tk.Label(sidebar, text="v1.0", font=FONT_SMALL,
                 bg=BG, fg=MUTED).pack(pady=(0, 18))
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=10, pady=4)

        self.nav_btns = []
        for name, num, _ in PAGES:
            btn = tk.Button(
                sidebar, text=f"{num}\n{name}",
                font=FONT_NAV, bg=BG, fg=MUTED,
                activebackground=PANEL, activeforeground=WHITE,
                relief="flat", cursor="hand2", pady=12,
                wraplength=120, justify="center"
            )
            btn.pack(fill="x", padx=6, pady=2)
            self.nav_btns.append(btn)

        # ── Content area ─────────────────────────
        right = tk.Frame(root, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        # Top bar
        topbar = tk.Frame(right, bg=PANEL, height=48)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        self.page_title_var = tk.StringVar(value="")
        tk.Label(topbar, textvariable=self.page_title_var,
                 font=("Courier New", 12, "bold"),
                 bg=PANEL, fg=ACCENT, anchor="w",
                 padx=20).pack(fill="both", expand=True)

        # Page container
        self.container = tk.Frame(right, bg=PANEL, padx=28, pady=20)
        self.container.pack(fill="both", expand=True)

        # Instantiate pages
        self.pages = []
        for _, _, PageClass in PAGES:
            p = PageClass(self.container)
            p.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.pages.append(p)

        # Wire buttons
        for i, btn in enumerate(self.nav_btns):
            btn.config(command=lambda idx=i: self.show(idx))

        self.show(0)

    def show(self, idx):
        name, num, _ = PAGES[idx]
        self.page_title_var.set(f"  /{num}  {name.replace(chr(10), ' ')}")
        for i, btn in enumerate(self.nav_btns):
            if i == idx:
                btn.config(bg=CARD, fg=WHITE,
                           highlightthickness=1, highlightbackground=BORDER,
                           highlightcolor=BORDER)
            else:
                btn.config(bg=BG, fg=MUTED,
                           highlightthickness=0)
        self.pages[idx].lift()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()