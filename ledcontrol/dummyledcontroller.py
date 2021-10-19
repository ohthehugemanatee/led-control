class DummyLEDController:
    def __init__(self):
        print("WARNING: Running in Preview mode, no LED signals will be sent!")

    def _cleanup(self):
        return

    def set_all_pixels_hsv_float(self, pixels, correction, saturation, brightness, gamma):
        return

    def set_all_pixels_rgb_float(self, pixels, correction, saturation, brightness, gamma):
        return
