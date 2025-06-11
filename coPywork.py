#!/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
import json
from datetime import datetime, timedelta
import sys  # Import sys module for command line arguments
import zipfile  # For creating and reading .cw files
import os  # For file operations
import tempfile  # For temporary files

# Global variables
current_mode = "edit"  # "edit" or "practice"
current_position = "1.0"
wpm_timer = datetime.now()
wpm_counter = 0
wpm_10s_avg = 0
wpm_max = 0  # Track max WPM
correct_chars = 0  # Track total correct characters
incorrect_chars = 0  # Track total incorrect characters
session_start_time = None  # When active typing started
session_chars = 0  # Characters typed in active session
session_typing_duration = 0  # Total active typing duration in seconds
last_typed_time = None  # Time of last keystroke
is_typing_active = False  # Flag to track if typing is currently active
current_file_path = None  # Track the currently open file

def handle_file_save(file_path):
    """Helper to check file extension and save using the correct method."""
    global current_file_path
    current_file_path = file_path
    if current_file_path.lower().endswith('.txt'):
        save_to_txt_file(current_file_path)
    else:
        # Add .cw extension if not present and not a .txt file
        if not current_file_path.lower().endswith('.cw'):
            current_file_path += '.cw'
        save_to_cw_file(current_file_path)

def save_file():
    global current_file_path
    
    # If we already have a file path, save directly to it
    if current_file_path:
        handle_file_save(current_file_path)
    else:
        # No current file, prompt for a location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".cw",
            filetypes=[("CoPywork files", "*.cw"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            handle_file_save(file_path)

def save_to_cw_file(file_path):
    """Save text content and color data to a .cw zip archive"""
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save text content to a temporary file
            text_file_path = os.path.join(temp_dir, "content.txt")
            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text_area.get(1.0, tk.END))
            
            # Prepare color data
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
            
            # Save color data to a temporary file
            color_file_path = os.path.join(temp_dir, "colors.json")
            with open(color_file_path, 'w', encoding='utf-8') as color_file:
                json.dump(color_data, color_file)
            
            # Create a zip archive containing both files
            with zipfile.ZipFile(file_path, 'w') as zip_file:
                zip_file.write(text_file_path, arcname="content.txt")
                zip_file.write(color_file_path, arcname="colors.json")
        
        # Show success message
        messagebox.showinfo("Save Successful", f"File saved to {file_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file: {str(e)}")

def save_to_txt_file(file_path):
    """Save text content and color data to separate .txt and .colors files"""
    try:
        # Save text content
        with open(file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text_area.get(1.0, tk.END))
        
        # Prepare color data
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
        with open(color_file_path, 'w', encoding='utf-8') as color_file:
            json.dump(color_data, color_file)
        
        # Show success message
        messagebox.showinfo("Save Successful", f"File saved to {file_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file: {str(e)}")

def open_file(file_path):
    global current_file_path
    
    try:
        # Check if file is a .cw file
        if file_path.lower().endswith('.cw'):
            open_cw_file(file_path)
        else:
            # Handle legacy .txt files
            with open(file_path, 'r', encoding='utf-8') as file:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, file.read())
            
            # Set the current file path
            current_file_path = file_path

            # Try to load color information from companion file
            color_file_path = file_path + ".colors"
            try:
                with open(color_file_path, 'r', encoding='utf-8') as color_file:
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
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error opening file: {str(e)}")

def open_cw_file(file_path):
    """Open a .cw zip archive and load its contents"""
    global current_file_path
    
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract the zip archive
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                zip_file.extractall(temp_dir)
            
            # Load text content
            text_file_path = os.path.join(temp_dir, "content.txt")
            with open(text_file_path, 'r', encoding='utf-8') as text_file:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, text_file.read())
            
            # Load color data
            color_file_path = os.path.join(temp_dir, "colors.json")
            with open(color_file_path, 'r', encoding='utf-8') as color_file:
                color_data = json.load(color_file)
                
                # Apply "correct" tags
                for start, end in color_data["correct"]:
                    text_area.tag_add("correct", start, end)
                
                # Apply "incorrect" tags
                for start, end in color_data["incorrect"]:
                    text_area.tag_add("incorrect", start, end)
        
        # Set the current file path
        current_file_path = file_path
    
    except Exception as e:
        messagebox.showerror("Error", f"Error opening .cw file: {str(e)}")

