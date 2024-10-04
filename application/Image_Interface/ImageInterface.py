from PIL import Image
import customtkinter
from application.Image_Interface.filter import apply_gamma, apply_saturation, apply_contrast
from application.Widgets.Image_Widgets.image_process import resize_image

class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class ImageInterface(Singleton):
    def __init__(self):
        self.root = None
        self.image_label = None
        self.widgets_size = None
        self.image = None
        self.result_image = None

    def load_image(self, image: Image.Image, image_path: str, image_label, root, widgets_size: tuple):
        self.root = root
        self.image_label = image_label
        self.widgets_size = widgets_size
        self.image = image
        self.result_image = image

    def apply_filter(self, slider_values: dict[int, dict[str, float]]):
        if self.image:
            result_image = self.image
            for op_id, sliders in slider_values.items():
                R, G, B, Y = (sliders[color].get() for color in "RGBY")
                match op_id:
                    case 0:
                        result_image = apply_saturation(result_image, R, G, B, Y)
                    case 1:
                        result_image = apply_contrast(result_image, R, G, B, Y)
                    case 2:
                        result_image = apply_gamma(result_image, R, G, B, Y)
            self.result_image = result_image
            self.redraw_image_label(result_image)

    def filter(self, color: str, current_option_id: int, op_slider_values: dict):
        if self.image:
            R, G, B, Y = (op_slider_values[color].get() for color in "RGBY")
            match current_option_id:
                case 0:
                    result_image = apply_saturation(self.result_image, R, G, B, Y)
                case 1:
                    result_image = apply_contrast(self.result_image, R, G, B, Y)
                case 2:
                    result_image = apply_gamma(self.result_image, R, G, B, Y)
            self.redraw_image_label(result_image)

    def redraw_image_label(self, image):
        resized_image = resize_image(image,self.widgets_size)
        CTkimage = customtkinter.CTkImage(light_image=resized_image, dark_image=resized_image, size=self.widgets_size)
        self.image_label.configure(image=CTkimage)
        self.image_label.image = CTkimage
    