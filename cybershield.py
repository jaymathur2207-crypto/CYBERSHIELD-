"""
CYBERSHIELD - Interactive Cyber Security Awareness and Simulation System
Class XII - Informatics Practices

Educational, offline-only simulations:
- Password strength checker (passwords are never saved)
- Phishing message analyser (does not open or visit links)
- Caesar cipher encryption/decryption demonstration (not real-world security)
- Firewall rule simulator (sample traffic only; does not change system settings)
- Cybersecurity awareness notes
- Cyber safety quiz
- SQLite activity dashboard

Run: python cybershield.py
Optional charts: pip install matplotlib


import re
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from urllib.parse import urlparse

APP_TITLE = "CYBERSHIELD | Cyber Security Awareness"
DB_NAME = "cybershield.db"


class CyberShieldApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1000x680")
        self.root.minsize(850, 580)
        self.root.configure(bg="#eef2f7")

        self.conn = sqlite3.connect(DB_NAME)
        self.create_database()

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("Treeview", rowheight=27, font=("Arial", 10))
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.style.configure("TButton", font=("Arial", 10), padding=7)
        self.style.configure("TLabel", background="#eef2f7", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 19, "bold"),
                             foreground="#12304a", background="#eef2f7")
        self.style.configure("Sub.TLabel", font=("Arial", 10),
                             foreground="#526579", background="#eef2f7")

        self.build_layout()
        self.show_home()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def create_database(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def log_activity(self, module, result):
        self.conn.execute(
            "INSERT INTO activity(module, result, created_at) VALUES (?, ?, ?)",
            (module, result[:250], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.conn.commit()

    def build_layout(self):
        header = tk.Frame(self.root, bg="#12304a", height=76)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🛡  CYBERSHIELD", bg="#12304a", fg="white",
                 font=("Arial", 21, "bold")).pack(side="left", padx=22, pady=15)
        tk.Label(header, text="LEARN • SIMULATE • STAY SAFE", bg="#12304a",
                 fg="#b9d8ee", font=("Arial", 10, "bold")).pack(side="right", padx=22)

        body = tk.Frame(self.root, bg="#eef2f7")
        body.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(body, bg="#1d405d", width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(body, bg="#eef2f7", padx=25, pady=22)
        self.content.pack(side="right", fill="both", expand=True)

        nav_items = [
            ("Home", self.show_home),
            ("Password Checker", self.show_password),
            ("Phishing Detector", self.show_phishing),
            ("Encryption Demo", self.show_cipher),
            ("Firewall Simulator", self.show_firewall),
            ("Safety Awareness", self.show_awareness),
            ("Cyber Safety Quiz", self.show_quiz),
            ("Security Dashboard", self.show_dashboard),
        ]
        tk.Label(self.sidebar, text="MAIN MENU", bg="#1d405d", fg="#a9c7dc",
                 font=("Arial", 9, "bold")).pack(anchor="w", padx=18, pady=(22, 12))
        for label, command in nav_items:
            tk.Button(self.sidebar, text=label, command=command, anchor="w",
                      bg="#1d405d", fg="white", activebackground="#2c5878",
                      activeforeground="white", relief="flat", bd=0,
                      font=("Arial", 10), padx=18, pady=11,
                      cursor="hand2").pack(fill="x")

        footer = tk.Frame(self.root, bg="#dce5ee", height=27)
        footer.pack(fill="x")
        footer.pack_propagate(False)
        tk.Label(footer, text="Class XII Informatics Practices  |  Educational simulations only",
                 bg="#dce5ee", fg="#526579", font=("Arial", 9)).pack(side="left", padx=14)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def page_title(self, title, subtitle=""):
        ttk.Label(self.content, text=title, style="Header.TLabel").pack(anchor="w")
        if subtitle:
            ttk.Label(self.content, text=subtitle, style="Sub.TLabel").pack(
                anchor="w", pady=(5, 18))

    def card(self, parent=None):
        parent = parent or self.content
        frame = tk.Frame(parent, bg="white", padx=18, pady=16,
                         highlightbackground="#d9e2ec", highlightthickness=1)
        frame.pack(fill="x", pady=8)
        return frame

    def make_text(self, parent, height=7, width=80):
        frame = tk.Frame(parent, bg="white")
        text = tk.Text(frame, height=height, width=width, wrap="word",
                       font=("Arial", 10), relief="solid", bd=1,
                       padx=9, pady=8)
        scroll = ttk.Scrollbar(frame, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return frame, text

    def show_home(self):
        self.clear_content()
        self.page_title("Welcome to CYBERSHIELD",
                        "An interactive learning application for basic cyber safety.")
        intro = self.card()
        tk.Label(intro, text="Your digital safety learning centre",
                 bg="white", fg="#12304a", font=("Arial", 15, "bold")).pack(anchor="w")
        tk.Label(intro, text=(
            "Explore common online risks using safe, offline demonstrations. "
            "Check password habits, inspect sample messages, practise a simple cipher, "
            "test firewall rules and take a knowledge quiz."
        ), bg="white", fg="#40566b", justify="left", wraplength=700,
                 font=("Arial", 11)).pack(anchor="w", pady=(9, 0))

        grid = tk.Frame(self.content, bg="#eef2f7")
        grid.pack(fill="both", expand=True, pady=10)
        tiles = [
            ("01", "Password Checker", "Learn what makes a password stronger."),
            ("02", "Phishing Detector", "Spot warning signs in suspicious messages."),
            ("03", "Encryption Demo", "Understand a basic text cipher."),
            ("04", "Firewall Simulator", "Apply simple allow/block rules to examples."),
            ("05", "Safety Awareness", "Read practical online safety guidance."),
            ("06", "Cyber Safety Quiz", "Check what you have learned."),
        ]
        for i, (number, title, desc) in enumerate(tiles):
            r, c = divmod(i, 2)
            box = tk.Frame(grid, bg="white", padx=15, pady=13,
                           highlightbackground="#d9e2ec", highlightthickness=1)
            box.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)
            tk.Label(box, text=number, bg="white", fg="#1681a7",
                     font=("Arial", 10, "bold")).pack(anchor="w")
            tk.Label(box, text=title, bg="white", fg="#12304a",
                     font=("Arial", 12, "bold")).pack(anchor="w", pady=3)
            tk.Label(box, text=desc, bg="white", fg="#526579",
                     wraplength=300, justify="left").pack(anchor="w")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        for r in range(3):
            grid.rowconfigure(r, weight=1)

        tk.Label(self.content,
                 text="Important: This project uses sample data only. It does not scan devices, "
                      "connect to networks, or change firewall settings.",
                 bg="#fff6df", fg="#805b12", padx=12, pady=10,
                 wraplength=760, justify="left").pack(fill="x", pady=8)

    def show_password(self):
        self.clear_content()
        self.page_title("Password Strength Checker",
                        "Evaluate password characteristics locally. The password is not stored.")
        box = self.card()
        tk.Label(box, text="Enter a sample password:", bg="white",
                 font=("Arial", 10, "bold")).pack(anchor="w")
        row = tk.Frame(box, bg="white")
        row.pack(fill="x", pady=8)
        entry = ttk.Entry(row, show="*", width=48)
        entry.pack(side="left", padx=(0, 8))
        show_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(row, text="Show", variable=show_var,
                        command=lambda: entry.configure(show="" if show_var.get() else "*")
                        ).pack(side="left")
        result = tk.Label(box, text="Your result will appear here.",
                          bg="white", fg="#526579", font=("Arial", 11))
        result.pack(anchor="w", pady=8)
        details = tk.Label(box, text="", bg="white", fg="#40566b",
                           justify="left", font=("Arial", 10))
        details.pack(anchor="w")

        def check():
            password = entry.get()
            if not password:
                messagebox.showwarning("Input required", "Please enter a sample password.")
                return
            checks = [
                ("At least 12 characters", len(password) >= 12),
                ("Contains uppercase letter", bool(re.search(r"[A-Z]", password))),
                ("Contains lowercase letter", bool(re.search(r"[a-z]", password))),
                ("Contains a number", bool(re.search(r"\d", password))),
                ("Contains a special character", bool(re.search(r"[^A-Za-z0-9]", password))),
            ]
            score = sum(ok for _, ok in checks)
            level = "Strong" if score == 5 else "Moderate" if score >= 3 else "Weak"
            result.config(text=f"Result: {level}  ({score}/5 checks passed)",
                          fg="#16804a" if score >= 4 else "#a36a00" if score == 3 else "#b33a3a")
            details.config(text="\n".join(("✓ " if ok else "• ") + name
                                          for name, ok in checks))
            self.log_activity("Password Checker", f"{level} ({score}/5 checks)")
            # Clear the field after evaluation to avoid leaving a password on screen.
            entry.delete(0, tk.END)

        ttk.Button(box, text="Check Strength", command=check).pack(anchor="w", pady=5)
        tk.Label(self.content, text="Tip: Use a long, unique passphrase and never reuse "
                 "the same password on different websites.",
                 bg="#e4f3ec", fg="#246342", padx=12, pady=10,
                 wraplength=760, justify="left").pack(fill="x", pady=8)

    def analyse_message(self, message):
        lower = message.lower()
        flags = []
        if re.search(r"\b(urgent|immediately|act now|account suspended|limited time)\b", lower):
            flags.append("Uses urgent or pressure-based language")
        if re.search(r"\b(password|otp|pin|cvv|bank details)\b", lower):
            flags.append("Requests sensitive information")
        urls = re.findall(r"(?:https?://|www\.)\S+", message, flags=re.I)
        if urls:
            flags.append("Contains a link: check the real domain carefully")
        if re.search(r"\b(prize|lottery|winner|free gift|claim reward)\b", lower):
            flags.append("Promises a prize or unexpected reward")
        if re.search(r"\b(verify your account|confirm your identity|click here)\b", lower):
            flags.append("Asks you to click or verify something")
        return flags

    def show_phishing(self):
        self.clear_content()
        self.page_title("Phishing Detection Simulator",
                        "Paste a sample message to review common phishing warning signs.")
        box = self.card()
        tk.Label(box, text="Sample email / SMS text:", bg="white",
                 font=("Arial", 10, "bold")).pack(anchor="w")
        frame, text_widget = self.make_text(box, height=8)
        frame.pack(fill="x", pady=8)
        text_widget.insert("1.0", "URGENT! Your account is suspended. Click here to verify "
                             "your password and claim your free reward: http://example.test")
        output = tk.Label(box, text="Analysis will appear here.", bg="white",
                          fg="#526579", justify="left", wraplength=730,
                          font=("Arial", 10))
        output.pack(anchor="w", pady=8)

        def analyse():
            message = text_widget.get("1.0", "end").strip()
            if not message:
                messagebox.showwarning("Input required", "Enter a sample message first.")
                return
            flags = self.analyse_message(message)
            if flags:
                result = "Warning signs found:\n" + "\n".join("• " + f for f in flags)
                verdict = "Potentially suspicious"
                color = "#a33b2f"
            else:
                result = ("No common warning signs were detected by this basic checker. "
                          "That does not prove the message is genuine.")
                verdict = "No obvious flags"
                color = "#8a6500"
            output.config(text=f"{verdict}\n\n{result}", fg=color)
            self.log_activity("Phishing Detector", f"{verdict}; {len(flags)} indicator(s)")

        ttk.Button(box, text="Analyse Message", command=analyse).pack(anchor="w")
        tk.Label(self.content, text="Safety note: This is a simple keyword-based demonstration. "
                 "It can make mistakes. Never click a suspicious link to test it; verify through "
                 "the organisation's official app or website.",
                 bg="#fff6df", fg="#805b12", padx=12, pady=10,
                 wraplength=760, justify="left").pack(fill="x", pady=8)

    @staticmethod
    def caesar(text, shift):
        output = []
        for char in text:
            if "a" <= char <= "z":
                output.append(chr((ord(char) - 97 + shift) % 26 + 97))
            elif "A" <= char <= "Z":
                output.append(chr((ord(char) - 65 + shift) % 26 + 65))
            else:
                output.append(char)
        return "".join(output)

    def show_cipher(self):
        self.clear_content()
        self.page_title("Encryption & Decryption Simulator",
                        "Try a Caesar cipher to see how letters can be shifted.")
        box = self.card()
        tk.Label(box, text="Enter text:", bg="white",
                 font=("Arial", 10, "bold")).pack(anchor="w")
        entry = ttk.Entry(box, width=75)
        entry.pack(fill="x", pady=7)
        entry.insert(0, "Hello CyberShield")
        row = tk.Frame(box, bg="white")
        row.pack(anchor="w", pady=5)
        tk.Label(row, text="Shift (0–25):", bg="white").pack(side="left")
        shift_var = tk.StringVar(value="3")
        ttk.Spinbox(row, from_=0, to=25, textvariable=shift_var,
                    width=6).pack(side="left", padx=8)
        output = tk.Label(box, text="Result will appear here.", bg="white",
                          fg="#12304a", wraplength=720, justify="left",
                          font=("Arial", 11))
        output.pack(anchor="w", pady=12)

        def run_cipher(direction):
            try:
                shift = int(shift_var.get())
                if not 0 <= shift <= 25:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid shift", "Enter a whole number from 0 to 25.")
                return
            text = entry.get()
            result = self.caesar(text, shift if direction == 1 else -shift)
            label = "Encrypted" if direction == 1 else "Decrypted"
            output.config(text=f"{label} text: {result}")
            self.log_activity("Encryption Demo", f"{label} sample text (shift {shift})")

        buttons = tk.Frame(box, bg="white")
        buttons.pack(anchor="w")
        ttk.Button(buttons, text="Encrypt", command=lambda: run_cipher(1)).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Decrypt", command=lambda: run_cipher(-1)).pack(side="left")
        tk.Label(self.content, text="Learning note: Caesar cipher is a historical teaching example, "
                 "not secure encryption. Do not use it to protect real passwords or private data.",
                 bg="#fff6df", fg="#805b12", padx=12, pady=10,
                 wraplength=760, justify="left").pack(fill="x", pady=8)

    def show_firewall(self):
        self.clear_content()
        self.page_title("Firewall Simulator",
                        "Apply example rules to fictional network traffic. No real traffic is inspected.")
        box = self.card()
        tk.Label(box, text="Choose a sample traffic item:", bg="white",
                 font=("Arial", 10, "bold")).pack(anchor="w")
        samples = [
            ("HTTPS web request", "TCP", 443, "192.0.2.10"),
            ("HTTP web request", "TCP", 80, "192.0.2.20"),
            ("Remote login example", "TCP", 22, "198.51.100.8"),
            ("DNS lookup example", "UDP", 53, "192.0.2.53"),
            ("Unlisted service example", "TCP", 8080, "203.0.113.9"),
        ]
        choice = tk.StringVar(value=samples[0][0])
        ttk.Combobox(box, textvariable=choice, values=[s[0] for s in samples],
                     state="readonly", width=35).pack(anchor="w", pady=8)
        rules = tk.Label(box, text="Example rules:\n• Allow TCP port 443\n• Allow UDP port 53\n• Block all other traffic",
                         bg="white", fg="#40566b", justify="left")
        rules.pack(anchor="w", pady=6)
        result = tk.Label(box, text="Simulation result will appear here.",
                          bg="white", fg="#526579", font=("Arial", 12, "bold"))
        result.pack(anchor="w", pady=12)

        def simulate():
            item = next(s for s in samples if s[0] == choice.get())
            name, protocol, port, ip = item
            allowed = (protocol == "TCP" and port == 443) or (protocol == "UDP" and port == 53)
            verdict = "ALLOWED" if allowed else "BLOCKED"
            result.config(text=f"{verdict}\n{protocol} | Port {port} | Example IP {ip}",
                          fg="#16804a" if allowed else "#b33a3a")
            self.log_activity("Firewall Simulator", f"{name}: {verdict}")

        ttk.Button(box, text="Run Simulation", command=simulate).pack(anchor="w")
        tk.Label(self.content, text="The IP addresses shown are documentation examples. "
                 "This module only demonstrates rule logic; it does not configure your computer's firewall.",
                 bg="#e4f3ec", fg="#246342", padx=12, pady=10,
                 wraplength=760, justify="left").pack(fill="x", pady=8)

    def show_awareness(self):
        self.clear_content()
        self.page_title("Cybersecurity Awareness",
                        "Simple habits that help protect your digital information.")
        topics = [
            ("Phishing", "Fraudulent messages try to trick people into sharing information or clicking unsafe links. "
             "Check the sender and domain, be cautious of urgency, and verify requests independently."),
            ("Strong passwords", "Use long, unique passwords or passphrases. Avoid personal details and password reuse. "
             "A password manager can help manage unique passwords."),
            ("Multi-factor authentication", "Turn on MFA where available. It adds another verification step beyond a password. "
             "Never share one-time passcodes with anyone."),
            ("Software updates", "Install updates from official settings or trusted app stores. Updates often fix security weaknesses."),
            ("Safe browsing", "Check website addresses carefully, use trusted downloads, and avoid entering private information "
             "on pages reached through unexpected messages."),
            ("Backups and privacy", "Keep important files backed up. Review app permissions and avoid sharing personal information publicly."),
        ]
        for title, description in topics:
            box = self.card()
            tk.Label(box, text=title, bg="white", fg="#12304a",
                     font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(box, text=description, bg="white", fg="#40566b",
                     wraplength=730, justify="left").pack(anchor="w", pady=(5, 0))
        self.log_activity("Safety Awareness", "Viewed awareness module")

    def show_quiz(self):
        self.clear_content()
        self.page_title("Cyber Safety Quiz",
                        "Choose one answer for each question, then submit your quiz.")
        questions = [
            ("What should you do with an unexpected message asking for your OTP?",
             ["Share it quickly", "Never share it; verify independently", "Post it online", "Forward it to everyone"], 1),
            ("Which password habit is safer?",
             ["Reuse one password", "Use your name and birth year", "Use a long, unique password", "Use 123456"], 2),
            ("What is phishing?",
             ["A type of printer", "A trick to steal information", "A software update", "A backup method"], 1),
            ("What does a firewall do?",
             ["Cleans the keyboard", "Filters network traffic using rules", "Creates passwords", "Charges a laptop"], 1),
            ("Is a Caesar cipher suitable for protecting real private data?",
             ["Yes, it is unbreakable", "No, it is only a learning example", "Only for banking", "Only for Wi-Fi"], 1),
        ]
        box = self.card()
        vars_ = []
        for i, (question, options, answer) in enumerate(questions, 1):
            tk.Label(box, text=f"{i}. {question}", bg="white", fg="#12304a",
                     font=("Arial", 10, "bold"), wraplength=730,
                     justify="left").pack(anchor="w", pady=(8, 4))
            var = tk.IntVar(value=-1)
            vars_.append(var)
            for j, option in enumerate(options):
                ttk.Radiobutton(box, text=option, variable=var, value=j).pack(anchor="w", padx=12)
        result = tk.Label(box, text="", bg="white", fg="#16804a",
                          font=("Arial", 12, "bold"))
        result.pack(anchor="w", pady=12)

        def submit():
            if any(v.get() == -1 for v in vars_):
                messagebox.showwarning("Incomplete quiz", "Please answer all questions.")
                return
            score = sum(v.get() == q[2] for v, q in zip(vars_, questions))
            result.config(text=f"Your score: {score} / {len(questions)}")
            self.log_activity("Cyber Safety Quiz", f"Score: {score}/{len(questions)}")

        ttk.Button(box, text="Submit Quiz", command=submit).pack(anchor="w")

    def show_dashboard(self):
        self.clear_content()
        self.page_title("Security Dashboard",
                        "A summary of learning activities recorded on this computer.")
        rows = self.conn.execute(
            "SELECT module, result, created_at FROM activity ORDER BY id DESC LIMIT 100"
        ).fetchall()
        summary = self.conn.execute(
            "SELECT COUNT(*), COUNT(DISTINCT module) FROM activity"
        ).fetchone()
        box = self.card()
        tk.Label(box, text=f"Total activities: {summary[0]}     Modules used: {summary[1]}",
                 bg="white", fg="#12304a", font=("Arial", 12, "bold")).pack(anchor="w")
        table_frame = tk.Frame(self.content, bg="#eef2f7")
        table_frame.pack(fill="both", expand=True, pady=8)
        columns = ("module", "result", "time")
        table = ttk.Treeview(table_frame, columns=columns, show="headings")
        table.heading("module", text="Module")
        table.heading("result", text="Result")
        table.heading("time", text="Date and Time")
        table.column("module", width=170, anchor="w")
        table.column("result", width=330, anchor="w")
        table.column("time", width=170, anchor="w")
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scroll.set)
        table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        for row in rows:
            table.insert("", "end", values=row)
        buttons = tk.Frame(self.content, bg="#eef2f7")
        buttons.pack(anchor="w", pady=5)
        ttk.Button(buttons, text="Refresh", command=self.show_dashboard).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Clear Activity History",
                   command=self.clear_history).pack(side="left")
        tk.Label(self.content, text="Only module names, short results and timestamps are stored. "
                 "The password checker never saves the password entered.",
                 bg="#e4f3ec", fg="#246342", padx=12, pady=10,
                 wraplength=760, justify="left").pack(fill="x", pady=8)

    def clear_history(self):
        if messagebox.askyesno("Confirm", "Delete all saved activity history?"):
            self.conn.execute("DELETE FROM activity")
            self.conn.commit()
            self.show_dashboard()

    def close_app(self):
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CyberShieldApp(root)
    root.mainloop()
