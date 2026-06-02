import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import hashlib
import sqlite3
import re

# =========================
# DATABASE SETUP
# =========================
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS password_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password_hash TEXT
)
""")

conn.commit()

# =========================
# HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# SAVE PASSWORD
# =========================
def save_password(password):
    hashed = hash_password(password)

    cursor.execute(
        "INSERT INTO password_history(password_hash) VALUES(?)",
        (hashed,)
    )

    conn.commit()

# =========================
# CHECK OLD PASSWORD
# =========================
def check_password_exists(password):
    hashed = hash_password(password)

    cursor.execute(
        "SELECT * FROM password_history WHERE password_hash=?",
        (hashed,)
    )

    return cursor.fetchone() is not None

# =========================
# PASSWORD STRENGTH
# =========================
def check_password_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    progress["value"] = score * 20

    # Crack Time Estimate
    if score == 5:
        crack_time = "Centuries 🔥"
        result = "Very Strong Password"
        color = "#00ff99"

    elif score >= 3:
        crack_time = "Few Days ⚠️"
        result = "Medium Password"
        color = "orange"

    else:
        crack_time = "Few Seconds ❌"
        result = "Weak Password"
        color = "red"

    result_label.config(
        text=f"{result}\nEstimated Crack Time: {crack_time}",
        fg=color
    )

# =========================
# GENERATE PASSWORD
# =========================
def generate_password():

    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = ''.join(
        random.choice(characters)
        for _ in range(14)
    )

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# =========================
# COPY PASSWORD
# =========================
def copy_password():

    root.clipboard_clear()
    root.clipboard_append(password_entry.get())

    messagebox.showinfo(
        "Copied",
        "Password copied successfully!"
    )

# =========================
# ANALYZE PASSWORD
# =========================
def analyze_password():

    password = password_entry.get()

    check_password_strength(password)

    if check_password_exists(password):

        history_label.config(
            text="⚠️ Password already used before",
            fg="orange"
        )

    else:

        save_password(password)

        history_label.config(
            text="✅ Password stored securely",
            fg="#00ff99"
        )

# =========================
# LOGIN SYSTEM
# =========================
def login():

    username = username_entry.get()
    password = login_password_entry.get()

    if username == "admin" and password == "admin123":

        login_frame.pack_forget()
        app_frame.pack(pady=20)

    else:

        messagebox.showerror(
            "Error",
            "Invalid Login Credentials"
        )

# =========================
# MAIN WINDOW
# =========================
root = tk.Tk()

root.title("CyberShield Password Intelligence System")
root.geometry("550x550")
root.configure(bg="#121212")

# =========================
# LOGIN FRAME
# =========================
login_frame = tk.Frame(root, bg="#121212")
login_frame.pack(pady=60)

title = tk.Label(
    login_frame,
    text="CyberShield Login",
    font=("Arial", 22, "bold"),
    bg="#121212",
    fg="white"
)

title.pack(pady=20)

username_entry = tk.Entry(
    login_frame,
    width=30,
    font=("Arial", 12)
)

username_entry.pack(pady=10)
username_entry.insert(0, "admin")

login_password_entry = tk.Entry(
    login_frame,
    width=30,
    show="*",
    font=("Arial", 12)
)

login_password_entry.pack(pady=10)
login_password_entry.insert(0, "admin123")

login_button = tk.Button(
    login_frame,
    text="Login",
    command=login,
    bg="#6c5ce7",
    fg="white",
    width=20,
    font=("Arial", 12, "bold")
)

login_button.pack(pady=20)

# =========================
# APP FRAME
# =========================
app_frame = tk.Frame(root, bg="#121212")

heading = tk.Label(
    app_frame,
    text="CyberShield Password Analyzer",
    font=("Arial", 20, "bold"),
    bg="#121212",
    fg="#00ffcc"
)

heading.pack(pady=20)

password_entry = tk.Entry(
    app_frame,
    width=35,
    font=("Arial", 14),
    justify="center"
)

password_entry.pack(pady=15)

progress = ttk.Progressbar(
    app_frame,
    orient="horizontal",
    length=300,
    mode="determinate"
)

progress.pack(pady=15)

check_button = tk.Button(
    app_frame,
    text="Check Password Strength",
    command=analyze_password,
    bg="#0984e3",
    fg="white",
    width=25,
    font=("Arial", 11, "bold")
)

check_button.pack(pady=10)

generate_button = tk.Button(
    app_frame,
    text="Generate Strong Password",
    command=generate_password,
    bg="#00b894",
    fg="white",
    width=25,
    font=("Arial", 11, "bold")
)

generate_button.pack(pady=10)

copy_button = tk.Button(
    app_frame,
    text="Copy Password",
    command=copy_password,
    bg="#e17055",
    fg="white",
    width=25,
    font=("Arial", 11, "bold")
)

copy_button.pack(pady=10)

result_label = tk.Label(
    app_frame,
    text="",
    font=("Arial", 14, "bold"),
    bg="#121212"
)

result_label.pack(pady=20)

history_label = tk.Label(
    app_frame,
    text="",
    font=("Arial", 11),
    bg="#121212"
)

history_label.pack()

footer = tk.Label(
    app_frame,
    text="Cybersecurity Project using Python",
    font=("Arial", 10),
    bg="#121212",
    fg="gray"
)

footer.pack(side="bottom", pady=20)

# =========================
# RUN APP
# =========================
root.mainloop()
