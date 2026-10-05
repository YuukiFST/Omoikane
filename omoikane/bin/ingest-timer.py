"""Start the scheduled ingest when coding sessions go quiet, with no window (#96).

session-capture.py arms the timer after every capture: the run is due once no turn came for the quiet period,
counted from the last turn (counted from the first, a session still going would be distilled in halves). One
waiter process per checkout sleeps until the due time, runs `wiki-ingest.ps1 -Commit` and exits; a turn meanwhile
moves the due time, a turn during the run leads to one more run. The state lives outside the repository: the
scope check of a headless run watches ignored files too. The daily task of install-schedule.ps1 calls `now`, for
files dropped into the inbox by hand and a waiter lost to a reboot.

Usage: python omoikane/bin/ingest-timer.py now [--agent claude|opencode]
       python omoikane/bin/ingest-timer.py wait
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import IO, Callable

from wikilib import REPO

# wiki-ingest.ps1 moves a capture once untouched for its -QuietMinutes (30); one more minute, so it has.
QUIET_SECONDS = 31 * 60
# A waiter re-reads the due time at least this often, so a later turn is seen without a signal.
POLL_SECONDS = 60.0
# No console window for the waiter or the run: CREATE_NO_WINDOW gives a console nobody sees, and a new process
# group keeps the harness from stopping the waiter with its own Ctrl+C. 0 off Windows, where neither exists.
HIDDEN = (subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP) if os.name == "nt" else 0


def state_dir(repo: Path = REPO) -> Path:
    """Where one checkout keeps its due time and lock, outside the repository.

    Example: state_dir(Path("C:/src/shop")) returns <temp>/omoikane-ingest-<12 hex chars>.
    """
    key = hashlib.sha1(str(repo.resolve()).lower().encode("utf-8")).hexdigest()[:12]
    return Path(tempfile.gettempdir()) / f"omoikane-ingest-{key}"


def read_due(state: Path) -> dict[str, object] | None:
    try:
        return json.loads((state / "due.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def write_due(state: Path, due: dict[str, object]) -> None:
    state.mkdir(parents=True, exist_ok=True)
    tmp = state / f"due.{os.getpid()}.tmp"
    tmp.write_text(json.dumps(due), encoding="utf-8")
    os.replace(tmp, state / "due.json")


def try_lock(state: Path) -> IO[str] | None:
    """The waiter's lock, held until the returned file is closed or the process dies; None when another holds it.

    Example: try_lock(state) returns a file the first time and None while that file stays open.
    """
    state.mkdir(parents=True, exist_ok=True)
    handle = open(state / "waiter.lock", "a+", encoding="utf-8")
    try:
        if os.name == "nt":
            import msvcrt
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        handle.close()
        return None
    return handle


def spawn_waiter() -> None:
    subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "wait"], cwd=REPO, creationflags=HIDDEN,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)


def arm(state: Path, delay: float, agent: str, now: Callable[[], float] = time.time,
        spawn: Callable[[], None] = spawn_waiter) -> None:
    """Make a run due `delay` seconds from now, unless one is already due later, and make sure a waiter exists.

    A pending later time wins, so the daily `now` neither advances a session still going nor drops it.
    Example: arm(state_dir(), QUIET_SECONDS, "claude") after a capture.
    """
    due = read_due(state)
    if due is None or float(due["at"]) < now() + delay:  # type: ignore[arg-type]
        write_due(state, {"at": now() + delay, "agent": agent})
    spawn()  # a second waiter finds the lock held and leaves


def run_ingest(agent: str) -> None:
    pwsh = shutil.which("pwsh")
    if pwsh is None:  # the waiter has no console, so the run's own log is where a human looks
        with open(REPO / "omoikane" / ".wiki-ingest.log", "a", encoding="utf-8") as log:
            log.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} ingest-timer: pwsh not found, nothing ran\n")
        return
    subprocess.run([pwsh, "-NoProfile", "-File", str(REPO / "omoikane" / "bin" / "wiki-ingest.ps1"), "-Agent", agent,
                    "-Commit"], cwd=REPO, creationflags=HIDDEN, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def wait(state: Path, run: Callable[[str], None] = run_ingest, now: Callable[[], float] = time.time,
         sleep: Callable[[float], None] = time.sleep) -> str:
    """Hold the lock, sleep until the due time, run, and repeat while a turn moved it meanwhile.

    Example: wait(state_dir()) returns "ran 1" after one run, "another waiter holds the lock" when one does.
    """
    lock = try_lock(state)
    if lock is None:
        return "another waiter holds the lock"
    runs = 0
    try:
        while (due := read_due(state)) is not None:
            left = float(due["at"]) - now()  # type: ignore[arg-type]
            if left > 0:
                sleep(min(left, POLL_SECONDS))
                continue
            # Cleared before the run, so a turn during it leaves a new due time and one more pass.
            if read_due(state) == due:
                (state / "due.json").unlink()
            run(str(due["agent"]))
            runs += 1
    finally:
        lock.close()
    return f"ran {runs}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("action", choices=("now", "wait"))
    parser.add_argument("--agent", choices=("claude", "opencode"), default="claude")
    args = parser.parse_args(argv)
    if args.action == "now":
        arm(state_dir(), 0, args.agent)
        return 0
    print(f"ingest-timer: {wait(state_dir())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
