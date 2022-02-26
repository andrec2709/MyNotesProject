import sqlite3
from time import time
from random import randint
from kivy.animation import Animation
from kivy.app import App
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ListProperty, ColorProperty, DictProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
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


class DarkModeDDMainButton(ButtonBehavior, Label):
    txt = StringProperty("")

    def __init__(self, **kwargs):
        super(DarkModeDDMainButton, self).__init__(**kwargs)



class DarkModeDD(DropDown):
    def __init__(self, **kwargs):
        super(DarkModeDD, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_select(self, data):
        self.app.back_color = data[0]
        self.app.color_text = data[1]
        self.app.color_text_hint = data[2]


class SettingsPopup(ModalView):
    """Show settings for the app"""
    pass


class DiscardPopup(ModalView):
    pass


class SavePopup(ModalView):
    def save_note(self, title, body, r=0.6196, g=1, b=1, a=1):
        """
        Adds note to the database, and updates the 'notes' attribute from StorageNotes class (update_notes()), which
        updates data for the RecycleView.
        """
        note_id = App.get_running_app().root.children[0].ids.title_input.note_id_num
        con = sqlite3.connect("example.db")
        cur = con.cursor()
        all_ids_db = []

        for rowid in cur.execute("SELECT ROWID FROM notes"):  # Getting all ids from table 'notes'
            all_ids_db.append(rowid[0])

        if note_id not in all_ids_db:
            cur.execute("INSERT INTO notes VALUES ('{}','{}',{},{},{},{});".format(title, body, r, g, b, a))

        else:
            cur.execute("UPDATE notes SET TITLE = '{}', BODY = '{}', R = {}, G = {}, B = {}, A = {} WHERE ROWID = {};"
                        .format(title, body, r, g, b, a, note_id))
        # TODO: Issue: cur.lastrowid returning 0, needs fix
        app = App.get_running_app()
        print(cur.lastrowid)
        app.root.children[0].ids.title_input.note_id_num = cur.lastrowid
        #app.root.children[0].ids.go_back_button.note_id_num = cur.lastrowid

        app.root.children[0].ids.save_button.disabled = False
        cur.close()
        con.commit()
        con.close()

        app.root.get_screen("main").ids.rv.data_model.update_notes()


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
    #title_opened = StringProperty("")
    #body_opened = StringProperty("")
    #note_id_num = NumericProperty(0)

    #def check_inputs(self, title, body, popup):
       # app = App.get_running_app()
       # if title.text != self.title_opened or body.text != self.body_opened:
           # popup.open()
        #else:
          #  app.root.current = "main"
  pass


class SaveButton(ButtonBehavior, Image):
    """
    Saves the changes/new note.
    """


class ViewModeButton(ButtonBehavior, Image):
    """TODO: Call a popup that allows the user to change the note's background color. May change class name aswell.
    """
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

    def on_text(self, instance, value):
        """
        Every time you type in something, it changes the RecycleView data.
        """
        self.app.root.children[0].ids.rv.data_model.data = []
        for note in self.app.root.children[0].ids.rv.data_model.notes:
            if self.text.lower() in note[1].lower():
                self.app.root.children[0].ids.rv.data.append({

                    'text': note[1][:100] if len(note[1]) > 100 else note[1],
                    'full_title': note[1],
                    'size_hint_y': None,
                    'height': dp(90) if len(note[1]) < 100 else dp(120),
                    'id_num': note[0],  # rowid
                    'body_txt': note[2],
                    'bg_color': [note[3], note[4], note[5], note[6]]

                })


class TitleInput(TextInput):
    note_id_num = NumericProperty(0)


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
    go_to_editor = BooleanProperty(True)
    full_title = StringProperty("")

    def __init__(self, **kwargs):
        super(NotesLabel, self).__init__(**kwargs)
        self.bg_color = self.colors_list[randint(0, len(self.colors_list)-1)]['color']
        self.remove_note = RemoveNote(size=self.size, pos=self.pos, on_release=self.remove)
        self.app = App.get_running_app()

    __events__ = ("on_long_press",)
    long_press_time = NumericProperty(.6)

    def collide_point(self, x, y):
        """
        Checks for collide point, if outside it removes the 'remove_note' widget.
        TODO: Needs to fix bug: Clicking outside only works if it's inside the RecycleView.
        """
        if self.pos[0] <= x <= self.pos[0] + self.width and self.pos[1] <= y <= self.pos[1] + self.height:
            return True
        else:
            self.remove_widget(self.remove_note)
            self.go_to_editor = True
            return False

    def remove(self, instance):
        """
        Removes the widget from database and updates the screen calling StorageNotes.update_notes()
        """
        con = sqlite3.connect("example.db")
        cur = con.cursor()
        cur.execute("DELETE FROM notes WHERE ROWID = {};".format(self.id_num))
        cur.close()
        con.commit()
        con.close()
        self.remove_widget(self.remove_note)
        App.get_running_app().root.children[0].ids.rv.data_model.update_notes()


    def on_state(self, instance, value):
        if value == "down":
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self.do_long_press, lpt)
        else:
            self._clockev.cancel()

    def do_long_press(self, dt):
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        self.remove_note.size = self.size
        self.remove_note.pos = self.pos
        self.add_widget(self.remove_note)
        self.go_to_editor = False
        print('long press!')

    def on_release(self):
        if self.go_to_editor:
            self.app.root.current = "note_editor"
            self.app.root.children[0].ids.title_input.text = self.full_title
            self.app.root.children[0].ids.body_input.text = self.body_txt
            self.app.root.children[0].ids.title_input.note_id_num = self.id_num

           # self.app.root.children[0].ids.go_back_button.title_opened = self.full_title
            #self.app.root.children[0].ids.go_back_button.body_opened = self.body_txt
            #self.app.root.children[0].ids.go_back_button.note_id_num = self.id_num
            print(self.id_num)


class RemoveNote(ButtonBehavior, Widget):
    pass


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
                      'full_title': note[1],
                      'size_hint_y': None,
                      'height': dp(90) if len(note[1]) < 100 else dp(120),
                      'id_num': note[0],  # rowid
                      'body_txt': note[2],
                      'bg_color': [note[3], note[4], note[5], note[6]]
                      } for note in self.notes]
        self.cur.close()
        self.con.close()

    def update_notes(self):
        self.notes.clear()

        con = sqlite3.connect("example.db")
        cur = con.cursor()

        for note in cur.execute("SELECT ROWID, * FROM notes"):
            self.notes.append(note)

        self.data = [{'text': note[1][:100] if len(note[1]) > 100 else note[1],
                      'full_title': note[1],
                      'size_hint_y': None,
                      'height': dp(90) if len(note[1]) < 100 else dp(120),
                      'id_num': note[0],  # rowid
                      'body_txt': note[2],
                      'bg_color': [note[3], note[4], note[5], note[6]]
                      } for note in self.notes]
        cur.close()
        con.close()


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data_model = StorageNotes()


class NotesApp(App):
    color_text = ColorProperty([1, 1, 1, 1])
    back_color = ColorProperty(get_color_from_hex("#252525"))
    color_text_hint = ColorProperty(get_color_from_hex("#9A9A9A"))
    setting_mode = StringProperty("Dark")

    def __init__(self, **kwargs):
        super(NotesApp, self).__init__(**kwargs)
        Window.clearcolor = self.back_color

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

    def on_back_color(self, instance, value):
        Window.clearcolor = self.back_color


if __name__ == "__main__":
    NotesApp().run()
