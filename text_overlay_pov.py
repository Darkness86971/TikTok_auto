#!/usr/bin/env python3
"""
POV-Style Image Text Overlay Tool for TikTok Content Automation (Center Aligned)
This script adds "POV" and motivational quotes to images with styling matching the example,
using center alignment and attempting to find a suitable font.
"""

import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

class POVTextOverlay:
    def __init__(self, font_path=None, output_dir="output"):
        """Initialize the text overlay tool with font path and output directory."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Attempt to find Comic Sans or use a fallback
        comic_sans_paths = [
            "/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS.ttf",
            "/usr/share/fonts/truetype/comic/comic.ttf" # Common location if installed manually
        ]
        
        found_font = None
        if font_path and os.path.exists(font_path):
            found_font = font_path
        else:
            for path in comic_sans_paths:
                if os.path.exists(path):
                    found_font = path
                    print(f"Using Comic Sans font found at: {found_font}")
                    break
        
        if not found_font:
            # Default system fonts if Comic Sans is not found
            print("Comic Sans font not found. Using default system font.")
            system_fonts = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
                "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
            ]
            for font in system_fonts:
                if os.path.exists(font):
                    found_font = font
                    print(f"Using fallback font: {found_font}")
                    break
            else:
                raise FileNotFoundError("No suitable font found. Please provide a valid font path or install Comic Sans.")
        
        self.font_path = found_font
    
    def add_pov_text_to_image(self, image_path, quote_text, output_filename=None):
        """Add POV and quote text to an image with center alignment."""
        try:
            # Open the image
            img = Image.open(image_path).convert("RGBA")
            
            # Create a copy for processing
            img_with_text = img.copy()
            
            # Get image dimensions
            width, height = img.size
            
            # Create a semi-transparent overlay to improve text readability
            overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Add a gradient shadow in the center for better text visibility
            for i in range(100):
                alpha = int(100 - i)
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
            
            # Calculate font sizes
            pov_font_size = int(width / 12)
            quote_font_size = int(width / 18)
            
            pov_font = ImageFont.truetype(self.font_path, pov_font_size)
            quote_font = ImageFont.truetype(self.font_path, quote_font_size)
            
            # POV text
            pov_text = "POV"
            pov_bbox = draw.textbbox((0, 0), pov_text, font=pov_font)
            pov_width = pov_bbox[2] - pov_bbox[0]
            pov_height = pov_bbox[3] - pov_bbox[1]
            
            # Position POV text at the top center
            pov_x = (width - pov_width) // 2
            pov_y = int(height * 0.35)
            
            # Wrap quote text
            margin = 40
            max_width = width - 2 * margin
            wrapped_quote = self.wrap_text(quote_text, quote_font, max_width)
            
            # Calculate quote text position (centered)
            # Use textbbox with align="center" for accurate multi-line height
            quote_bbox = draw.textbbox((0, 0), wrapped_quote, font=quote_font, align="center")
            quote_width = quote_bbox[2] - quote_bbox[0]
            quote_height = quote_bbox[3] - quote_bbox[1]
            
            # Position quote text below POV, centered horizontally
            quote_x = (width - quote_width) // 2
            quote_y = pov_y + pov_height + int(height * 0.05)
            
            # Add white text with black outline, using center alignment for the quote
            self.draw_text_with_outline(draw, (pov_x, pov_y), pov_text, pov_font, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), align="center")
            self.draw_text_with_outline(draw, (quote_x, quote_y), wrapped_quote, quote_font, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), align="center")
            
            # Convert back to RGB for saving as JPG
            img_with_text = img_with_text.convert("RGB")
            
            # Generate output filename
            if not output_filename:
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_filename = os.path.join(self.output_dir, f"{base_name}_pov_quote_centered.jpg")
            
            # Save the image
            img_with_text.save(output_filename, quality=95)
            print(f"Created: {output_filename}")
            
            return output_filename
            
        except Exception as e:
            print(f"Error adding centered POV text to image: {e}")
            return None
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a given width."""
        lines = textwrap.wrap(text, width=int(max_width / (font.size * 0.5))) # Estimate characters per line
        return '\n'.join(lines)
    
    def draw_text_with_outline(self, draw, position, text, font, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), outline_width=2, align="left"):
        """Draw text with an outline for better visibility, supporting alignment."""
        x, y = position
        
        # Draw the outline
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=outline, align=align)
        
        # Draw the main text
        draw.text((x, y), text, font=font, fill=fill, align=align)
    
    def process_random_quote(self, image_path, quotes_file, output_filename=None):
        """Select a random quote and add it to an image with centered POV style."""
        try:
            with open(quotes_file, "r") as f:
                quotes = [q.strip() for q in f.read().splitlines() if q.strip()]
            
            if not quotes:
                print("No quotes found in the file.")
                return None
            
            quote = random.choice(quotes)
            return self.add_pov_text_to_image(image_path, quote, output_filename)
            
        except Exception as e:
            print(f"Error processing random quote: {e}")
            return None

def main():
    """Main function to demonstrate the centered POV text overlay tool."""
    overlay_tool = POVTextOverlay(output_dir="/home/ubuntu/tiktok_automation/output")
    
    image_dir = "/home/ubuntu/tiktok_automation/images"
    quotes_file = "/home/ubuntu/tiktok_automation/quotes/quotes.txt"
    
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    
    if not image_files:
        print("No images found. Creating a sample image for testing...")
        sample_img = Image.new("RGB", (1080, 1920), color=(20, 20, 30))
        sample_img_path = os.path.join(image_dir, "sample_dark_bg.jpg")
        sample_img.save(sample_img_path)
        image_files = ["sample_dark_bg.jpg"]
        
    # Process the first image found
    image_path = os.path.join(image_dir, image_files[0])
    overlay_tool.process_random_quote(image_path, quotes_file)

if __name__ == "__main__":
    main()

