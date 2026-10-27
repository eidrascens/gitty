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



from typing import Self, Optional
import gi

from gi.repository import Adw, Gtk

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

APP_ID = "io.gitty.Gitty"
APP_NAME = "Gitty"


class GittyApp(Adw.Application):
    def __init__(self: Self) -> None:
        super().__init__(application_id=APP_ID)
        self.window: Optional[Adw.ApplicationWindow] = None
        self.file_rows: list[dict[str, object]] = []
        self._chooser: Optional[Gtk.FileChooserNative] = None
