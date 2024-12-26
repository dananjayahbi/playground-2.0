import tkinter as tk
from tkinter import ttk, font, colorchooser

def create_rich_text_editor(parent, font_family="Arial", font_size=12):
    current_font_family = font_family
    current_font_size = font_size
    font_family_var = tk.StringVar(value=current_font_family)
    font_size_var = tk.IntVar(value=current_font_size)

    frame = ttk.Frame(parent)

    def apply_bold():
        current_tags = text_widget.tag_names("sel.first")
        if "bold" in current_tags:
            text_widget.tag_remove("bold", "sel.first", "sel.last")
        else:
            text_widget.tag_add("bold", "sel.first", "sel.last")
            text_widget.tag_config("bold", font=(current_font_family, current_font_size, "bold"))

    def apply_italic():
        current_tags = text_widget.tag_names("sel.first")
        if "italic" in current_tags:
            text_widget.tag_remove("italic", "sel.first", "sel.last")
        else:
            text_widget.tag_add("italic", "sel.first", "sel.last")
            text_widget.tag_config("italic", font=(current_font_family, current_font_size, "italic"))

    def change_font_family(event=None):
        nonlocal current_font_family
        current_font_family = font_family_var.get()
        text_widget.config(font=(current_font_family, current_font_size))

    def change_font_size(event=None):
        nonlocal current_font_size
        current_font_size = font_size_var.get()
        text_widget.config(font=(current_font_family, current_font_size))

    def change_text_color():
        color = colorchooser.askcolor()[1]
        if color:
            text_widget.tag_add("colored", "sel.first", "sel.last")
            text_widget.tag_config("colored", foreground=color)

    # Toolbar
    toolbar = ttk.Frame(frame)
    toolbar.pack(side="top", fill="x")

    font_families = list(font.families())
    font_family_combo = ttk.Combobox(toolbar, textvariable=font_family_var, values=font_families, width=20)
    font_family_combo.bind("<<ComboboxSelected>>", change_font_family)
    font_family_combo.pack(side="left", padx=5)

    font_size_combo = ttk.Combobox(toolbar, textvariable=font_size_var, values=list(range(8, 72)), width=5)
    font_size_combo.bind("<<ComboboxSelected>>", change_font_size)
    font_size_combo.pack(side="left", padx=5)

    bold_button = ttk.Button(toolbar, text="Bold", command=apply_bold)
    bold_button.pack(side="left", padx=5)

    italic_button = ttk.Button(toolbar, text="Italic", command=apply_italic)
    italic_button.pack(side="left", padx=5)

    color_button = ttk.Button(toolbar, text="Text Color", command=change_text_color)
    color_button.pack(side="left", padx=5)

    text_widget = tk.Text(frame, wrap="word", font=(current_font_family, current_font_size))
    text_widget.pack(expand=1, fill="both")

    return frame, text_widget