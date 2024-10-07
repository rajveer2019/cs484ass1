import tkinter as tk
from gui import ImageBrowserGUI

def main():
    root = tk.Tk()
    app = ImageBrowserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()