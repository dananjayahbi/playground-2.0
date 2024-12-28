import os
import uuid
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, Canvas, IntVar, OptionMenu, colorchooser, Text, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter
from helpers import create_labeled_input
from db_helper import ensure_default_directory, load_default_settings, save_default_settings

FONTS_DIR = "fonts"
POSTS_DIR = "posts"

if not os.path.exists(FONTS_DIR):
    os.makedirs(FONTS_DIR)

if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)


class FacebookPostGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Post Generator")
        self.root.configure(padx=10, pady=10)

        # Initialize variables for image preview
        self.original_image = None
        self.preview_image = None

        # Variable Zone
        self.input_image_path = StringVar()
        self.output_directory = StringVar(value=os.getcwd())
        self.quote_text = StringVar(value="The future belongs to those who believe in the beauty of their dreams.") # Default quote text
        self.signature_text = StringVar(value="Isuru Dananjaya")
        self.quote_font_path = StringVar(value="CaveatBrush-Regular.ttf") #default quote font
        self.quote_font_path.trace("w", lambda *args: self.update_preview())
        self.signature_font_path = StringVar(value="CaveatBrush-Regular.ttf") #default signature font
        self.signature_font_path.trace("w", lambda *args: self.update_preview())

        # Ensure fonts folder exists and load available fonts
        if not os.path.exists(FONTS_DIR):
            os.makedirs(FONTS_DIR)
        self.available_fonts = self.load_fonts()

        self.quote_font_size = IntVar(value=40)
        self.signature_font_size = IntVar(value=20)
        self.left_margin = IntVar(value=150)
        self.right_margin = IntVar(value=150)
        self.top_margin = IntVar(value=50)
        self.bottom_margin = IntVar(value=50)
        self.quote_y_position = IntVar(value=300)
        self.signature_y_position = IntVar(value=1200)
        self.quote_x_position = IntVar(value=0)
        self.signature_x_position = IntVar(value=0)
        self.quote_align_horizontal = StringVar(value="center")
        self.quote_align_vertical = StringVar(value="center")
        self.signature_align_horizontal = StringVar(value="center")
        self.signature_align_vertical = StringVar(value="bottom")
        self.quote_color = StringVar(value="#111")
        self.signature_color = StringVar(value="#111")
        self.fb_width = IntVar(value=1080)
        self.fb_width.trace("w", lambda *args: self.update_preview())  # Bind updates to preview
        self.fb_height = IntVar(value=1350)
        self.fb_height.trace("w", lambda *args: self.update_preview())  # Bind updates to preview
        self.background_blur_factor = IntVar(value=5)

        # Preview Canvas
        self.canvas = Canvas(root, width=540, height=675)
        self.canvas.grid(row=0, column=0, rowspan=20, padx=10, pady=10)

        # Initialize `quote_input` before applying default settings
        Label(root, text="Quote Text:").grid(row=4, column=1, sticky="nw")
        self.quote_input = Text(root, width=40, height=5, wrap="word")
        self.quote_input.insert("1.0", self.quote_text.get())
        self.quote_input.grid(row=4, column=2, sticky="w")
        self.quote_input.bind("<KeyRelease>", lambda event: self.update_quote_text())
        self.quote_input.bind("<Shift-Return>", self.prevent_newline_and_generate)

        # Ensure default settings
        ensure_default_directory()
        self.default_settings = load_default_settings()
        self.apply_default_settings()
        
        # Control Panel
        Button(root, text="Open Image", command=self.open_image).grid(row=0, column=1, sticky="w")
        Button(root, text="Output Directory", command=self.select_output_directory).grid(row=0, column=3, sticky="w")

        # Font Upload Section
        Button(self.root, text="Upload Font", command=self.upload_font).grid(row=0, column=5, sticky="w")

        # Add Update Default button
        Button(root, text="Update Default", command=self.update_default).grid(row=1, column=1)

        Label(root, text="Post Width:").grid(row=2, column=1, sticky="w")
        create_labeled_input(root, "Post Width:", self.fb_width, 2, 1, 1, 1080, 1, self.update_preview)

        Label(root, text="Post Height:").grid(row=3, column=1, sticky="w")
        create_labeled_input(root, "Post Height:", self.fb_height, 3, 1, 1, 1350, 1, self.update_preview)

        Label(root, text="Signature Text:").grid(row=5, column=1, sticky="w", pady=(5, 0))
        Entry(root, textvariable=self.signature_text, width=40).grid(row=5, column=2, sticky="w", pady=(5, 0))
        self.signature_text.trace("w", lambda *args: self.update_preview())

        # Font Selection Section
        Label(self.root, text="Quote Font:").grid(row=6, column=1, sticky="w")
        self.quote_font_menu = OptionMenu(self.root, self.quote_font_path, *self.available_fonts, command=lambda _: self.update_preview())
        self.quote_font_menu.grid(row=6, column=2, sticky="w")

        Label(self.root, text="Signature Font:").grid(row=7, column=1, sticky="w")
        self.signature_font_menu = OptionMenu(self.root, self.signature_font_path, *self.available_fonts, command=lambda _: self.update_preview())
        self.signature_font_menu.grid(row=7, column=2, sticky="w")

        Label(root, text="Quote Font Size:").grid(row=8, column=1, sticky="w")
        create_labeled_input(root, "Quote Font Size:", self.quote_font_size, 8, 1, 10, 100, 1, self.update_preview)

        Label(root, text="Signature Font Size:").grid(row=9, column=1, sticky="w")
        create_labeled_input(root, "Signature Font Size:", self.signature_font_size, 9, 1, 10, 50, 1, self.update_preview)

        Label(root, text="Quote Font Color:").grid(row=10, column=1, sticky="w", pady=(5, 0))
        Button(root, text="Select Color", command=self.select_quote_color).grid(row=10, column=2, pady=(5, 0))

        Label(root, text="Signature Font Color:").grid(row=11, column=1, sticky="w", pady=(5, 0))
        Button(root, text="Select Color", command=self.select_signature_color).grid(row=11, column=2, pady=(5, 0))

        Label(root, text="Background Blur Factor:").grid(row=12, column=1, sticky="w")
        create_labeled_input(root, "Background Blur Factor:", self.background_blur_factor, 12, 1, 0, 20, 1, self.update_preview)

        Label(root, text="Quote Alignment Horizontal:").grid(row=13, column=1, sticky="w")
        OptionMenu(root, self.quote_align_horizontal, "left", "center", "right", command=self.update_preview).grid(row=13, column=2)

        Label(root, text="Quote Alignment Vertical:").grid(row=14, column=1, sticky="w")
        OptionMenu(root, self.quote_align_vertical, "top", "center", "bottom", command=self.update_preview).grid(row=14, column=2)

        Label(root, text="Signature Alignment Horizontal:").grid(row=15, column=1, sticky="w")
        OptionMenu(root, self.signature_align_horizontal, "left", "center", "right", command=self.update_preview).grid(row=15, column=2)

        Label(root, text="Signature Alignment Vertical:").grid(row=16, column=1, sticky="w")
        OptionMenu(root, self.signature_align_vertical, "top", "center", "bottom", command=self.update_preview).grid(row=16, column=2)

        Label(root, text="Left Margin:").grid(row=2, column=4, sticky="w")
        create_labeled_input(root, "Left Margin:", self.left_margin, 2, 4, 0, 300, 1, self.update_preview)

        Label(root, text="Right Margin:").grid(row=3, column=4, sticky="w")
        create_labeled_input(root, "Right Margin:", self.right_margin, 3, 4, 0, 300, 1, self.update_preview)

        Label(root, text="Top Margin:").grid(row=4, column=4, sticky="w")
        create_labeled_input(root, "Top Margin:", self.top_margin, 4, 4, 0, 300, 1, self.update_preview)

        Label(root, text="Bottom Margin:").grid(row=5, column=4, sticky="w")
        create_labeled_input(root, "Bottom Margin:", self.bottom_margin, 5, 4, 0, 300, 1, self.update_preview)

        Label(root, text="Quote X Position:").grid(row=6, column=4, sticky="w")
        create_labeled_input(root, "Quote X Position:", self.quote_x_position, 6, 4, 0, 1080, 1, self.update_preview)

        Label(root, text="Quote Y Position:").grid(row=7, column=4, sticky="w")
        create_labeled_input(root, "Quote Y Position:", self.quote_y_position, 7, 4, 0, 1350, 1, self.update_preview)

        Label(root, text="Signature X Position:").grid(row=8, column=4, sticky="w")
        create_labeled_input(root, "Signature X Position:", self.signature_x_position, 8, 4, 0, 1080, 1, self.update_preview)

        Label(root, text="Signature Y Position:").grid(row=9, column=4, sticky="w")
        create_labeled_input(root, "Signature Y Position:", self.signature_y_position, 9, 4, 0, 1350, 1, self.update_preview)

        Button(root, text="Generate Post", command=self.generate_post).grid(row=18, column=2, columnspan=2, pady=10)

    def upload_font(self):
        font_file = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf")])
        if font_file:
            try:
                font_name = os.path.basename(font_file)
                destination = os.path.join(FONTS_DIR, font_name)
                with open(font_file, "rb") as source, open(destination, "wb") as dest:
                    dest.write(source.read())
                messagebox.showinfo("Success", f"Font {font_name} uploaded successfully!")
                
                # Refresh the available fonts and update the menus
                self.available_fonts = self.load_fonts()
                self.update_font_menus()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload font: {e}")

    def load_fonts(self):
        return [f for f in os.listdir(FONTS_DIR) if f.endswith(".ttf")]
    
    def update_font_menus(self):
        """Update the font selection menus dynamically."""
        # Update Quote Font OptionMenu
        menu = self.quote_font_menu["menu"]
        menu.delete(0, "end")  # Clear the existing menu items
        for font in self.available_fonts:
            menu.add_command(label=font, command=lambda value=font: self.set_font(self.quote_font_path, value))

        # Update Signature Font OptionMenu
        menu = self.signature_font_menu["menu"]
        menu.delete(0, "end")  # Clear the existing menu items
        for font in self.available_fonts:
            menu.add_command(label=font, command=lambda value=font: self.set_font(self.signature_font_path, value))

    def set_font(self, font_variable, font_value):
        font_variable.set(font_value)
        self.update_preview()  # Update the preview when font changes

    def open_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if filepath:
            self.input_image_path.set(filepath)
            self.original_image = Image.open(filepath)
            self.update_preview()

    def select_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory.set(directory)

    def select_quote_color(self):
        color_code = colorchooser.askcolor(title="Select Quote Color")[1]
        if color_code:
            self.quote_color.set(color_code)
            self.update_preview()

    def select_signature_color(self):
        color_code = colorchooser.askcolor(title="Select Signature Color")[1]
        if color_code:
            self.signature_color.set(color_code)
            self.update_preview()

    def update_quote_text(self):
        self.quote_text.set(self.quote_input.get("1.0", "end").strip())
        self.update_preview()

    def update_preview(self, *args):
        """Update the preview canvas with the current settings."""
        if not self.original_image:
            return

        # Update the quote text from the input field
        self.quote_text.set(self.quote_input.get("1.0", "end").strip())

        # Get Facebook post dimensions
        fb_width, fb_height = self.fb_width.get(), self.fb_height.get()
        try:
            # Resize the original image to match the target dimensions
            image = self.original_image.resize((fb_width, fb_height), Image.Resampling.LANCZOS)
        except Exception:
            messagebox.showerror("Error", "Invalid dimensions. Ensure width and height are positive integers.")
            return

        # Apply background blur
        image = image.filter(ImageFilter.GaussianBlur(self.background_blur_factor.get()))
        draw = ImageDraw.Draw(image)

        # Load the selected fonts
        try:
            quote_font_path = os.path.join(FONTS_DIR, self.quote_font_path.get())
            signature_font_path = os.path.join(FONTS_DIR, self.signature_font_path.get())
            quote_font = ImageFont.truetype(quote_font_path, self.quote_font_size.get())
            signature_font = ImageFont.truetype(signature_font_path, self.signature_font_size.get())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load fonts: {e}")
            return

        # Wrap the quote text to fit within the defined margins
        quote_text_lines = self.wrap_text(draw, self.quote_text.get(), quote_font, self.left_margin.get(), self.right_margin.get(), fb_width)
        quote_y = self.quote_y_position.get()
        for line in quote_text_lines:
            text_bbox = draw.textbbox((0, 0), line, font=quote_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            quote_x = self.calculate_alignment(self.quote_align_horizontal.get(), text_width, fb_width)
            draw.text((quote_x, quote_y), line, font=quote_font, fill=self.quote_color.get())
            quote_y += text_height + 5

        # Draw the signature text
        text_bbox = draw.textbbox((0, 0), self.signature_text.get(), font=signature_font)
        signature_text_width = text_bbox[2] - text_bbox[0]
        signature_text_height = text_bbox[3] - text_bbox[1]
        signature_x = self.signature_x_position.get() or self.calculate_alignment(self.signature_align_horizontal.get(), signature_text_width, fb_width)
        signature_y = self.signature_y_position.get()
        draw.text((signature_x, signature_y), self.signature_text.get(), font=signature_font, fill=self.signature_color.get())

        # Scale the image proportionally to fit the preview canvas
        canvas_width, canvas_height = 540, 675
        scale_factor = min(canvas_width / fb_width, canvas_height / fb_height)
        scaled_width = int(fb_width * scale_factor)
        scaled_height = int(fb_height * scale_factor)

        scaled_image = image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(scaled_image)

        # Clear the canvas and display the updated image
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width // 2, canvas_height // 2,
            image=self.preview_image,
            anchor="center"
        )

    def wrap_text(self, draw, text, font, left_margin, right_margin, width):
        words = text.split()
        lines, line = [], ""
        max_width = width - left_margin - right_margin
        for word in words:
            test_line = f"{line} {word}".strip()
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            test_width = text_bbox[2] - text_bbox[0]
            if test_width <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
        return lines

    def calculate_alignment(self, alignment, text_width, container_width):
        if alignment == "center":
            return (container_width - text_width) // 2
        elif alignment == "right":
            return container_width - text_width
        return 0
    
    def apply_default_settings(self):
        """Apply settings from the default JSON file."""
        settings = self.default_settings

        # Set dimensions
        self.fb_width.set(settings.get("fb_width", 1080))
        self.fb_height.set(settings.get("fb_height", 1350))

        # Set text values
        self.quote_text.set(settings.get("quote_text", "The future belongs to those who believe in the beauty of their dreams."))
        self.signature_text.set(settings.get("signature_text", "Isuru Dananjaya"))

        # Set colors
        self.quote_color.set(settings.get("quote_color", "#111"))
        self.signature_color.set(settings.get("signature_color", "#111"))

        # Set font paths
        self.quote_font_path.set(settings.get("quote_font_path", "CaveatBrush-Regular.ttf"))
        self.signature_font_path.set(settings.get("signature_font_path", "CaveatBrush-Regular.ttf"))

        # Set font sizes
        self.quote_font_size.set(settings.get("quote_font_size", 40))
        self.signature_font_size.set(settings.get("signature_font_size", 20))

        # Set margins
        self.left_margin.set(settings.get("left_margin", 150))
        self.right_margin.set(settings.get("right_margin", 150))
        self.top_margin.set(settings.get("top_margin", 50))
        self.bottom_margin.set(settings.get("bottom_margin", 50))

        # Set positions
        self.quote_x_position.set(settings.get("quote_x_position", 0))
        self.quote_y_position.set(settings.get("quote_y_position", 300))
        self.signature_x_position.set(settings.get("signature_x_position", 0))
        self.signature_y_position.set(settings.get("signature_y_position", 1200))

        # Set alignments
        self.quote_align_horizontal.set(settings.get("quote_align_horizontal", "center"))
        self.quote_align_vertical.set(settings.get("quote_align_vertical", "center"))
        self.signature_align_horizontal.set(settings.get("signature_align_horizontal", "center"))
        self.signature_align_vertical.set(settings.get("signature_align_vertical", "bottom"))

        # Set blur factor
        self.background_blur_factor.set(settings.get("background_blur_factor", 5))

        # Load the background image path
        background_image_path = settings.get("background_image", "")
        if os.path.exists(background_image_path):
            self.input_image_path.set(background_image_path)
            self.original_image = Image.open(background_image_path)
        else:
            self.input_image_path.set("")
            self.original_image = None

        # Populate the input fields
        self.quote_input.delete("1.0", "end")
        self.quote_input.insert("1.0", self.quote_text.get())
        self.update_preview()

    def update_default(self):
        """Save current settings and background as the default."""
        current_settings = {
            "fb_width": self.fb_width.get(),
            "fb_height": self.fb_height.get(),
            "quote_text": self.quote_input.get("1.0", "end").strip(),
            "signature_text": self.signature_text.get(),
            "quote_color": self.quote_color.get(),
            "signature_color": self.signature_color.get(),
            "quote_font_path": self.quote_font_path.get(),
            "signature_font_path": self.signature_font_path.get(),
            "quote_font_size": self.quote_font_size.get(),
            "signature_font_size": self.signature_font_size.get(),
            "left_margin": self.left_margin.get(),
            "right_margin": self.right_margin.get(),
            "top_margin": self.top_margin.get(),
            "bottom_margin": self.bottom_margin.get(),
            "quote_x_position": self.quote_x_position.get(),
            "quote_y_position": self.quote_y_position.get(),
            "signature_x_position": self.signature_x_position.get(),
            "signature_y_position": self.signature_y_position.get(),
            "quote_align_horizontal": self.quote_align_horizontal.get(),
            "quote_align_vertical": self.quote_align_vertical.get(),
            "signature_align_horizontal": self.signature_align_horizontal.get(),
            "signature_align_vertical": self.signature_align_vertical.get(),
            "background_image": self.input_image_path.get(),
            "background_blur_factor": self.background_blur_factor.get()
        }
        background_image_path = self.input_image_path.get()
        save_default_settings(current_settings, background_image_path)
        messagebox.showinfo("Success", "Default settings updated successfully!")

    def prevent_newline_and_generate(self, event=None):
        """Prevent newline on Shift+Enter and trigger silent post generation."""
        self.silent_generate_post()
        return "break"  # Prevent further processing of the keypress

    def generate_post(self):
        if not self.original_image:
            messagebox.showerror("Error", "Please select an image.")
            return

        if not os.path.exists(POSTS_DIR):
            os.makedirs(POSTS_DIR)

        fb_width, fb_height = self.fb_width.get(), self.fb_height.get()
        try:
            # Resize image to fit Facebook post dimensions
            image = self.original_image.resize((fb_width, fb_height), Image.Resampling.LANCZOS)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid dimensions: {e}")
            return

        # Apply background blur
        image = image.filter(ImageFilter.GaussianBlur(self.background_blur_factor.get()))
        draw = ImageDraw.Draw(image)

        # Load fonts
        try:
            quote_font_path = os.path.join(FONTS_DIR, self.quote_font_path.get())
            signature_font_path = os.path.join(FONTS_DIR, self.signature_font_path.get())
            quote_font = ImageFont.truetype(quote_font_path, self.quote_font_size.get())
            signature_font = ImageFont.truetype(signature_font_path, self.signature_font_size.get())
        except Exception as e:
            messagebox.showerror("Error", f"Font loading failed: {e}")
            return

        # Draw quote text
        try:
            quote_text_lines = self.wrap_text(draw, self.quote_text.get(), quote_font, self.left_margin.get(), self.right_margin.get(), fb_width)
            quote_y = self.quote_y_position.get()
            for line in quote_text_lines:
                text_bbox = draw.textbbox((0, 0), line, font=quote_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                quote_x = self.calculate_alignment(self.quote_align_horizontal.get(), text_width, fb_width)
                draw.text((quote_x, quote_y), line, font=quote_font, fill=self.quote_color.get())
                quote_y += text_height + 5
        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw quote text: {e}")
            return

        # Draw signature text
        try:
            text_bbox = draw.textbbox((0, 0), self.signature_text.get(), font=signature_font)
            signature_text_width = text_bbox[2] - text_bbox[0]
            signature_text_height = text_bbox[3] - text_bbox[1]
            signature_x = self.signature_x_position.get() or self.calculate_alignment(self.signature_align_horizontal.get(), signature_text_width, fb_width)
            signature_y = self.signature_y_position.get()
            draw.text((signature_x, signature_y), self.signature_text.get(), font=signature_font, fill=self.signature_color.get())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw signature text: {e}")
            return

        # Save the generated post with a unique filename
        try:
            unique_id = uuid.uuid4().hex
            output_path = os.path.join(POSTS_DIR, f"facebook_post_{unique_id}.jpg")
            image.save(output_path)
            messagebox.showinfo("Success", f"Post saved successfully at {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the post: {e}")

    def silent_generate_post(self, event=None):
        """Generate the post silently without showing the success message."""
        if not self.original_image:
            messagebox.showerror("Error", "Please select an image.")
            return

        if not os.path.exists(POSTS_DIR):
            os.makedirs(POSTS_DIR)

        fb_width, fb_height = self.fb_width.get(), self.fb_height.get()
        try:
            # Resize image to fit Facebook post dimensions
            image = self.original_image.resize((fb_width, fb_height), Image.Resampling.LANCZOS)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid dimensions: {e}")
            return

        # Apply background blur
        image = image.filter(ImageFilter.GaussianBlur(self.background_blur_factor.get()))
        draw = ImageDraw.Draw(image)

        # Load fonts
        try:
            quote_font_path = os.path.join(FONTS_DIR, self.quote_font_path.get())
            signature_font_path = os.path.join(FONTS_DIR, self.signature_font_path.get())
            quote_font = ImageFont.truetype(quote_font_path, self.quote_font_size.get())
            signature_font = ImageFont.truetype(signature_font_path, self.signature_font_size.get())
        except Exception as e:
            messagebox.showerror("Error", f"Font loading failed: {e}")
            return

        # Draw quote text
        try:
            quote_text_lines = self.wrap_text(draw, self.quote_text.get(), quote_font, self.left_margin.get(), self.right_margin.get(), fb_width)
            quote_y = self.quote_y_position.get()
            for line in quote_text_lines:
                text_bbox = draw.textbbox((0, 0), line, font=quote_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                quote_x = self.calculate_alignment(self.quote_align_horizontal.get(), text_width, fb_width)
                draw.text((quote_x, quote_y), line, font=quote_font, fill=self.quote_color.get())
                quote_y += text_height + 5
        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw quote text: {e}")
            return

        # Draw signature text
        try:
            text_bbox = draw.textbbox((0, 0), self.signature_text.get(), font=signature_font)
            signature_text_width = text_bbox[2] - text_bbox[0]
            signature_text_height = text_bbox[3] - text_bbox[1]
            signature_x = self.signature_x_position.get() or self.calculate_alignment(self.signature_align_horizontal.get(), signature_text_width, fb_width)
            signature_y = self.signature_y_position.get()
            draw.text((signature_x, signature_y), self.signature_text.get(), font=signature_font, fill=self.signature_color.get())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw signature text: {e}")
            return

        # Save the generated post with a unique filename
        try:
            unique_id = uuid.uuid4().hex
            output_path = os.path.join(POSTS_DIR, f"facebook_post_{unique_id}.jpg")
            image.save(output_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the post: {e}")

if __name__ == "__main__":
    root = Tk()
    app = FacebookPostGenerator(root)
    root.mainloop()
