---
name: screenshot-ui
description: Opens the application either in headless or native styling and captures a screenshot of the given UI element.
---

# Screenshotting

Workflow for grabbing PNG screenshots of the application — either headless
(no window ever appears) or with native macOS chrome (real window flashes briefly).

## Setup

- Use the `.env` venv: `.env/bin/python3`
- If comparing two branches (e.g. a PR head vs. `main`), check each one out into
  its own `git worktree` rather than switching branches in place:
  ```
  git worktree add /path/to/wt-main origin/main --detach
  git worktree add /path/to/wt-feat origin/feat-branch --detach
  ```
- Point Python at the branch's package code instead of the venv's editable
  install by prepending the worktree path:
  ```
  PYTHONPATH=/path/to/wt-main .env/bin/python3 screenshot.py out.png
  ```

## Screenshot Target

By default, unless stated otherwise, this skill assumes:
- `simple_example.py` is the base script to reference for launching and capturing screenshots/snapshots.
- The `BuscadorDeCosas` debugger widget (`ui_debugger`) is the primary Qt widget to `grab()` for the output screenshot, unless stated otherwise.
- `~/Downloads` is where final output PNGs get copied for the user, unless stated otherwise.

## Screenshot Setup

- Reference the `simple_example.py` and create a temporary copy for any adjusted assumptions.

## Option A — native macOS (real Cocoa window) - DEFAULT

- Run: `.env/bin/python3 simple_example.py out.png`
- Run with no `QT_QPA_PLATFORM` override — Qt defaults to `cocoa` on macOS
- Dark mode is picked up automatically from the system appearance setting, no extra code needed
- A real window briefly appears on screen while it's grabbed, then the process exits

## Option B — headless (`QT_QPA_PLATFORM=offscreen`)

- Run: `QT_QPA_PLATFORM=offscreen .env/bin/python3 simple_example.py out.png`
- No window ever appears on screen — safe for CI / SSH / no-display environments
- ⚠️ Default style under offscreen is `fusion`, not `macos` — there's no real
  windowing system for Qt's native macOS style to draw against, so you lose
  the authentic Aqua/dark chrome

## Cleanup

- Remove the worktrees when done: `git worktree remove /path/to/wt-main --force`
- If any temporary copies of the `simple_example.py` were created, prompt for their removal
