from PIL import Image

COLOR_PROTOTYPES = {
    1: (60, 60, 60),      # black
    2: (250, 220, 70),    # yellow
    3: (175, 215, 95),    # green
    4: (90, 165, 235),    # blue
    5: (130, 100, 170),   # purple
    6: (235, 80, 95),     # red
}

def classify_color(rgb):
    r, g, b = rgb

    best_id = None
    best_dist = float("inf")

    for color_id, (cr, cg, cb) in COLOR_PROTOTYPES.items():
        dist = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2
        if dist < best_dist:
            best_dist = dist
            best_id = color_id

    return best_id

def detect_image(image_path):
    image = Image.open(image_path)
    width, height = image.size

    cols, rows = 8,7
    cell_w = width // cols
    cell_h = height // rows

    grid = []
    for row in range(rows):
        row_arr = []
        for col in range(cols):
            # The plus 10 is because screenshots may have grey margins
            x = col * cell_w + 10
            y = row * cell_h + 10

            pixel = image.getpixel((x, y))
            row_arr.append(classify_color(pixel))
        grid.append(row_arr)
    return grid


