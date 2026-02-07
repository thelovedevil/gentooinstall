import numpy as np
from PIL import Image
import curses

class AsciiArt:
    ascii_chars = "@@@%%%###***+++===---:::...!!!/// "

    def __init__(self, image_path):
        self.image_path = image_path
        self.start_row = 0
        self.start_col = 0
        self.art_matrix = None
        self.art_height = 0
        self.art_width = 0

    def convert_ascii(self, width, height):
        im = Image.open(self.image_path)
        im.thumbnail((width, height), Image.Resampling.LANCZOS)
        
        pixel_matrix = np.array(im)
        # Ensure image is RGB (3 channels) for luminosity calculation
        if pixel_matrix.ndim == 2: # Grayscale image
            luminosity_matrix = pixel_matrix
        elif pixel_matrix.ndim == 3 and pixel_matrix.shape[2] == 4: # RGBA image
            # Convert to RGB by discarding alpha or blend with white background
            # For simplicity, discarding alpha channel
            pixel_matrix = pixel_matrix[:, :, :3]
            luminosity_matrix = 0.21 * pixel_matrix[:, :, 0] + 0.72 * pixel_matrix[:, :, 1] + 0.07 * pixel_matrix[:, :, 2]
        elif pixel_matrix.ndim == 3 and pixel_matrix.shape[2] == 3: # RGB image
            luminosity_matrix = 0.21 * pixel_matrix[:, :, 0] + 0.72 * pixel_matrix[:, :, 1] + 0.07 * pixel_matrix[:, :, 2]
        else:
            raise ValueError(f"Unsupported image format: {self.image_path}. Expected grayscale, RGB, or RGBA.")

        # Handle potential division by zero if min and max are the same (e.g., solid color image)
        min_luminosity = luminosity_matrix.min()
        max_luminosity = luminosity_matrix.max()

        if max_luminosity == min_luminosity:
            normalized_luminosity = np.full(luminosity_matrix.shape, 0.5) # Assign middle value
        else:
            normalized_luminosity = (luminosity_matrix - min_luminosity) / (max_luminosity - min_luminosity)
        
        indices = (normalized_luminosity * (len(self.ascii_chars) - 1)).astype(int)
        ascii_matrix = np.array([[self.ascii_chars[idx] for idx in row] for row in indices])
        
        self.art_matrix = ascii_matrix
        self.art_height, self.art_width = self.art_matrix.shape
        
        return ascii_matrix

    def get_ascii_art_lines(self):
        if self.art_matrix is None:
            return []
        return ["".join(row) for row in self.art_matrix]

    # The draw_menu and handle_input methods from asuka_menu.py will be integrated into the CursedPrinter class.
    # For now, they are removed from here as AsciiArt should only be responsible for generating the art.
