import tkinter as tk
from tkinter import messagebox
import ctypes

# --- CONSTANTS (Change these to change the whole app's look) ---
BG_COLOR = "black"
MATRIX_GREEN = "#00FF41"
FONT_MAIN = ("Courier", 18)
FONT_BOLD = ("Courier", 12, "bold")

# --- FUNCTIONS ---

def dark_title_bar(window):
    window.update()
    try:
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ctypes.windll.user32.GetParent
        hwnd = get_parent(window.winfo_id())
        value = ctypes.c_int(2)
        set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
    except:
        pass # Fallback for non-windows systems

def add_task(event=None): # 'event' allows this to work with the Enter key
    task = task_entry.get()
    if task.strip() != "":
        listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("System Error", "Entry field is empty.")

def remove_task():
    try:
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
    except IndexError:
        messagebox.showwarning("System Error", "No task selected for deletion.")

def save_tasks():
    tasks = listbox.get(0, tk.END) 
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")

def load_tasks():
    try:
        with open("tasks.txt", "r") as f:
            for line in f:
                listbox.insert(tk.END, line.strip())
    except FileNotFoundError:
        pass

# --- GUI SETUP ---

root = tk.Tk()
dark_title_bar(root)
root.title("MATRIX TODO FACTORY")
root.geometry("400x550")
root.configure(bg=BG_COLOR)

# Header
tk.Label(root, text="TO THE STARS", font=("Courier", 20, "bold"), 
         bg=BG_COLOR, fg=MATRIX_GREEN).pack(pady=10)

# Input Box
task_entry = tk.Entry(root, font=FONT_MAIN, bg="#101010", fg=MATRIX_GREEN, 
                      insertbackground=MATRIX_GREEN, borderwidth=0, highlightthickness=0)
task_entry.pack(pady=5)
task_entry.bind('<Return>', add_task) # <--- Hits 'Enter' to add!

# Add Button
add_button = tk.Button(root, text="[ ADD TASK ]", font=FONT_BOLD, bg=BG_COLOR, 
                       fg=MATRIX_GREEN, activebackground=MATRIX_GREEN, 
                       activeforeground="black", command=add_task) # <--- Added command
add_button.pack(pady=5)

# Listbox
listbox = tk.Listbox(root, font=FONT_MAIN, width=40, height=10, bg=BG_COLOR, 
                     fg=MATRIX_GREEN, selectbackground="#003305", 
                     selectforeground=MATRIX_GREEN, activestyle="none", 
                     highlightthickness=0, borderwidth=0)
listbox.pack(pady=10)

# Remove Button
remove_button = tk.Button(root, text="[ REMOVE TASK ]", font=FONT_BOLD, bg=BG_COLOR, 
                          fg=MATRIX_GREEN, activebackground=MATRIX_GREEN, 
                          activeforeground="black", borderwidth=1, 
                          highlightthickness=0, command=remove_task)
remove_button.pack(pady=5)

# --- RUN ---

load_tasks()
root.protocol("WM_DELETE_WINDOW", lambda: [save_tasks(), root.destroy()])
root.mainloop()
