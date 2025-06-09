#!/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
import json
from datetime import datetime, timedelta

# Global variables
current_mode = "edit"  # "edit" or "practice"
current_position = "1.0"
wpm_timer = datetime.now()
wpm_counter = 0
wpm_10s_avg = 0
wpm_max = 0  # New variable to track max WPM
correct_chars = 0  # Track total correct characters
incorrect_chars = 0  # Track total incorrect characters

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        # Save the text content
        with open(file_path, 'w') as file:
            file.write(text_area.get(1.0, tk.END))
        
        # Save color information to a companion file
        color_data = {
            "correct": [],
            "incorrect": []
        }
        
        # Get all ranges with "correct" tag
        correct_ranges = text_area.tag_ranges("correct")
        for i in range(0, len(correct_ranges), 2):
            start = text_area.index(correct_ranges[i])
            end = text_area.index(correct_ranges[i+1])
            color_data["correct"].append((start, end))
        
        # Get all ranges with "incorrect" tag
        incorrect_ranges = text_area.tag_ranges("incorrect")
        for i in range(0, len(incorrect_ranges), 2):
            start = text_area.index(incorrect_ranges[i])
            end = text_area.index(incorrect_ranges[i+1])
            color_data["incorrect"].append((start, end))
        
        # Save color data to a companion file
        color_file_path = file_path + ".colors"
        with open(color_file_path, 'w') as color_file:
            json.dump(color_data, color_file)

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Open the text content
        with open(file_path, 'r') as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())
        
        # Clear existing color tags
        text_area.tag_remove("correct", "1.0", tk.END)
        text_area.tag_remove("incorrect", "1.0", tk.END)
        
        # Try to load color information from companion file
        color_file_path = file_path + ".colors"
        try:
            with open(color_file_path, 'r') as color_file:
                color_data = json.load(color_file)
                
                # Apply "correct" tags
                for start, end in color_data["correct"]:
                    text_area.tag_add("correct", start, end)
                
                # Apply "incorrect" tags
                for start, end in color_data["incorrect"]:
                    text_area.tag_add("incorrect", start, end)
        except FileNotFoundError:
            # No color data file exists, that's okay
            pass

def toggle_mode():
    global current_mode, current_position, wpm_timer, wpm_counter
    
    if current_mode == "edit":
        current_mode = "practice"
        mode_label.config(text="Mode: Practice")
        text_area.config(state=tk.DISABLED)
        # Reset WPM tracking when entering practice mode
        wpm_timer = datetime.now()
        wpm_counter = 0
        # Don't reset the cursor position if returning to practice mode
        if current_position == "1.0":  # Only set to beginning if first time
            current_position = "1.0"
            text_area.mark_set("insert", current_position)
        # Don't remove color tags anymore
        app.bind("<Key>", check_typing)
        text_area.bind("<Button-1>", set_cursor_position)
    else:
        current_mode = "edit"
        mode_label.config(text="Mode: Edit")
        text_area.config(state=tk.NORMAL)
        app.unbind("<Key>")
        text_area.unbind("<Button-1>")

def update_10s_wpm(delta_t):
    global wpm_timer, wpm_counter, wpm_10s_avg, wpm_max
    wpm_10s_avg = (wpm_counter / delta_t) * 60 / 5  # Divide by 5 chars per word
    
    # Update max WPM if current 10s average is higher
    if wpm_10s_avg > wpm_max:
        wpm_max = wpm_10s_avg
    
    # Calculate accuracy
    total_chars = correct_chars + incorrect_chars
    accuracy = (correct_chars / total_chars * 100) if total_chars > 0 else 100
    
    # Update the WPM and accuracy displays
    wpm_label.config(text=f'10s Avg: {wpm_10s_avg:.1f} | Max: {wpm_max:.1f} WPM')
    accuracy_label.config(text=f'Accuracy: {accuracy:.1f}%')
    
    wpm_counter = 0
    wpm_timer = datetime.now()

