# GUI file interface

This project created a GUI interface for file opening / editing and saving across multiple tabs

## Usage / key functions

```python
def create_file(content, title):
    Creates a new file and packs it into the container, hashing it's contents to allow comparison to check for unsaved changes


def check_for_changes():
    Compares the hashed saved file to the current, adding an "*" to the filename if there are unsaved changes


def save_file():
    Uses filedialogue.asksaveasfilename() to allow users to choose where to save the file and how to name it etc


def open_file():
    Uses filedialogue.asksopenfilename() to allow users to choose where to open the file they wish to work on


def confirm_quit():
    Allows the user to quit the program, along with a warning message to the user if there are unsaved changes

```

## Notes
- This was a practice project on utilising GUI's with Python to enable a more fluid user experience when interacting with our program
- The goal was to provide a functional, practical program to enable easy usability and program flow.
