import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys

def main():
    """
    Main function to load pre-aligned images and create an interactive overlay.
    """
    # --- Load Images ---
    # The base image (e.g., H&E or counterstain)
    image_base_path = 'image1.png'
    # The image to overlay (e.g., IHC)
    image_overlay_path = 'image2.png'
    
    img_base_bgr = cv2.imread(image_base_path)
    img_overlay_bgr = cv2.imread(image_overlay_path)

    # Check if images loaded correctly
    if img_base_bgr is None or img_overlay_bgr is None:
        print(f"Error: Could not load one or both images.")
        print(f"Please ensure '{image_base_path}' and '{image_overlay_path}' are in the correct directory.")
        sys.exit(1)

    print("Images loaded successfully.")

    # --- Ensure Images Have the Same Dimensions ---
    h_base, w_base, _ = img_base_bgr.shape
    h_overlay, w_overlay, _ = img_overlay_bgr.shape

    # If dimensions are different, resize the overlay to match the base
    if (h_base, w_base) != (h_overlay, w_overlay):
        print("Warning: Image dimensions do not match.")
        print(f"Resizing overlay image from {w_overlay}x{h_overlay} to {w_base}x{h_base}.")
        img_overlay_bgr = cv2.resize(img_overlay_bgr, (w_base, h_base), interpolation=cv2.INTER_AREA)

    print("Creating interactive viewer...")

    # Convert images from BGR (OpenCV's format) to RGB (Matplotlib's format) for display
    img_base_rgb = cv2.cvtColor(img_base_bgr, cv2.COLOR_BGR2RGB)
    img_overlay_rgb = cv2.cvtColor(img_overlay_bgr, cv2.COLOR_BGR2RGB)
    
    # --- Create Interactive Plot ---
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2) # Make space for the slider
    plt.title('Image Overlay Tool')
    ax.axis('off') # Hide axes ticks

    # Initial display with 50% opacity
    initial_alpha = 0.5
    # Use cv2.addWeighted for efficient blending
    blended_image = cv2.addWeighted(img_overlay_rgb, initial_alpha, img_base_rgb, 1 - initial_alpha, 0)
    displayed_image = ax.imshow(blended_image)

    # Create the slider widget
    slider_ax = plt.axes([0.25, 0.1, 0.5, 0.03]) # [left, bottom, width, height]
    opacity_slider = Slider(
        ax=slider_ax,
        label='Overlay Opacity',
        valmin=0.0,
        valmax=1.0,
        valinit=initial_alpha,
    )

    # --- Update Function for the Slider ---
    def update(val):
        # Get the current alpha value from the slider
        alpha = opacity_slider.val
        # Blend the two images
        blended = cv2.addWeighted(img_overlay_rgb, alpha, img_base_rgb, 1 - alpha, 0)
        # Update the image data being displayed
        displayed_image.set_data(blended)
        # Redraw the figure
        fig.canvas.draw_idle()

    # Register the update function with the slider
    opacity_slider.on_changed(update)

    plt.show()


if __name__ == '__main__':
    main()