import sys
import os
import json
import urllib.request
import threading
from packaging import version as pkg_version

from r8lib import SpawnFile, SpawnPoint

from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox,
                                QPushButton, QHBoxLayout, QLabel, QSizePolicy,
                                QStyledItemDelegate, QLineEdit)
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
from PySide6.QtCore import Qt, QTimer, Signal, QObject
from mainWindow_ui import Ui_MainWindow
from mainTable import DictTableModel
from spawnDetailDialog import SpawnDetailDialog
from instructionsDialog import InstructionsDialog
from aboutDialog import AboutDialog
from version import VERSION


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def check_for_updates(timeout=5):
    """
    Check GitHub for newer releases.
    Returns: (has_update, latest_version, release_url, error_message)
    """
    try:
        # GitHub API endpoint for latest release
        api_url = "https://api.github.com/repos/sjstein/Run8-AI-Spawn-Point-Tool/releases/latest"

        # Create request with timeout
        req = urllib.request.Request(api_url)
        req.add_header('Accept', 'application/vnd.github.v3+json')

        # Make request with timeout
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())

        # Extract version from tag_name (handles both "v1.2.3" and "1.2.3")
        latest_tag = data.get('tag_name', '')
        latest_version = latest_tag.lstrip('v')
        release_url = data.get('html_url', 'https://github.com/sjstein/Run8-AI-Spawn-Point-Tool/releases')

        # Compare versions using packaging library for semantic versioning
        current = pkg_version.parse(VERSION)
        latest = pkg_version.parse(latest_version)

        has_update = latest > current

        return (has_update, latest_version, release_url, None)

    except Exception as e:
        # Return error information
        return (False, None, None, str(e))


INTLEN = 4
BYTLEN = 1
SHTLEN = 2


class VisualSelectDelegate(QStyledItemDelegate):
    """Custom delegate that visually highlights all text when editing"""
    def createEditor(self, parent, option, index):
        """Create the editor and configure it for text selection"""
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            # Connect to selectAll when the editor is shown
            QTimer.singleShot(0, editor.selectAll)
        return editor


