# SnipShot

*Objective: A simple image capturing tool focused for Linux, designed to replicate the very basic functionality of Microsoft's Snipping Tool.*

## Description

SnipShot is a lightweight application that allows users to capture screenshots on Linux. It aims to provide a straightforward and intuitive interface similar to Microsoft's Snipping Tool, offering basic functionality to capture and save screenshots.

## How to Build

If you want to generate your own executable, simply run:

```bash
pyinstaller --onefile SnippingTool.py
```

Make sure you have PyQt5 installed by running:

```bash
pip install PyQt5
```

Check the `dist` folder for the release, or download the one I generated from the [Releases](https://github.com/williamsuttondev/SnipShot/releases) section.

## How to Run

1. Navigate to the `dist` folder containing the executable.
2. Make the file executable:

   ```bash
   chmod +x SnippingTool
   ```

3. Run the executable:

   ```bash
   ./SnippingTool
   ```

## Issues and Bugs

If you encounter any issues or bugs, please [open an issue](https://github.com/williamsuttondev/SnipShot/issues) on the GitHub repository. Your feedback and contributions are welcome!

---

*Check the [Releases](https://github.com/williamsuttondev/SnipShot/releases) section for the latest versions and updates.*
