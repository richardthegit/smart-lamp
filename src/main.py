import time
from rb.dev.neo_led import LEDStrip
from rb.dev.phototransistor import Phototransistor


def lamp():
    strip = LEDStrip(0, 5, 0)
    pt = Phototransistor(1)
    
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

        if not changed:
            time.sleep(1)
        else:
            for i in range(fade_steps + 1):
                strip.brightness_step()
                strip.set_mono(strip.fade(c))
                time.sleep(1 / 60)


def calibrate():
    pt = Phototransistor(1)
    while True:
        print(pt.read())
        time.sleep(1/5)


lamp()