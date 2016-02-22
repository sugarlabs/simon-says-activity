"""SimonSays Activity: An implementation of the simon-says game"""

from gi.repository import GObject
from gi.repository import Gtk 
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Pango
import logging

from gettext import gettext as _

#from sugar3.presence.wrapper import CollabWrapper

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.icon import Icon
#from sugar3.graphics.texteditor import CollabTextEditor

from gameloader import GameLoader
import time

#Style the different elements and widgets using CSS
#With the help of Gtk css style providers
style_provider = Gtk.CssProvider()

#This is the css that is being used by Gtk
button_style1 = """ #button1 { background-color: #FF3333; } """
button_style2 = """ #button2 { background-color: #00E64D; } """
button_style3 = """ #button3 { background-color: #FFD636; } """
button_style4 = """ #button4 { background-color: #4DA6FF; } """

button_style_hover1 = """ #button1 { background-color: #E60000; } """
button_style_hover2 = """ #button2 { background-color: #00B300; } """
button_style_hover3 = """ #button3 { background-color: #E6B800; } """
button_style_hover4 = """ #button4 { background-color: #007ACC; } """

#Loads the css specified
def load_css(css):
    style_provider.load_from_data(css)

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), 
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

class SimonSaysActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        
        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        self.gameLoader = GameLoader()
        self.userInput = False

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        description_item = DescriptionItem(self)
        toolbar_box.toolbar.insert(description_item, -1)
        description_item.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()
        
        execute_button = ToolButton('run-icon')
        toolbar_box.toolbar.insert(execute_button, -1)
        execute_button.connect("clicked", self.start_game)
        execute_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
	   
        self.grid = Gtk.Grid(column_homogeneous=True,row_homogeneous=True,column_spacing=20,row_spacing=20)
        self.add(self.grid)
        
        self.title = Gtk.Label('Simon-Says')
        self.title.modify_font(Pango.FontDescription("sans 32"))
        self.title.show()
        self.grid.attach(self.title,0,0,8,1)

        self.score = Gtk.Label('')
        self.score.modify_font(Pango.FontDescription("sans 18"))
        self.score.show()
        self.grid.attach(self.score,0,1,8,1)

        self.set_canvas(self.grid)
        self.grid.show()

    def start_game(self, widget):
        self.button1 = Gtk.Button(label='Red')
        self.button1.set_name('button1')
        self.button1.connect("clicked", self.button_clicked, "Red")
        self.button1.show()
        self.button2 = Gtk.Button(label='Green')
        self.button2.set_name('button2')
        self.button2.connect("clicked", self.button_clicked, "Green")
        self.button2.show()
        self.button3 = Gtk.Button(label='Yellow')
        self.button3.set_name('button3')
        self.button3.connect("clicked", self.button_clicked, "Yellow")
        self.button3.show()
        self.button4 = Gtk.Button(label='Blue')
        self.button4.set_name('button4')
        self.button4.connect("clicked", self.button_clicked, "Blue")
        self.button4.show()

        css = button_style1 + button_style2 + button_style3 + button_style4
        load_css(css)
        
        self.score.set_text(str(self.gameLoader.get_score()))
        self.grid.attach(self.button1,0,4,4,4)
        self.grid.attach(self.button2,4,4,4,4)
        self.grid.attach(self.button3,0,8,4,4)
        self.grid.attach(self.button4,4,8,4,4)
        
        self.play_animation()

    def button_clicked(self, widget, button_name):
        self.score.set_text(str(self.gameLoader.get_score()))
        if self.userInput == False:
            return
        self.display_color(button_name)
        GLib.timeout_add(250, self.display_color, 'None')
        button_required = self.gameLoader.get_current_button()
        if button_name == button_required:
            self.gameLoader.go_to_next_button()
            if self.gameLoader.sequence_end():
                self.gameLoader.next_level()
                self.play_animation()
        else:
            self.gameLoader.reset_game()
            self.play_animation()
        self.score.set_text(str(self.gameLoader.get_score()))

    def allow_player(self):
        self.userInput = True

    def display_color(self, button):
        css = button_style1 + button_style2 + button_style3 + button_style4
        load_css(css)
        if button == 'Red':
            css = button_style_hover1 + button_style2 + button_style3 + button_style4
            load_css(css)
        elif button == 'Green':
            css = button_style1 + button_style_hover2 + button_style3 + button_style4
            load_css(css)
        elif button == 'Yellow':
            css = button_style1 + button_style2 + button_style_hover3 + button_style4
            load_css(css)
        elif button == 'Blue':
             css = button_style1 + button_style2 + button_style3 + button_style_hover4
             load_css(css)

    def play_animation(self):
        cnt = 0
        self.userInput = False
        sequence = self.gameLoader.get_sequence_list()
        for button in sequence:
            cnt += 1
            GLib.timeout_add(1000*cnt, self.display_color, button)
            GLib.timeout_add(1000*cnt+800, self.display_color, 'None')
        cnt += 1
        GLib.timeout_add(1000*cnt, self.display_color, 'None')
        GLib.timeout_add(1000*cnt, self.allow_player)

