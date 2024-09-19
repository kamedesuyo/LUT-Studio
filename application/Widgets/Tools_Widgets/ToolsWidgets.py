import customtkinter
from application.Image_Interface.ImageInterface import ImageInterface
from typing import Literal
from CTkMessagebox import CTkMessagebox

WIDTH = 896
HEIGHT = 186

class ToolsWidgets(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(master=root, width=WIDTH, height=HEIGHT, corner_radius=0)
        self.root = root
        # インターフェース接続
        self.ImageInterface = ImageInterface()
        # 初期値
        self.current_option = customtkinter.IntVar(value=0)
        self._sliders_list = []
        self._value_labels_dict = {}  # スライダーの値表示用のラベルを辞書で管理
        self._reset_button_list = []

        # slider info 初期化
        self.setting_slider_info()

        # 描画関連
        self.grid_propagate(False)
        self.draw_tools()

    # slider_infoの作成
    def setting_slider_info(self):
        self.options = {
            0: "Saturation",
            1: "Contrast",
            2: "Gamma",
        }

        self._slider_id = ["R", "G", "B", "Y"]
        self.slider_values = {
            0: {id: customtkinter.DoubleVar(value=1) for id in self._slider_id},
            1: {id: customtkinter.DoubleVar(value=1) for id in self._slider_id},
            2: {id: customtkinter.DoubleVar(value=1) for id in self._slider_id},
        }

    # radioButton(optionButton)の配置
    def draw_tools(self):
        y, x, pady = 35, 20, 30
        for i, (option_id, option) in enumerate(self.options.items()):
            _button = customtkinter.CTkRadioButton(
                self, text=option, variable=self.current_option,
                value=option_id, command=self.reload_slider
            )
            _button.place(x=x, y=y + pady * i)
            if i == 0:
                _button.invoke(True)

    # オプションごとのslider描画 apply_fillter
    def reload_slider(self):
        self.ImageInterface.apply_filter(self.slider_values)
        self.draw_sliders(self.slider_values[self.get_current_option_id()])

    # slider_valuesのvalueを受け取りsliderに適応、値ラベル共に描画
    def draw_sliders(self, slider_values: dict):
        # スライダーとラベルを削除
        self.clear_widgets()

        # スライダー要素の作成(reset,slider,label)
        for i, (color, val) in enumerate(slider_values.items()):
            # スライダーの値をリセットするボタン
            button = customtkinter.CTkButton(self, text="reset", width=10, height=10,
                                             command=lambda color=color: self.reset_slider_value(color))
            self._reset_button_list.append(button)

            slider = customtkinter.CTkSlider(
                self, corner_radius=0, button_corner_radius=1, button_length=7,
                from_=0.1, to=3.0, height=120, variable=val, orientation="vertical",
                command=lambda value, c=color, v=val: self.update(c, v)
            )
            self._sliders_list.append(slider)

            # スライダーの値を表示するラベル
            label = customtkinter.CTkLabel(self, text=f"{color}: {val.get():.2f}")
            self._value_labels_dict[color] = label

            # スライダーとリセットボタンの配置
            self.place_widgets(button, slider, label, i)

            # オプション「Saturation」の場合は1スライダーだけ
            if self.get_current_option_id() == 0:
                break

    # ウィジェットの配置
    def place_widgets(self, button, slider, label, i, x_offset=150, y=35, padx=100):
        x_pos = x_offset + padx * i
        button.place(x=x_pos - 10, y=10)  # スライダーの上に配置
        slider.place(x=x_pos, y=y)
        label.place(x=x_pos - 10, y=y + 120)

    # ウィジェットのクリア
    def clear_widgets(self):
        for slider in self._sliders_list:
            slider.destroy()
        self._sliders_list.clear()

        for label in self._value_labels_dict.values():
            label.destroy()
        self._value_labels_dict.clear()

        for button in self._reset_button_list:
            button.destroy()
        self._reset_button_list.clear()

    # スライダーの値が変わるたびにラベルを更新, ここで画像処理が走る
    def update(self, color, variable):
        if color in self._value_labels_dict:
            label = self._value_labels_dict[color]
            label.configure(text=f"{color}: {variable.get():.2f}")
        self.ImageInterface.filter(color, self.get_current_option_id(), self.slider_values[self.get_current_option_id()])

    # sliderの値をリセット
    def reset_slider_value(self, color, op_id=None):
        op_id = op_id if op_id is not None else self.get_current_option_id()
        slider_value = self.slider_values[op_id][color]
        slider_value.set(1)
        self.update(color, slider_value)
        self.ImageInterface.apply_filter(self.slider_values)

    # すべてのスライダーをリセット
    def reset_all_sliders(self):
        for op_id, sliders in self.slider_values.items():
            for color in sliders.keys():
                self.reset_slider_value(color, op_id)
        self.ImageInterface.apply_filter(self.slider_values)

    # 現在のオプションの全てのスライダーをリセット
    def reset_all_current_sliders(self):
        for color in self._slider_id:
            self.reset_slider_value(color)
        self.ImageInterface.apply_filter(self.slider_values)

    # 外部呼び出し
    def get_current_option_id(self) -> int:
        return self.current_option.get()

    def get_current_option_name(self) -> str:
        return self.options[self.current_option.get()]

    def get_optionid2name(self, id):
        return self.options[id]

    def get_slider_values(self) -> list:
        return [slider for sliders in self.slider_values.values() for slider in sliders.values()]

    def print_slider_values(self):
        for op_id, sliders in self.slider_values.items():
            print(self.options[op_id])
            for color, slider in sliders.items():
                print(f"{color}: {slider.get():.2f}")

    # 引数でリセットスコープを指定
    def check_reset(self, reset_scope: Literal["All", "CurrentOption"]):
        reset, message = (self.reset_all_sliders, "パラメータを全てリセットしますか？") if reset_scope == "All" else (self.reset_all_current_sliders, f"{self.get_current_option_name()}のパラメータをリセットしますか？")

        msg = CTkMessagebox(title="確認", message=message, icon="question", option_1="キャンセル", option_2="はい")
        response = msg.get()
        if response == "はい":
            reset()
            self.reload_slider()
            CTkMessagebox(title="Info", message="リセットしました。")
        else:
            CTkMessagebox(title="Info", message="リセットをキャンセルしました。")
