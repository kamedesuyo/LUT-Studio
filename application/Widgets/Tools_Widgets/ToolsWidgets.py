import customtkinter
from application.Image_Interface.ImageInterface import ImageInterface
from typing import Literal
from CTkMessagebox import CTkMessagebox

WIDTH = 896
HEIGHT = 186

class ToolsWidgets(customtkinter.CTkFrame):
    def __init__(self,root):
        super().__init__(master=root,
                         width=WIDTH,
                         height=HEIGHT,
                         corner_radius=0,
                         )
        self.root = root
        # インターフェース接続
        self.ImageInterface = ImageInterface()
        # 初期値
        self.current_option = customtkinter.IntVar(value=0)
        self._sliders_list = []
        self._value_labels_list = []  # スライダーの値表示用のラベルを管理

        # slider info 初期化
        self.setting_slider_info()

        # 描画関連
        self.grid_propagate(False)
        self.draw_tools()

    # slider_infoの作成
    def setting_slider_info(self):
        self.options = {
            0:"Saturation",
            1:"Contrast",
            2:"Gamma",
            3:"Offset",
        }

        self._slider_id = ["R","G","B","Y"]
        Saturation_slider_values = {id:customtkinter.DoubleVar() for id in self._slider_id}
        Contrast_slider_values = {id:customtkinter.DoubleVar() for id in self._slider_id}
        Gamma_slider_values = {id:customtkinter.DoubleVar() for id in self._slider_id}
        Offset_slider_values = {id:customtkinter.DoubleVar() for id in self._slider_id}

        self.slider_values = {
            0:Saturation_slider_values,
            1:Contrast_slider_values,
            2:Gamma_slider_values,
            3:Offset_slider_values,
        }

    # radioButton(optionButton)の配置
    def draw_tools(self):
        y = 35
        x = 20
        pady = 30
        for i,(option_id,option) in enumerate(self.options.items()):
            _button = customtkinter.CTkRadioButton(
                self,
                text=option,
                variable=self.current_option,
                value=option_id,
                command=self.reload_slider,
            )
            _button.place(x=x, y=y + pady * i)
            if i == 0:
                _button.invoke(True)

    # オプションごとのslider描画
    def reload_slider(self):
        self.draw_sliders(self.slider_values[self.get_current_option_id()])
    
    # slider_valuesのvalueを受け取りsliderに適応、値ラベル共に描画
    def draw_sliders(self, slider_values: dict):
        # スライダーとラベルを削除
        for slider in self._sliders_list:
            slider.destroy()
        for label in self._value_labels_list:
            label.destroy()

        x = 150
        y = 35
        padx = 100
        self._sliders_list = []
        self._value_labels_list = []

        # スライダー要素の作成(reset,slider,label)
        for i, (color, val) in enumerate(slider_values.items()):
            
            # スライダーの値をリセットするボタン
            button = customtkinter.CTkButton(self,text="reset",width=10,height=10,command=lambda color=color: self.reset_slider_value(color))
            button.place(x=x + padx * i-10, y=10)  # スライダーの上に配置

            slider = customtkinter.CTkSlider(
                self,
                corner_radius=0,
                button_corner_radius=1,
                button_length=7,
                from_=-1,
                to=1,
                height=120,
                variable=val,
                orientation="vertical",
                command=lambda value, c=color, v=val: self.update(c, v),
            )
            slider.place(x=x + padx * i, y=y)
            self._sliders_list.append(slider)

            # スライダーの値を表示するラベル
            label = customtkinter.CTkLabel(self, text=f"{color}: {val.get():.2f}")
            # スライダーの下に配置
            label.place(x=x + padx * i-10, y=y + 120) 
            self._value_labels_list.append(label)

    # sliderの値をリセット
    def reset_slider_value(self,color):
        slider_value = self.slider_values[self.get_current_option_id()][color]
        slider_value.set(0)
        self.update(color,slider_value)

    # スライダーの値が変わるたびにラベルを更新, ここで画像処理が走る
    def update(self, color, variable):
        for label in self._value_labels_list:
            if label.cget("text").startswith(f"{color}:"):
                label.configure(text=f"{color}: {variable.get():.2f}")
                self.ImageInterface.apply_filter(color,self.get_current_option_id(),variable.get())
                
    # すべてのスライダーをリセット
    def reset_all_sliders(self):
        for sliders in self.slider_values.values():
            for slider in sliders.values():
                slider.set(0)
    # 現在のオプションの全てのスライダーをリセット
    def reset_all_current_sliders(self):
        sliders = self.slider_values[self.get_current_option_id()]
        for value in sliders.values():
            value.set(0)

    # 外部呼び出し
    def get_current_option_id(self) -> int:
        return self.current_option.get()
    
    def get_current_option_name(self) -> str:
        return self.options[self.current_option.get()]

    def get_optionid2name(self,id):
        return self.options[id]

    def get_slider_values(self)->list:
        sliders = []
        for op_id, sliders in self.slider_values.items():
            for color, slider in sliders.items():
                sliders.append(slider)
        return sliders
    
    def print_slider_values(self):
        for op_id, sliders in self.slider_values.items():
            print(self.options[op_id])
            for color, slider in sliders.items():
                print(f"{color}: {slider.get():.2f}")
    # 引数でリセットスコープを指定
    def check_reset(self,reset_scope:Literal["All","CurrentOption"]):
        # scopeによって変更
        match reset_scope:
            case "All":
                reset = self.reset_all_sliders
                message = f"パラメータを全てリセットしますか？"
            case "CurrentOption":
                reset =self.reset_all_current_sliders
                message = f"{self.get_current_option_name()}のパラメータをリセットしますか？"
        
        msg = CTkMessagebox(title="確認", message=message,icon="question", option_1="キャンセル",option_2="はい")
        response = msg.get()
        if response=="はい":
            reset()
            self.reload_slider()
            CTkMessagebox(title="Info", message="リセットしました。")
        else:
            CTkMessagebox(title="Info", message="リセットをキャンセルしました。")
            