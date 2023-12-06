from pathlib import Path

import drawsvg as draw

from bunt import crc
from bunt.constants import COLORS, INSET, POSITIONS, SHAPES, WIDTH


def create_code(media_ref: int):
    assert media_ref.bit_length() <= 25
    encoded_data = crc.sign(media_ref)

    # We use 3 bits per color and 4 bits per shape. In total, we have 4 colored shapes.
    # So (3+4)*4 = 28 bits.

    # As a result we use max 28 bits.

    # Draw background
    full_width = WIDTH + (2 * INSET)
    d = draw.Drawing(full_width, full_width, origin="center")
    d.append(
        draw.Rectangle(
            -full_width // 2, -full_width // 2, full_width, full_width, fill="white"
        )
    )

    # Draw the shapes
    for c, (x, y) in enumerate(POSITIONS):
        color_mask = (1 << 3) - 1  # The last three bits are the color.
        color = COLORS[encoded_data & color_mask]
        encoded_data >>= 3  # Shift the bits we just used out of the way.
        shape_mask = (1 << 4) - 1  # The next four bits are the shape.
        shape = SHAPES[encoded_data & shape_mask]
        encoded_data >>= 4

        radius = WIDTH // 4
        center = (2 * x - 1) * WIDTH // 4, (2 * y - 1) * WIDTH // 4
        d.append(draw.Circle(*center, radius, fill=color))
        for i, filled in enumerate(shape):
            if filled:
                w = WIDTH // 4
                tl = center[0] - radius + (i & 1) * w, center[1] - radius + (i >> 1) * w
                d.append(
                    draw.Rectangle(
                        *tl,
                        width=w,
                        height=w,
                        fill=color,
                    )
                )
    return d


if __name__ == "__main__":
    media_ref = 12345678
    drawing = create_code(media_ref)
    out_file = Path(__file__).parent / f"../samples/{media_ref}.svg"
    drawing.save_svg(str(out_file))
    drawing.save_svg(str(out_file))
