import os
import json
from PIL import Image
from db_helper import save_template, load_templates

def ensure_default_template():
    """Ensure the default template exists."""
    templates_dir = "templates"
    if os.path.exists(os.path.join(templates_dir, "difault")):
        default_template_dir = os.path.join(templates_dir, "difault")
    else:
        default_template_dir = os.path.join(templates_dir, "default_template")

    # Check if the directory and database entry for the default template exist
    if not os.path.exists(default_template_dir):
        os.makedirs(default_template_dir, exist_ok=True)

        # Save a blank placeholder image for the default template
        placeholder_image_path = os.path.join(default_template_dir, "./tempimg1.jpg")
        if not os.path.exists(placeholder_image_path):
            Image.new("RGB", (1080, 1350), "white").save(placeholder_image_path)

        # Define default settings
        default_settings = {
            "quote_text": "This is the default template quote.",
            "signature_text": "Default Signature",
            "quote_font_path": "CaveatBrush-Regular.ttf",  # Default font path
            "signature_font_path": "CaveatBrush-Regular.ttf",
            "quote_font_size": 40,
            "signature_font_size": 20,
            "fb_width": 1080,
            "fb_height": 1350,
            "background_blur_factor": 5,
            "left_margin": 150,
            "right_margin": 150,
            "top_margin": 50,
            "bottom_margin": 50,
            "quote_x_position": 0,
            "quote_y_position": 300,
            "signature_x_position": 0,
            "signature_y_position": 1200,
            "quote_align_horizontal": "center",
            "quote_align_vertical": "center",
            "signature_align_horizontal": "center",
            "signature_align_vertical": "bottom",
            "quote_color": "#111111",
            "signature_color": "#111111",
        }

        # Save template to database
        save_template(
            "default",  # Template ID
            "Default Template",  # Template name
            json.dumps(default_settings),  # Settings as JSON
            placeholder_image_path  # Background image path
        )

    else:
        # If directory exists, ensure it's registered in the database
        placeholder_image_path = os.path.join(default_template_dir, "./tempimg1.jpg")
        templates = load_templates()
        if not any(template[0] == "default" for template in templates):
            default_settings = {
                "quote_text": "This is the default template quote.",
                "signature_text": "Default Signature",
                "quote_font_path": "CaveatBrush-Regular.ttf",  # Default font path
                "signature_font_path": "CaveatBrush-Regular.ttf",
                "quote_font_size": 40,
                "signature_font_size": 20,
                "fb_width": 1080,
                "fb_height": 1350,
                "background_blur_factor": 5,
                "left_margin": 150,
                "right_margin": 150,
                "top_margin": 50,
                "bottom_margin": 50,
                "quote_x_position": 0,
                "quote_y_position": 300,
                "signature_x_position": 0,
                "signature_y_position": 1200,
                "quote_align_horizontal": "center",
                "quote_align_vertical": "center",
                "signature_align_horizontal": "center",
                "signature_align_vertical": "bottom",
                "quote_color": "#111111",
                "signature_color": "#111111",
            }

            save_template(
                "default",  # Template ID
                "Default Template",  # Template name
                json.dumps(default_settings),  # Settings as JSON
                placeholder_image_path  # Background image path
            )

# Define the reset_environment method
def reset_environment(app):
    """Reset the app to load the default template."""
    app.load_selected_template("Default Template")