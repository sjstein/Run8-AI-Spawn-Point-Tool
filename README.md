# Run8 AI Spawn-point Tool

A GUI application for viewing and editing Run8 Train Simulator AI spawn point files (AISpecialLocations.r8).

## NOTE: This software is not an official product from Run8 Studios

Please do **not** contact the developers at Run8 Studios for support with this tool - instead, create an issue in this repo.

## Features

- View and edit AI spawn point configurations
- Edit spawn point properties (name, type, route, track, direction, time, skip autotrain)
- Edit unknown fields for experimentation
- Visual indicators for unsaved changes
- Export configurations to new files
- Find/Replace functionality (coming soon)

## Simple Download

An executable will be available in Releases in the middle right of this page once the first release is published.

## Requirements to compile yourself

- Python 3.8+
- PySide6 6.10.1

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python src/spawnEditor.py
```

## Building an Executable

See [build.bat](build.bat) for building a standalone executable using PyInstaller.

## Usage

1. **Open a File**: File → Open, navigate to your Run8 region directory (e.g., `\Content\V3Routes\Regions\SouthernCA`), and select `AISpecialLocations.r8`
2. **Edit Spawn Points**: Double-click any spawn point row to open the detail dialog
3. **Save Changes**: File → Save (or Save As...)

See [instructions.md](instructions.md) for detailed usage instructions.

## File Structure

- `src/spawnEditor.py` - Main application entry point
- `src/r8lib.py` - Core data structures for Run8
- `src/mainTable.py` - Table model with dirty tracking
- `src/spawnDetailDialog.py` - Spawn point detail viewer/editor
- `src/aboutDialog.py` - About dialog
- `src/instructionsDialog.py` - Instructions dialog
- `src/*.ui` files - Qt Designer UI definitions
- `src/version.py` - Version tracking

## License

GPL V3 (See https://github.com/sjstein/Run8-AI-Spawn-Point-Tool/blob/main/LICENSE)
