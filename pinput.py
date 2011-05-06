#!/usr/bin/env python

from __future__ import print_function

#import pygtk
#pygtk.require('2.0')
import gtk
import re, subprocess

class GInput:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)
        self.button = gtk.Button('Hello')
        self.window.add(self.button)
        self.xi2_masters = []
        self.button.connect('clicked', self.get_info, self.xi2_masters)
        #self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.window.show_all()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

    def get_info(self, widget, xi2_masters):
        args = ["xinput",  "list",  "--short"]
        p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
        regex = re.compile("^.*id=([0-9]*).*\[(\w+) *(\w+) .*\].*$")
        for line in p.stdout:
            (id, ms, ty) = regex.match(line).group(1,2,3)
            print(id, ms, ty)




if __name__ == "__main__":
    #GInput().main()
    GInput().get_info(None, None)

# vim: set sw=4 et sts=4 :
