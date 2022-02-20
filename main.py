import sqlite3

from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import *
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
#from kivymd.app import MDApp

Window.size = (260, 490)
Window.minimum_width, Window.minimum_height = Window.size


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
        self.app.root.children[0] \
            .ids.notes_list.all_notes \
            .append(('This is a test, to see if '
                     'notes are updating everytime '
                     'all_notes changes its value', ':3', ''))

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

    def on_text(self, instance, value):
        self.app.root.children[0].ids.notes_list.search_notes(self)


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


class NotesLabel(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super(NotesLabel, self).__init__(**kwargs)


class NotesList(BoxLayout):
    """Where all the notes saved are showed"""

    all_notes = ListProperty()

    def __init__(self, **kwargs):
        super(NotesList, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.bind(all_notes=self.add_notes_to_main)
        self.all_notes = self.app.read_notes()
        # print(self.all_notes)

    def test(self):

        self.app.read_notes()

    def add_notes_to_main(self, instance, value):
        """Adds the notes from all_notes attribute to the main screen"""

        self.clear_widgets()

        for row in self.all_notes:
            label = NotesLabel(text=row[0])
            self.add_widget(Widget(size_hint_y=None, height=dp(10)))
            self.add_widget(label)

    def search_notes(self, widget):
        """Shows the notes that contain text from text input"""

        self.clear_widgets()

        for row in self.all_notes:
            if widget.text.lower() in row[0].lower():  # Verifies if text from text input is contained in note text
                label = NotesLabel(text=row[0])
                self.add_widget(Widget(size_hint_y=None, height=dp(10)))
                self.add_widget(label)


class NotesApp(App):
    color_text = ListProperty([1, 1, 1, 1])
    def __init__(self, **kwargs):
        super(NotesApp, self).__init__(**kwargs)
        Window.clearcolor = get_color_from_hex("#252525")
        self.con = sqlite3.connect("example.db")
        self.cur = self.con.cursor()

    def build(self):
        sm = MyScreenManager(transition=SwapTransition())
        sm.add_widget(Main(name="main"))
        sm.add_widget(NoteEditor(name="note_editor"))
        return sm

    def read_notes(self):
        temp = []
        for row in self.cur.execute("SELECT * FROM Notes"):
            temp.append(row)
        # all_notes = temp[:]
        return temp[:]


if __name__ == "__main__":
    NotesApp().run()