def check_wpm_timer():
    """Check if 10 seconds have passed and update WPM if needed"""
    global wpm_timer
    current_time = datetime.now()
    delta_t = (current_time - wpm_timer).total_seconds()
    
    if delta_t >= 10:
        update_10s_wpm(delta_t)
    
    # Schedule this function to run again in 1 second
    app.after(1000, check_wpm_timer)

def check_typing(event):
    global current_position, wpm_counter, correct_chars, incorrect_chars
    
    # Handle backspace
    if event.keysym == 'BackSpace':
        # Get previous position
        line, col = current_position.split('.')
        if int(col) > 0:
            # Move back one character in the same line
            current_position = f"{line}.{int(col)-1}"
        elif int(line) > 1:
            # Move to the end of the previous line
            prev_line = int(line) - 1
            prev_line_length = len(text_area.get(f"{prev_line}.0", f"{prev_line}.end"))
            current_position = f"{prev_line}.{prev_line_length}"
        
        # Remove any color tags from the character
        text_area.tag_remove("correct", current_position)
        text_area.tag_remove("incorrect", current_position)
        
        # Move cursor to the new position
        text_area.mark_set("insert", current_position)
        return "break"
    
    if event.char and event.keysym not in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
        # Get the character at current position
        expected_char = text_area.get(current_position)
        
        # Skip newlines and move to next character
        if expected_char == '\n':
            line, col = current_position.split('.')
            current_position = f"{int(line)+1}.0"
            text_area.mark_set("insert", current_position)
            return "break"
            
        # Check if typed character matches expected character
        if event.char == expected_char:
            # Apply green color to the character
            text_area.tag_add("correct", current_position)
            # Add one to the character counter
            wpm_counter += 1
            correct_chars += 1
        else:
            # Apply red color to the character
            text_area.tag_add("incorrect", current_position)
            incorrect_chars += 1
        
        # Move to next character
        line, col = current_position.split('.')
        current_position = f"{line}.{int(col)+1}"
        text_area.mark_set("insert", current_position)
    
    return "break"  # Prevent default handling

def set_cursor_position(event):
    global current_position
    
    # Get the position where the user clicked
    index = text_area.index(f"@{event.x},{event.y}")
    
    # Update current position
    current_position = index
    
    # Move cursor to the new position
    text_area.mark_set("insert", current_position)
    
    return "break"

def reset_colors():
    # Remove all color tags from the text
    text_area.tag_remove("correct", "1.0", tk.END)
    text_area.tag_remove("incorrect", "1.0", tk.END)
    messagebox.showinfo("Reset", "All color formatting has been reset.")

app = tk.Tk()
app.title("CoPywork")
app.geometry("600x400")

# Create a frame for the mode label
frame = tk.Frame(app)
frame.pack(fill='x')

# Mode indicator
mode_label = tk.Label(frame, text="Mode: Edit")
mode_label.pack(side='left')

# WPM indicator
wpm_label = tk.Label(frame, text=f'10s Avg: {wpm_10s_avg:.1f} | Max: {wpm_max:.1f} WPM')
wpm_label.pack(side='right')

# Accuracy indicator
accuracy_label = tk.Label(frame, text='Accuracy: 100.0%')
accuracy_label.pack(side='right', padx=(0, 10))

# Text area
text_area = tk.Text(app, wrap='word', font=('Fira Code', 12), bg="#333333", fg="#C1E4F6")  # dark gray background
text_area.pack(expand=1, fill='both')

# Configure tags for correct and incorrect typing
text_area.tag_configure("correct", foreground="#56DB3A")  # Less saturated green
text_area.tag_configure("incorrect", foreground="#FC6A21")  # Less saturated red

# Menu bar
menu_bar = tk.Menu(app)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add mode menu
mode_menu = tk.Menu(menu_bar, tearoff=0)
mode_menu.add_command(label="Toggle Mode", command=toggle_mode)
mode_menu.add_command(label="Reset Colors", command=reset_colors)
menu_bar.add_cascade(label="Mode", menu=mode_menu)

app.config(menu=menu_bar)
app.after(1000, check_wpm_timer)
app.mainloop()