class UpdateChecker(QObject):
    """Worker class for checking updates in background thread"""
    # Define signals
    update_found = Signal(str, str)  # (latest_version, release_url)
    no_update = Signal()
    error_occurred = Signal(str)  # (error_message)

    def __init__(self):
        super().__init__()

    def check(self):
        """Perform the update check (runs in background thread)"""
        has_update, latest_version, release_url, error = check_for_updates()

        if error:
            self.error_occurred.emit(error)
        elif has_update:
            self.update_found.emit(latest_version, release_url)
        else:
            self.no_update.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup UI from generated file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set window icon
        icon_path = resource_path('app_icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Initialize table model with empty data
        # Headers will be auto-generated from the dictionary keys when data is loaded
        self.table_model = DictTableModel([])
        self.ui.tableView.setModel(self.table_model)

        # Apply custom delegate for proper text selection on edit
        self.ui.tableView.setItemDelegate(VisualSelectDelegate(self))

        # Set edit triggers to prevent editing on selection
        from PySide6.QtWidgets import QAbstractItemView
        self.ui.tableView.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )

        # Set selection behavior to select entire rows
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Disable grid lines
        self.ui.tableView.setShowGrid(False)

        # Add buttons in lower section
        button_layout = QHBoxLayout()

        # Add spawn point button
        self.add_button = QPushButton("Add Spawn Point")
        self.add_button.clicked.connect(self.add_spawn_point)
        self.add_button.setMaximumWidth(150)
        button_layout.addWidget(self.add_button)

        # Delete spawn point button
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_spawn_points)
        self.delete_button.setMaximumWidth(150)
        button_layout.addWidget(self.delete_button)

        # Add the button layout to the main vertical layout
        central_widget = self.ui.centralwidget
        central_widget.layout().addLayout(button_layout)

        # Connect model's dataChanged signal to sync changes back to spawn points
        self.table_model.dataChanged.connect(self.on_table_data_changed)

        # Connect menu actions
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionSaveAs.triggered.connect(self.save_file_as)
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionFind.triggered.connect(self.show_find)
        self.ui.actionInstructions.triggered.connect(self.show_instructions)
        self.ui.actionCheckUpdates.triggered.connect(self.check_updates_manual)
        self.ui.actionAbout.triggered.connect(self.show_about)

        # Create file info label for menu bar corner
        self.file_info_label = QLabel("No file loaded")
        self.file_info_label.setStyleSheet("QLabel { padding: 0 10px; }")
        self.file_info_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.file_info_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.file_info_label.setMinimumWidth(300)
        self.menuBar().setCornerWidget(self.file_info_label, Qt.Corner.TopRightCorner)

        # Disable Save and Save As until a file is loaded
        self.ui.actionSave.setEnabled(False)
        self.ui.actionSaveAs.setEnabled(False)

        # Disable Add/Delete buttons until a file is loaded
        self.add_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        # Check for updates on startup (non-blocking)
        QTimer.singleShot(500, self.check_updates_on_startup)

    def open_file(self):
        # Check for unsaved changes before opening a new file
        if self.table_model._dirty_rows:
            reply = QMessageBox.question(
                self,
                'Unsaved Changes',
                f'You have {len(self.table_model._dirty_rows)} unsaved changes.\\n\\n'
                'Opening a new file will discard these changes. Continue?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.No:
                return  # User cancelled, don't open new file

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            '',
            'Spawn Point Files (*.r8);;All Files (*)'
        )
        if file_name:
            print(f'Selected file: {file_name}')
            with open(file_name, 'rb') as fp:
                mem_ptr = 0
                mem_map = fp.read()

                # Parse the spawn file
                global spawnFile1
                spawnFile1 = SpawnFile()
                spawnFile1.unk1 = mem_map[mem_ptr:mem_ptr + INTLEN]
                mem_ptr += INTLEN
                spawnFile1.num_rec = int.from_bytes(mem_map[mem_ptr:mem_ptr + INTLEN], 'little')
                mem_ptr += INTLEN

                # Read spawn points
                for _ in range(spawnFile1.num_rec):
                    spawn_point = SpawnPoint(mem_map, mem_ptr)
                    spawnFile1.spawn_points.append(spawn_point)
                    mem_ptr += spawn_point.name_len + 30  # 30 is the fixed size of other fields

            # Update file info in menu bar
            filename = os.path.basename(file_name)
            self.file_info_label.setText(f'{filename}  [{spawnFile1.num_rec} spawn points]')
            self.file_info_label.setToolTip(f'Full path: {file_name}')
            self.file_info_label.adjustSize()

            # Store the loaded file path globally
            global loaded_file_path
            loaded_file_path = file_name

            # Convert spawn points to dictionaries for table display
            spawn_data = [sp.to_dict() for sp in spawnFile1.spawn_points]

            # Update table model
            self.table_model.update_data(spawn_data)

            # Configure column widths
            from PySide6.QtWidgets import QHeaderView
            header = self.ui.tableView.horizontalHeader()

            # Get column indices for headers we want to resize
            headers = self.table_model._headers
            resize_to_contents = ['Route', 'Track ID', 'dir', 'time', 'skip', 'unk1', 'unk2', 'unk3', 'unk5', 'Pos. Offset']

            for col_name in resize_to_contents:
                if col_name in headers:
                    col_index = headers.index(col_name)
                    header.setSectionResizeMode(col_index, QHeaderView.ResizeMode.ResizeToContents)

            # Make name column stretch to fill remaining space
            if 'name' in headers:
                name_index = headers.index('name')
                header.setSectionResizeMode(name_index, QHeaderView.ResizeMode.Stretch)

            # Enable Save and Save As
            self.ui.actionSave.setEnabled(True)
            self.ui.actionSaveAs.setEnabled(True)

            # Enable Add/Delete buttons
            self.add_button.setEnabled(True)
            self.delete_button.setEnabled(True)

            self.statusBar().showMessage(f'Loaded {file_name}', 5000)

    def save_file(self):
        """Save to the currently loaded file"""
        if 'loaded_file_path' not in globals():
            self.save_file_as()
            return

        # Confirm overwrite
        reply = QMessageBox.question(
            self,
            'Confirm Overwrite',
            f'Overwrite the file?\\n{loaded_file_path}',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return

        try:
            # Write file
            with open(loaded_file_path, 'wb') as fp:
                fp.write(spawnFile1.to_bytes())

            # Clear dirty flags
            self.table_model.clear_dirty_rows()

            self.statusBar().showMessage(f'Saved to {loaded_file_path}', 5000)

        except Exception as e:
            QMessageBox.critical(self, 'Save Error', f'Failed to save file:\\n{str(e)}')

    def save_file_as(self):
        """Save to a new file"""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            'Save File As',
            '',
            'Spawn Point Files (*.r8);;All Files (*)'
        )

        if not file_name:
            return  # User cancelled

        try:
            # Write file
            with open(file_name, 'wb') as fp:
                fp.write(spawnFile1.to_bytes())

            # Update loaded file path
            global loaded_file_path
            loaded_file_path = file_name

            # Update file info in menu bar
            filename = os.path.basename(file_name)
            self.file_info_label.setText(f'{filename}  [{spawnFile1.num_rec} spawn points]')
            self.file_info_label.setToolTip(f'Full path: {file_name}')

            # Clear dirty flags
            self.table_model.clear_dirty_rows()

            self.statusBar().showMessage(f'Saved to {file_name}', 5000)

        except Exception as e:
            QMessageBox.critical(self, 'Save Error', f'Failed to save file:\\n{str(e)}')

    def on_table_data_changed(self, top_left, bottom_right, roles):
        """Sync table edits back to spawn point objects"""
        if 'spawnFile1' not in globals():
            return

        # Get the changed rows
        for row in range(top_left.row(), bottom_right.row() + 1):
            original_index = self.table_model.get_original_index(row)
            spawn_point = spawnFile1.spawn_points[original_index]

            # Get the updated data from the table
            row_data = self.table_model._data[row]

            # Update spawn point object from the row data
            # Parse the type field (it's displayed as "0 (Spawn Point)" format)
            type_str = str(row_data.get('type', '0'))
            type_value = int(type_str.split()[0]) if type_str else 0

            # Update fields
            if row_data.get('name') != spawn_point.name:
                spawn_point.rename(row_data.get('name', ''))

            spawn_point.type = type_value
            spawn_point.route_prefix = int(row_data.get('Route', 0))
            spawn_point.track_id = int(row_data.get('Track ID', 0))
            spawn_point.dir = int(row_data.get('dir', 0))
            spawn_point.time = int(row_data.get('time', 0))

            # Parse skip field
            skip_str = str(row_data.get('skip', 'No'))
            spawn_point.skip = 1 if skip_str.lower() in ['yes', 'y', '1', 'true'] else 0

            # Parse position offset as float
            try:
                spawn_point.unk4 = float(row_data.get('Pos. Offset', '0'))
            except (ValueError, TypeError):
                spawn_point.unk4 = 0.0

            # Parse other unknown fields as hex
            try:
                spawn_point.unk1 = bytes.fromhex(row_data.get('unk1', '00000000'))
                spawn_point.unk2 = bytes.fromhex(row_data.get('unk2', '00'))
                spawn_point.unk3 = bytes.fromhex(row_data.get('unk3', '0000'))
                spawn_point.unk5 = bytes.fromhex(row_data.get('unk5', '0000'))
            except (ValueError, TypeError):
                pass  # Keep existing values if parsing fails

        self.statusBar().showMessage('Changes saved to spawn points', 2000)

    def add_spawn_point(self):
        """Add a new spawn point with default values"""
        if 'spawnFile1' not in globals():
            QMessageBox.warning(self, "No File", "Please open a file first.")
            return

        # Create a new spawn point with default values
        from r8lib import encode_run8string
        default_name = f"New Spawn Point {len(spawnFile1.spawn_points) + 1}"
        enc_name = encode_run8string(default_name)

        # Create spawn point data manually
        spawn_data = bytearray()
        spawn_data.extend((0).to_bytes(INTLEN, 'little'))  # unk1
        spawn_data.extend(len(enc_name).to_bytes(INTLEN, 'little'))  # name_len
        spawn_data.extend(enc_name)  # enc_name
        spawn_data.extend((0).to_bytes(BYTLEN, 'little'))  # type
        spawn_data.extend((1).to_bytes(INTLEN, 'little'))  # route_prefix
        spawn_data.extend((100).to_bytes(INTLEN, 'little'))  # track_id
        spawn_data.extend((0).to_bytes(BYTLEN, 'little'))  # dir
        spawn_data.extend((0).to_bytes(BYTLEN, 'little'))  # unk2
        spawn_data.extend((0).to_bytes(SHTLEN, 'little'))  # unk3
        import struct
        spawn_data.extend(struct.pack('f', 0.0))  # unk4 (position offset as float)
        spawn_data.extend((0).to_bytes(SHTLEN, 'little'))  # time
        spawn_data.extend((0).to_bytes(SHTLEN, 'little'))  # unk5
        spawn_data.extend((0).to_bytes(BYTLEN, 'little'))  # skip

        # Create spawn point object
        new_spawn = SpawnPoint(spawn_data, 0)

        # Add to spawn file
        spawnFile1.spawn_points.append(new_spawn)
        spawnFile1.num_rec += 1

        # Refresh table
        spawn_data = [sp.to_dict() for sp in spawnFile1.spawn_points]
        self.table_model.update_data(spawn_data)

        # Mark the new row as dirty
        new_row = len(spawnFile1.spawn_points) - 1
        self.table_model.mark_row_dirty(new_row)

        self.statusBar().showMessage(f'Added new spawn point', 3000)

    def delete_spawn_points(self):
        """Delete selected spawn points"""
        if 'spawnFile1' not in globals():
            return

        # Get selected rows
        selection = self.ui.tableView.selectionModel()
        if not selection.hasSelection():
            QMessageBox.warning(self, "No Selection", "Please select spawn point(s) to delete.")
            return

        selected_rows = sorted(set(index.row() for index in selection.selectedRows()))

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Delete {len(selected_rows)} spawn point(s)?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return

        # Get original indices for the selected rows
        original_indices = [self.table_model.get_original_index(row) for row in selected_rows]

        # Sort in reverse order to delete from end to beginning
        original_indices.sort(reverse=True)

        # Delete from spawn file
        for orig_idx in original_indices:
            del spawnFile1.spawn_points[orig_idx]
            spawnFile1.num_rec -= 1

        # Refresh table
        spawn_data = [sp.to_dict() for sp in spawnFile1.spawn_points]
        self.table_model.update_data(spawn_data)

        # Update file info
        if 'loaded_file_path' in globals():
            filename = os.path.basename(loaded_file_path)
            self.file_info_label.setText(f'{filename}  [{spawnFile1.num_rec} spawn points]')

        self.statusBar().showMessage(f'Deleted {len(selected_rows)} spawn point(s)', 3000)

    def show_instructions(self):
        """Show the instructions dialog (non-modal)"""
        dialog = InstructionsDialog(self)
        dialog.show()

    def show_about(self):
        """Show the about dialog"""
        dialog = AboutDialog(self)
        dialog.exec()

    def show_find(self):
        """Show the find dialog"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Find")
        dialog.setModal(False)
        dialog.setMinimumWidth(400)

        # Create layout
        layout = QVBoxLayout()

        # Search input
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Find:"))
        search_input = QLineEdit()
        search_layout.addWidget(search_input)
        layout.addLayout(search_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        find_next_button = QPushButton("Find Next")
        find_prev_button = QPushButton("Find Previous")
        close_button = QPushButton("Close")

        button_layout.addWidget(find_prev_button)
        button_layout.addWidget(find_next_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        # Status label
        status_label = QLabel("")
        layout.addWidget(status_label)

        dialog.setLayout(layout)

        # Keep track of search state
        search_state = {'current_index': -1, 'matches': []}

        def find_matches():
            """Find all matching rows"""
            search_text = search_input.text().lower()
            if not search_text:
                status_label.setText("Please enter search text")
                return []

            matches = []
            for row in range(self.table_model.rowCount()):
                # Search across all columns
                for col in range(self.table_model.columnCount()):
                    index = self.table_model.index(row, col)
                    cell_value = str(self.table_model.data(index, Qt.ItemDataRole.DisplayRole)).lower()
                    if search_text in cell_value:
                        matches.append(row)
                        break  # Found in this row, move to next row

            return matches

        def find_next():
            """Find next match"""
            search_state['matches'] = find_matches()
            if not search_state['matches']:
                status_label.setText("No matches found")
                return

            # Move to next match
            search_state['current_index'] = (search_state['current_index'] + 1) % len(search_state['matches'])
            row = search_state['matches'][search_state['current_index']]

            # Select and scroll to row
            self.ui.tableView.selectRow(row)
            self.ui.tableView.scrollTo(self.table_model.index(row, 0))
            # Clear current index to avoid cell focus indicators
            self.ui.tableView.setCurrentIndex(self.table_model.index(-1, -1))

            status_label.setText(f"Match {search_state['current_index'] + 1} of {len(search_state['matches'])}")

        def find_previous():
            """Find previous match"""
            search_state['matches'] = find_matches()
            if not search_state['matches']:
                status_label.setText("No matches found")
                return

            # Move to previous match
            search_state['current_index'] = (search_state['current_index'] - 1) % len(search_state['matches'])
            row = search_state['matches'][search_state['current_index']]

            # Select and scroll to row
            self.ui.tableView.selectRow(row)
            self.ui.tableView.scrollTo(self.table_model.index(row, 0))
            # Clear current index to avoid cell focus indicators
            self.ui.tableView.setCurrentIndex(self.table_model.index(-1, -1))

            status_label.setText(f"Match {search_state['current_index'] + 1} of {len(search_state['matches'])}")

        # Connect buttons
        find_next_button.clicked.connect(find_next)
        find_prev_button.clicked.connect(find_previous)
        close_button.clicked.connect(dialog.close)

        # Enter key finds next
        search_input.returnPressed.connect(find_next)

        # Focus search input
        search_input.setFocus()

        dialog.show()

    def check_updates_on_startup(self):
        """Check for updates on startup in background thread"""
        # Create worker and keep reference to prevent garbage collection
        self._startup_checker = UpdateChecker()

        # Connect signals to slots (auto_check=True)
        self._startup_checker.update_found.connect(lambda v, u: self.show_update_dialog(v, u, auto_check=True))
        self._startup_checker.no_update.connect(lambda: None)  # Silent on startup
        self._startup_checker.error_occurred.connect(lambda e: None)  # Silent on startup

        # Run check in background thread
        thread = threading.Thread(target=self._startup_checker.check, daemon=True)
        thread.start()

    def check_updates_manual(self):
        """Check for updates manually via menu"""
        # Create worker
        self._manual_checker = UpdateChecker()

        # Connect signals (auto_check=False)
        self._manual_checker.update_found.connect(lambda v, u: self.show_update_dialog(v, u, auto_check=False))
        self._manual_checker.no_update.connect(lambda: QMessageBox.information(
            self, "No Updates", f"You are running the latest version ({VERSION})."
        ))
        self._manual_checker.error_occurred.connect(lambda e: QMessageBox.warning(
            self, "Update Check Failed", f"Could not check for updates:\\n{e}"
        ))

        # Run check in background thread
        thread = threading.Thread(target=self._manual_checker.check, daemon=True)
        thread.start()

    def show_update_dialog(self, latest_version, release_url, auto_check=True):
        """Show update available dialog"""
        if auto_check:
            # Non-intrusive notification
            msg = f"Version {latest_version} is available. Current version: {VERSION}"
            self.statusBar().showMessage(msg, 10000)
        else:
            # Full dialog for manual check
            reply = QMessageBox.question(
                self,
                "Update Available",
                f"A new version is available!\\n\\n"
                f"Current version: {VERSION}\\n"
                f"Latest version: {latest_version}\\n\\n"
                f"Would you like to visit the download page?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )

            if reply == QMessageBox.StandardButton.Yes:
                import webbrowser
                webbrowser.open(release_url)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
