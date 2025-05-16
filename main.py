import tkinter as tk
from controlador import Controlador

def main():
    root = tk.Tk()
    app = Controlador(root)
    root.mainloop()

if __name__ == "__main__":
    main()