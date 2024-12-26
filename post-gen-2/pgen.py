from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Variable Zone
input_image_path = "m2.jpg"
output_image_path = "facebook_post.jpg"
quote_text = "The future belongs to those who believe in the beauty of their dreams."
signature_text = "Isuru Dananjaya"
quote_font_path = "CaveatBrush-Regular.ttf"
signature_font_path = "CaveatBrush-Regular.ttf"
quote_font_size = 40
signature_font_size = 20
left_margin = 150
right_margin = 150
top_margin = 50
bottom_margin = 50
quote_y_position = 300
signature_y_position = 1200
quote_align_horizontal = "center"
quote_align_vertical = "center"
signature_align_horizontal = "center"
signature_align_vertical = "bottom"
quote_color = "#111"
signature_color = "#111"
fb_width = 1080
fb_height = 1350
background_blur_factor = 5

def generate_facebook_post(input_image_path, output_image_path, quote_text, signature_text,
                           quote_font_path, signature_font_path, quote_font_size, signature_font_size, 
                           left_margin, right_margin, top_margin, bottom_margin, 
                           quote_y_position, signature_y_position,
                           quote_align_horizontal, quote_align_vertical,
                           signature_align_horizontal, signature_align_vertical,
                           quote_color, signature_color, fb_width, fb_height, background_blur_factor):
    image = Image.open(input_image_path).resize((fb_width, fb_height), Image.Resampling.LANCZOS)
    image = image.filter(ImageFilter.GaussianBlur(background_blur_factor))
    draw = ImageDraw.Draw(image)

    try:
        quote_font = ImageFont.truetype(quote_font_path, quote_font_size)
        signature_font = ImageFont.truetype(signature_font_path, signature_font_size)
    except Exception as e:
        print(f"Font file error: {e}")
        return

    text_width = fb_width - left_margin - right_margin
    quote_lines, line = [], ""
    for word in quote_text.split(' '):
        test_line = f"{line} {word}".strip()
        test_width = draw.textbbox((0, 0), test_line, font=quote_font)[2]
        if test_width <= text_width:
            line = test_line
        else:
            quote_lines.append(line)
            line = word
    quote_lines.append(line)

    total_text_height = len(quote_lines) * (quote_font_size + 5)
    y = (fb_height - total_text_height) // 2 if quote_align_vertical == "center" else \
        fb_height - bottom_margin - total_text_height if quote_align_vertical == "bottom" else quote_y_position

    for line in quote_lines:
        text_width_line = draw.textbbox((0, 0), line, font=quote_font)[2]
        x = (fb_width - text_width_line) // 2 if quote_align_horizontal == "center" else \
            fb_width - right_margin - text_width_line if quote_align_horizontal == "right" else left_margin
        draw.text((x, y), line, fill=quote_color, font=quote_font)
        y += quote_font_size + 5

    signature_width, signature_height = draw.textbbox((0, 0), signature_text, font=signature_font)[2:]
    signature_y = (fb_height - signature_height) // 2 if signature_align_vertical == "center" else \
                  fb_height - bottom_margin - signature_height if signature_align_vertical == "bottom" else signature_y_position
    signature_x = (fb_width - signature_width) // 2 if signature_align_horizontal == "center" else \
                  fb_width - right_margin - signature_width if signature_align_horizontal == "right" else left_margin

    draw.text((signature_x, signature_y), signature_text, fill=signature_color, font=signature_font)
    image.save(output_image_path)
    print(f"Image saved to {output_image_path}")

generate_facebook_post(input_image_path, output_image_path, quote_text, signature_text,
                       quote_font_path, signature_font_path, quote_font_size, signature_font_size, 
                       left_margin, right_margin, top_margin, bottom_margin, 
                       quote_y_position, signature_y_position,
                       quote_align_horizontal, quote_align_vertical,
                       signature_align_horizontal, signature_align_vertical,
                       quote_color, signature_color, fb_width, fb_height, background_blur_factor)
