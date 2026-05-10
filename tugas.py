import tkinter as tk
from tkinter import messagebox

class BaseConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Base Converter")
        self.root.geometry("600x500")
        self.root.configure(bg="#ffffff")
        
        title = tk.Label(root, text="Smart Base Converter", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#111111")
        title.pack(pady=20)
        
        frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
        frame.pack(pady=10, fill="x", padx=40)
        
        tk.Label(frame, text="Angka Input:", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").pack(anchor="w")
        tk.Label(frame, text="Gunakan prefix: 0b (biner), 0o (oktal), 0x (hex), langsung angka (desimal)", font=("Segoe UI", 9), bg="#ffffff", fg="#777777").pack(anchor="w", pady=(0,5))
        
        self.entry_val = tk.Entry(frame, font=("Segoe UI", 14), bg="#f5f5f5", fg="#111111", insertbackground="black", relief="flat", highlightthickness=1, highlightcolor="#cccccc", highlightbackground="#eeeeee")
        self.entry_val.pack(fill="x", pady=5, ipady=4)
        
        tk.Label(frame, text="Konversi ke Basis (2-36):", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").pack(anchor="w", pady=(15,0))
        self.entry_base = tk.Entry(frame, font=("Segoe UI", 14), bg="#f5f5f5", fg="#111111", insertbackground="black", relief="flat", highlightthickness=1, highlightcolor="#cccccc", highlightbackground="#eeeeee")
        self.entry_base.pack(fill="x", pady=5, ipady=4)
        
        btn = tk.Button(frame, text="Konversi", font=("Segoe UI", 12, "bold"), bg="#111111", fg="#ffffff", 
                        activebackground="#333333", activeforeground="#ffffff", relief="flat", cursor="hand2", command=self.convert)
        btn.pack(pady=20, fill="x")
        
        self.result_lbl = tk.Label(root, text="", font=("Segoe UI", 14), justify="left", bg="#ffffff", fg="#111111")
        self.result_lbl.pack(pady=10)

    def convert(self):
        raw_input = self.entry_val.get().strip().lower()
        if not raw_input:
            messagebox.showerror("Error", "Input tidak boleh kosong!")
            return
            
        if raw_input.startswith("0b"):
            basis_asal, angka_bersih = 2, raw_input[2:]
        elif raw_input.startswith("0o"):
            basis_asal, angka_bersih = 8, raw_input[2:]
        elif raw_input.startswith("0x"):
            basis_asal, angka_bersih = 16, raw_input[2:]
        else:
            basis_asal, angka_bersih = 10, raw_input
            
        if not angka_bersih:
            messagebox.showerror("Error", "Tidak ada angka setelah prefix.")
            return

        try:
            basis_tujuan = int(self.entry_base.get().strip())
            if basis_tujuan < 2 or basis_tujuan > 36:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Basis tujuan harus angka antara 2-36.")
            return

        try:
            nilai_desimal = int(angka_bersih, basis_asal)
            
            digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            hasil_akhir = ""
            temp_desimal = nilai_desimal
            
            if temp_desimal == 0:
                hasil_akhir = "0"
            else:
                while temp_desimal > 0:
                    hasil_akhir = digits[temp_desimal % basis_tujuan] + hasil_akhir
                    temp_desimal //= basis_tujuan
            
            res_text = (f"Basis Asal: {basis_asal}\n"
                        f"Desimal   : {nilai_desimal}\n"
                        f"Hasil Basis {basis_tujuan} : {hasil_akhir}")
            self.result_lbl.config(text=res_text)
            
        except ValueError:
            messagebox.showerror("Error", f"Angka '{angka_bersih}' tidak valid untuk basis {basis_asal}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BaseConverterApp(root)
    root.mainloop()