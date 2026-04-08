import numpy as np
from PIL import Image
import curses

class AsciiArt:
    ascii_chars = "@@@@@%%%%%#####*****+++++=====-----:::::.....!!!!!///// "

    def __init__(self, image_path):
        self.image_path = image_path
        self.start_row = 0
        self.start_col = 0
        self.art_matrix = None
        self.art_height = 0
        self.art_width = 0
        self._cache = {}

    def convert_ascii(self, width, height):
        cache_key = (width, height)
        if cache_key in self._cache:
            self.art_matrix = self._cache[cache_key]
            self.art_height, self.art_width = self.art_matrix.shape
            return self.art_matrix

        try:
            im = Image.open(self.image_path)
            im.thumbnail((width, height), Image.Resampling.LANCZOS)
            
            # Using the logic from the snippet
            resized_path = "temp_resized.jpg"
            im.save(resized_path)
            img = Image.open(resized_path)
            
            pixel_matrix = np.array(img)
            
            if pixel_matrix.ndim == 2:
                luminosity_matrix = pixel_matrix
            else:
                if pixel_matrix.shape[2] == 4:
                    pixel_matrix = pixel_matrix[:, :, :3]
                luminosity_matrix = 0.21 * pixel_matrix[:, :, 0] + 0.72 * pixel_matrix[:, :, 1] + 0.07 * pixel_matrix[:, :, 2]
            
            min_lum = luminosity_matrix.min()
            max_lum = luminosity_matrix.max()
            
            if max_lum == min_lum:
                normalized_luminosity = np.full(luminosity_matrix.shape, 0.5)
            else:
                normalized_luminosity = (luminosity_matrix - min_lum) / (max_lum - min_lum)
            
            indices = (normalized_luminosity * (len(self.ascii_chars) - 1)).astype(int)
            ascii_matrix = np.array([[self.ascii_chars[idx] for idx in row] for row in indices])
            
            self.art_matrix = ascii_matrix
            self.art_height, self.art_width = self.art_matrix.shape
            self._cache[cache_key] = self.art_matrix
            return ascii_matrix
            
        except Exception:
            self.art_matrix = np.full((height, width), " ")
            return self.art_matrix

    def get_ascii_art_lines(self):
        if self.art_matrix is None:
            return []
        return ["".join(row) for row in self.art_matrix]

    def handle_input(self, key, view_width, view_height):
        if self.art_matrix is None:
            return False
            
        moved = False
        # Logic from snippet (W/S/A/D)
        if key == ord("w") and self.start_row > 0:
            self.start_row -= 1
            moved = True
        elif key == ord("s") and self.start_row < self.art_height - view_height:
            self.start_row += 1
            moved = True
        elif key == ord("d") and self.start_col > 0:
            self.start_col -= 1
            moved = True
        elif key == ord("a") and self.start_col < self.art_width - view_width:
            self.start_col += 1
            moved = True
        return moved

    # The draw_menu and handle_input methods from asuka_menu.py will be integrated into the CursedPrinter class.
    # For now, they are removed from here as AsciiArt should only be responsible for generating the art.
