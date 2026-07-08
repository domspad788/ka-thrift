import os
from PIL import Image, ImageOps

SRC = "images"
OUT = "img"
os.makedirs(OUT, exist_ok=True)

# Target max dimensions for different uses
FULL_MAX = 1600   # gallery/lightbox full view
CARD_MAX = 900    # cards / section images
HERO_MAX = 2000   # hero background

files = [f for f in os.listdir(SRC) if f.lower().endswith((".jpeg", ".jpg", ".png"))]

for f in sorted(files):
    name = os.path.splitext(f)[0]
    src_path = os.path.join(SRC, f)
    img = Image.open(src_path)
    img = ImageOps.exif_transpose(img)  # honor orientation
    img = img.convert("RGB")

    # full size (capped)
    full = img.copy()
    full.thumbnail((FULL_MAX, FULL_MAX), Image.LANCZOS)
    full.save(os.path.join(OUT, f"{name}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)

    # card/thumb size
    card = img.copy()
    card.thumbnail((CARD_MAX, CARD_MAX), Image.LANCZOS)
    card.save(os.path.join(OUT, f"{name}-sm.jpg"), "JPEG", quality=78, optimize=True, progressive=True)

    print(f"{name}: {img.size} -> full {full.size}, sm {card.size}")

# Hero versions (larger, from storefront shots)
for hero in ["IMG_0989", "IMG_0988"]:
    p = os.path.join(SRC, f"{hero}.jpeg")
    if os.path.exists(p):
        img = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        img.thumbnail((HERO_MAX, HERO_MAX), Image.LANCZOS)
        img.save(os.path.join(OUT, f"{hero}-hero.jpg"), "JPEG", quality=85, optimize=True, progressive=True)
        print(f"hero {hero}: {img.size}")

print("done")
