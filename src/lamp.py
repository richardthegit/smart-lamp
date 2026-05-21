import machine, time

from rb.core.color import fade
from rb.core.persist import store
from rb.core.richtext import rt
from rb.dev.neo_led import LEDStrip
from rb.dev.phototransistor import Phototransistor


default_c = (255, 140, 50)
default_range = (200, 400)


def lamp():
    strip = LEDStrip(0, 5, 0)
    pt = Phototransistor(1)

    c = store.get('color', default_c)
    on, off = store.get('range', default_range)
    lit = False
    fade_steps = 30 * 4

    while True:
        val = pt.read_raw()
        changed = True

        if val <= on and not lit:
            strip.brightness_target(1, fade_steps)
            lit = True
        elif val >= off and lit:
            strip.brightness_target(0, fade_steps)
            lit = False
        else:
            changed = False

        if not changed:
            if False and not lit:
                machine.deepsleep(10 * 1000)
            else:
                time.sleep(1)
        else:
            rt.info('Light changed to: {"on" if lit else "off"}')
            for i in range(fade_steps + 1):
                strip.brightness_step()
                strip.set_mono(strip.fade(c))
                time.sleep(1 / 30)


def configure():
    c = store.get('color', default_c)
    on, off = store.get('range', default_range)

    rt.info(f'Current color: {c}')
    if input('Change color? (y/N): ') == 'y':
        store.set('color', (int(input('R: ')), int(input('G: ')), int(input('B: '))))

    rt.info(f'Current range: on at {on}, off at {off}')
    if input('Change range? (y/N): ') == 'y':
        store.set('range', (int(input('on: ')), int(input('off: '))))


def monitor():
    pt = Phototransistor(1)
    while True:
        print(pt.read_raw())
        time.sleep(1 / 5)
