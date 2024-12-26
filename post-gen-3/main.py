import os
from tkinter import Tk, Label, Button, Scale, Entry, StringVar, filedialog, Toplevel, Canvas, HORIZONTAL, VERTICAL, IntVar, OptionMenu, colorchooser, Text, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter

class FacebookPostGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Post Generator")
        self.root.configure(padx=10, pady=10)

        # Variable Zone
        self.input_image_path = StringVar()
        self.output_directory = StringVar(value=os.getcwd())
        self.quote_text = StringVar(value="The future belongs to those who believe in the beauty of their dreams.")
        self.signature_text = StringVar(value="Isuru Dananjaya")
        self.quote_font_path = StringVar(value="CaveatBrush-Regular.ttf")
        self.signature_font_path = StringVar(value="CaveatBrush-Regular.ttf")

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
        
        # Control Panel
        Button(root, text="Open Image", command=self.open_image).grid(row=0, column=1, sticky="w")
        Button(root, text="Output Directory", command=self.select_output_directory).grid(row=1, column=1, sticky="w")

        Label(root, text="Quote Text:").grid(row=2, column=1, sticky="nw")
        self.quote_input = Text(root, width=40, height=5, wrap="word")
        self.quote_input.insert("1.0", self.quote_text.get())
        self.quote_input.grid(row=2, column=2, sticky="w")
        self.quote_input.bind("<KeyRelease>", lambda event: self.update_quote_text())

        Label(root, text="Signature Text:").grid(row=3, column=1, sticky="w")
        Entry(root, textvariable=self.signature_text, width=40).grid(row=3, column=2, sticky="w")
        self.signature_text.trace("w", lambda *args: self.update_preview())

        Label(root, text="Quote Font Size:").grid(row=4, column=1, sticky="w")
        Scale(root, from_=10, to=100, orient=HORIZONTAL, variable=self.quote_font_size, command=self.update_preview).grid(row=4, column=2)

        Label(root, text="Signature Font Size:").grid(row=5, column=1, sticky="w")
        Scale(root, from_=10, to=50, orient=HORIZONTAL, variable=self.signature_font_size, command=self.update_preview).grid(row=5, column=2)

        Label(root, text="Left Margin:").grid(row=6, column=1, sticky="w")
        Scale(root, from_=0, to=300, orient=HORIZONTAL, variable=self.left_margin, command=self.update_preview).grid(row=6, column=2)

        Label(root, text="Right Margin:").grid(row=7, column=1, sticky="w")
        Scale(root, from_=0, to=300, orient=HORIZONTAL, variable=self.right_margin, command=self.update_preview).grid(row=7, column=2)

        Label(root, text="Top Margin:").grid(row=8, column=1, sticky="w")
        Scale(root, from_=0, to=300, orient=HORIZONTAL, variable=self.top_margin, command=self.update_preview).grid(row=8, column=2)

        Label(root, text="Bottom Margin:").grid(row=9, column=1, sticky="w")
        Scale(root, from_=0, to=300, orient=HORIZONTAL, variable=self.bottom_margin, command=self.update_preview).grid(row=9, column=2)

        Label(root, text="Quote X Position:").grid(row=10, column=1, sticky="w")
        Scale(root, from_=0, to=1080, orient=HORIZONTAL, variable=self.quote_x_position, command=self.update_preview).grid(row=10, column=2)

        Label(root, text="Quote Y Position:").grid(row=11, column=1, sticky="w")
        Scale(root, from_=0, to=1350, orient=HORIZONTAL, variable=self.quote_y_position, command=self.update_preview).grid(row=11, column=2)

        Label(root, text="Signature X Position:").grid(row=12, column=1, sticky="w")
        Scale(root, from_=0, to=1080, orient=HORIZONTAL, variable=self.signature_x_position, command=self.update_preview).grid(row=12, column=2)

        Label(root, text="Signature Y Position:").grid(row=13, column=1, sticky="w")
        Scale(root, from_=0, to=1350, orient=HORIZONTAL, variable=self.signature_y_position, command=self.update_preview).grid(row=13, column=2)

        Label(root, text="Quote Alignment Horizontal:").grid(row=14, column=1, sticky="w")
        OptionMenu(root, self.quote_align_horizontal, "left", "center", "right", command=self.update_preview).grid(row=14, column=2)

        Label(root, text="Quote Alignment Vertical:").grid(row=15, column=1, sticky="w")
        OptionMenu(root, self.quote_align_vertical, "top", "center", "bottom", command=self.update_preview).grid(row=15, column=2)

        Label(root, text="Signature Alignment Horizontal:").grid(row=16, column=1, sticky="w")
        OptionMenu(root, self.signature_align_horizontal, "left", "center", "right", command=self.update_preview).grid(row=16, column=2)

        Label(root, text="Signature Alignment Vertical:").grid(row=17, column=1, sticky="w")
        OptionMenu(root, self.signature_align_vertical, "top", "center", "bottom", command=self.update_preview).grid(row=17, column=2)

        Label(root, text="Quote Font Color:").grid(row=18, column=1, sticky="w")
        Button(root, text="Select Color", command=self.select_quote_color).grid(row=18, column=2)

        Label(root, text="Signature Font Color:").grid(row=19, column=1, sticky="w")
        Button(root, text="Select Color", command=self.select_signature_color).grid(row=19, column=2)

        Label(root, text="Background Blur Factor:").grid(row=20, column=1, sticky="w")
        Scale(root, from_=0, to=20, orient=HORIZONTAL, variable=self.background_blur_factor, command=self.update_preview).grid(row=20, column=2)

        Label(root, text="Post Width:").grid(row=22, column=1, sticky="w")
        Entry(root, textvariable=self.fb_width, width=10).grid(row=22, column=2, sticky="w")

        Label(root, text="Post Height:").grid(row=23, column=1, sticky="w")
        Entry(root, textvariable=self.fb_height, width=10).grid(row=23, column=2, sticky="w")

        Button(root, text="Generate Post", command=self.generate_post).grid(row=21, column=1, columnspan=2, pady=10)

        # Initialize variables for image preview
        self.original_image = None
        self.preview_image = None

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
        if not self.original_image:
            return

        self.quote_text.set(self.quote_input.get("1.0", "end").strip())

        fb_width, fb_height = self.fb_width.get(), self.fb_height.get()
        try:
            image = self.original_image.resize((fb_width, fb_height), Image.Resampling.LANCZOS)
        except Exception:
            messagebox.showerror("Error", "Invalid dimensions. Ensure width and height are positive integers.")
            return
        
        image = image.filter(ImageFilter.GaussianBlur(self.background_blur_factor.get()))
        draw = ImageDraw.Draw(image)

        try:
            quote_font = ImageFont.truetype(self.quote_font_path.get() or "arial.ttf", self.quote_font_size.get())
            signature_font = ImageFont.truetype(self.signature_font_path.get() or "arial.ttf", self.signature_font_size.get())
        except Exception:
            return

        # Wrap quote text to fit within margins
        quote_text_lines = self.wrap_text(draw, self.quote_text.get(), quote_font, self.left_margin.get(), self.right_margin.get(), fb_width)
        quote_y = self.quote_y_position.get()
        for line in quote_text_lines:
            text_bbox = draw.textbbox((0, 0), line, font=quote_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            quote_x = self.calculate_alignment(self.quote_align_horizontal.get(), text_width, fb_width)
            draw.text((quote_x, quote_y), line, font=quote_font, fill=self.quote_color.get())
            quote_y += text_height + 5

        text_bbox = draw.textbbox((0, 0), self.signature_text.get(), font=signature_font)
        signature_text_width = text_bbox[2] - text_bbox[0]
        signature_text_height = text_bbox[3] - text_bbox[1]
        signature_x = self.signature_x_position.get() or self.calculate_alignment(self.signature_align_horizontal.get(), signature_text_width, fb_width)
        signature_y = self.signature_y_position.get()
        draw.text((signature_x, signature_y), self.signature_text.get(), font=signature_font, fill=self.signature_color.get())

        # Scale image proportionally to fit within preview canvas
        canvas_width, canvas_height = 540, 675
        fb_width, fb_height = self.fb_width.get(), self.fb_height.get()

        scale_factor = min(canvas_width / fb_width, canvas_height / fb_height)
        scaled_width = int(fb_width * scale_factor)
        scaled_height = int(fb_height * scale_factor)

        scaled_image = image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(scaled_image)

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

    def generate_post(self):
        if not self.original_image or not self.output_directory.get():
            messagebox.showerror("Error", "Please select an image and output directory.")
            return

        fb_width, fb_height = self.fb_width.get(), self.fb_height.get()
        try:
            image = self.original_image.resize((fb_width, fb_height), Image.Resampling.LANCZOS)
        except Exception:
            messagebox.showerror("Error", "Invalid dimensions. Ensure width and height are positive integers.")
            return
        
        image = image.filter(ImageFilter.GaussianBlur(self.background_blur_factor.get()))
        draw = ImageDraw.Draw(image)

        try:
            quote_font = ImageFont.truetype(self.quote_font_path.get() or "arial.ttf", self.quote_font_size.get())
            signature_font = ImageFont.truetype(self.signature_font_path.get() or "arial.ttf", self.signature_font_size.get())
        except Exception as e:
            messagebox.showerror("Error", f"Font loading failed: {e}")
            return

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

            text_bbox = draw.textbbox((0, 0), self.signature_text.get(), font=signature_font)
            signature_text_width = text_bbox[2] - text_bbox[0]
            signature_text_height = text_bbox[3] - text_bbox[1]
            signature_x = self.signature_x_position.get() or self.calculate_alignment(self.signature_align_horizontal.get(), signature_text_width, fb_width)
            signature_y = self.signature_y_position.get()
            draw.text((signature_x, signature_y), self.signature_text.get(), font=signature_font, fill=self.signature_color.get())

            output_path = os.path.join(self.output_directory.get(), "facebook_post.jpg")
            image.save(output_path)
            messagebox.showinfo("Success", f"Post saved successfully at {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate the post: {e}")

if __name__ == "__main__":
    root = Tk()
    app = FacebookPostGenerator(root)
    root.mainloop()
