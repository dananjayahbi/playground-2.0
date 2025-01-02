import os
import pandas as pd
from tkinter import Tk, StringVar, messagebox, Text, Menu
from ttkbootstrap import Style, ttk
import pyperclip
import textwrap

# Constants
ROOT_FOLDER = os.getcwd()
DATA_FOLDER = os.path.join(ROOT_FOLDER, "data")
FILES = {
    "facts.csv": ["Fact", "Used"],
    "quotes.csv": ["Quote", "Used"],
    "quotes_with_author.csv": ["Quote", "Used"]
}

# Ensure data folder and files exist
os.makedirs(DATA_FOLDER, exist_ok=True)
for filename, columns in FILES.items():
    filepath = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(filepath):
        pd.DataFrame(columns=columns).to_csv(filepath, index=False)

class CSVEditorApp:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme="superhero")
        self.root.title("CSV Editor")
        self.root.state('zoomed')  # Maximize window

        self.selected_file = None
        self.show_used = False  # Default to showing unused texts

        # GUI Setup
        self.file_selection_frame = ttk.Frame(root, padding=10)
        self.file_selection_frame.pack(fill="x", pady=5)

        self.file_label = ttk.Label(self.file_selection_frame, text="Select a file:")
        self.file_label.pack(side="left", padx=5)

        self.file_combobox = ttk.Combobox(
            self.file_selection_frame, values=list(FILES.keys()), state="readonly"
        )
        self.file_combobox.pack(side="left", fill="x", expand=True, padx=5)
        self.file_combobox.bind("<<ComboboxSelected>>", self.display_data)

        self.toggle_button = ttk.Checkbutton(
            self.file_selection_frame,
            text="Show Used",
            style="TButton",
            command=self.toggle_used_texts,
        )
        self.toggle_button.pack(side="left", padx=10)

        self.tree_frame = ttk.Frame(root, padding=10)
        self.tree_frame.pack(fill="both", expand=True, pady=5)

        self.tree = ttk.Treeview(self.tree_frame, show="headings", height=30, selectmode="extended")  # Enable multiple selection
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)  # Bind double-click to copy

        # Add context menu for right-click
        self.create_context_menu()

        self.input_frame = ttk.Frame(root, padding=10)
        self.input_frame.pack(fill="x", pady=5)

        self.input_label = ttk.Label(self.input_frame, text="Enter value:")
        self.input_label.pack(side="left", padx=5)

        self.input_var = StringVar()
        self.input_entry = ttk.Entry(self.input_frame, textvariable=self.input_var)
        self.input_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.input_entry.bind("<Shift-Return>", self.add_entry)
        self.input_entry.bind("<Return>", self.add_entry)

        self.add_button = ttk.Button(
            self.input_frame, text="Add", command=self.add_entry
        )
        self.add_button.pack(side="left", padx=5)

        self.delete_button = ttk.Button(
            self.input_frame, text="Delete Selected", command=self.delete_selected_rows
        )
        self.delete_button.pack(side="left", padx=5)

        self.mark_used_button = ttk.Button(
            self.input_frame, text="Mark as Used", command=self.mark_as_used
        )
        self.mark_used_button.pack(side="left", padx=5)

    def truncate_text(self, text, max_length=50):
        """Truncate text to fit within the column width, adding '...' if necessary."""
        return textwrap.shorten(text, width=max_length, placeholder="...")

    def toggle_used_texts(self):
        """Toggle between showing used and unused texts."""
        self.show_used = not self.show_used
        if self.show_used:
            self.toggle_button.config(text="Show Unused")
        else:
            self.toggle_button.config(text="Show Used")
        self.display_data()

    def display_data(self, event=None):
        """Display all rows of the selected CSV file in a grid with truncated text."""
        selected_file = self.file_combobox.get()
        if selected_file:
            self.selected_file = selected_file  # Ensure selected_file is updated
            filepath = os.path.join(DATA_FOLDER, selected_file)
            data = pd.read_csv(filepath)

            # Filter rows based on the toggle state
            if self.show_used:
                data = data[data["Used"] == True]  # Show only used rows
            else:
                data = data[data["Used"] != True]  # Show only unused rows

            # Clear existing data in Treeview
            self.tree.delete(*self.tree.get_children())

            # Set up Treeview columns
            self.tree["columns"] = ["#"] + list(data.columns) + ["Actions"]
            self.tree.column("#", minwidth=30, width=30, stretch=False, anchor="center")  # Narrow "#" column
            self.tree.column("Actions", anchor="center", width=100)  # Center align "Actions" column

            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)

            # Populate Treeview with data
            for i, row in data.iterrows():
                row_values = []
                for col, value in zip(data.columns, row):
                    truncated_value = self.truncate_text(str(value), max_length=50)  # Adjust max_length as needed
                    row_values.append(truncated_value)
                # Add "#" column and "Actions" column
                values = [i + 1] + row_values + ["Copy"]
                self.tree.insert("", "end", values=values)

    def add_entry(self, event=None):
        """Add a new entry to the selected CSV file."""
        if not self.selected_file:
            return

        filepath = os.path.join(DATA_FOLDER, self.selected_file)
        columns = FILES[self.selected_file]

        # Use raw input without splitting it into multiple columns
        new_entry = [self.input_var.get(), False]  # Treat the entire input as one value, with "Used" as False
        
        # Add the new row to the CSV
        try:
            data = pd.read_csv(filepath)
            new_row = pd.DataFrame([new_entry], columns=columns)
            data = pd.concat([data, new_row], ignore_index=True)
            data.to_csv(filepath, index=False)
            self.input_var.set("")  # Clear the input field
            self.display_data()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while adding the entry: {e}")

    def delete_selected_rows(self):
        """Delete the selected rows from the Treeview and the CSV file."""
        if not self.selected_file:
            messagebox.showwarning("Warning", "No file selected!")
            return

        selected_items = self.tree.selection()  # Get all selected items
        if not selected_items:
            messagebox.showwarning("Warning", "No rows selected!")
            return

        filepath = os.path.join(DATA_FOLDER, self.selected_file)
        data = pd.read_csv(filepath)

        # Remove rows corresponding to selected items
        indexes_to_remove = [int(self.tree.item(item, "values")[0]) - 1 for item in selected_items]
        data = data.drop(indexes_to_remove).reset_index(drop=True)

        # Save updated CSV and refresh Treeview
        data.to_csv(filepath, index=False)
        self.display_data()

    def mark_as_used(self):
        """Mark the selected rows as 'Used' in the CSV file."""
        if not self.selected_file:
            messagebox.showwarning("Warning", "No file selected!")
            return

        selected_items = self.tree.selection()  # Get all selected items
        if not selected_items:
            messagebox.showwarning("Warning", "No rows selected!")
            return

        filepath = os.path.join(DATA_FOLDER, self.selected_file)
        data = pd.read_csv(filepath)

        # Update the "Used" column for the selected rows
        indexes_to_update = [int(self.tree.item(item, "values")[0]) - 1 for item in selected_items]
        data.loc[indexes_to_update, "Used"] = True

        # Save updated CSV and refresh Treeview
        data.to_csv(filepath, index=False)
        self.display_data()

    def create_context_menu(self):
        """Create a context menu for viewing full text."""
        self.context_menu = Menu(self.root, tearoff=0)  # Use tkinter.Menu
        self.context_menu.add_command(label="View Full Text", command=self.view_full_text)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        """Show the context menu at the cursor position."""
        try:
            self.selected_item = self.tree.identify_row(event.y)
            self.selected_column = self.tree.identify_column(event.x)
            if self.selected_item and self.selected_column:
                self.context_menu.post(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def view_full_text(self):
        """Show the full text of the selected cell in a popup."""
        if not self.selected_item or not self.selected_column:
            messagebox.showwarning("Warning", "No cell selected!")
            return

        col_index = int(self.selected_column.replace("#", "")) - 1  # Convert column to index
        row_data = self.tree.item(self.selected_item, "values")
        if col_index < 0 or col_index >= len(row_data):
            return

        full_text = row_data[col_index]  # Get the full text of the clicked cell

        # Show the full text in a popup window
        popup = Tk()
        popup.title("Full Text Viewer")
        popup.geometry("400x300")

        text_widget = Text(popup, wrap="word", padx=10, pady=10)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", full_text)  # Insert the full text
        text_widget.config(state="disabled")  # Make it read-only

        close_button = ttk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

        popup.mainloop()

    def on_double_click(self, event):
        """Handle double-click events to copy data, excluding '#' and 'Actions' columns."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "No row selected!")
            return
        row_data = self.tree.item(selected_item, "values")
        # Exclude the first ('#') and last ('Actions') columns
        text = ", ".join(map(str, row_data[1:-1]))
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Row copied to clipboard!")

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = CSVEditorApp(root)
    root.mainloop()
