#!/usr/bin/env python3
"""
Image Collector for TikTok Content Automation
This script collects dark anime images from the web to use as backgrounds for motivational quotes.
"""

import os
import random
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus
import json
from PIL import Image
from io import BytesIO

# Create directories if they don't exist
os.makedirs("images", exist_ok=True)

class ImageCollector:
    def __init__(self, search_terms=None, save_dir="images"):
        """Initialize the image collector with search terms and save directory."""
        self.search_terms = search_terms or ["dark anime aesthetic", "dark anime background", "anime silhouette"]
        self.save_dir = save_dir
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
    def search_unsplash(self, query, num_images=5):
        """Search Unsplash for images."""
        print(f"Searching Unsplash for '{query}'...")
        encoded_query = quote_plus(query)
        url = f"https://unsplash.com/s/photos/{encoded_query}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img', class_='YVj9w')
            
            image_urls = []
            for img in img_tags[:num_images]:
                if 'src' in img.attrs:
                    image_urls.append(img['src'])
            
            return image_urls
        except Exception as e:
            print(f"Error searching Unsplash: {e}")
            return []

    def search_pexels(self, query, num_images=5):
        """Search Pexels for images."""
        print(f"Searching Pexels for '{query}'...")
        encoded_query = quote_plus(query)
        url = f"https://www.pexels.com/search/{encoded_query}/"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img', class_='photo-item__img')
            
            image_urls = []
            for img in img_tags[:num_images]:
                if 'src' in img.attrs:
                    image_urls.append(img['src'])
                elif 'data-big-src' in img.attrs:
                    image_urls.append(img['data-big-src'])
            
            return image_urls
        except Exception as e:
            print(f"Error searching Pexels: {e}")
            return []

    def download_image(self, url, filename):
        """Download an image from a URL and save it to the specified filename."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Check if the image is valid
            img = Image.open(BytesIO(response.content))
            
            # Check if the image is large enough (minimum 640x640)
            if img.width < 640 or img.height < 640:
                print(f"Image too small: {img.width}x{img.height}")
                return False
            
            # Save the image
            img.save(filename)
            print(f"Downloaded: {filename}")
            return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False

    def is_dark_image(self, img_path, threshold=100):
        """Check if an image is dark enough to be used as a background."""
        try:
            img = Image.open(img_path).convert('L')  # Convert to grayscale
            avg_brightness = sum(img.getdata()) / len(img.getdata())
            return avg_brightness < threshold
        except Exception as e:
            print(f"Error checking image brightness: {e}")
            return False

    def collect_images(self, num_images=15):
        """Collect images from various sources based on search terms."""
        collected_count = 0
        
        for term in self.search_terms:
            if collected_count >= num_images:
                break
                
            # Try Unsplash
            unsplash_urls = self.search_unsplash(term, num_images=5)
            for i, url in enumerate(unsplash_urls):
                if collected_count >= num_images:
                    break
                    
                filename = os.path.join(self.save_dir, f"dark_anime_{collected_count+1}.jpg")
                if self.download_image(url, filename):
                    # Check if the image is dark enough
                    if self.is_dark_image(filename):
                        collected_count += 1
                    else:
                        print(f"Image not dark enough, removing: {filename}")
                        os.remove(filename)
                
                # Be nice to the server
                time.sleep(1)
            
            # Try Pexels
            pexels_urls = self.search_pexels(term, num_images=5)
            for i, url in enumerate(pexels_urls):
                if collected_count >= num_images:
                    break
                    
                filename = os.path.join(self.save_dir, f"dark_anime_{collected_count+1}.jpg")
                if self.download_image(url, filename):
                    # Check if the image is dark enough
                    if self.is_dark_image(filename):
                        collected_count += 1
                    else:
                        print(f"Image not dark enough, removing: {filename}")
                        os.remove(filename)
                
                # Be nice to the server
                time.sleep(1)
        
        print(f"Collected {collected_count} images.")
        return collected_count

def main():
    """Main function to run the image collector."""
    collector = ImageCollector(save_dir="/home/ubuntu/tiktok_automation/images")
    collector.collect_images(num_images=15)

if __name__ == "__main__":
    main()
