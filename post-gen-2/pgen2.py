import os
from tkinter import Tk, Label, Button, Scale, Entry, StringVar, filedialog, Toplevel, Canvas, HORIZONTAL, VERTICAL, IntVar
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter

class FacebookPostGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Post Generator")

        # Variable Zone
        self.input_image_path = StringVar()
        self.output_directory = StringVar()
        self.quote_text = StringVar(value="The future belongs to those who believe in the beauty of their dreams.")
        self.signature_text = StringVar(value="Isuru Dananjaya")
        self.quote_font_path = StringVar()
        self.signature_font_path = StringVar()

        self.quote_font_size = IntVar(value=40)
        self.signature_font_size = IntVar(value=20)
        self.left_margin = IntVar(value=150)
        self.right_margin = IntVar(value=150)
        self.top_margin = IntVar(value=50)
        self.bottom_margin = IntVar(value=50)
        self.quote_y_position = IntVar(value=300)
        self.signature_y_position = IntVar(value=1200)
        self.quote_color = StringVar(value="#111")
        self.signature_color = StringVar(value="#111")
        self.fb_width = IntVar(value=1080)
        self.fb_height = IntVar(value=1350)
        self.background_blur_factor = IntVar(value=5)

        # Preview Canvas
        self.canvas = Canvas(root, width=540, height=675)
        self.canvas.grid(row=0, column=0, rowspan=15, padx=10, pady=10)
        
        # Control Panel
        Button(root, text="Open Image", command=self.open_image).grid(row=0, column=1, sticky="w")
        Button(root, text="Output Directory", command=self.select_output_directory).grid(row=1, column=1, sticky="w")

        Label(root, text="Quote Text:").grid(row=2, column=1, sticky="w")
        Entry(root, textvariable=self.quote_text, width=40).grid(row=2, column=2, sticky="w")

        Label(root, text="Signature Text:").grid(row=3, column=1, sticky="w")
        Entry(root, textvariable=self.signature_text, width=40).grid(row=3, column=2, sticky="w")

        Label(root, text="Quote Font Size:").grid(row=4, column=1, sticky="w")
        Scale(root, from_=10, to=100, orient=HORIZONTAL, variable=self.quote_font_size, command=self.update_preview).grid(row=4, column=2)

        Label(root, text="Signature Font Size:").grid(row=5, column=1, sticky="w")
        Scale(root, from_=10, to=50, orient=HORIZONTAL, variable=self.signature_font_size, command=self.update_preview).grid(row=5, column=2)

        Label(root, text="Background Blur Factor:").grid(row=6, column=1, sticky="w")
        Scale(root, from_=0, to=20, orient=HORIZONTAL, variable=self.background_blur_factor, command=self.update_preview).grid(row=6, column=2)

        Button(root, text="Generate Post", command=self.generate_post).grid(row=7, column=1, columnspan=2, pady=10)

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

    def update_preview(self, *args):
        if not self.original_image:
            return

        # Generate preview image
        fb_width, fb_height = self.fb_width.get(), self.fb_height.get()
        image = self.original_image.resize((fb_width, fb_height), Image.Resampling.LANCZOS)
        image = image.filter(ImageFilter.GaussianBlur(self.background_blur_factor.get()))
        draw = ImageDraw.Draw(image)

        try:
            quote_font = ImageFont.truetype(self.quote_font_path.get() or "arial.ttf", self.quote_font_size.get())
            signature_font = ImageFont.truetype(self.signature_font_path.get() or "arial.ttf", self.signature_font_size.get())
        except Exception:
            return

        draw.text((self.left_margin.get(), self.quote_y_position.get()), self.quote_text.get(), font=quote_font, fill=self.quote_color.get())
        draw.text((self.left_margin.get(), self.signature_y_position.get()), self.signature_text.get(), font=signature_font, fill=self.signature_color.get())

        self.preview_image = ImageTk.PhotoImage(image.resize((540, 675), Image.Resampling.LANCZOS))
        self.canvas.create_image(0, 0, image=self.preview_image, anchor="nw")

    def generate_post(self):
        if not self.original_image or not self.output_directory.get():
            return

        fb_width, fb_height = self.fb_width.get(), self.fb_height.get()
        image = self.original_image.resize((fb_width, fb_height), Image.Resampling.LANCZOS)
        image = image.filter(ImageFilter.GaussianBlur(self.background_blur_factor.get()))
        draw = ImageDraw.Draw(image)

        try:
            quote_font = ImageFont.truetype(self.quote_font_path.get() or "arial.ttf", self.quote_font_size.get())
            signature_font = ImageFont.truetype(self.signature_font_path.get() or "arial.ttf", self.signature_font_size.get())
        except Exception:
            return

        draw.text((self.left_margin.get(), self.quote_y_position.get()), self.quote_text.get(), font=quote_font, fill=self.quote_color.get())
        draw.text((self.left_margin.get(), self.signature_y_position.get()), self.signature_text.get(), font=signature_font, fill=self.signature_color.get())

        output_path = os.path.join(self.output_directory.get(), "facebook_post.jpg")
        image.save(output_path)
        print(f"Post saved at {output_path}")

if __name__ == "__main__":
    root = Tk()
    app = FacebookPostGenerator(root)
    root.mainloop()
