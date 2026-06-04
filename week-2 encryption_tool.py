import tkinter as tk
from tkinter import messagebox, filedialog
import hashlib
import sqlite3
import random

# Database
conn = sqlite3.connect("crypt.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS history(
id INTEGER PRIMARY KEY,
message TEXT,
result TEXT
)
""")
conn.commit()

PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

# Functions
def login():
    entered = password_entry.get()

    if hashlib.sha256(entered.encode()).hexdigest() == PASSWORD_HASH:
        login_frame.pack_forget()
        main_frame.pack()
    else:
        messagebox.showerror("Error", "Wrong Password")

def encrypt():
    try:
        shift = int(shift_entry.get())
    except:
        messagebox.showerror("Error", "Enter number")
        return

    text = input_box.get("1.0", tk.END)

    result = ""

    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char)-start+shift)%26+start)
        else:
            result += char

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

    cur.execute(
        "INSERT INTO history(message,result) VALUES (?,?)",
        (text, result)
    )
    conn.commit()

def decrypt():
    try:
        shift = int(shift_entry.get())
    except:
        messagebox.showerror("Error", "Enter number")
        return

    text = input_box.get("1.0", tk.END)

    result = ""

    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char)-start-shift)%26+start)
        else:
            result += char

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

def random_key():
    shift_entry.delete(0, tk.END)
    shift_entry.insert(0, random.randint(1, 25))

def export():
    data = output_box.get("1.0", tk.END)

    file = filedialog.asksaveasfilename(
        defaultextension=".txt"
    )

    if file:
        with open(file, "w") as f:
            f.write(data)

        messagebox.showinfo("Saved", "File Exported")

# GUI
root = tk.Tk()
root.title("SecureCrypt Pro Lite")
root.geometry("700x550")
root.configure(bg="white")

# Login Frame
login_frame = tk.Frame(root, bg="white")
login_frame.pack()

tk.Label(
    login_frame,
    text="🌸 SecureCrypt Login",
    font=("Arial",20,"bold"),
    bg="white",
    fg="deeppink"
).pack(pady=20)

password_entry = tk.Entry(
    login_frame,
    show="*",
    width=30
)
password_entry.pack()

tk.Button(
    login_frame,
    text="Login",
    bg="#FFD1DC",
    command=login
).pack(pady=10)

# Main Frame
main_frame = tk.Frame(root, bg="white")

tk.Label(
    main_frame,
    text="SecureCrypt Pro Lite",
    font=("Arial",18,"bold"),
    bg="white",
    fg="deeppink"
).pack(pady=10)

input_box = tk.Text(main_frame, height=6, width=60)
input_box.pack()

shift_entry = tk.Entry(main_frame)
shift_entry.pack(pady=5)

tk.Button(
    main_frame,
    text="Encrypt",
    bg="#FFB6C1",
    command=encrypt
).pack(pady=3)

tk.Button(
    main_frame,
    text="Decrypt",
    bg="#FFD1DC",
    command=decrypt
).pack(pady=3)

tk.Button(
    main_frame,
    text="Random Key",
    bg="#FFE4E1",
    command=random_key
).pack(pady=3)

output_box = tk.Text(main_frame, height=6, width=60)
output_box.pack(pady=10)

tk.Button(
    main_frame,
    text="Export Result",
    bg="#FFC0CB",
    command=export
).pack()

root.mainloop()
