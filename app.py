import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

text_contents = dict()

def create_file(content="", title="Untitled"):
    container = ttk.Frame(notebook)
    container.pack()

    text_area = tk.Text(container) # creates a text widget inside the container frame
    text_area.insert("end", content) # if there is content, i.e. via the open_file function inserts it
    text_area.pack(side="left", fill="both", expand=True) # filling the left space
    
    notebook.add(container, text=title) # adds a tab to the notebook, linking it to the container
    notebook.select(container)

    text_contents[str(text_area)] = hash(content) # hashing the contents (to a shorter length to allow comparison for unsaved changes)

    text_scroll = ttk.Scrollbar(container, orient="vertical", command=text_area.yview) # putting the ScrollBar in the container Frame, vertical orientation and setting it to scroll the y vertical view
    text_scroll.pack(side="right", fill="y")
    text_area["yscrollcommand"] = text_scroll.set


def check_for_changes():
    current = get_text_widget() # get the currently selected text widget

    content = current.get("1.0", "end-1c") # get current's content
    name = notebook.tab("current")["text"] # get current tab's label

    if hash(content) != text_contents[str(current)]:
        if name[-1] != "*":
            notebook.tab("current", text=name + "*") # if the hashes between original and new are different, adds a * to the end
    elif name[-1] == "*": # if contents are the same and there is a * at the end need to remove it
        notebook.tab("current", text=name[:-1]) 


def get_current_tab():
    return notebook.nametowidget(notebook.select())


def get_text_widget():
    current_tab = get_current_tab()
    text_widget = current_tab.winfo_children()[0] # needed due to the container frame then inside it is the text_area element

    return text_widget


def current_tab_unsaved():
    text_widget = get_text_widget()
    content = text_widget.get("1.0", "end-1c")

    return hash(content) != text_contents[str(text_widget)] # returns true if hash of content is different to that saved, i.e. unsaved changes


def confirm_close():
    return messagebox.askyesno(
        message="you have unsaved changes, are you sure you want to close this tab?",
        icon="question",
        title="Unsaved changes"
    )


def close_current_tab():
    if current_tab_unsaved() and not confirm_close(): # is unsaved and confirm close is no, close current tab
        return

    current= get_current_tab()
    
    if len(notebook.tabs()) == 1:
        create_file() # if there is only 1 tab opep, creating a new one so that when we forget below it still looks okay
    
    notebook.forget(current) # closes current tab in all other situations


def confirm_quit():
    unsaved = False

    # cycling through all tabs, getting the content and comparing the hashes, if any are different means unsaved changes are present
    for tab in notebook.tabs():
        tab_widget = root.nametowidget(tab)
        text_widget = tab_widget.winfo_children()[0] 
        content = text_widget.get("1.0", "end-1c")

        if hash(content) != text_contents[str(text_widget)]:
            unsaved = True
            break
        
    if unsaved and not confirm_close(): 
        return # if they don't confirm, return i.e. don't quit the program
    
    root.destroy() # if they do confirm, ends the app


def save_file():
    file_path = filedialog.asksaveasfilename() # asks user where to save (opens windows options)
    # e.g. /Users/paul/file.txt

    try:
        filename = os.path.basename(file_path) # above e.g. gives you file.txt
        text_widget = get_text_widget() # selects the current notebook textfield, to get the content below

        content = text_widget.get("1.0", "end-1c") # selects all content from the text_widget, removing the last character (which would be a \n)

        with open(file_path, "w") as file:
            file.write(content) #opens full file path in writing mode, writing all the contents from the text_widget
    
    except (AttributeError, FileNotFoundError):
        print(f' save operation unsuccessful')
        return

    notebook.tab("current", text=filename) # renames current tab to the filename e.g. file.txt

    text_contents[str(text_widget)] = hash(content)


def open_file():
    file_path = filedialog.askopenfilename()

    try:
        filename = os.path.basename(file_path) # above e.g. gives you file.txt
            
        with open(file_path, "r") as file:
            content = file.read() # read the file contents
    
    except (AttributeError, FileNotFoundError):
        print(f' open operation unsuccessful')
        return

    create_file(content, filename) # creating a new file / tab with the file contents


def show_about_info():
    messagebox.showinfo(
        title = "About",
        message="This application is a simple text editor which allows you to create, edit and save mulitple tabs / files"
    )


root = tk.Tk()
root.title("Text Editor")
root.option_add("*tearOff", False) # disables tear-off feature for menus (where it could be torn off into a separate window)

# configuring main frame

main = ttk.Frame(root)
main.pack(fill="both", expand=True, padx=8, pady=8)

# creating and configuring menu bar

menubar = tk.Menu()
root.config(menu=menubar) 

# creating the notebook widget and packing it into the main frame
notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

# dropdown of menu elements

file_menu = tk.Menu(menubar)
help_menu = tk.Menu(menubar)
menubar.add_cascade(menu=file_menu, label="File") # creating Menu dropdown button
menubar.add_cascade(menu=help_menu, label="Help")

help_menu.add_command(label="About", command=show_about_info)

file_menu.add_command(label="New", command=create_file, accelerator="Ctrl+N") # option in the menu dropdown, calling the create_file function
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O") # option in the menu dropdown, calling the open_file function
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S") # option in the menu dropdown, calling the save_file function
file_menu.add_command(label="Close tab", command=close_current_tab, accelerator = "Ctrl+Q")
file_menu.add_command(label="Exit", command=confirm_quit)

create_file()

root.bind("<KeyPress>", lambda event: check_for_changes())
root.bind("<Control-n>", lambda event: create_file()) # binding shortcut to the root window, linking the shortcut to the create_file function
# above we are defining a function, NOT calling it
root.bind("<Control-o>", lambda event: open_file()) # binding shortcut to the root window, linking the shortcut to the create_file function
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-q>", lambda event: close_current_tab())


root.mainloop()
