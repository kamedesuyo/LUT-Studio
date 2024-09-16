import customtkinter
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image
from application.Widgets.Image_Widgets.image_process import resize_image
from application.Image_Interface.ImageInterface import ImageInterface

WIDTH = 896
HEIGHT = 504

class ImageWidgets(customtkinter.CTkFrame):  
    def __init__(self, root: TkinterDnD.Tk):
        super().__init__(root,
                         width=WIDTH,
                         height=HEIGHT,
                         fg_color="#000000",
                         corner_radius=0,
                         )
        self.root = root
        # インターフェース接続
        self.ImageInterface = ImageInterface()
        # dndのバインド
        self.enable_dnd()
        self.draw_dnd_label()
        self.pack_propagate(False)

    # drop時処理: path取得→ open → image更新 → resize → labelで表示(初回でD&Dlabel削除) → ImageInterface
    def drop(self, event: TkinterDnD.DnDEvent):
        image_file_path = event.data[1:-1]  # path取得 両端にある{}除去
        # open, resize, [create]image_labed
        try:
            image = Image.open(image_file_path)
        except Exception as e:
            print(e)
        image = resize_image(image, (WIDTH, HEIGHT))
        self.draw_image_label(image)
        self.ImageInterface.load_image(image,image_file_path,self.image_label,self.root,(WIDTH, HEIGHT))

    def draw_image_label(self,image):
        self.image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(WIDTH, HEIGHT))
        # [update]image_label [del]label
        self.label.destroy()
        self.image_label.destroy()
        self.image_label = customtkinter.CTkLabel(self, image=self.image,text="")
        self.image_label.pack()

    def draw_dnd_label(self):
        # d&d領域にlabel設置、image_labelの仮置き
        self.label = customtkinter.CTkLabel(self.root, text="ここに画像をD&D", text_color="white", fg_color="#000000", font=(None,30))  # LabelをCTkLabelに変更
        self.image_label = customtkinter.CTkLabel(self,text="")
        self.label.place(relx=0.37, rely=0.37, anchor="center")
        
    def enable_dnd(self):
        # tkinterのwrapperであるtkinterdnd2で提供されているメソッドを使用してD&Dを有効化。ウィジェットにdrop時のトリガーをセット
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop)

