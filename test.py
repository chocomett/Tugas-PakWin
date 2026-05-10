import tkinter as tk
from tkinter import messagebox
import math

class EquationGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Boolean Equation Generator")
        self.root.geometry("600x400")
        self.root.configure(bg="#ffffff")
        
        title = tk.Label(root, text="Boolean Equation Generator", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#111111")
        title.pack(pady=20)
        
        frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
        frame.pack(pady=10, fill="x", padx=40)
        
        tk.Label(frame, text="Masukkan Truth Table Output (0/1):", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").pack(anchor="w")
        tk.Label(frame, text="Contoh: 0 1 1 0 1 0 0 1 (dipisah spasi)", font=("Segoe UI", 10), bg="#ffffff", fg="#777777").pack(anchor="w", pady=(0,5))
        
        self.entry = tk.Entry(frame, font=("Segoe UI", 14), bg="#f5f5f5", fg="#111111", insertbackground="black", relief="flat", highlightthickness=1, highlightcolor="#cccccc", highlightbackground="#eeeeee")
        self.entry.pack(fill="x", pady=5, ipady=5)
        
        btn = tk.Button(frame, text="Generate Equation", font=("Segoe UI", 12, "bold"), bg="#111111", fg="#ffffff", 
                        activebackground="#333333", activeforeground="#ffffff", relief="flat", cursor="hand2", command=self.generate)
        btn.pack(pady=15, fill="x")
        
        self.result_lbl = tk.Label(root, text="", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#111111", wraplength=550)
        self.result_lbl.pack(pady=20)

    def generate(self):
        raw_input = self.entry.get().strip()
        if not raw_input:
            messagebox.showerror("Error", "Input tidak boleh kosong!")
            return
            
        try:
            if ' ' in raw_input:
                data = [int(x) for x in raw_input.split()]
            else:
                data = [int(x) for x in list(raw_input)]
        except ValueError:
            messagebox.showerror("Error", "Harap masukkan angka 0 atau 1 saja!")
            return
            
        if not all(x in [0, 1] for x in data):
            messagebox.showerror("Error", "Input hanya boleh 0 atau 1.")
            return

        total_rows = len(data)
        num_vars = math.log2(total_rows)
        
        if not num_vars.is_integer() or total_rows < 2:
            messagebox.showerror(
                "Error", 
                f"Jumlah data saat ini: {total_rows}\n"
                f"Data harus sesuai pangkat 2 (contoh: 2, 4, 8, 16...).\n"
                f"Silakan tambah atau kurangi angka input Anda.\n"
                f"Contoh Valid (4 buah): 1 0 1 0 atau 1010\n"
                f"Contoh Valid (8 buah): 10101010"
            )
            return

        num_vars = int(num_vars)
        var_names = [chr(65 + i) for i in range(num_vars)]
        
        minterms = []
        for i, val in enumerate(data):
            if val == 1:
                bin_str = format(i, f'0{num_vars}b')
                term_parts = []
                for j, bit in enumerate(bin_str):
                    current_var = var_names[j]
                    if bit == '0':
                        term_parts.append(f"{current_var}'")
                    else:
                        term_parts.append(current_var)
                full_term = "".join(term_parts)
                minterms.append(full_term)

        if not minterms:
            self.result_lbl.config(text="Result: F = 0")
        else:
            equation = " + ".join(minterms)
            self.result_lbl.config(text=f"Variables: {', '.join(var_names)}\n\nResult: F = {equation}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EquationGeneratorApp(root)
    root.mainloop()