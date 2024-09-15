from application.Widgets.Image_Widgets.ImageWidgets import ImageWidgets
from application.Widgets.Color_Area_Widgets.ColorAreaWidgets import ColorAreaWidgets
from application.Widgets.Tools_Widgets.ToolsWidgets import ToolsWidgets
from application.Widgets.Util_Area.UtilArea import UtilArea
import customtkinter
from tkinterdnd2 import TkinterDnD

customtkinter.set_appearance_mode("System")  # ダークモードとライトモードの自動切替え
customtkinter.set_default_color_theme("blue")  # テーマカラー設定

WIDTH = 1160
HEIGHT = 690

class ColorGrading(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("ColorGrading")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)
        
        # ウィジェットの作成と配置
        self.ImageWidgets = ImageWidgets(root=self)
        self.ImageWidgets.place(x=0, y=0)

        self.ColorAreaWidgets = ColorAreaWidgets(root=self)
        self.ColorAreaWidgets.place(x=896, y=0)

        self.ToolWidgets = ToolsWidgets(root=self)
        self.ToolWidgets.place(x=0, y=504)

        self.UtilArea = UtilArea(root=self,ToolWidgets=self.ToolWidgets)
        self.UtilArea.place(x=896, y=504)

if __name__ == "__main__":
    app = ColorGrading()
    app.mainloop()
