import customtkinter

WIDTH = 264
HEIGHT = 504
# todo
class ColorAreaWidgets(customtkinter.CTkFrame):
    def __init__(self,root):
        super().__init__(root,
                         width=WIDTH,
                         height=HEIGHT,
                         corner_radius=0,
                         )
        self.root = root
