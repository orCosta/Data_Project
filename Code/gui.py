from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
import pyperclip
from Code.recipes_finder import suggest_recipes
import pandas as pd


inputs = []
dp_btns = []
supported_ings = pd.read_csv("../Data/New Data/new_foods_short.csv")
supported_ings = list(supported_ings['normalized_name'].values)
class DropBut(Button):
    def __init__(self, **kwargs):
        super(DropBut, self).__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()
        self.picked = False
        self.id = self.get_id()

        for ing in supported_ings:
            btn = Button(text=ing, size_hint_y=None, height=25)
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))
            self.drop_list.add_widget(btn)

        self.bind(on_release=self.drop_list.open)
        self.drop_list.bind(on_select=self.pick_ing)

    def get_id(self):
        dp_btns.append(True)
        return str(len(dp_btns) - 1)

    def pick_ing(self, instance, x):
        setattr(self, 'text', x)
        if not self.picked:
            inputs.append(x)
            self.picked = True
        else:
            inputs[int(self.id)] = x
        print(inputs)


class Search(Button):
    def __init__(self, **kwargs):
        super(Search, self).__init__(**kwargs)
        self.searching = False
        self.bind(on_release=self.search_recipes)

    def create_results_popup(self, results):
        layout_popup = GridLayout(cols=1, spacing=10, size_hint=(1, None), padding=[0,60,0,0])
        layout_popup.bind(minimum_height=layout_popup.setter('height'))

        self.exit_popup = Button(text="Return to Home Screen", size_hint=(0.1, None), background_color=[0.1,0.6,0.9,1])
        layout_popup.add_widget(self.exit_popup)
        for res, URL in results:
            label_i = Button(text=res + URL, size_hint=(1, None))
            label_i.bind(on_release=lambda _, url=URL:pyperclip.copy(url))
            layout_popup.add_widget(label_i)

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout_popup)
        return Popup(title='Results - click to copy URL to clipboard', content=root, size_hint=(1, 1))

    def search_recipes(self, instance):
        if not self.searching:
            self.searching = True
            setattr(self, 'text', "Searching...")
            print("Searching...")
            results = suggest_recipes(inputs)
            popup = self.create_results_popup(results)
            popup.open()
            self.exit_popup.bind(on_release=lambda _: self.reset(popup))
        else:
            pass

    def reset(self, popup):
        popup.dismiss()
        self.searching = False
        setattr(self, 'text', "Find My Next Dish")


class WelcomeScreen(Widget):
    pass


class ChefApp(App):
    def build(self):
        return WelcomeScreen()

if __name__ == '__main__':
    ratio = (9, 16)
    size = 70
    height = size * ratio[0]
    width = size * ratio[1]

    Window.size = (width, height)

    ChefApp().run()
