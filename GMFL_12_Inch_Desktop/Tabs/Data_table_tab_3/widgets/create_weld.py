from PyQt5 import QtWidgets, QtCore
import GMFL_12_Inch_Desktop.Components.style1 as Style


class CreateWeldButton(QtWidgets.QWidget):
    """Reusable 'Create Weld and Pipe' button."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent   # this will be TabShowData
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # --- Button setup ---
        self.create_weld = QtWidgets.QPushButton()
        self.create_weld.setGeometry(QtCore.QRect(480, 265, 180, 43))
        self.create_weld.setObjectName("Create Weld Data")
        self.create_weld.setText("Create Weld and Pipe")
        self.create_weld.setStyleSheet(Style.btn_type_primary)

        # --- Connect to parent tab's CreateWeld method ---
        self.create_weld.clicked.connect(self.parent.parent.CreateWeld)

        layout.addWidget(self.create_weld)
        self.setLayout(layout)