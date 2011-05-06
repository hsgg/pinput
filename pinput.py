#!/usr/bin/env python
# 2011 Henry Gebhardt <hsggebhardt@googlemail.com>

from __future__ import print_function

#import pygtk
#pygtk.require('2.0')
import gtk
import re, subprocess

debug = 1
def dbg(args):
    if debug == 1:
        print(' '.join(args))

class PInput:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(15)
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)
        self.create_button_box()
        self.window.show_all()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

    def create_button_box(self):
        args = ["xinput",  "list",  "--short"]
        p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
        dbg(args)
        regex = re.compile("^(.*)\s*id=([0-9]*).*\[(\w+) *(\w+) .*\].*$")
        self.vbox = gtk.VBox()
        for line in p.stdout:
            line = line.strip()
            (na, id, ms, ty) = regex.match(line).group(1,2,3,4)
            l = gtk.Label(na + "    id=" + id + " (" + ms + " " + ty + ")  ")
            b = gtk.Button(self.get_status(id))
            b.connect('clicked', self.toggle_device, id)
            h = gtk.HBox()
            h.add(l)
            h.add(b)
            self.vbox.add(h)
            #print(id, ms, ty)
        self.window.add(self.vbox)

    def get_status(self, id):
        args = ["xinput", "list-props", str(id)]
        p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
        dbg(args)
        regex_state = re.compile("^\s*Device Enabled \(([0-9]*)\):\s*([0-9])$")
        line = p.stdout.next().strip()
        line = p.stdout.next().strip()
        (prop, enabled) = regex_state.match(line).group(1, 2)
        if int(enabled) == 0:
            return "Disabled"
        else:
            return "Enabled"

    def toggle_device(self, widget, id):
        args = ["xinput", "list-props", str(id)]
        p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
        dbg(args)
        regex_state = re.compile("^\s*Device Enabled \(([0-9]*)\):\s*([0-9])$")
        line = p.stdout.next().strip()
        line = p.stdout.next().strip()
        (prop, enabled) = regex_state.match(line).group(1, 2)
        if int(enabled) == 0:
            enabled = 1
        else:
            enabled = 0
        args = ["xinput", "set-int-prop", str(id), str(prop), "8", str(enabled)]
        p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
        dbg(args)
        widget.set_label(self.get_status(id))
        widget.show()


if __name__ == "__main__":
    PInput().main()

# vim: set sw=4 et sts=4 :
