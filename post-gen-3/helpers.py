def create_labeled_input(root, text, var, row, column, min_val, max_val, step, update_callback):
    from tkinter import Button, Entry, Label, Frame

    def increment():
        if var.get() < max_val:
            var.set(var.get() + step)
            update_callback()

    def decrement():
        if var.get() > min_val:
            var.set(var.get() - step)
            update_callback()

    def on_key_press(event):
        if event.keysym == "Up":
            increment()
        elif event.keysym == "Down":
            decrement()

    # Add label
    Label(root, text=text).grid(row=row, column=column, sticky="w")

    # Create a frame to hold increment, input box, and decrement together
    frame = Frame(root)
    frame.grid(row=row, column=column + 1, columnspan=3, sticky="w")

    # Add buttons and input inside the frame
    Button(frame, text="-", command=decrement, width=2).pack(side="left")
    entry = Entry(frame, textvariable=var, width=5, justify="center")
    entry.pack(side="left", padx=5)

    # Bind keypress events to the entry widget
    entry.bind("<Up>", lambda event: increment())
    entry.bind("<Down>", lambda event: decrement())

    Button(frame, text="+", command=increment, width=2).pack(side="left")
