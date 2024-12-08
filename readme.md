
# Scratchpad

A minimal text editor for quick note-taking and text manipulation.

Built out of frustration with having to open full-featured text editors and deal with save and other prompts even for simple text manipulation operations.

My usecase is to set a AutoHotKey shortcut to open the executable and do quick text manipulation such as editing before pasting, formatting text. Also great for temporary code snippets, drafting quick messages, or jotting down quick notes without saving.

## Features

- Instant startup with a clean, borderless interface
- Automatically focused text area - just start typing
- Keyboard shortcuts:
  - `Ctrl+w`: Close window
  - `Ctrl+=`: Increase font size
  - `Ctrl+-`: Decrease font size
- Customizable appearance through `display_config.json`
- No save functionality - designed for temporary text operations. Does not autosave too.

## Usage

There are two ways you can use this.

1. Directly with the pythonw.exe:  Run `pythonw Scratchpad.pyw`
2. Compile with pyinstaller: Run `pyinstaller --onefile --name Scratchpad  --windowed  --exclude-module tkinter --exclude display_config.json  Scratchpad.pyw`

You can download the precompiled binaries from [here](https://github.com/adithyarao3103/Scratchpad/releases/tag/v1.0)

## Configuration

Place the `display_config.json` in the same directory as `Scratchpad.pyw/Scratchpad.exe`:

```json
{
    "font": {
        "family": "Inter, sans-serif",
        "size": "16px",
        "url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"
    },
    "editor": {
        "backgroundColor": "#000",
        "textColor": "#fff",
        "lineHeight": "1.6",
        "letterSpacing": "0.02em",
        "padding": "20px"
    }
}
```

## Requirements

- Python 3.x
- pywebview

# ToDo

Add optional autosave functionality.
