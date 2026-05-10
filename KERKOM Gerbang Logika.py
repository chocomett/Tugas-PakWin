import tkinter as tk
from tkinter import messagebox
import schemdraw
import schemdraw.logic as logic
from PIL import Image, ImageTk
import os

def parse_expression(expr):
    expr = expr.replace(" ", "")
    terms = expr.split("+")
    parsed = []
    for term in terms:
        factors = []
        i = 0
        while i < len(term):
            if i+1 < len(term) and term[i+1] == "'":
                factors.append((term[i], True))
                i += 2
            else:
                factors.append((term[i], False))
                i += 1
        parsed.append(factors)
    return parsed

def draw_circuit(expr):
    import schemdraw.elements as elm
    schemdraw.theme('default')
    parsed = parse_expression(expr)
    d = schemdraw.Drawing(canvas='matplotlib')
    
    or_gate = None
    and_outputs = []
    y_offset = 0
    for term in parsed:
        if len(term) == 1:
            var, neg = term[0]
            if neg:
                line = d.add(logic.Line().at((0, y_offset)).to((2.5, y_offset)).label(var, loc='left'))
                not_gate = d.add(logic.Not().at((2.5, y_offset)).right())
                and_outputs.append(not_gate.out)
            else:
                line = d.add(logic.Line().at((0, y_offset)).to((4, y_offset)).label(var, loc='left'))
                and_outputs.append(line.end)
        else:
            and_gate = d.add(logic.And(inputs=len(term)).at((2, y_offset)))
            for i, (var, neg) in enumerate(term):
                inp = getattr(and_gate, f'in{i+1}')
                if neg:
                    not_gate = d.add(logic.Not().at((0.5, inp[1])).to(inp))
                    d.add(logic.Line().at((0, inp[1])).to((0.5, inp[1])).label(var, loc='left'))
                else:
                    d.add(logic.Line().at((0, inp[1])).to(inp).label(var, loc='left'))
            and_outputs.append(and_gate.out)
        y_offset -= 3 # Give a bit more vertical space between gates

    if len(and_outputs) > 1:
        center_y = -(len(parsed) - 1) * 1.5
        or_gate = d.add(logic.Or(inputs=len(and_outputs)).at((7, center_y)))
        for i, out_point in enumerate(and_outputs):
            d.add(logic.Wire('|-').at(out_point).to(getattr(or_gate, f'in{i+1}')))
        d.add(logic.Line().at(or_gate.out).right().label("Output"))
    elif len(and_outputs) == 1:
        d.add(logic.Line().at(and_outputs[0]).right().label("Output"))
        
    d.save("circuit.png")

class LogicGateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logic Gate Generator")
        self.root.geometry("800x650")
        self.root.configure(bg="#ffffff")
        
        title = tk.Label(root, text="Logic Gate Generator", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#111111")
        title.pack(pady=15)
        
        frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
        frame.pack(pady=5, fill="x", padx=40)
        
        tk.Label(frame, text="Masukkan Ekspresi SOP:", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").pack(anchor="w")
        tk.Label(frame, text="Contoh: B+AC atau A'BC+AB'", font=("Segoe UI", 9), bg="#ffffff", fg="#777777").pack(anchor="w", pady=(0,5))
        
        self.entry = tk.Entry(frame, font=("Segoe UI", 14), bg="#f5f5f5", fg="#111111", insertbackground="black", relief="flat", highlightthickness=1, highlightcolor="#cccccc", highlightbackground="#eeeeee")
        self.entry.pack(fill="x", pady=5, ipady=4)
        
        btn = tk.Button(frame, text="Generate Circuit", font=("Segoe UI", 12, "bold"), bg="#111111", fg="#ffffff", 
                        activebackground="#333333", activeforeground="#ffffff", relief="flat", cursor="hand2", command=self.generate)
        btn.pack(pady=15, fill="x")
        
        self.lbl_image = tk.Label(root, bg="#ffffff")
        self.lbl_image.pack(pady=10)

    def generate(self):
        expr = self.entry.get().strip()
        if not expr:
            messagebox.showerror("Error", "Masukkan ekspresi logika!")
            return

        try:
            draw_circuit(expr)
            if os.path.exists("circuit.png"):
                img = Image.open("circuit.png")
                
                img.thumbnail((700, 400))
                self.img_tk = ImageTk.PhotoImage(img)
                self.lbl_image.config(image=self.img_tk)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat generate gambar!\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LogicGateApp(root)
    root.mainloop()