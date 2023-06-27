from pathlib import Path

import pygame as pg

DATA_DIR = Path(__file__).parent.parent.parent / "data"
assert DATA_DIR.exists(), f"Data directory {DATA_DIR} does not exist"


def im_path(path: str | Path) -> Path:
    return DATA_DIR / path


CACHE: dict[str, pg.Surface] = {}


def load_im(
    path: str | Path,
    scale: float = 1,
    color_key: tuple[int, int, int] | int = -1,
) -> pg.Surface:
    path = (DATA_DIR / path).resolve()
    if str(path) in CACHE:
        return CACHE[str(path)]
    assert path.exists(), f"File {path} does not exist"
    image = pg.image.load(str(DATA_DIR / path))
    if scale != 1:
        image = pg.transform.scale(
            image,
            (int(image.get_width() * scale), int(image.get_height() * scale)),
        )
    color_key = image.get_at((0, 0)) if color_key == -1 else color_key
    image.set_colorkey(color_key)
    CACHE[str(path)] = image
    return image

def load_audio(path: str | Path) -> pg.mixer.Sound:
    path = (DATA_DIR / path).resolve()
    assert path.exists(), f"File {path} does not exist"
    return pg.mixer.Sound(str(path))