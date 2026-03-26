import tkinter as tk
import time
import ctypes

############ LOGIC SECTION

class LearningTimer():
    def __init__(self, seconds=0, name="Study Timer"):
        self.start_time = None
        self.total_seconds = 0
        self.is_running = False
    
    def start(self):
        self.start_time = time.time()
        self.is_running = True

    def stop(self):
        if self.is_running:
            elapsed = time.time() - self.start_time
            self.total_seconds += elapsed
            self.is_running = False
        else:
            pass

    def get_time(self):
        if self.is_running and self.start_time != None:
            return self.total_seconds + (time.time() - self.start_time)
        else:
            return self.total_seconds

my_timer = LearningTimer(seconds=0, name="Study Timer")

def start_learning():
    my_timer.start()

def stop_learning():
    my_timer.stop()

def update_timer():
    current_time = my_timer.get_time()  # get seconds from the timer
    whole_seconds = int(current_time)   # convert to whole number of seconds

    hours = whole_seconds // 3600
    minutes = (whole_seconds // 60) % 60
    seconds = whole_seconds % 60

    # update the label with formatted time
    timer_label.config(text=f"{hours}:{minutes:02}:{seconds:02}")

    # schedule this function to run again in 1 second
    root.after(1000, update_timer)

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

############ GUI SECTION

#this creates the window
root = tk.Tk()
root.title("MATRIX LEARNING TRACKER")
root.geometry("400x200")
root.configure(bg="black")
dark_title_bar(root)

#label for TO THE STARS
title_phrase = tk.Label(
    root,
    text="TO THE STARS",
    font=("Courier", 30, "bold"),  # big and bold
    fg="#00FF41",  # Matrix green
    bg="black"     # match background
)
title_phrase.pack(pady=(10, 0))


#label for timer
timer_label = tk.Label(
    root,
    text="0:00:00",
    font=("Courier", 40, "bold"),
    fg="#00FF41",    # Matrix green
    bg="black"       # match window background
)
timer_label.pack(expand=True) #expand=True centers it

start_button = tk.Button(
    root,
    text="Learning",
    command=start_learning,
    fg="#00FF41",   # green text
    bg="black",     # dark background
    activebackground="black",
    activeforeground="#00FF41",
    font=("Courier", 12, "bold")
)

stop_button = tk.Button(
    root,
    text="Not Learning",
    command=stop_learning,
    fg="#00FF41",
    bg="black",
    activebackground="black",
    activeforeground="#00FF41",
    font=("Courier", 12, "bold")
)

start_button.pack(side="left", padx=20, pady=20)
stop_button.pack(side="right", padx=20, pady=20)

update_timer()

root.mainloop()