#!/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variables
current_mode = "edit"  # "edit" or "practice"
current_position = "1.0"

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_area.get(1.0, tk.END))

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())

def toggle_mode():
    global current_mode, current_position
    
    if current_mode == "edit":
        current_mode = "practice"
        mode_label.config(text="Mode: Practice")
        text_area.config(state=tk.DISABLED)
        current_position = "1.0"
        text_area.tag_remove("correct", "1.0", tk.END)
        text_area.tag_remove("incorrect", "1.0", tk.END)
        text_area.mark_set("insert", current_position)
        app.bind("<Key>", check_typing)
    else:
        current_mode = "edit"
        mode_label.config(text="Mode: Edit")
        text_area.config(state=tk.NORMAL)
        app.unbind("<Key>")

def check_typing(event):
    global current_position
    
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
        else:
            # Apply red color to the character
            text_area.tag_add("incorrect", current_position)
        
        # Move to next character
        line, col = current_position.split('.')
        current_position = f"{line}.{int(col)+1}"
        text_area.mark_set("insert", current_position)
    
    return "break"  # Prevent default handling

app = tk.Tk()
app.title("Text Editor with Practice Mode")
app.geometry("600x400")

# Create a frame for the mode label
frame = tk.Frame(app)
frame.pack(fill='x')

# Mode indicator
mode_label = tk.Label(frame, text="Mode: Edit")
mode_label.pack(side='left')

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
menu_bar.add_cascade(label="Mode", menu=mode_menu)

app.config(menu=menu_bar)
app.mainloop()
