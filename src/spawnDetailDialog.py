from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt
from spawnDetailDialog_ui import Ui_SpawnDetailDialog


class SpawnDetailDialog(QDialog):
    def __init__(self, spawn_point, parent=None, spawn_index=None):
        super().__init__(parent)
        self.spawn_point = spawn_point
        self.spawn_index = spawn_index  # Index in main table

        # Setup UI from generated file
        self.ui = Ui_SpawnDetailDialog()
        self.ui.setupUi(self)

        # Set window title with spawn point name
        self.setWindowTitle(f"Spawn Point Details - {spawn_point.name}")

        # Populate type combobox
        self.type_names = {
            0: "Spawn Point",
            1: "Crew Change",
            2: "Crew Change & Hold",
            3: "Passenger",
            4: "Passenger Crew Change",
            5: "Passenger Crew Change & Hold",
            6: "Relinquish",
            7: "Passenger Relinquish"
        }
        for type_id, type_name in self.type_names.items():
            self.ui.type_combo.addItem(f"{type_id} - {type_name}", type_id)

        # Connect signals
        self.ui.save_button.clicked.connect(self.accept)
        self.ui.cancel_button.clicked.connect(self.reject)

        # Set Update button as the default (activated by Enter key)
        self.ui.save_button.setDefault(True)
        self.ui.save_button.setAutoDefault(True)
        self.ui.cancel_button.setAutoDefault(False)

        # Load data
        self.load_data()

    def load_data(self):
        """Load spawn point data into the form"""
        self.ui.name_edit.setText(self.spawn_point.name)

        # Set type combobox to current value
        index = self.ui.type_combo.findData(self.spawn_point.type)
        if index >= 0:
            self.ui.type_combo.setCurrentIndex(index)

        self.ui.route_prefix_edit.setText(str(self.spawn_point.route_prefix))
        self.ui.track_id_edit.setText(str(self.spawn_point.track_id))
        self.ui.direction_edit.setText(str(self.spawn_point.dir))
        self.ui.time_edit.setText(str(self.spawn_point.time))
        self.ui.skip_check.setChecked(bool(self.spawn_point.skip))

        # Load unknown fields
        self.ui.unk1_edit.setText(bytes(self.spawn_point.unk1).hex())
        self.ui.unk2_edit.setText(bytes(self.spawn_point.unk2).hex())
        self.ui.unk3_edit.setText(bytes(self.spawn_point.unk3).hex())
        self.ui.unk4_edit.setText(str(self.spawn_point.unk4))  # Display as float
        self.ui.unk5_edit.setText(bytes(self.spawn_point.unk5).hex())

    def save_data(self):
        """Save form data back to the spawn point object"""
        # Update name (this will re-encode it)
        if self.ui.name_edit.text() != self.spawn_point.name:
            self.spawn_point.rename(self.ui.name_edit.text())

        # Update numeric fields
        try:
            # Get type from combobox
            self.spawn_point.type = self.ui.type_combo.currentData()

            self.spawn_point.route_prefix = int(self.ui.route_prefix_edit.text())
            self.spawn_point.track_id = int(self.ui.track_id_edit.text())
            self.spawn_point.dir = int(self.ui.direction_edit.text())
            self.spawn_point.time = int(self.ui.time_edit.text())
            self.spawn_point.skip = 1 if self.ui.skip_check.isChecked() else 0

            # Update unknown fields
            self.spawn_point.unk1 = bytes.fromhex(self.ui.unk1_edit.text())
            self.spawn_point.unk2 = bytes.fromhex(self.ui.unk2_edit.text())
            self.spawn_point.unk3 = bytes.fromhex(self.ui.unk3_edit.text())
            self.spawn_point.unk4 = float(self.ui.unk4_edit.text())  # Parse as float
            self.spawn_point.unk5 = bytes.fromhex(self.ui.unk5_edit.text())

        except ValueError as e:
            raise ValueError(f"Invalid numeric value: {str(e)}")

    def accept(self):
        """Override accept to save data before closing"""
        try:
            self.save_data()
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Error Saving", f"Failed to save changes:\\n{str(e)}")
