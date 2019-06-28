"""The main TyTan application module"""
import gi
import jupyter
import os
import sys

gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, WebKit2, GLib


# setup WebkitWebView alias for glade
WebkitWebView = WebKit2.WebView
WebKitSettings = WebKit2.Settings

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

TITAN_GLADE_FILE = resource_path('tytan-ui.glade')


class App(object):
    """TyTan Application"""

    def __init__(self):
        builder = Gtk.Builder.new_from_file(TITAN_GLADE_FILE)

        # objects (typed to get completion)
        self.main_window: Gtk.ApplicationWindow = builder.get_object('main-window')
        self.webview: WebkitWebView = builder.get_object('jupyter-view')
        self.conda_install_dialog: Gtk.Dialog = builder.get_object('conda-install-dialog')
        self.conda_buff: Gtk.TextBuffer = builder.get_object('conda-out')
        self.conda_box: Gtk.TextView = builder.get_object('conda-install-box')
        self.done_button: Gtk.Button = builder.get_object('install-done-button')
        self.loading_image: Gtk.Image = builder.get_object('loading')

        # keep the builder
        self.builder = builder

        # when window is destroy, shutdown everything
        self.main_window.connect('destroy', self.stop)


    def update_terminal(self):
        """Update the log view for conda installation"""
        try:
            line = self.term.get_nowait()
        except Exception:
            pass
        else:
            if line is not None:
                end_iter = self.conda_buff.get_end_iter()
                self.conda_buff.insert(end_iter, line.decode('utf-8'))

                end_iter = self.conda_buff.get_end_iter()
                self.conda_box.scroll_to_iter(end_iter, 0.0, False, 0, 0)
            if line is None:
                print("Install done")
                self.done_button.show()
                self.loading_image.hide()
            return line is not None
        return True

    @staticmethod
    def stop(*args):
        """Stop JupyterLab and quit"""
        jupyter.stop_jupyter()
        Gtk.main_quit()

    def start(self):
        """Prepare conda if needed, and then open Jupyter"""
        if not jupyter.check_conda():
            # Error, explain that user must install Conda
            conda_not_found_dialog: Gtk.Dialog = self.builder.get_object('conda-not-found-dialog')
            close_button: Gtk.Button = self.builder.get_object('error-close-button')
            close_button.connect('clicked', Gtk.main_quit)
            conda_not_found_dialog.show_all()

        elif not jupyter.conda_env_installed():
            # install TyTan environment in conda
            self.conda_install_dialog.show_all()
            self.done_button.hide()
            self.done_button.connect('clicked', self.open_jupyter)
            self.loading_image.show()

            self.term = jupyter.init_conda()
            GLib.timeout_add(10, self.update_terminal)

        else:
            # everything is right, open jupyterlab
            self.open_jupyter()

        Gtk.main()

    def open_jupyter(self, *args):
        """Start JupyterLab server and open the webview"""
        self.conda_install_dialog.destroy()
        jupyter.start_jupyter()
        jupyter.wait_for_port()

        self.webview.load_uri('http://127.0.0.1:8888')
        self.main_window.show_all()
