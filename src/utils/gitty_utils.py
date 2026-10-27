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

from subprocess import run as RUN, CompletedProcess, PIPE
from os.path import realpath
from os import fsdecode


def git_run(
        repo: str, *args: str, check: bool = True
    ) -> CompletedProcess[str]:
    """Run Git without a shell, so paths and commit messages
    are not shell-expanded."""
    result = RUN(
        ["git", "-C", repo, *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=PIPE,
        stderr=PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            (
                result.stderr.strip() or
                result.stdout.strip() or
                "Git command failed."
            )
        )
    return result


def find_repo_root(path: str) -> str:
    result = RUN(
        [
            "git",
            "-C",
            path,
            "rev-parse",
            "--show-toplevel"
        ],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=PIPE,
        stderr=PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or
            "%s is not a Git Repository" % (
                path
            )
        )
    return realpath(result.stdout.strip())


def read_changed_files(repo: str) -> list[tuple[str, str]]:
    """Return (relative_path, short_status) entries, excluding
    ignored untracked files.
    """
    result = RUN(
        [
            "git",
            "-C",
            repo,
            "status",
            "--porcelain=v1",
            "-z",
            "--untracked-files=all",
            "--no-renames",
        ],
        stdout=PIPE,
        stderr=PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            fsdecode(
                result.stderr
            ).strip() or
            "Could not read Git status."
        )

    entries: list[tuple[str, str]] = []
    for record in result.stdout.split(b"\0"):
        if not record:
            continue

        if len(record) < 4:
            continue

        status = record[:2].decode("ascii", errors="replace")

        if (path := fsdecode(record[3:])):
            entries.append((path, status))

    return sorted(
        entries, key=lambda item: item[0].casefold()
    )


def literal_pathspec(path: str) -> str:
    """Make a Git pathspec literal"""
    return ":(literal)" + path
