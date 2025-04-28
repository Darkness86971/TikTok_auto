#!/usr/bin/env python3
"""
Image Text Overlay Tool for TikTok Content Automation
This script adds motivational quotes to images with proper styling and positioning.
"""

import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

class TextOverlay:
    def __init__(self, font_path=None, output_dir="output"):
        """Initialize the text overlay tool with font path and output directory."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Try to use a good font for motivational quotes
        if font_path and os.path.exists(font_path):
            self.font_path = font_path
        else:
            # Default system fonts that should be available
            system_fonts = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
                "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
            ]
            
            for font in system_fonts:
                if os.path.exists(font):
                    self.font_path = font
                    break
            else:
                raise FileNotFoundError("No suitable font found. Please provide a valid font path.")
    
    def add_text_to_image(self, image_path, text, output_filename=None):
        """Add text to an image with proper styling and positioning."""
        try:
            # Open the image
            img = Image.open(image_path).convert("RGBA")
            
            # Create a copy for processing
            img_with_text = img.copy()
            
            # Get image dimensions
            width, height = img.size
            
            # Create a semi-transparent overlay to improve text readability
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Add a gradient shadow in the center for better text visibility
            for i in range(100):
                # Draw a rectangle with decreasing transparency from center
                alpha = int(100 - i)  # Decreasing alpha value
                draw.rectangle(
                    [width/2 - width/2 * (1 - i/100), 
                     height/2 - height/2 * (1 - i/100),
                     width/2 + width/2 * (1 - i/100), 
                     height/2 + height/2 * (1 - i/100)],
                    fill=(0, 0, 0, alpha)
                )
            
            # Apply the overlay
            img_with_text = Image.alpha_composite(img_with_text, overlay)
            
            # Prepare to draw text
            draw = ImageDraw.Draw(img_with_text)
            
            # Calculate font size based on image dimensions
            font_size = int(width / 15)  # Adjust this ratio as needed
            font = ImageFont.truetype(self.font_path, font_size)
            
            # Wrap text to fit width
            margin = 20
            max_width = width - 2 * margin
            wrapped_text = self.wrap_text(text, font, max_width)
            
            # Calculate text position (center)
            text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2
            
            # Add white text with black outline for better visibility
            self.draw_text_with_outline(draw, (text_x, text_y), wrapped_text, font, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
            
            # Convert back to RGB for saving as JPG
            img_with_text = img_with_text.convert("RGB")
            
            # Generate output filename if not provided
            if not output_filename:
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_filename = os.path.join(self.output_dir, f"{base_name}_quote.jpg")
            
            # Save the image
            img_with_text.save(output_filename, quality=95)
            print(f"Created: {output_filename}")
            
            return output_filename
            
        except Exception as e:
            print(f"Error adding text to image: {e}")
            return None
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a given width."""
        words = text.split()
        wrapped_lines = []
        current_line = []
        
        for word in words:
            # Try adding the word to the current line
            test_line = ' '.join(current_line + [word])
            text_bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), test_line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            
            if text_width <= max_width:
                # Word fits, add it to the current line
                current_line.append(word)
            else:
                # Word doesn't fit, start a new line
                if current_line:
                    wrapped_lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line
        if current_line:
            wrapped_lines.append(' '.join(current_line))
        
        return '\n'.join(wrapped_lines)
    
    def draw_text_with_outline(self, draw, position, text, font, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), outline_width=2):
        """Draw text with an outline for better visibility."""
        x, y = position
        
        # Draw the outline
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x == 0 and offset_y == 0:
                    continue  # Skip the center (will be drawn later)
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=outline)
        
        # Draw the main text
        draw.text((x, y), text, font=font, fill=fill)
    
    def process_random_quote(self, image_path, quotes_file, output_filename=None):
        """Select a random quote from a file and add it to an image."""
        try:
            with open(quotes_file, 'r') as f:
                quotes = f.read().splitlines()
            
            # Filter out empty lines
            quotes = [q for q in quotes if q.strip()]
            
            if not quotes:
                print("No quotes found in the file.")
                return None
            
            # Select a random quote
            quote = random.choice(quotes)
            
            # Add the quote to the image
            return self.add_text_to_image(image_path, quote, output_filename)
            
        except Exception as e:
            print(f"Error processing random quote: {e}")
            return None

def main():
    """Main function to demonstrate the text overlay tool."""
    # Example usage
    overlay_tool = TextOverlay(output_dir="/home/ubuntu/tiktok_automation/output")
    
    # Test with a sample image if available
    image_dir = "/home/ubuntu/tiktok_automation/images"
    quotes_file = "/home/ubuntu/tiktok_automation/quotes/quotes.txt"
    
    # Create a sample image if none exists
    if not os.listdir(image_dir):
        print("No images found. Creating a sample image for testing...")
        sample_img = Image.new('RGB', (1080, 1920), color=(20, 20, 30))
        sample_img_path = os.path.join(image_dir, "sample_dark_bg.jpg")
        sample_img.save(sample_img_path)
        
        # Process the sample image
        overlay_tool.process_random_quote(sample_img_path, quotes_file)
    else:
        # Process the first image found
        for filename in os.listdir(image_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(image_dir, filename)
                overlay_tool.process_random_quote(image_path, quotes_file)
                break

if __name__ == "__main__":
    main()
