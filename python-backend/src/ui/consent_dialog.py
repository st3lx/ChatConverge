# src/ui/consent_dialog.py
import tkinter as tk
from tkinter import messagebox

class ConsentDialog:
    """
    Consent dialog used at application start.
    Usage:
        dlg = ConsentDialog()
        agreed = dlg.run()   # True/False
    """

    def __init__(self, master=None):
        # create a hidden root if no master provided
        self._external_master = master is not None
        self._master = master or tk.Tk()
        if not self._external_master:
            # only configure root if this class owns it
            self._master.title("ChatConverge — Consent")
            self._master.geometry("520x320")
            self._master.resizable(False, False)

        self._agreed = False
        self._build_ui()

    def _build_ui(self):
        text = (
            "Welcome to ChatConverge!\n\n"
            "Before importing your chat history, please review:\n\n"
            "• All processing occurs locally on your device.\n"
            "• No messages or attachments are uploaded unless you explicitly enable cloud sync.\n"
            "• VirusTotal (optional) only checks file SHA256 hashes with your explicit consent.\n\n"
            "By clicking 'I Agree', you consent to ChatConverge reading your exported chat file\n"
            "for indexing and search. Do not import data you are not authorized to access."
        )

        frame = tk.Frame(self._master, padx=16, pady=12)
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text=text, justify="left", wraplength=480)
        label.pack(pady=(6, 12))

        # small link button for privacy (if desired)
        def open_privacy():
            messagebox.showinfo("Privacy", "All data is processed locally. See PRIVACY_POLICY.md for details.")

        privacy_btn = tk.Button(frame, text="View Privacy Policy", command=open_privacy)
        privacy_btn.pack(pady=(0, 12))

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=(6, 6))

        agree_btn = tk.Button(btn_frame, text="I Agree", width=14, bg="#4CAF50", fg="white", command=self._agree)
        agree_btn.grid(row=0, column=0, padx=8)

        decline_btn = tk.Button(btn_frame, text="Decline", width=14, bg="#f44336", fg="white", command=self._decline)
        decline_btn.grid(row=0, column=1, padx=8)

    def _agree(self):
        self._agreed = True
        # only destroy if this class created the master
        if not self._external_master:
            self._master.destroy()
        else:
            # hide dialog if embedded
            self._master.quit()

    def _decline(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            self._agreed = False
            if not self._external_master:
                self._master.destroy()
            else:
                self._master.quit()

    def run(self) -> bool:
        """
        Show the dialog and block until user chooses.
        Returns True if user agreed; False otherwise.
        """
        # If we created the hidden root, call mainloop; otherwise assume external loop
        if not self._external_master:
            # run the window (this will block)
            self._master.mainloop()
        else:
            # if embedded, start transient dialog behaviour (not used in current code)
            self._master.update()
        return self._agreed

