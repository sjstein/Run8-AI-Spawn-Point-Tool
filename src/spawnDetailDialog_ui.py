# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spawnDetailDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFormLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_SpawnDetailDialog(object):
    def setupUi(self, SpawnDetailDialog):
        if not SpawnDetailDialog.objectName():
            SpawnDetailDialog.setObjectName(u"SpawnDetailDialog")
        SpawnDetailDialog.resize(500, 450)
        self.verticalLayout = QVBoxLayout(SpawnDetailDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.spawnInfoGroup = QGroupBox(SpawnDetailDialog)
        self.spawnInfoGroup.setObjectName(u"spawnInfoGroup")
        self.formLayout = QFormLayout(self.spawnInfoGroup)
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(self.spawnInfoGroup)
        self.labelName.setObjectName(u"labelName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelName)

        self.name_edit = QLineEdit(self.spawnInfoGroup)
        self.name_edit.setObjectName(u"name_edit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.name_edit)

        self.labelType = QLabel(self.spawnInfoGroup)
        self.labelType.setObjectName(u"labelType")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelType)

        self.type_combo = QComboBox(self.spawnInfoGroup)
        self.type_combo.setObjectName(u"type_combo")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.type_combo)

        self.labelRoutePrefix = QLabel(self.spawnInfoGroup)
        self.labelRoutePrefix.setObjectName(u"labelRoutePrefix")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelRoutePrefix)

        self.route_prefix_edit = QLineEdit(self.spawnInfoGroup)
        self.route_prefix_edit.setObjectName(u"route_prefix_edit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.route_prefix_edit)

        self.labelTrackID = QLabel(self.spawnInfoGroup)
        self.labelTrackID.setObjectName(u"labelTrackID")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelTrackID)

        self.track_id_edit = QLineEdit(self.spawnInfoGroup)
        self.track_id_edit.setObjectName(u"track_id_edit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.track_id_edit)

        self.labelDirection = QLabel(self.spawnInfoGroup)
        self.labelDirection.setObjectName(u"labelDirection")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelDirection)

        self.direction_edit = QLineEdit(self.spawnInfoGroup)
        self.direction_edit.setObjectName(u"direction_edit")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.direction_edit)

        self.labelTime = QLabel(self.spawnInfoGroup)
        self.labelTime.setObjectName(u"labelTime")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.labelTime)

        self.time_edit = QLineEdit(self.spawnInfoGroup)
        self.time_edit.setObjectName(u"time_edit")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.time_edit)

        self.labelSkip = QLabel(self.spawnInfoGroup)
        self.labelSkip.setObjectName(u"labelSkip")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.labelSkip)

        self.skip_check = QCheckBox(self.spawnInfoGroup)
        self.skip_check.setObjectName(u"skip_check")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.skip_check)

        self.labelUnk1 = QLabel(self.spawnInfoGroup)
        self.labelUnk1.setObjectName(u"labelUnk1")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.labelUnk1)

        self.unk1_edit = QLineEdit(self.spawnInfoGroup)
        self.unk1_edit.setObjectName(u"unk1_edit")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.unk1_edit)

        self.labelUnk2 = QLabel(self.spawnInfoGroup)
        self.labelUnk2.setObjectName(u"labelUnk2")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.labelUnk2)

        self.unk2_edit = QLineEdit(self.spawnInfoGroup)
        self.unk2_edit.setObjectName(u"unk2_edit")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.unk2_edit)

        self.labelUnk3 = QLabel(self.spawnInfoGroup)
        self.labelUnk3.setObjectName(u"labelUnk3")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.labelUnk3)

        self.unk3_edit = QLineEdit(self.spawnInfoGroup)
        self.unk3_edit.setObjectName(u"unk3_edit")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.unk3_edit)

        self.labelUnk4 = QLabel(self.spawnInfoGroup)
        self.labelUnk4.setObjectName(u"labelUnk4")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.labelUnk4)

        self.unk4_edit = QLineEdit(self.spawnInfoGroup)
        self.unk4_edit.setObjectName(u"unk4_edit")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.FieldRole, self.unk4_edit)

        self.labelUnk5 = QLabel(self.spawnInfoGroup)
        self.labelUnk5.setObjectName(u"labelUnk5")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.labelUnk5)

        self.unk5_edit = QLineEdit(self.spawnInfoGroup)
        self.unk5_edit.setObjectName(u"unk5_edit")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.FieldRole, self.unk5_edit)


        self.verticalLayout.addWidget(self.spawnInfoGroup)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.buttonSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.buttonSpacer)

        self.save_button = QPushButton(SpawnDetailDialog)
        self.save_button.setObjectName(u"save_button")

        self.buttonLayout.addWidget(self.save_button)

        self.cancel_button = QPushButton(SpawnDetailDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.buttonLayout.addWidget(self.cancel_button)


        self.verticalLayout.addLayout(self.buttonLayout)


        self.retranslateUi(SpawnDetailDialog)

        QMetaObject.connectSlotsByName(SpawnDetailDialog)
    # setupUi

    def retranslateUi(self, SpawnDetailDialog):
        SpawnDetailDialog.setWindowTitle(QCoreApplication.translate("SpawnDetailDialog", u"Spawn Point Details", None))
        self.spawnInfoGroup.setTitle(QCoreApplication.translate("SpawnDetailDialog", u"Spawn Point Information", None))
        self.labelName.setText(QCoreApplication.translate("SpawnDetailDialog", u"Name:", None))
        self.labelType.setText(QCoreApplication.translate("SpawnDetailDialog", u"Type:", None))
        self.labelRoutePrefix.setText(QCoreApplication.translate("SpawnDetailDialog", u"Route Prefix:", None))
        self.labelTrackID.setText(QCoreApplication.translate("SpawnDetailDialog", u"Track ID:", None))
        self.labelDirection.setText(QCoreApplication.translate("SpawnDetailDialog", u"Direction:", None))
        self.labelTime.setText(QCoreApplication.translate("SpawnDetailDialog", u"Time (minutes):", None))
        self.labelSkip.setText(QCoreApplication.translate("SpawnDetailDialog", u"Skip AutoTrain:", None))
        self.skip_check.setText("")
        self.labelUnk1.setText(QCoreApplication.translate("SpawnDetailDialog", u"Unk 1:", None))
        self.labelUnk2.setText(QCoreApplication.translate("SpawnDetailDialog", u"Unk 2:", None))
        self.labelUnk3.setText(QCoreApplication.translate("SpawnDetailDialog", u"Unk 3:", None))
        self.labelUnk4.setText(QCoreApplication.translate("SpawnDetailDialog", u"Position Offset:", None))
        self.labelUnk5.setText(QCoreApplication.translate("SpawnDetailDialog", u"Unk 5:", None))
        self.save_button.setText(QCoreApplication.translate("SpawnDetailDialog", u"Update", None))
        self.cancel_button.setText(QCoreApplication.translate("SpawnDetailDialog", u"Cancel", None))
    # retranslateUi

