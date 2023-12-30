import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

text_contents = dict()

def create_file(content="", title="Untitled"):
    container = ttk.Frame(notebook)
    container.pack()

    text_area = tk.Text(container)
    text_area.insert("end", content)
    text_area.pack(side="left", fill="both", expand=True)
    
    notebook.add(container, text=title)
    notebook.select(container)


# hashing the contents (to a shorter length to allow comparison for unsaved changes)
    text_contents[str(text_area)] = hash(content)

    text_scroll = ttk.Scrollbar(container, orient="vertical", command=text_area.yview)
    text_scroll.pack(side="right", fill="y")
    text_area["yscrollcommand"] = text_scroll.set


def check_for_changes():
    current = get_text_widget()

    content = current.get("1.0", "end-1c") 
    name = notebook.tab("current")["text"]

    if hash(content) != text_contents[str(current)]:
        if name[-1] != "*":
            notebook.tab("current", text=name + "*") # if the hashes between original and new are different, adds a * to the end
    elif name[-1] == "*": # if contents are the same and there is a * at the end, need to remove it
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
    if current_tab_unsaved() and not confirm_close():
        return

    current= get_current_tab()
    
    if len(notebook.tabs()) == 1:
        create_file() #
    
    notebook.forget(current)


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
        return
    
    root.destroy()


def save_file():
    file_path = filedialog.asksaveasfilename()

    try:
        filename = os.path.basename(file_path) 
        text_widget = get_text_widget()

        content = text_widget.get("1.0", "end-1c")

        with open(file_path, "w") as file:
            file.write(content)
    
    except (AttributeError, FileNotFoundError):
        print(f' save operation unsuccessful')
        return

    notebook.tab("current", text=filename)

    text_contents[str(text_widget)] = hash(content)


def open_file():
    file_path = filedialog.askopenfilename()

    try:
        filename = os.path.basename(file_path)
            
        with open(file_path, "r") as file:
            content = file.read()
    
    except (AttributeError, FileNotFoundError):
        print(f' open operation unsuccessful')
        return

    create_file(content, filename)


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
menubar.add_cascade(menu=file_menu, label="File")
menubar.add_cascade(menu=help_menu, label="Help")

help_menu.add_command(label="About", command=show_about_info)

file_menu.add_command(label="New", command=create_file, accelerator="Ctrl+N") 
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O") 
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S") 
file_menu.add_command(label="Close tab", command=close_current_tab, accelerator = "Ctrl+Q")
file_menu.add_command(label="Exit", command=confirm_quit)

create_file()

root.bind("<KeyPress>", lambda event: check_for_changes())
root.bind("<Control-n>", lambda event: create_file()) 
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-q>", lambda event: close_current_tab())


root.mainloop()
