import argparse
import logging
import sys
import os
import sqlite3

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import PyQt5.Qt

from mc import mc_global
from mc.gui import main_win
import mc.model
import mc.db


class MatC:

    def __init__(self, i_matc_qapplication):

        self.main_window = main_win.MbMainWindow()
        self.matc_qapplication = i_matc_qapplication
        self.matc_qapplication.setQuitOnLastWindowClosed(False)


        # System tray
        # Please note: We cannot move the update code into another function, even here in
        # this file (very strange), if we do we won't see the texts, only the separators,
        # unknown why but it may be because of a bug
        self.main_window.tray_icon = QtWidgets.QSystemTrayIcon(
            QtGui.QIcon(mc_global.get_app_icon_path()),
            self.matc_qapplication
        )
        self.main_window.tray_icon.show()
        # self.update_tray_menu()
        if not self.main_window.tray_icon.supportsMessages():
            logging.warning("Your system doesn't support notifications. If you are using MacOS please install growl")

        settings = mc.model.SettingsM.get()

        self.tray_menu = QtWidgets.QMenu(self.main_window)

        self.tray_restore_action = QtWidgets.QAction("Restore")
        self.tray_menu.addAction(self.tray_restore_action)
        self.tray_restore_action.triggered.connect(self.main_window.showNormal)
        self.tray_maximize_action = QtWidgets.QAction("Maximize")
        self.tray_menu.addAction(self.tray_maximize_action)
        self.tray_maximize_action.triggered.connect(self.main_window.showMaximized)
        self.tray_quit_action = QtWidgets.QAction("Quit")
        self.tray_menu.addAction(self.tray_quit_action)
        self.tray_quit_action.triggered.connect(self.main_window.exit_application)

        self.tray_menu.addSeparator()
        mc_global.tray_rest_progress_qaction = QtWidgets.QAction("")
        self.tray_menu.addAction(mc_global.tray_rest_progress_qaction)
        mc_global.tray_rest_progress_qaction.setDisabled(True)
        mc_global.update_tray_rest_progress_bar(0, 1)
        self.tray_rest_now_qaction = QtWidgets.QAction("Take a Break Now")
        self.tray_menu.addAction(self.tray_rest_now_qaction)
        self.tray_rest_now_qaction.triggered.connect(self.main_window.show_rest_reminder)
        mc_global.tray_rest_enabled_qaction = QtWidgets.QAction("Enable Rest Reminder")
        self.tray_menu.addAction(mc_global.tray_rest_enabled_qaction)
        mc_global.tray_rest_enabled_qaction.setCheckable(True)
        mc_global.tray_rest_enabled_qaction.toggled.connect(
            self.main_window.rest_settings_widget.on_switch_toggled
        )
        mc_global.tray_rest_enabled_qaction.setChecked(settings.rest_reminder_active_bool)

        self.tray_menu.addSeparator()
        mc_global.tray_breathing_enabled_qaction = QtWidgets.QAction("Enable Breathing Reminder")
        self.tray_menu.addAction(mc_global.tray_breathing_enabled_qaction)
        mc_global.tray_breathing_enabled_qaction.setCheckable(True)
        mc_global.tray_breathing_enabled_qaction.setChecked(settings.breathing_reminder_active_bool)
        mc_global.tray_breathing_enabled_qaction.toggled.connect(
            self.main_window.breathing_settings_widget.on_switch_toggled
        )
        mc_global.tray_breathing_enabled_qaction.setDisabled(True)

        self.main_window.tray_icon.setContextMenu(self.tray_menu)



