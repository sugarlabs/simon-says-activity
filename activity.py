"""SimonSays Activity: An implementation of the simon-says game"""

from gi.repository import GObject
from gi.repository import Gtk 
from gi.repository import Gdk 
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

#Style the different elements and widgets using CSS
#With the help of Gtk css style providers

style_provider = Gtk.CssProvider()

#This is the css file that is being used by Gtk
css = """
    #button1 {
        background-color: #FF0000;
    }
    #button2 {
        background-color: #00FF00;
    }
    #button3 {
        background-color: #FFFF00;
    }
    #button4 {
        background-color: #0000FF;
    }
"""

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
        self.title.show()
        self.grid.attach(self.title,0,0,6,1)

        #self._collab = CollabWrapper(self)

        #self.texteditor = CollabTextEditor(self, 1, self._collab)
        #self.texteditor2 = CollabTextEditor(self, 2, self._collab)
        #self.box.pack_start(self.texteditor, True, True, 0)
        #self.box.pack_start(self.texteditor2, True, True, 0)
        self.set_canvas(self.grid)
        self.grid.show()
        #self._collab.setup()

    def start_game(self, widget):
        self.button1 = Gtk.Button(label='Red')
        self.button1.set_name('button1')
        self.button1.show()
        self.button2 = Gtk.Button(label='Green')
        self.button2.set_name('button2')
        self.button2.show()
        self.button3 = Gtk.Button(label='Blue')
        self.button3.set_name('button3')
        self.button3.show()
        self.button4 = Gtk.Button(label='Yellow')
        self.button4.set_name('button4')
        self.button4.show()

        self.grid.attach(self.button1,0,3,3,3)
        self.grid.attach(self.button2,3,3,3,3)
        self.grid.attach(self.button3,0,6,3,3)
        self.grid.attach(self.button4,3,6,3,3)

