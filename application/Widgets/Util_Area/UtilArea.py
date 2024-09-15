import customtkinter

WIDTH = 264
HEIGHT = 186

class UtilArea(customtkinter.CTkFrame):
    def __init__(self,root,ToolWidgets):
        super().__init__(root,
                         width=WIDTH,
                         height=HEIGHT,
                         corner_radius=0,
                         fg_color="#555555")
        self.root = root
        self.ToolWidgets = ToolWidgets
        self.propagate(False)
        self.draw_output_button()
        self.draw_reset_button()
        self.draw_all_reset_button()

    # todo 外部出力
    def draw_output_button(self):
        x = 150
        y = 130
        button = customtkinter.CTkButton(
            self,
            text="出力",
            width= 100,
            command=lambda:self.ToolWidgets.print_slider_values()
        )
        button.place(x=x,y=y)

    def draw_all_reset_button(self):
        x = 20
        y = 130
        button = customtkinter.CTkButton(
            self,
            text="全てリセット",
            width= 100,
            command=lambda:self.ToolWidgets.check_reset("All")
        )
        button.place(x=x,y=y)

    def draw_reset_button(self):
        x = 20
        y = 50
        button = customtkinter.CTkButton(
            self,
            text="リセット",
            width= 100,
            command=lambda:self.ToolWidgets.check_reset("CurrentOption")
        )
        button.place(x=x,y=y)