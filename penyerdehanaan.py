import tkinter as tk
from tkinter import messagebox

def int_to_binary(n, bits):
    return format(n, f'0{bits}b')

def differ_by_one_bit(term1, term2):
    diff_count = 0
    for b1, b2 in zip(term1, term2):
        if b1 != b2: diff_count += 1
    return diff_count == 1

def combine_terms(term1, term2):
    return ''.join('-' if b1 != b2 else b1 for b1, b2 in zip(term1, term2))

def get_prime_implicants(minterms, num_vars):
    groups = {}
    for minterm in minterms:
        bin_str = int_to_binary(minterm, num_vars)
        ones_count = bin_str.count('1')
        if ones_count not in groups: groups[ones_count] = set()
        groups[ones_count].add(bin_str)
    
    prime_implicants = set()
    while groups:
        new_groups = {}
        combined_this_round = set()
        sorted_keys = sorted(groups.keys())
        for i in range(len(sorted_keys) - 1):
            key1, key2 = sorted_keys[i], sorted_keys[i+1]
            if key2 - key1 != 1: continue
            for term1 in groups[key1]:
                for term2 in groups[key2]:
                    if differ_by_one_bit(term1, term2):
                        combined_term = combine_terms(term1, term2)
                        ones_count = combined_term.count('1')
                        if ones_count not in new_groups: new_groups[ones_count] = set()
                        new_groups[ones_count].add(combined_term)
                        combined_this_round.update([term1, term2])
        for key in groups:
            for term in groups[key]:
                if term not in combined_this_round:
                    prime_implicants.add(term)
        groups = new_groups 
    return prime_implicants

def get_essential_prime_implicants(prime_implicants, minterms, num_vars):
    chart = {pi: [] for pi in prime_implicants}
    for pi in prime_implicants:
        for minterm in minterms:
            bin_m = int_to_binary(minterm, num_vars)
            match = True
            for i in range(num_vars):
                if pi[i] != '-' and pi[i] != bin_m[i]:
                    match = False
                    break
            if match:
                chart[pi].append(minterm)
                
    minterm_counts = {m: 0 for m in minterms}
    for pi, covered_minterms in chart.items():
        for m in covered_minterms:
            minterm_counts[m] += 1
            
    essential_prime_implicants = set()
    covered_minterms_global = set()
    for m, count in minterm_counts.items():
        if count == 1:
            for pi, covered_m in chart.items():
                if m in covered_m:
                    essential_prime_implicants.add(pi)
                    covered_minterms_global.update(covered_m)
    return essential_prime_implicants, covered_minterms_global

def format_output(implicants):
    variables = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    for term in implicants:
        term_str = ""
        for i, char in enumerate(term):
            if char == '1': term_str += variables[i]
            elif char == '0': term_str += variables[i] + "'"
        if term_str == "":
            term_str = "1"
        result.append(term_str)
    return " + ".join(result) if result else "0"

class SimplificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SOP Simplifier (Quine-McCluskey)")
        self.root.geometry("600x600")
        self.root.configure(bg="#ffffff")
        
        title = tk.Label(root, text="SOP Simplifier Tool", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#111111")
        title.pack(pady=15)
        
        frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
        frame.pack(pady=5, fill="x", padx=40)
        
        tk.Label(frame, text="Jumlah Variabel:", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").pack(anchor="w")
        self.entry_vars = tk.Entry(frame, font=("Segoe UI", 14), bg="#f5f5f5", fg="#111111", insertbackground="black", relief="flat", highlightthickness=1, highlightcolor="#cccccc", highlightbackground="#eeeeee")
        self.entry_vars.pack(fill="x", pady=5, ipady=4)
        
        tk.Label(frame, text="Minterms (pisahkan dengan koma):", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").pack(anchor="w", pady=(10,0))
        tk.Label(frame, text="Contoh: 0, 1, 2, 5, 6, 7", font=("Segoe UI", 9), bg="#ffffff", fg="#777777").pack(anchor="w")
        self.entry_minterms = tk.Entry(frame, font=("Segoe UI", 14), bg="#f5f5f5", fg="#111111", insertbackground="black", relief="flat", highlightthickness=1, highlightcolor="#cccccc", highlightbackground="#eeeeee")
        self.entry_minterms.pack(fill="x", pady=5, ipady=4)
        
        btn = tk.Button(frame, text="Sederhanakan", font=("Segoe UI", 12, "bold"), bg="#111111", fg="#ffffff", 
                        activebackground="#333333", activeforeground="#ffffff", relief="flat", cursor="hand2", command=self.solve)
        btn.pack(pady=15, fill="x")
        
        self.txt_result = tk.Text(root, font=("Consolas", 12), bg="#f9f9f9", fg="#111111", height=10, relief="flat", padx=10, pady=10, highlightthickness=1, highlightcolor="#eeeeee", highlightbackground="#eeeeee")
        self.txt_result.pack(pady=10, padx=40, fill="both", expand=True)

    def solve(self):
        try:
            num_vars = int(self.entry_vars.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Jumlah variabel harus angka!")
            return
            
        raw_minterms = self.entry_minterms.get().strip()
        try:
            minterm_list = [int(x.strip()) for x in raw_minterms.split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("Error", "Minterms harus angka yang dipisahkan koma!")
            return
            
        if not minterm_list:
            messagebox.showerror("Error", "Minterms tidak boleh kosong!")
            return

        pis = get_prime_implicants(minterm_list, num_vars)
        epis, covered = get_essential_prime_implicants(pis, minterm_list, num_vars)
        
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, f"--- HASIL PENYEDERHANAAN ---\n\n")
        self.txt_result.insert(tk.END, f"Minterm: {minterm_list}\n\n")
        
        self.txt_result.insert(tk.END, f"Prime Implicants (Biner):\n{list(pis)}\n\n")
        self.txt_result.insert(tk.END, f"Prime Implicants (Variabel):\n{format_output(pis)}\n\n")
        
        self.txt_result.insert(tk.END, f"Essential Prime Implicants (Biner):\n{list(epis)}\n\n")
        self.txt_result.insert(tk.END, f"BENTUK SEDERHANA AKHIR (EPI):\n>> F = {format_output(epis)} <<\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplificationApp(root)
    root.mainloop()