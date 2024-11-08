import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Hello World App")
    root.geometry("300x100")
    
    label = tk.Label(root, text="Hello, World!", font=("Arial", 16))
    label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
