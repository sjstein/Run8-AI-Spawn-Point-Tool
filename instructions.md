# Run8 AI Spawn-point Tool - Instructions

## Overview
This tool allows you to view and edit Run8 Train Simulator AI spawn point files (AISpecialLocations.r8).

## Getting Started

### **Important**: Always back up your original files before making changes!

### Opening a File
1. Go to **File → Open** (or press Ctrl+O)
2. Navigate to the specific Run8 Regions directory (ex: \Content\V3Routes\Regions\SouthernCA)
3. Select an AISpecialLocations.r8 file
4. The main window will display all spawn points in the file

## Viewing and Editing Spawn Points

### Main Window
The main window displays a table with the following columns:
- **Name**: Spawn point name
- **Type**: Spawn point type
- **Route**: Route prefix/ID
- **Track**: Track ID
- **Dir**: Direction (0 or 1)
- **Time**: Time in minutes (0-1440, representing a 24-hour day)
- **Skip**: Whether to skip AutoTrain (Yes/No)

### Editing a Spawn Point
1. **Double-click** any row in the table to open the detail dialog
2. In the detail dialog, you can edit:
   - **Name:** Spawn point identifier
   - **Type:** Spawn point type (Spawn Point, Crew Change, Passenger, etc.)
   - **Route Prefix:** Which route this spawn point is on
   - **Track ID:** Which track segment
   - **Direction:** Which end of the track segment (0 or 1)
   - **Position Offset:** Distance from the specified end of the track segment
   - **Time:** Spawn time in minutes (0-1440 for 24-hour day)
   - **Skip AutoTrain:** Whether to skip AutoTrain at this location
   - **Unknown fields** (Unk 1, 2, 3, 5) - These appear to be constant/reserved fields
3. Click **Update** to keep changes or **Cancel** to discard

### Unknown Fields
The remaining unknown fields (Unk 1, 2, 3, 5) appear to be constant values across all spawn points and are likely reserved/padding fields. They are displayed as hexadecimal values and can be edited if needed:
- **Unk 1, 2, 3, 5:** Reserved fields - appear to have fixed values
- Enter valid hexadecimal values (0-9, a-f) if editing
- These fields are preserved when saving to maintain file compatibility

## Saving Changes

### Save File
- Go to **File → Save** (or press Ctrl+S) to overwrite the file originally loaded
- Use **File → Save As...** to create a new file
- *Note*: If overwriting the original file, you'll be prompted to confirm

### Unsaved Changes
- Rows with unsaved changes are highlighted in yellow
- You'll be warned if you try to close the application or open a new file with unsaved changes

## Tips

- Always keep backups of your original files
- Test changes in a test environment before using them in your main game
- The **Position Offset** field determines where along the track segment the AI train will spawn
- The **Direction** field (0 or 1) determines which end of the track segment the offset is measured from

## Troubleshooting

### File Won't Open
- Make sure you're opening an AISpecialLocations.r8 file
- Verify the file isn't corrupted (try opening it in the original Run8 game first)

### Changes Don't Appear in Game
- Make sure you saved the file
- Verify you saved to the correct location
- Restart Run8 to load the new configuration

## Support

Found a bug or have a feature request? Please create an issue on GitHub:
https://github.com/sjstein/Run8-AI-Spawn-Point-Tool/issues
