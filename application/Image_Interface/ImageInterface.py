from PIL import Image
import customtkinter
from tkinterdnd2 import TkinterDnD,DND_FILES
import cv2
# Singleton 
class Singleton():
    def __new__(cls, *args,**kargs):
        if not hasattr(cls,"_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
    
class ImageInterface(Singleton):
    def __init__(self):
        # ImageWidgets info
        self.root: TkinterDnD.Tk|None = None
        self.image_label:customtkinter.CTkLabel|None = None
        self.widgets_size: tuple = None
        self.image: Image.Image | None = None
        self.image_path: str | None = None

        # ToolWidgets
        self.color: str | None = None
        self.current_option_id: int = 1
        self.value: float = 0

    def load_image(self, image: Image.Image, image_path: str, image_label, root, widgets_size: tuple):
        self.root = root
        self.image_label = image_label
        self.widgets_size = widgets_size
        self.image = image
        self.image_path = image_path

    def apply_filter(self, color: str, current_option_id: int, value: float):
        self.color = color
        self.current_option_id = current_option_id
        self.value = value
        
        self.redraw_image_label()

    def redraw_image_label(self):
        # 画像をCTkImageに変換
        CTkimage = customtkinter.CTkImage(light_image=self.image, dark_image=self.image, size=self.widgets_size)
        # image_labelを更新
        self.image_label.configure(image=CTkimage)
        # 参照を保持する必要があるため、self.image_label.imageに保持
        self.image_label.image = CTkimage
