import tkinter as tk
from gui import ImageViewer

def main():
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()