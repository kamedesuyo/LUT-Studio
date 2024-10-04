import customtkinter
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image
from application.Widgets.Image_Widgets.image_process import resize_image
from application.Image_Interface.ImageInterface import ImageInterface

WIDTH = 896
HEIGHT = 504

class ImageWidgets(customtkinter.CTkFrame):  
    def __init__(self, root: TkinterDnD.Tk):
        super().__init__(root, width=WIDTH, height=HEIGHT, fg_color="#000000", corner_radius=0)
        self.root = root
        self.ImageInterface = ImageInterface()  # インターフェース接続
        self.label = None  # ラベルを初期化
        self.image_label = None  # 画像ラベルを初期化
        self.enable_dnd()  # D&Dを有効化
        self.draw_dnd_label()  # D&D用ラベル描画
        self.pack_propagate(False)

    def drop(self, event: TkinterDnD.DnDEvent):
        image_file_path = event.data.strip("{}s")  # path取得 両端にある{}除去
        try:
            image_origin = Image.open(image_file_path)
        except Exception as e:
            print(f"Image open error: {e}")
            return

        resized_image = resize_image(image_origin, (WIDTH, HEIGHT))
        self.update_image_label(resized_image)
        self.ImageInterface.load_image(image_origin, image_file_path, self.image_label, self.root, (WIDTH, HEIGHT))

    def update_image_label(self, image):
        self.image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(WIDTH, HEIGHT))
        
        # labelが存在する場合はdestroyして新たに生成する
        if self.label:
            self.label.destroy()
        if self.image_label:
            self.image_label.destroy()

        # 新しいimage_labelの生成
        self.image_label = customtkinter.CTkLabel(self, image=self.image, text="")
        self.image_label.pack()

    def draw_dnd_label(self):
        # D&D領域にlabel設置、image_labelの仮置き
        self.label = customtkinter.CTkLabel(self, text="ここに画像をD&D", text_color="white", fg_color="#000000", font=(None, 30))
        self.label.place(relx=0.5, rely=0.5, anchor="center")

    def enable_dnd(self):
        # tkinterdnd2の機能でD&Dを有効化し、ドロップイベントをバインド
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop)
