#!/usr/bin/env python3
"""
Content Creation Pipeline for TikTok Automation (POV Style)
This script orchestrates the process of selecting quotes and images,
and using the POVTextOverlay tool to generate the final content.
"""

import os
import random
import argparse
import sys

# Ensure the text_overlay_pov module can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the new POV style overlay class
    from text_overlay_pov import POVTextOverlay
except ImportError:
    print("Error: Could not import POVTextOverlay from text_overlay_pov.py.")
    print("Ensure text_overlay_pov.py is in the same directory.")
    sys.exit(1)

# Define base directory and subdirectories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUOTES_DIR = os.path.join(BASE_DIR, "quotes")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
QUOTES_FILE = os.path.join(QUOTES_DIR, "quotes.txt")

class ContentPipeline:
    def __init__(self):
        """Initialize the content pipeline."""
        self.quotes = self._load_quotes()
        self.images = self._find_images()
        # Use the new POVTextOverlay class
        self.overlay_tool = POVTextOverlay(output_dir=OUTPUT_DIR)
        self.used_quotes = set()
        self.used_images = set()

    def _load_quotes(self):
        """Load quotes from the quotes file."""
        if not os.path.exists(QUOTES_FILE):
            print(f"Error: Quotes file not found at {QUOTES_FILE}")
            return []
        try:
            with open(QUOTES_FILE, 'r') as f:
                quotes = [line.strip() for line in f if line.strip()]
            if not quotes:
                print(f"Warning: No quotes found in {QUOTES_FILE}")
            return quotes
        except Exception as e:
            print(f"Error reading quotes file: {e}")
            return []

    def _find_images(self):
        """Find image files in the images directory."""
        if not os.path.isdir(IMAGES_DIR):
            print(f"Error: Images directory not found at {IMAGES_DIR}")
            print("Please create the directory and add background images.")
            return []
        try:
            images = [
                os.path.join(IMAGES_DIR, f) 
                for f in os.listdir(IMAGES_DIR) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
            ]
            if not images:
                print(f"Warning: No images found in {IMAGES_DIR}. Please add images.")
            return images
        except Exception as e:
            print(f"Error finding images: {e}")
            return []

    def _get_random_quote(self):
        """Get a random quote, trying not to repeat recently used ones."""
        available_quotes = [q for q in self.quotes if q not in self.used_quotes]
        if not available_quotes:
            # Reset used quotes if all have been used
            self.used_quotes = set()
            available_quotes = self.quotes
        
        if not available_quotes:
            return None # No quotes available at all
            
        quote = random.choice(available_quotes)
        self.used_quotes.add(quote)
        return quote

    def _get_random_image(self):
        """Get a random image path, trying not to repeat recently used ones."""
        available_images = [img for img in self.images if img not in self.used_images]
        if not available_images:
            # Reset used images if all have been used
            self.used_images = set()
            available_images = self.images
            
        if not available_images:
             return None # No images available at all

        image_path = random.choice(available_images)
        self.used_images.add(image_path)
        return image_path

    def generate_content(self, num_posts=3):
        """Generate the specified number of content images using POV style."""
        if not self.quotes:
            print("Cannot generate content: No quotes loaded.")
            return
        if not self.images:
            print("Cannot generate content: No images found.")
            print(f"Please add images to the '{IMAGES_DIR}' directory.")
            # Create a sample image if none exists, using the logic from text_overlay_pov.py
            print("Creating a sample dark background image for demonstration...")
            try:
                from PIL import Image
                sample_img = Image.new('RGB', (1080, 1920), color=(20, 20, 30))
                sample_img_path = os.path.join(IMAGES_DIR, "sample_dark_bg.jpg")
                sample_img.save(sample_img_path)
                self.images = [sample_img_path] # Update image list
                print(f"Sample image created at {sample_img_path}")
            except Exception as e:
                 print(f"Failed to create sample image: {e}")
                 return

        print(f"Starting POV-style content generation for {num_posts} posts...")
        generated_count = 0
        for i in range(num_posts):
            quote = self._get_random_quote()
            image_path = self._get_random_image()

            if not quote or not image_path:
                print("Error: Could not get a quote or image. Stopping generation.")
                break

            # Generate a unique output filename for POV style
            output_filename = os.path.join(OUTPUT_DIR, f"post_pov_{i+1:03d}.jpg")

            print(f"Generating post {i+1}/{num_posts}: Using image '{os.path.basename(image_path)}'")
            # Call the new POV style method
            result_path = self.overlay_tool.add_pov_text_to_image(image_path, quote, output_filename)

            if result_path:
                generated_count += 1
            else:
                print(f"Failed to generate post {i+1}.")

        print(f"\nContent generation complete. {generated_count}/{num_posts} POV-style posts created in '{OUTPUT_DIR}'.")

def main():
    parser = argparse.ArgumentParser(description="Generate TikTok motivational content images (POV Style).")
    parser.add_argument(
        "-n", "--number", 
        type=int, 
        default=3, 
        help="Number of content images to generate (default: 3)"
    )
    args = parser.parse_args()

    pipeline = ContentPipeline()
    pipeline.generate_content(num_posts=args.number)

if __name__ == "__main__":
    main()
