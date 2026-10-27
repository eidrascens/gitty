"""
gitty: Commit without terminal and quicly.
Copyright (C) 2026 Atracēla Eculantia (eidrascens)
<atracela.eculantia [at] protonmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""



from pathlib import Path
from typing import Self, Optional
import gi

from gi.repository import Adw, Gtk, GLib

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")


class GittyApp(Adw.Application):
    def __init__(self: Self) -> None:
        self.APP_ID = "io.gitty.Gitty"
        self.APP_NAME = "Gitty"

        super().__init__(application_id=self.APP_ID)

        self.window: Optional[Adw.ApplicationWindow] = None
        self.file_rows: list[dict[str, object]] = []
        self._chooser: Optional[Gtk.FileChooserNative] = None
        self.CONF: Path = Path(
                GLib.get_user_config_dir()
            ) / "git-commit-popup" / "config.json"
    def _build_window(self: Self) -> None:
        self.window = Adw.ApplicationWindow(
                application=self, title=self.APP_NAME
            )
        self.window.set_default_size(560, 290)
        self.window.set_resizable(False)
        self.window.connect(
            "close-request", self._on_close_request
        )


        self.error_label = Gtk.Label(label="")
        self.error_label.set_xalign(0)
        self.error_label.set_wrap(True)
        self.error_label.add_css_class("error")
        self.error_label.set_visible(False)
        root.append(self.error_label)


    def _show_error(self: Self, message: str) -> None:
        if not self.window or not hasattr(self, "error_label"):
            return

        self.error_label.set_text(message[:1800])
        self.error_label.set_visible(True)
