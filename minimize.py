import sys
try:
    from PIL import Image as im
    from PIL import ImageSequence
except ModuleNotFoundError:
    print("Could not find library: [%s]. Trying to install it... \nTry disabling system proxy if any error occurs. \n" % "pillow")

    try:
        from pip import main as pipmain
    except:
        from pip._internal.main import main as pipmain
    # pipmain.main(['install', '-r', 'requirements.txt'])
    pipmain(['install', 'pillow'])

    from PIL import Image as im
    from PIL import ImageSequence


def minimize(filename, threshold = [10, 24, 48]):
    img = im.open(filename)
    width, height = img.size
    filename_split = filename.split(".")
    img_name = filename_split[0]
    img_extension = filename_split[1]
    img_format = img.format

    if min(width, height) < min(threshold):
        print("Error: Image size smaller than threshold.")
        return
    
    for limit in threshold:
        scale = (limit / width if width <= height else limit / height)
        w, h = int(scale * width), int(scale * height)

        new_filename = img_name + '_x' + str(limit) + '.' + img_extension
        
        if img_format == 'GIF':
            frames = ImageSequence.Iterator(img)
            resized = gif_resize(w, h, frames)
            generated = next(resized)
            generated.info = img.info
            tp = 255
            if 'transparency' in img.info:
                tp = img.info["transparency"]
            generated.save(new_filename, format=img_format, transparency=tp, save_all=True, append_images=list(resized), loop=0, disposal=2, optimize=False)
        else:
            resized = img.resize((w, h), 1)
            resized.save(new_filename, format=img_format)
        print("[Done]: %s" % new_filename)


def gif_resize(w, h, frames):
    for frame in frames:
        resized = frame.copy().resize((w, h), 1)
        yield resized


if __name__ == "__main__":
    if len(sys.argv) == 2:
        minimize(sys.argv[1])
    if len(sys.argv) == 3:
        minimize(sys.argv[1], sys.argv[2])