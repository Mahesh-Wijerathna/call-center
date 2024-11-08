import tkinter as tk

class ToggleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Toggle Start/Stop")
        self.root.geometry("300x150")

        # Initialize the state variable
        self.state = "Stopped"

        # Label to display the current state
        self.state_label = tk.Label(root, text=f"Current State: {self.state}", font=("Arial", 14))
        self.state_label.pack(pady=20)

        # Button to toggle the state
        self.toggle_button = tk.Button(root, text="Start", font=("Arial", 12), command=self.toggle_state)
        self.toggle_button.pack(pady=10)

    def toggle_state(self):
        # Toggle between "Started" and "Stopped" states
        if self.state == "Stopped":
            self.state = "Started"
            self.toggle_button.config(text="Stop")
        else:
            self.state = "Stopped"
            self.toggle_button.config(text="Start")

        # Update the label to show the current state
        self.state_label.config(text=f"Current State: {self.state}")

def main():
    root = tk.Tk()
    app = ToggleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
