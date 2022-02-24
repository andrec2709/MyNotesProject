import sqlite3
from random import randint
from kivy.animation import Animation
from kivy.app import App
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ListProperty, ColorProperty, DictProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView, RecycleDataModel
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import *
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
#from kivymd.app import MDApp

#Window.size = (260, 490)
#Window.minimum_width, Window.minimum_height = Window.size
Window.softinput_mode = "below_target"


class SettingsPopup(ModalView):
    """Show settings for the app"""
    pass


class DiscardPopup(ModalView):
    pass


class SavePopup(ModalView):
    pass


class DiscardButton(Button):
    pass


class KeepButton(Button):
    pass


class AddButton(ButtonBehavior, Image):
    def collide_point(self, x, y):
        if self.pos[0] - dp(7.5) <= x <= self.pos[0] + self.width + dp(7.5):
            if self.pos[1] - dp(7.5) <= y <= self.pos[1] + self.height + dp(7.5):
                return True
        return False


class SearchButton(ButtonBehavior, Image):
    """Button that shows the Search Bar"""

    def __init__(self, **kwargs):
        super(SearchButton, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def collide_point(self, x, y):
        if self.pos[0] - dp(10) <= x <= self.pos[0] + self.width + dp(10):
            if self.pos[1] - dp(10) <= y <= self.pos[1] + self.height + dp(10):
                return True
        return False

    def test(self):
        self.app.root.children[0].ids.rv.data.append({'text': 'this is a test.'})

    def call_search_bar(self, closbtn, sbtn, lbl, toolbar, main_page, sbar):
        if sbar.opacity == 0.0:
            sbtn.opacity = 0
            sbtn.disabled = True
            closbtn.opacity = 1
            closbtn.disabled = False
            lbl.opacity = 0
            self.opacity = 0
            self.disabled = True
            sbar.children[1].focus = True
            pos = [main_page.center_x - sbar.width/2.0, main_page.height - sbar.height/2.0 - toolbar.height + toolbar.padding[3]]
            anim = Animation(opacity=1.0, width=toolbar.width, pos=pos, x=dp(0)+main_page.ids.wrap_box.padding[0], d=.1)
            anim.start(sbar)


class SettingsButton(ButtonBehavior, Image):
    """Button that pops up settings screen"""

    def collide_point(self, x, y):
        if self.pos[0] - dp(10) <= x <= self.pos[0] + self.width + dp(10):
            if self.pos[1] - dp(10) <= y <= self.pos[1] + self.height + dp(10):
                return True
        return False


class GoBackButton(ButtonBehavior, Image):
    pass


class SaveButton(ButtonBehavior, Image):
    pass


class ViewModeButton(ButtonBehavior, Image):
    pass


class SearchBar(ButtonBehavior, Widget):
    """Bar for searching the notes"""
    pass


class CloseButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(CloseButton, self).__init__(**kwargs)

    def close_search_bar(self, searbtn, setbtn, lbl, toolbar, main_page, sbar):
        if sbar.opacity == 1.0:
            setbtn.opacity = 1
            setbtn.disabled = False
            lbl.opacity = 1
            self.opacity = 0
            self.disabled = True
            searbtn.opacity = 1
            searbtn.disabled = False
            sbar.children[1].focus = False
            sbar.children[1].text = ""
            pos = [main_page.center_x - sbar.width / 2.0,
                   main_page.height - sbar.height / 2.0 - toolbar.height + toolbar.padding[3]]
            anim = Animation(opacity=0.0, width=0, d=.1)
            anim.start(sbar)


class SearchInput(TextInput):
    """TextInput from the search bar"""
    def __init__(self, **kwargs):
        super(SearchInput, self).__init__(**kwargs)
        self.app = App.get_running_app()

    #def on_text(self, instance, value):
        #self.app.root.children[0].ids.notes_list.search_notes(self)

    def on_text(self, instance, value):
        self.app.root.children[0].ids.rv.data = []
        for note in self.app.root.children[0].ids.rv.data_model.notes:
            if self.text.lower() in note[1].lower():
                self.app.root.children[0].ids.rv.data.append({'text': note[1],
                                                              'id_num': note[0],
                                                              'body_txt': note[2]})


class TitleInput(TextInput):
    pass


class BodyTextInput(TextInput):
    def __init__(self, **kwargs):
        super(BodyTextInput, self).__init__(**kwargs)


class MyScreenManager(ScreenManager):
    """Class for managing screens."""
    pass


class Main(Screen):
    """Main Screen"""

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)

    def test(self):
        print(App.get_running_app().reading())


class NoteEditor(Screen):
    """Screen where user edit notes"""
    pass


class NotesLabel(RecycleDataViewBehavior, ButtonBehavior, Label):
    colors_list = ListProperty([#{'color': [252/255, 186/255, 3/255], 'font_color': [0, 0, 0]},
                                {'color': [253/255, 153/255, 255/255], 'font_color': [0, 0, 0]},
                                {'color': [255/255, 158/255, 158/255], 'font_color': [0, 0, 0]},
                                {'color': [145/255, 244/255, 143/255], 'font_color': [0, 0, 0]},
                                {'color': [158/255, 255/255, 255/255], 'font_color': [0, 0, 0]},
                                {'color': [182/255, 156/255, 255/255], 'font_color': [0, 0, 0]},
                                {'color': [255/255, 245/255, 153/255], 'font_color': [0, 0, 0]},
                                ])
    bg_color = ColorProperty()

    def __init__(self, **kwargs):
        super(NotesLabel, self).__init__(**kwargs)
        self.bg_color = self.colors_list[randint(0, len(self.colors_list)-1)]['color']


class StorageNotes(RecycleDataModel):
    notes = ListProperty()  # Stores tuples that represent notes == (ROWID, Title, Body Text, [r,g,b,a])
    default_bg_color = ColorProperty([0.6196, 1, 1, 1])
    def __init__(self, **kwargs):
        super(StorageNotes, self).__init__(**kwargs)
        self.recycleview = RV
        self.app = App.get_running_app()
        self.con = sqlite3.connect("example.db")
        self.cur = self.con.cursor()
        print(self.default_bg_color)
        for note in self.cur.execute("SELECT ROWID, * FROM notes"):
            self.notes.append(note)

        self.data = [{'text': note[1][:100] if len(note[1]) > 100 else note[1],
                      'size_hint_y': None,
                      'height': dp(90) if len(note[1]) < 100 else dp(120),
                      'id_num': note[0],  # rowid
                      'body_txt': note[2],
                      'bg_color': [note[3], note[4], note[5], note[6]]
                      } for note in self.notes]
        self.con.close()


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data_model = StorageNotes()


class NotesApp(App):
    color_text = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(NotesApp, self).__init__(**kwargs)
        Window.clearcolor = get_color_from_hex("#252525")

    def build(self):
        sm = MyScreenManager(transition=SwapTransition())
        sm.add_widget(Main(name="main"))
        sm.add_widget(NoteEditor(name="note_editor"))
        return sm

    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27 and self.root.current == "note_editor":
            self.root.current = "main"
            return True


if __name__ == "__main__":
    NotesApp().run()
