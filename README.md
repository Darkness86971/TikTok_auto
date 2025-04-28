# TikTok Motivational Content Automation System (POV Style)

## Overview

This system automates the creation of motivational content images suitable for platforms like TikTok, using the specific "POV" style you requested. It combines motivational quotes with background images (ideally dark anime style, as requested) and saves the resulting images, ready for you to upload to your preferred scheduling platform.

## Latest Updates

- Added center alignment for text to match your example
- Attempted to use Comic Sans font (falls back to system fonts if not available)
- Positioned text for optimal readability

## Project Structure

```
/home/ubuntu/tiktok_automation/
├── images/             # Directory to store your background images
│   └── (add your .jpg, .png, .jpeg, .webp images here)
├── output/             # Directory where generated content images are saved
│   └── post_pov_001.jpg
│   └── post_pov_002.jpg
│   └── ...
├── quotes/             # Directory containing the quotes database
│   └── quotes.txt      # File with motivational quotes (one per line)
├── image_collector.py  # Script to attempt image collection (currently non-functional due to website blocks)
├── text_overlay.py     # Original script for centered text overlay (not used by default pipeline)
├── text_overlay_pov.py # Script that handles adding text in POV style with center alignment
├── pipeline.py         # Main script to run the POV-style content generation process
└── README.md           # This usage guide
```

## How to Use

1.  **Add Background Images:**
    *   The automated image collection (`image_collector.py`) failed because websites like Unsplash and Pexels block scraping attempts. Pinterest also prevents automated downloading.
    *   **You need to manually download your desired background images** (e.g., dark anime style images from Pinterest) into the `/home/ubuntu/tiktok_automation/images/` directory.
    *   Supported formats are JPG, JPEG, PNG, and WEBP.
    *   The system works best with images that are relatively dark or have areas where white text with a black outline will be clearly visible.
    *   Images should ideally be in a vertical aspect ratio suitable for TikTok (e.g., 1080x1920), although the script will attempt to work with other sizes.

2.  **Customize Quotes (Optional):**
    *   A list of 100 motivational quotes is provided in `/home/ubuntu/tiktok_automation/quotes/quotes.txt`.
    *   You can edit this file to add, remove, or modify quotes. Ensure each quote is on a new line.

3.  **Generate Content (POV Style with Center Alignment):**
    *   Open a terminal or command line in the `/home/ubuntu/tiktok_automation/` directory.
    *   Run the main pipeline script using the following command:
        ```bash
        python3 pipeline.py
        ```
    *   This will use the `text_overlay_pov.py` script to generate images with "POV" at the top and the quote below in center alignment, matching the style you requested.
    *   By default, this will generate 3 images.
    *   To generate a different number of images, use the `-n` or `--number` flag. For example, to generate 5 images:
        ```bash
        python3 pipeline.py -n 5
        ```

4.  **Find Output:**
    *   The generated POV-style images will be saved in the `/home/ubuntu/tiktok_automation/output/` directory.
    *   Files will be named `post_pov_001.jpg`, `post_pov_002.jpg`, etc.

5.  **Upload to Scheduler:**
    *   Take the images from the `output` folder and upload them to your preferred TikTok scheduling platform or post them directly.

## Font Information

The system attempts to use Comic Sans font if available on your system. If Comic Sans is not found (which is the case in most Linux systems without Microsoft fonts installed), it will automatically fall back to a system font like DejaVu Sans Bold.

If you want to use Comic Sans specifically:
1. You would need to install the Microsoft TrueType Core Fonts package on your system
2. Or manually add the Comic Sans font file to your system's font directory

## Important Notes

*   **Image Source:** You are responsible for ensuring you have the rights to use the background images you add to the `images` folder.
*   **Scheduling:** This system *creates* the content images but does *not* automatically post or schedule them on TikTok or any other platform. You need to handle the uploading and scheduling process manually using your chosen tools.
*   **Text Alignment:** All text is now center-aligned as requested in your example.

Let me know if you have any questions!
