from PIL import Image
# Singleton 
class Singleton():
    def __new__(cls, *args,**kargs):
        if not hasattr(cls,"_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
    
class ImageInterface(Singleton):
    def __init__(self):
        # ImageWidgets info
        self.image:Image.Image|None = None
        self.image_path:str|None = None

        # ToolWidgets
        self.color:str|None = None
        self.current_option_id:int = 1
        self.value:float = 0
    
    def load_image(self,image:Image.Image,image_path:str):
        self.image = image
        self.image_path = image_path

    def apply_filter(self,color:str,current_option_id:int,value:float):
        self.color = color
        self.current_option_id = current_option_id
        self.value = value
