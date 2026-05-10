import tkinter as tk
from tkinter import ttk, messagebox

class SimDigProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SimDig Pro - Simulator Logika Digital")
        self.root.geometry("600x480")
        self.root.configure(bg="#ecf0f1")
        
        # --- Styling UI ---
        style = ttk.Style()
        style.theme_use('clam')
        
        # Konfigurasi warna dan font
        style.configure("TNotebook", background="#ecf0f1")
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[10, 5], background="#bdc3c7")
        style.map("TNotebook.Tab", background=[("selected", "#3498db")], foreground=[("selected", "white")])
        
        style.configure("TLabelframe", background="#ffffff", borderwidth=1)
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"), background="#ffffff", foreground="#2c3e50")
        
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10), foreground="#34495e")
        style.configure("Res.TLabel", font=("Consolas", 12, "bold"), foreground="#e74c3c")
        
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#2ecc71", foreground="white", padding=5)
        style.map("TButton", background=[("active", "#27ae60")])
        
        # --- Notebook (Tabs) ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=15, padx=15, expand=True, fill='both')
        
        # Buat Frame untuk tiap Tab
        self.tab_alu = ttk.Frame(self.notebook)
        self.tab_calc = ttk.Frame(self.notebook)
        self.tab_encoder = ttk.Frame(self.notebook)
        self.tab_decoder = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_alu, text=" ALU 1-Bit ")
        self.notebook.add(self.tab_calc, text=" Aritmatika Biner ")
        self.notebook.add(self.tab_encoder, text=" Encoder 8-to-3 ")
        self.notebook.add(self.tab_decoder, text=" Decoder 3-to-8 ")
        
        # --- Inisialisasi Konten Tab ---
        self.setup_alu_tab()
        self.setup_calc_tab()
        self.setup_encoder_tab()
        self.setup_decoder_tab()

    # ================= TAB 1: ALU 1-BIT =================
    def setup_alu_tab(self):
        frame = ttk.LabelFrame(self.tab_alu, text=" Full Adder & Subtractor ", padding=20)
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Input A (0/1):").grid(row=0, column=0, pady=5, sticky="e")
        self.alu_a = ttk.Entry(frame, width=10)
        self.alu_a.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Input B (0/1):").grid(row=1, column=0, pady=5, sticky="e")
        self.alu_b = ttk.Entry(frame, width=10)
        self.alu_b.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Carry/Borrow In:").grid(row=2, column=0, pady=5, sticky="e")
        self.alu_cin = ttk.Entry(frame, width=10)
        self.alu_cin.grid(row=2, column=1, pady=5, padx=10)

        btn_frame = ttk.Frame(self.tab_alu)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Hitung Adder", command=lambda: self.calc_alu("adder")).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Hitung Subtractor", command=lambda: self.calc_alu("sub")).grid(row=0, column=1, padx=5)

        self.lbl_alu_res = ttk.Label(self.tab_alu, text="Hasil...", style="Res.TLabel", justify="center")
        self.lbl_alu_res.pack(pady=20)

    def calc_alu(self, mode):
        try:
            a, b, c = int(self.alu_a.get()), int(self.alu_b.get()), int(self.alu_cin.get())
            if not all(x in (0,1) for x in (a,b,c)): raise ValueError
            
            if mode == "adder":
                s = a ^ b ^ c
                cout = (a & b) | (b & c) | (a & c)
                self.lbl_alu_res.config(text=f"∑ Sum (S) = {s}\nCarry Out (Cout) = {cout}")
            else:
                diff = a ^ b ^ c
                bout = (int(not a) & c) | (int(not a) & b) | (b & c)
                self.lbl_alu_res.config(text=f"Δ Difference (D) = {diff}\nBorrow Out (Bout) = {bout}")
        except:
            messagebox.showerror("Error", "Input ALU harus berupa angka 0 atau 1!")

    # ================= TAB 2: ARITMATIKA BINER =================
    def setup_calc_tab(self):
        frame = ttk.LabelFrame(self.tab_calc, text=" Kalkulator N-Bit ", padding=20)
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Biner 1:").grid(row=0, column=0, pady=5, sticky="e")
        self.calc_bin1 = ttk.Entry(frame, width=15)
        self.calc_bin1.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Operasi:").grid(row=1, column=0, pady=5, sticky="e")
        self.calc_op = ttk.Combobox(frame, values=["+", "-", "*"], width=12, state="readonly")
        self.calc_op.current(0)
        self.calc_op.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Biner 2:").grid(row=2, column=0, pady=5, sticky="e")
        self.calc_bin2 = ttk.Entry(frame, width=15)
        self.calc_bin2.grid(row=2, column=1, pady=5, padx=10)

        ttk.Button(frame, text="Hitung", command=self.calc_binary).grid(row=3, column=0, columnspan=2, pady=15)

        self.lbl_calc_res = ttk.Label(self.tab_calc, text="Hasil...", style="Res.TLabel")
        self.lbl_calc_res.pack(pady=10)

    def calc_binary(self):
        try:
            val1 = int(self.calc_bin1.get(), 2)
            val2 = int(self.calc_bin2.get(), 2)
            op = self.calc_op.get()
            
            if op == "+": res = val1 + val2
            elif op == "-": res = val1 - val2
            elif op == "*": res = val1 * val2
            
            if res < 0:
                bin_res = "-" + bin(res)[3:]
            else:
                bin_res = bin(res)[2:]
                
            self.lbl_calc_res.config(text=f"Hasil: {bin_res}\n(Desimal: {res})")
        except:
            messagebox.showerror("Error", "Input harus berupa bilangan biner yang valid!")

    # ================= TAB 3: PRIORITY ENCODER 8-TO-3 =================
    def setup_encoder_tab(self):
        frame = ttk.LabelFrame(self.tab_encoder, text=" Input Jalur (Pilih yang aktif) ", padding=10)
        frame.pack(padx=20, pady=10, fill="x")

        self.enc_vars = [tk.IntVar() for _ in range(8)]
        # Bikin checkbox dari I7 sampai I0
        for i in range(7, -1, -1):
            chk = ttk.Checkbutton(frame, text=f"I{i}", variable=self.enc_vars[i])
            chk.grid(row=0, column=7-i, padx=5, pady=10)

        ttk.Button(self.tab_encoder, text="Encode", command=self.calc_encoder).pack(pady=10)
        self.lbl_enc_res = ttk.Label(self.tab_encoder, text="Output (A2 A1 A0): -", style="Res.TLabel")
        self.lbl_enc_res.pack(pady=10)

    def calc_encoder(self):
        # Mengecek dari I7 ke I0 (Priority Encoder: urutan tertinggi menang)
        output = "000"
        for i in range(7, -1, -1):
            if self.enc_vars[i].get() == 1:
                output = format(i, '03b') # Format ke 3 digit biner
                break
        
        if all(v.get() == 0 for v in self.enc_vars):
            self.lbl_enc_res.config(text="Status: IDLE (Semua 0)")
        else:
            self.lbl_enc_res.config(text=f"Output (A2 A1 A0) : {output}")

    # ================= TAB 4: DECODER 3-TO-8 =================
    def setup_decoder_tab(self):
        frame = ttk.LabelFrame(self.tab_decoder, text=" Input 3-Bit ", padding=20)
        frame.pack(padx=20, pady=10, fill="x")

        ttk.Label(frame, text="Input (misal: 101) :").grid(row=0, column=0, pady=5, sticky="e")
        self.dec_entry = ttk.Entry(frame, width=10)
        self.dec_entry.grid(row=0, column=1, pady=5, padx=10)

        ttk.Button(frame, text="Decode", command=self.calc_decoder).grid(row=0, column=2, padx=10)

        self.lbl_dec_res = ttk.Label(self.tab_decoder, text="", font=("Consolas", 11, "bold"), foreground="#2980b9")
        self.lbl_dec_res.pack(pady=15)

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
            
        self.lbl_dec_res.config(text=res_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimDigProApp(root)
    root.mainloop()