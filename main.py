from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
iterations = 0
timer = None
# isPaused = False
paused_count = 0
# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer")
    check_symbols.config(text="")
    global iterations
    iterations = 0
    # global isPaused
    # isPaused = False
    start_button.config(state="normal")
    pause_button.config(state="disabled")
    resume_button.config(state="disabled")


# ---------------------------- TIMER MECHANISM ------------------------------- #


def pause_timer():
    # global isPaused
    # isPaused = True
    window.after_cancel(timer)
    timer_label.config(text="Paused", fg=RED)
    resume_button.config(state="normal")
    pause_button.config(state="disabled")


def resume_timer():
    # global isPaused
    # isPaused = False
    if iterations % 8 == 0:
        timer_label.config(text="Break", fg=PINK)
    elif iterations % 2 == 0:
        timer_label.config(text="Break", fg=RED)
    else:
        timer_label.config(text="Work", fg=GREEN)
    window.after_cancel(timer)
    count_down(paused_count)
    resume_button.config(state="disabled")
    pause_button.config(state="normal")


def start_timer():
    pause_button.config(state="normal")
    resume_button.config(state="disabled")
    reset_button.config(state="normal")

    global iterations
    iterations += 1
    work_seconds = WORK_MIN * 60
    short_break_seconds = SHORT_BREAK_MIN * 60
    long_break_seconds = LONG_BREAK_MIN * 60
    start_button.config(state="disabled")
    if iterations % 8 == 0:
        count_down(long_break_seconds)
        timer_label.config(text="Break", fg=PINK)
    elif iterations % 2 == 0:
        count_down(short_break_seconds)
        timer_label.config(text="Break", fg=RED)
    else:
        count_down(work_seconds)
        timer_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    global paused_count
    paused_count = count
    count_minute = math.floor(count / 60)
    count_seconds = count % 60
    if count_seconds < 10:
        count_seconds = f"0{count_seconds}"
    canvas.itemconfig(timer_text, text=f"{count_minute}:{count_seconds}")
    if count > 0:
        # if isPaused == False:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        check_marks = ""
        work_sessions = math.floor(iterations / 2)
        for _ in range(work_sessions):
            check_marks += "✔"
        check_symbols.config(text=check_marks)


# ---------------------------- UI SETUP ------------------------------- #

# Creating Window for view
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Creating Timer Label
timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
timer_label.grid(row=0, column=1)

# Creating Canvas to display image and text
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_image = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_image)
timer_text = canvas.create_text(
    110, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
)
canvas.grid(row=1, column=1)


# Creating Buttons to Start, Reset Timer, Pause amd Resume

start_button = Button(text="Start", highlightbackground=YELLOW, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightbackground=YELLOW, command=reset_timer)
reset_button.grid(row=2, column=2)
reset_button.config(state="disabled")

pause_button = Button(text="Pause", highlightbackground=YELLOW, command=pause_timer)
pause_button.grid(row=3, column=2)
pause_button.config(state="disabled")

resume_button = Button(text="Resume", highlightbackground=YELLOW, command=resume_timer)
resume_button.grid(row=3, column=0)
resume_button.config(state="disabled")

# Check symbols for intervals

check_symbols = Label(bg=YELLOW, fg=GREEN)
check_symbols.grid(row=3, column=1)

# Keeping the window open
window.mainloop()
