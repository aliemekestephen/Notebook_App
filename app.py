import os.path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

text_contents = dict()


def create_file(content="", title="Untitled"):
    container = ttk.Frame(notebook)  # for the scrollbar
    container.pack()

    text_area = tk.Text(container)
    text_area.insert("end", content)  # adds an empty content
    text_area.pack(side="left", fill="both", expand=True)

    notebook.add(container, text=title)
    notebook.select(container)  # selects the new tab

    text_contents[str(text_area)] = hash(content)  # adds the hashed content into a dictionary

    text_scroll = ttk.Scrollbar(container, orient="vertical", command=text_area.yview)
    text_scroll.pack(side="right", fill="y")
    text_area["yscrollcommand"] = text_scroll.set


#  checks for changes in the text and adds * to the tab if unsaved
def check_for_changes():
    current = get_text_widget()
    content = current.get("1.0", "end-1c")
    name = notebook.tab("current")["text"]

    if hash(content) != text_contents[str(current)]:
        if name[-1] != "*":
            notebook.tab("current", text=name + "*")
    elif name[-1] == "*":
        notebook.tab("current", text=name[:-1])


# selects the currently active tab
def get_text_widget():
    tab_widget = window.nametowidget(notebook.select())
    text_widget = tab_widget.winfo_children()[0]  # selects both children of the frame and selects the text area
    return text_widget


def close_current_tab():
    current = get_text_widget()
    if current_tab_unsaved() and not confirm_close():
        return

    if len(notebook.tabs()) == 1:  # check the number of tab and keeps one always
        create_file()

    notebook.forget(current)


def current_tab_unsaved():
    text_widget = get_text_widget()
    content = text_widget.get("1.0", "end-1c")
    return hash(content) != text_contents[str(text_widget)]


def confirm_close():
    return messagebox.askyesno(
        message="You have unsaved messages, do you want to close Tab?",
        icon="question",
        title="Unsaved Changes"
    )


def confirm_exit():
    unsaved = False

    for tab in notebook.tabs():
        tab_widget = window.nametowidget(tab)
        text_widget = tab_widget.winfo_children()[0]
        content = text_widget.get("1.0", "end-1c")

        if hash(content) != text_contents[str(text_widget)]:
            unsaved = True
            break

    if unsaved and not confirm_close():
        return

    window.destroy()


def save_file():
    file_path = filedialog.asksaveasfilename()

    try:
        filename = os.path.basename(file_path)
        text_widget = get_text_widget()  # selects the currently active tab
        content = text_widget.get("1.0", "end-1c")  # selects the content of the current text area

        with open(file_path, "w") as file:
            file.write(content)  # saves the file
    except (AttributeError, FileNotFoundError):
        print("Save operation cancelled")
        return

    notebook.tab("current", text=filename)  # renames the untitled tab to the current file name
    text_contents[str(text_widget)] = hash(content)


def open_file():
    file_path = filedialog.askopenfilename()

    try:
        filename = os.path.basename(file_path)

        with open(file_path, "r") as file:
            content = file.read()

    except (AttributeError, FileNotFoundError):
        print("Open operation cancelled")
        return

    create_file(content, filename)
    if content == "" and filename == "Untitled": # to make sure an opened file replaces the empty tab
        pass


def show_about_info():
    messagebox.showinfo(
        title="About",
        message="St. Stephen Editor is a simple tabbed text editor that demonstrates my experience with Tkinter"
    )


window = tk.Tk()  # creates the window
window.title("St. Stephen Editor")
window.option_add("*tearOff", False)

main = ttk.Frame(window)
main.pack(fill="both", expand=True, padx=1, pady=(4, 0))

menubar = tk.Menu()  # creates a menubar
window.config(menu=menubar)

file_menu = tk.Menu(menubar)  # add a tab/cascade in the menubar
help_menu = tk.Menu(menubar)

menubar.add_cascade(menu=file_menu, label="File")
menubar.add_cascade(menu=help_menu, label="Help")

file_menu.add_command(label="New", command=create_file, accelerator="ctrl+N")  # add a command to the tab/cascade
file_menu.add_command(label="Open...", command=open_file, accelerator="ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="ctrl+S")
file_menu.add_command(label="Close Tab", command=close_current_tab, accelerator="ctrl+Q")
file_menu.add_command(label="Exit", command=confirm_exit)

help_menu.add_command(label="About", command=show_about_info)


notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)
create_file()

window.bind("<KeyPress>", lambda event: check_for_changes()) # binds the short cut to the active window
window.bind("<Control-n>", lambda event: create_file())
window.bind("<Control-o>", lambda event: open_file())
window.bind("<Control-q>", lambda event: close_current_tab())
window.bind("<Control-s>", lambda event: save_file())

window.mainloop()
