import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

from simulator.simulate import simulate

class XRayGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Minimal X-ray Simulator")

        # --- Controls ---
        ctrl = ttk.Frame(self, padding=8)
        ctrl.pack(side="left", fill="y")

        self.current = tk.DoubleVar(value=200)
        self.voltage = tk.DoubleVar(value=70)
        self.exp_ms = tk.DoubleVar(value=10)
        self.expn = tk.DoubleVar(value=1.7)

        ttk.Label(ctrl, text="Tube current (mA)").pack()
        tk.Scale(ctrl, from_=10, to=500, orient=tk.HORIZONTAL, variable=self.current, 
                  command=self._on_change, length=200).pack()
        ttk.Label(ctrl, text="Tube voltage (kVp)").pack(pady=(10, 0))
        tk.Scale(ctrl, from_=40, to=120, orient=tk.HORIZONTAL, variable=self.voltage, 
                  command=self._on_change, length=200).pack()
        
        ttk.Label(ctrl, text="Exposure (ms)").pack(pady=(10, 0))
        tk.Scale(ctrl, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.exp_ms, 
                  command=self._on_change, length=200).pack()
        
        ttk.Label(ctrl, text="Dose exponent n").pack(pady=(10,0))
        tk.Scale(ctrl, from_=1.0, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
                  variable=self.expn, command=self._on_change, 
                  length=200).pack()
        
        ttk.Button(ctrl, text="Generate", command=self._draw).pack(pady=8)

        # --- Canvas for image ---
        self.canvas = tk.Label(self)
        self.canvas.pack(side="right", expand=True, fill="both", padx=8, pady=8)

        self._draw()
    
    def _draw(self) -> None:
        img_arr = simulate(
            self.current.get(), 
            self.voltage.get(),
            exp_ms=self.exp_ms.get(),
            exponent_n=self.expn.get(),
        )
        pil = Image.fromarray(img_arr)
        # keep reference
        self.photo = ImageTk.PhotoImage(pil.resize((256, 256)))
        self.canvas.config(image=self.photo)

    def _on_change(self, *_):
        self._draw()

if __name__ == "__main__":
    XRayGUI().mainloop()