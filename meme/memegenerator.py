"""
memegenerator.py

This module provides functionality to generate memes from images and quotes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

class MemeGenerator:
    """Class to generate memes from images and quotes."""

    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def make_meme(self, image_path, text, author):
        """Create a meme from an image, text, author, and output directory."""

        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            return None
        except OSError as error:
            print(f"An error occurred opening the image {image_path}: {error}")
            return None

        draw = ImageDraw.Draw(img)

        # Load the font
        font_path = "./path/to/your/font.ttf"  # Update this path
        try:
            font = ImageFont.truetype(font_path, size=30)
        except OSError:
            print(f"Could not load font from {font_path}. Using default font.")
            font = ImageFont.load_default()

        # Calculate text size
        #text_width, text_height = draw.textsize(text, font=font)
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top

        # Calculate positions to center the text at the bottom of the image
        width, height = img.size
        x_pos = (width - text_width) / 2
        y_pos = height - text_height - 20  # Add some padding

        # Draw the text on the image
        draw.text((x_pos, y_pos), text, font=font, fill=(255, 255, 255))

        # Handle author
        #author_width, author_height = draw.textsize(author, font=font)
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        author_width = right - left
        author_height = bottom - top

        x_author_pos = (width - author_width) / 2
        y_author_pos = height - author_height - 5
        draw.text((x_author_pos, y_author_pos), author, font=font, fill=(255, 255, 255))

        # Save the meme
        meme_path = os.path.join(self.output_dir,
                                  f"{os.path.basename(image_path).split('.')[0]}_meme.jpg")
        img.save(meme_path)

        print(f"Meme created successfully: {meme_path}")
        return meme_path
