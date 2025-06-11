# CoPywork

A tool that allows you to type over custom text.

coPywork is a practice tool designed for writers, programmers, and anyone else to study real-world technical documentation, reports, literary works, or even code while improving their typing speed and accuracy at the same time.

## What is Copywork?
The practice of **copywork** has been used by writers for generations to enhance their voice by closely studying the style of other writers.

Copywork remains useful for studying writing style today, but it can also be used to closely study technical reports, code, or any other text-based content.

Finally, with the inclusion of typing-speed tracking, users can level up their typing at the same time.

## Features

- **Edit/Practice Modes**: Switch between editing text and practicing typing
- **Real-time Statistics**: 
  - Words Per Minute (WPM) tracking
  - 10-second rolling average WPM
  - Maximum WPM achieved
  - Typing accuracy percentage
- **Color-coded Feedback**: Visual indication of correct and incorrect typing
- **Code-friendly Font**: Uses Fira Code font for better code readability
- **Save/Load Functionality**: Save your progress and color-coded feedback
- **Dark Mode**: Easy on the eyes with a dark theme optimized for code

## Installation

1. Ensure you have Python 3.x installed
2. Clone this repository
3. Install required dependencies:
```bash
pip install tkinter
```

## Usage

Run the application:
```bash
python coPywork.py [/path/to/file.txt]
```

- Use the `Mode` menu to toggle between Edit and Practice modes or reset your progress
- In Practice mode, type to match the text
- Use File menu to open and save documents
- WPM and accuracy stats are displayed in real-time

## Shortcuts
- Ctrl + S: Save the current file
- Ctrl + M: Toggle between Edit Mode & Practice Mode

## Save format
- coPywork files are saved as a zip archive with a .cw extension
- The .cw files contain the text content as well as copying progress & statistics
- If you wish to access the text content as a .txt file, simply unzip the .cw file and look for `content.txt`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
