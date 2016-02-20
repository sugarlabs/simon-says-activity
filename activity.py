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
	   
        self.box = Gtk.Box(spacing = 10)
        self.box.set_homogeneous(True)
        self.add(self.box)
        
        #self._collab = CollabWrapper(self)

        #self.texteditor = CollabTextEditor(self, 1, self._collab)
        #self.texteditor2 = CollabTextEditor(self, 2, self._collab)
        #self.box.pack_start(self.texteditor, True, True, 0)
        #self.box.pack_start(self.texteditor2, True, True, 0)
        self.set_canvas(self.box)
        self.box.show()
        #self._collab.setup()

    def start_game(self, widget):
        self.button1 = Gtk.Button(label='Red')
        self.box.pack_start(self.button1, True, True, 0)
        self.button1.show()

