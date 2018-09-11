"""
Module to provide exploration credit tracking.
"""

import json
import Tkinter as tk
import sys
import zlib

import plugin
import xmit

import myNotebook as nb


SHOW_EXPLORATION_VALUE = 'ShowExploValue'


class ExplorationPlugin(plugin.HuttonHelperPlugin):
    "Tracks exploration data gathering."

    def __init__(self, config):
        "Initialise the ``ExplorationPlugin``."

        plugin.HuttonHelperPlugin.__init__(self, config)
        self.frame = None
        self.__reset(cmdr=None)

    def __reset(self, cmdr=None):
        "Reset the ``ExplorationPlugin``."

        self.credits = None
        self.cmdr = cmdr

    @property
    def ready(self):
        "Are we ready?"

        return self.credits is not None

    def plugin_app(self, parent):
        "Called once to get the plugin widget. Return a ``tk.Frame``."

        # An additional internal frame that we can grid_forget if disabled:
        frame = self.frame = tk.Frame(parent)
        frame.columnconfigure(1, weight=1)

        self.textvariable = tk.StringVar()
        self.textvariable.set("(Waiting...)")
        tk.Label(frame, text="UNSOLD exploration credits:", anchor=tk.NW).grid(row=0, column=0, sticky=tk.NW)
        tk.Label(frame, textvariable=self.textvariable, anchor=tk.NE).grid(row=0, column=1, sticky=tk.NE)

        enabled = self.config.getint(SHOW_EXPLORATION_VALUE)
        self.enabled_var = tk.IntVar(value=enabled)
        self.__update_hidden()

        return self.frame

    def plugin_prefs(self, parent, cmdr, is_beta):
        "Called each time the user opens EDMC settings. Return an ``nb.Frame``."

        prefs_frame = nb.Frame(parent)
        prefs_frame.columnconfigure(0, weight=1)

        nb.Label(prefs_frame, text="Exploration Display Options :-").grid(row=0, column=0, sticky=tk.W)
        nb.Checkbutton(
            prefs_frame,
            text="Show UNSOLD Exploration Credits",
            variable=self.enabled_var
        ).grid(row=1, column=0, sticky=tk.W)

        self.prefs_changed(cmdr, is_beta)
        return prefs_frame

    def prefs_changed(self, cmdr, is_beta):
        "Called when the user clicks OK on the settings dialog."

        self.config.set(SHOW_EXPLORATION_VALUE, self.enabled_var.get())
        self.__update_hidden()

    def __update_hidden(self):
        "Update our ``hidden`` flag."
        self.hidden = not self.enabled_var.get()

    def journal_entry(self, cmdr, _is_beta, _system, _station, entry, _state):
        "Act like a tiny EDMC plugin."

        if cmdr != self.cmdr:
            self.__reset(cmdr=cmdr)

        if entry['event'] == 'Scan' or not self.ready:
            self.__check_again()

    def cmdr_data(self, data, is_beta):
        "Act like a tiny EDMC plugin."

        cmdr = data.get('commander').get('name')
        self.__reset(cmdr=cmdr)
        self.__check_again()

    def __check_again(self):
        "Called when we need to check again."

        if self.frame:
            self.frame.after_idle(self.__check_again_action)
        else:
            self.__check_again_action()

    def __check_again_action(self):
        "Get and display exploration credits."

        path = '/explocredit.json/{}'.format(self.cmdr)
        json_data = xmit.get(path)
        self.credits = float(json_data['ExploCredits'])

        if self.textvariable:
            self.textvariable.set("{:,.0f}".format(self.credits))

        self.refresh()
