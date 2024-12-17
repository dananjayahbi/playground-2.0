from PIL import Image, ImageDraw, ImageFont

def generate_facebook_post(input_image_path, output_image_path, quote_text, signature_text,
                           quote_font_path, signature_font_path, quote_font_size, signature_font_size, 
                           left_margin, right_margin, top_margin, bottom_margin, 
                           quote_y_position, signature_y_position,
                           quote_align_horizontal, quote_align_vertical,
                           signature_align_horizontal, signature_align_vertical,
                           quote_color, signature_color):
    """
    Generates a Facebook post with a cropped image, quote, and signature.

    Parameters:
    - input_image_path (str): Path to the input image file.
    - output_image_path (str): Path to save the output image.
    - quote_text (str): The quote to display on the image.
    - signature_text (str): The signature to display at the bottom.
    - quote_font_path (str): Path to the .ttf font file for the quote.
    - signature_font_path (str): Path to the .ttf font file for the signature.
    - quote_font_size (int): Font size for the quote text.
    - signature_font_size (int): Font size for the signature text.
    - left_margin (int): Left margin for the text.
    - right_margin (int): Right margin for the text.
    - top_margin (int): Top margin for the text.
    - bottom_margin (int): Bottom margin for the text.
    - quote_y_position (int): Y-coordinate of the quote text.
    - signature_y_position (int): Y-coordinate of the signature.
    - quote_align_horizontal (str): Horizontal alignment for the quote ('left', 'center', 'right').
    - quote_align_vertical (str): Vertical alignment for the quote ('top', 'center', 'bottom').
    - signature_align_horizontal (str): Horizontal alignment for the signature ('left', 'center', 'right').
    - signature_align_vertical (str): Vertical alignment for the signature ('top', 'center', 'bottom').
    - quote_color (str): Color of the quote text.
    - signature_color (str): Color of the signature text.
    """
    # Step 1: Open the image
    image = Image.open(input_image_path)
    
    # Step 2: Resize (crop) the image to Facebook's standard post size: 1080x1350
    fb_width, fb_height = 1080, 1350
    image = image.resize((fb_width, fb_height), Image.Resampling.LANCZOS)
    
    # Step 3: Prepare to draw on the image
    draw = ImageDraw.Draw(image)
    
    # Load fonts
    try:
        quote_font = ImageFont.truetype(quote_font_path, quote_font_size)
        signature_font = ImageFont.truetype(signature_font_path, signature_font_size)
    except Exception as e:
        print(f"Font file not found or invalid: {e}")
        return

    # Step 4: Align and Draw the Quote
    text_width = fb_width - left_margin - right_margin
    quote_lines = []
    words = quote_text.split(' ')
    line = ""

    # Wrap text manually
    for word in words:
        test_line = f"{line} {word}".strip()
        text_bbox = draw.textbbox((0, 0), test_line, font=quote_font)
        test_width = text_bbox[2] - text_bbox[0]
        
        if test_width <= text_width:
            line = test_line
        else:
            quote_lines.append(line)
            line = word
    quote_lines.append(line)

    # Calculate vertical alignment for the quote
    total_text_height = len(quote_lines) * (quote_font_size + 5)
    if quote_align_vertical == "center":
        y = (fb_height - total_text_height) // 2
    elif quote_align_vertical == "bottom":
        y = fb_height - bottom_margin - total_text_height
    else:  # Default is "top"
        y = quote_y_position

    # Draw each line of the quote
    for line in quote_lines:
        text_bbox = draw.textbbox((0, 0), line, font=quote_font)
        text_width_line = text_bbox[2] - text_bbox[0]

        if quote_align_horizontal == "center":
            x = (fb_width - text_width_line) // 2
        elif quote_align_horizontal == "right":
            x = fb_width - right_margin - text_width_line
        else:  # Default is "left"
            x = left_margin
        
        draw.text((x, y), line, fill=quote_color, font=quote_font)
        y += quote_font_size + 5  # Line spacing

    # Step 5: Align and Draw the Signature
    signature_bbox = draw.textbbox((0, 0), signature_text, font=signature_font)
    signature_width = signature_bbox[2] - signature_bbox[0]
    signature_height = signature_bbox[3] - signature_bbox[1]

    if signature_align_vertical == "center":
        signature_y = (fb_height - signature_height) // 2
    elif signature_align_vertical == "bottom":
        signature_y = fb_height - bottom_margin - signature_height
    else:  # Default is "top"
        signature_y = signature_y_position

    if signature_align_horizontal == "center":
        signature_x = (fb_width - signature_width) // 2
    elif signature_align_horizontal == "right":
        signature_x = fb_width - right_margin - signature_width
    else:  # Default is "left"
        signature_x = left_margin

    draw.text((signature_x, signature_y), signature_text, fill=signature_color, font=signature_font)

    # Step 6: Save the output image
    image.save(output_image_path)
    print(f"Image saved to {output_image_path}")


# Example usage:
if __name__ == "__main__":
    # Define parameters
    input_image_path = "m1.jpg"  # Path to your input image
    output_image_path = "facebook_post.jpg"  # Output path
    quote_text = "The future belongs to those who believe in the beauty of their dreams."
    signature_text = "Isuru Dananjaya"
    quote_font_path = "arial.ttf"  # Path to the .ttf font file for the quote
    signature_font_path = "PlaywriteMXGuides-Regular.ttf"  # Path to the .ttf font file for the signature
    
    # Adjustable parameters
    quote_font_size = 40
    signature_font_size = 20
    left_margin = 50
    right_margin = 50
    top_margin = 50
    bottom_margin = 50
    quote_y_position = 300
    signature_y_position = 1200

    # Alignment parameters
    quote_align_horizontal = "center"  # Options: 'left', 'center', 'right'
    quote_align_vertical = "center"    # Options: 'top', 'center', 'bottom'
    signature_align_horizontal = "center"  # Options: 'left', 'center', 'right'
    signature_align_vertical = "bottom"    # Options: 'top', 'center', 'bottom'

    # Color parameters
    quote_color = "grey"
    signature_color = "yellow"

    # Generate the Facebook post
    generate_facebook_post(input_image_path, output_image_path, quote_text, signature_text,
                           quote_font_path, signature_font_path, quote_font_size, signature_font_size, 
                           left_margin, right_margin, top_margin, bottom_margin, 
                           quote_y_position, signature_y_position,
                           quote_align_horizontal, quote_align_vertical,
                           signature_align_horizontal, signature_align_vertical,
                           quote_color, signature_color)
