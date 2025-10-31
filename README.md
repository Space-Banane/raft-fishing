# Raft Fishing Automation

Detects the text "LMB"(or any specified key) a little above the center of the screen and left-clicks automatically.

## Requirements

- Python 3.11 (tested)
- Packages: `pyautogui`, `easyocr`, `opencv-python`, `numpy`
- Windows OS (for EXE build and automation)

## Setup

```sh
pip install pyautogui easyocr opencv-python numpy
```

## Usage

```sh
python main.py
```

## Build as EXE

1. Install PyInstaller:
    ```sh
    pip install pyinstaller
    ```
2. Build:
    ```sh
    pyinstaller --onefile raft_angel.py
    ```
3. The EXE will be in the `dist` folder.

## Notes

- Make sure you have a display (not headless/WSL).
- The script will click and hold for 2 seconds if "LMB" is detected.
