import tkinter as tk
from tkinter import messagebox

class ConsentDialog:
    """
    Displays a consent dialog before importing or analyzing chats.
    Returns True if user agrees, False otherwise.
    """

    def __init__(self):
        self.agreed = False
        self.root = tk.Tk()
        self.root.title("ChatConverge — User Consent")
        self.root.geometry("480x300")
        self.root.resizable(False, False)

        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        text = (
            "Welcome to ChatConverge!\n\n"
            "Before importing your chat history, please review:\n\n"
            "• All processing occurs locally on your device.\n"
            "• No messages or attachments are uploaded.\n"
            "• You can optionally enable file safety scans later.\n\n"
            "By clicking 'I Agree', you consent to ChatConverge "
            "reading your exported chat file for indexing and search."
        )

        label = tk.Label(self.root, text=text, justify="left", wraplength=440)
        label.pack(pady=20, padx=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        agree_btn = tk.Button(
            button_frame,
            text="I Agree",
            width=15,
            bg="#4CAF50",
            fg="white",
            command=self._agree
        )
        agree_btn.grid(row=0, column=0, padx=10)

        decline_btn = tk.Button(
            button_frame,
            text="Decline",
            width=15,
            bg="#f44336",
            fg="white",
            command=self._decline
        )
        decline_btn.grid(row=0, column=1, padx=10)

    def _agree(self):
        self.agreed = True
        self.root.destroy()

    def _decline(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            self.root.destroy()
        else:
            return

    def get_consent(self):
        return self.agreed