def open_file_from_menu():
    file_path = filedialog.askopenfilename(
        filetypes=[("CoPywork files", "*.cw"), ("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        open_file(file_path)

def open_file_from_cmdline(file_path):
    open_file(file_path)

def toggle_mode():
    global current_mode, current_position, wpm_timer, wpm_counter
    
    if current_mode == "edit":
        current_mode = "practice"
        mode_label.config(text="Mode: Practice")
        text_area.config(state=tk.DISABLED)
        # Reset WPM tracking when entering practice mode
        wpm_timer = datetime.now()
        wpm_counter = 0
        
        # Save current cursor position before switching modes
        current_position = text_area.index("insert")
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
    
    # Calculate session average if typing is active
    session_avg = 0
    if session_typing_duration > 0:
        session_avg = (session_chars / session_typing_duration) * 60 / 5
    
    # Update the WPM and accuracy displays
    wpm_label.config(text=f'10s: {wpm_10s_avg:.1f} | Avg: {session_avg:.1f} | Max: {wpm_max:.1f} WPM')
    accuracy_label.config(text=f'Accuracy: {accuracy:.1f}%')
    
    wpm_counter = 0
    wpm_timer = datetime.now()

def check_typing_activity():
    """Check if typing has been inactive for 5 seconds"""
    global is_typing_active, last_typed_time, session_typing_duration
    
    current_time = datetime.now()
    
    # If typing is active but no keystrokes for 5 seconds
    if is_typing_active and last_typed_time:
        inactive_time = (current_time - last_typed_time).total_seconds()
        if inactive_time >= 5:
            # Pause the session timer
            is_typing_active = False
            # remove previous 5 seconds from the duration
            if session_typing_duration <= 5:
                session_typing_duration -= 5
        elif session_start_time:
            session_typing_duration += 1
            # Don't reset session_start_time so we can resume
    
    # Schedule this function to run again in 1 second
    app.after(1000, check_typing_activity)

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
    global session_start_time, session_chars, last_typed_time, is_typing_active
    
    # Update typing activity tracking
    current_time = datetime.now()
    last_typed_time = current_time
    
    # If this is the first keystroke or resuming after pause
    if not is_typing_active:
        is_typing_active = True
        session_start_time = current_time
    
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
            session_chars += 1
        else:
            # Apply red color to the character
            text_area.tag_add("incorrect", current_position)
            incorrect_chars += 1
        
        # Move to next character
        line, col = current_position.split('.')
        current_position = f"{line}.{int(col)+1}"
        text_area.mark_set("insert", current_position)
    
    return "break"  # Prevent default handling (to prevent normal text editing)

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

def bind_shortcuts():
    """Bind keyboard shortcuts to functions"""
    # Ctrl+S to save
    app.bind("<Control-s>", lambda event: save_file())
    app.bind("<Control-m>", lambda event: toggle_mode())

def save_as_file():
    """Save the current file with a new name"""
    global current_file_path
    
    # Prompt for a new file location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".cw",
        filetypes=[("CoPywork files", "*.cw"), ("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if file_path:
        handle_file_save(file_path)

app = tk.Tk()
app.title("coPywork")
app.geometry("600x400")

# Create a frame for the mode label
frame = tk.Frame(app)
frame.pack(fill='x')

# Mode indicator
mode_label = tk.Label(frame, text="Mode: Edit")
mode_label.pack(side='left')

# WPM indicator
wpm_label = tk.Label(frame, text=f'10s: {wpm_10s_avg:.1f} | Avg: 0.0 | Max: {wpm_max:.1f} WPM')
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
file_menu.add_command(label="Open", command=open_file_from_menu)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add mode menu
mode_menu = tk.Menu(menu_bar, tearoff=0)
mode_menu.add_command(label="Toggle Mode", command=toggle_mode)
mode_menu.add_command(label="Reset Colors", command=reset_colors)
menu_bar.add_cascade(label="Mode", menu=mode_menu)

app.config(menu=menu_bar)

# Bind keyboard shortcuts
bind_shortcuts()

# Check for command line arguments
# Open file if one is specified
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    open_file(file_path)

app.after(1000, check_wpm_timer)
app.after(1000, check_typing_activity)
app.mainloop()
