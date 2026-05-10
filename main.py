import tkinter as tk
from tkinter import font
import subprocess
import sys
import os

class MainDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Logic & Tools Dashboard")
        self.root.geometry("700x550")
        self.root.configure(bg="#ffffff")
        
        # Header
        header_frame = tk.Frame(root, bg="#ffffff", pady=20)
        header_frame.pack(fill="x")
        
        title = tk.Label(header_frame, text="Digital Logic Dashboard", font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#111111")
        title.pack()
        
        subtitle = tk.Label(header_frame, text="Pilih program untuk dijalankan", font=("Segoe UI", 12), bg="#ffffff", fg="#777777")
        subtitle.pack(pady=(5,0))
        
        # Tools Container
        container = tk.Frame(root, bg="#f5f5f5", pady=30)
        container.pack(fill="both", expand=True)

        # Helper method for styling buttons
        def create_tool_button(parent, text, description, command, color):
            frame = tk.Frame(parent, bg="#ffffff", pady=10, padx=20, highlightthickness=1, highlightbackground="#dddddd", highlightcolor="#dddddd")
            frame.pack(fill="x", padx=50, pady=10)
            
            btn = tk.Button(frame, text=text, width=15, font=("Segoe UI", 14, "bold"), bg="#111111", fg="#ffffff", 
                            relief="flat", activebackground="#333333", activeforeground="#ffffff", cursor="hand2", command=command)
            btn.pack(side="left", fill="y", ipadx=10)
            
            desc = tk.Label(frame, text=description, font=("Segoe UI", 10), bg="#ffffff", fg="#333333", justify="left")
            desc.pack(side="left", padx=20)

        create_tool_button(container, "Base Converter", "Konversi bilangan (Biner, Oktal, Hex, dll)",
                           lambda: self.launch("tugas.py"), "#89b4fa")
                           
        create_tool_button(container, "SOP Simplifier", "Sederhanakan SOP (Quine-McCluskey)",
                           lambda: self.launch("penyerdehanaan.py"), "#f9e2af")
                           
        create_tool_button(container, "Equation Gen", "Buat persamaan dari Truth Table Output",
                           lambda: self.launch("test.py"), "#a6e3a1")
                           
        create_tool_button(container, "Gate Generator", "Gambar rangkaian gerbang logika dari ekspresi",
                           lambda: self.launch("KERKOM Gerbang Logika.py"), "#eba0ac")

    def launch(self, script_name):
        path = os.path.join(os.path.dirname(__file__), script_name)
        if os.path.exists(path):
            subprocess.Popen([sys.executable, path])
        else:
            tk.messagebox.showerror("Error", f"File {script_name} tidak ditemukan!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainDashboard(root)
    root.mainloop()
