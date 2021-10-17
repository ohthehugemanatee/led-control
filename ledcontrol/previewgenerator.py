from os import path
from PIL import Image
from colorsys import hsv_to_rgb
from ledcontrol.animationcontroller import AnimationController
from tempfile import NamedTemporaryFile
import ledcontrol.animationpatterns as animpatterns
import ledcontrol.colorpalettes as colorpalettes
import ledcontrol.pixelmappings as pixelmappings
import ledcontrol.driver as driver
import ledcontrol.utils as utils

def generate_preview(params):
    controller = AnimationController(None, 0, 256, pixelmappings.line(256), (0, 0, 0), False, True)

    s = params['s']
    t = params['t'] # Time units
    gif_t = 300 # Animated gif duration

    source = animpatterns.default[params['primary_pattern']]

    errors, warnings, pattern = controller.compile_pattern(source)

    img = Image.new('RGB', (t, s), 'black')
    pixels = img.load()

    prev = [(0, 0, 0) for i in range(s)]

    frames = []

    for i in range(img.size[0]):
        frame = Image.new('RGB', (s, 1), 'black')
        frame_pixels = frame.load()
        for j in range(img.size[1]):
            p = pattern((params['primary_speed'] / 0.2)
                        * i / s, 1.0 / s, j / s, 0, 0, prev[j])
            prev[j] = p[0]
            if p[1] == animpatterns.ColorMode.hsv:
                c = tuple([int(x * 255) for x in hsv_to_rgb(*p[0])])
                pixels[i, j] = c
                frame_pixels[j, 0] = c
            else:
                c = tuple([int(x * 255) for x in p[0]])
                pixels[i, j] = c
                frame_pixels[j, 0] = c
        if i < gif_t:
            frames.append(frame)

    ftmp = NamedTemporaryFile()
    gif_name = ftmp.name + ".gif"
    file_path, filename = path.split(ftmp.name)

    frames[0].save(gif_name, save_all=True, append_images=frames[1:], duration=100, loop=0)
    return file_path, filename
