import time
from rb.dev.neo_led import LEDStrip
from rb.dev.phototransistor import Phototransistor


def lamp():
    pt = Phototransistor(0)
    strip = LEDStrip(1, 5, 0)
    c = [255, 140, 50]
    on = 0.2
    off = 0.3
    fade_steps = 60 * 4

    while True:
        val = pt.read()
        changed = True

        if val <= on and strip.brightness != 1:
            strip.brightness_target(1, fade_steps)
        elif val >= off and strip.brightness != 0:
            strip.brightness_target(0, fade_steps)
        else:
            changed = False

        if changed:
            for i in range(fade_steps + 1):
                strip.brightness_step()
                strip.set_mono(strip.fade(c))
                time.sleep(1 / 60)

lamp()