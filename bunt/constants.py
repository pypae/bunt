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


""">>> import random
>>> SHUFFLE_PERMUTATION = list(range(28))
>>> random.seed(hash("bunt"))
>>> random.shuffle(SHUFFLE_PERMUTATION)"""
SHUFFLE_PERMUTATION = [26, 2, 5, 16, 9, 12, 1, 4, 13, 20, 3, 10, 18, 22, 7, 14, 15, 17, 6, 23, 8, 24, 25, 11, 21, 19, 27, 0]

""">>> REVERSE_PERMUTATION = [SHUFFLE_PERMUTATION.index(i) for i in range(len(SHUFFLE_PERMUTATION))]"""
REVERSE_PERMUTATION = [27, 6, 1, 10, 7, 2, 18, 14, 20, 4, 11, 23, 5, 8, 15, 16, 3, 17, 12, 25, 9, 24, 13, 19, 21, 22, 0, 26]
