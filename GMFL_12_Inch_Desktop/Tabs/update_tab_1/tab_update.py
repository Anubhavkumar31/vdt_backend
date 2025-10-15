# # frontend/tabs/tab_update.py
# from PyQt5 import QtWidgets
# from GMFL_12_Inch_Desktop.Components import style1 as Style
# import GMFL_12_Inch_Desktop.Components.update_form as formComponent
#
# class UpdateTab(QtWidgets.QWidget):
#     """
#     Update Tab - contains the Update form layout and styling.
#     This tab is added inside the main right_tabWidget.
#     """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.parent = parent
#
#         # Basic setup
#         self.setObjectName("tab_update")
#         self.setStyleSheet(Style.tab_update)
#
#         # Layout for the tab
#         self.layout = QtWidgets.QVBoxLayout(self)
#
#         # Instantiate UpdateForm just for this tab
#         self.form_component = formComponent.UpdateForm()
#         self.form_component._init_form_layout(self, self.layout)




# frontend/tabs/tab_update.py
from PyQt5 import QtWidgets
from GMFL_12_Inch_Desktop.Components import style1 as Style
# import GMFL_12_Inch_Desktop.Tabs.update_tab_1.widgets.update_form as formComponent
from .widgets import update_form as formComponent

class UpdateTab(QtWidgets.QWidget):
    """
    UpdateTab - A dedicated tab inside the main right_tabWidget.
    Contains the UpdateForm widget for editing project details.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # --- Basic setup ---
        self.setObjectName("tab_update")
        self.setStyleSheet(Style.tab_update)

        # --- Layout for the tab ---
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(15)

        # --- Create and add the UpdateForm widget ---
        self.form = formComponent.UpdateForm(self)
        self.layout.addWidget(self.form)

        # --- (Optional) Stretch to keep layout responsive ---
        self.layout.addStretch(1)

        # --- Final layout assignment ---
        self.setLayout(self.layout)

    # -------------------------------------------------------------------------
    # Wrapper methods to interact with form easily from main window
    # -------------------------------------------------------------------------
    def set_previous_form_data(self, company_name):
        """
        Pass-through to form method for filling existing project data.
        """
        return self.form.set_previous_form_data(company_name)

    def update_data(self):
        """
        Trigger data update from the form.
        """
        self.form.update_data()

    def upload_data(self):
        """
        Trigger upload function from the form.
        """
        self.form.upload_data()

