import itertools

# Source for visually distinct colors: https://mokole.com/palette.html
BGR_TO_COLORS = {
    (0, 100, 0): "darkgreen",
    (0, 69, 255): "orangered",
    (0, 215, 255): "gold",
    (133, 21, 199): "mediumvioletred",
    (0, 255, 0): "lime",
    (255, 255, 0): "aqua",
    (255, 0, 0): "blue",
    (255, 144, 30): "dodgerblue",
}


COLORS = list(BGR_TO_COLORS.values())

SHAPES = list(itertools.product((True, False), repeat=4))

POSITIONS = (
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1),
)

WIDTH = 512
INSET = 24
