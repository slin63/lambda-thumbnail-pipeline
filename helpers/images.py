# https://pillow.readthedocs.io/en/latest/handbook/tutorial.html#create-jpeg-thumbnails
import cv2
import piexif


def to_thumbnail(path, max_size=500):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    # Scale % = max_size / (max width or height)
    scale_percent = max_size / max(
        img.shape[0], img.shape[1]
    )
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)

    # Preserve exif data, if any
    was_ok = False
    try:
        exif_bytes = piexif.dump(piexif.load(path))
        was_ok = True
    except:
        print(path, " did not have exif data.")

    # Resize image
    resized = cv2.resize(
        img, dim, interpolation=cv2.INTER_AREA
    )

    # Save image
    cv2.imwrite(path, resized)

    # Transfer exif data
    if was_ok:
        piexif.insert(exif_bytes, path)

    return True
