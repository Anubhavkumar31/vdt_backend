# frontend/tabs/tab_ShowData.py
from PyQt5 import QtWidgets
from .widgets.ShowWeld import ShowWeldSelection
from .widgets.WeldTable import WeldTable
from .widgets.create_weld import CreateWeldButton
from .widgets.weld_pipe_table import FetchWeldToPipe, FetchWeldToPipeButton
from .widgets.defect_pipe_table import FetchDefectList, FetchDefectListButton
from GMFL_12_Inch_Desktop.Components import config as Config
from PyQt5.QtWidgets import QAbstractItemView
import os, json
from google.cloud import bigquery


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\utils\GCS_Auth.json"
connection = Config.connection
credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
config = json.loads(open(r'D:\Anubhav\vdt_backend\GMFL_12_Inch_Desktop\utils\proximity_base_value.json').read())


class TabShowData(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # main window
        self.setObjectName("tab_3")
        self.setStyleSheet("background-color: #EDF6FF;")

        layout = QtWidgets.QVBoxLayout(self)



        # --- Weld data table (now self-contained class) ---
        self.myTableWidget = WeldTable(self)
        self.myTableWidget.bind_double_click(self.parent.viewClicked)
        layout.addWidget(self.myTableWidget)

        # --- Fetch Weld button ---
        self.ShowWeld = ShowWeldSelection(self)
        layout.addWidget(self.ShowWeld)

        # --- create weld button ---
        self.CreateWeldSection = CreateWeldButton(self)
        layout.addWidget(self.CreateWeldSection)

        # --- weld to pipe table ---
        self.myTableWidget1 = FetchWeldToPipe(self)
        layout.addWidget(self.myTableWidget1)

        # --- weld to pipe button ---
        self.Show_Weld_to_Pipe = FetchWeldToPipeButton(self)
        layout.addWidget(self.Show_Weld_to_Pipe)

        # --- defect table ---
        self.myTableWidget2 = FetchDefectList(self)
        layout.addWidget(self.myTableWidget2)

        # --- defect table button ---
        self.Show_Defect_list = FetchDefectListButton(self)
        layout.addWidget(self.Show_Defect_list)

        self.setLayout(layout)

    # --- Logic for fetching and populating weld data ---
    def Show_Weld(self):
        runid = self.parent.runid
        try:
            with connection.cursor() as cursor:
                query = (
                    "select weld_number,runid,analytic_id,sensitivity,length,"
                    "start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2 "
                    "from welds where runid=%s and id>%s"
                )
                cursor.execute(query, (int(runid), 1))
                rows = cursor.fetchall()

                table = self.myTableWidget
                table.setRowCount(0)

                if rows:
                    for r, row_data in enumerate(rows):
                        table.insertRow(r)
                        for c, data in enumerate(row_data):
                            table.setItem(r, c, QtWidgets.QTableWidgetItem(str(data)))
                else:
                    Config.warning_msg("No record found", "")

                weld_ids = [str(i[0]) for i in rows]
                print("weld_id_list:", weld_ids)

                # combos belong to main window
                self.parent.combo.addItems(weld_ids)
                self.parent.combo_orientation.addItems(weld_ids)
                self.parent.combo_box.addItems(weld_ids)
                self.parent.combo_graph.addItems(weld_ids)
                self.parent.combo_box1.addItems(weld_ids)
                self.parent.combo_tab9.addItems(weld_ids)

        except Exception as e:
            print("Error in Show_Weld:", e)
            Config.warning_msg("Error fetching weld data", str(e))

    def ShowWeldToPipe(self):
        """
        Populate the Weld→Pipe table for the selected run.
        """
        main = self.parent  # access main window
        runid = getattr(main, "runid", None)
        if runid is None:
            Config.warning_msg("No RunID loaded", "")
            return

        try:
            with connection.cursor() as cursor:
                query = (
                    "SELECT id, runid, analytic_id, lower_sensitivity, "
                    "upper_sensitivity, length, start_index, end_index "
                    "FROM pipes WHERE runid = %s"
                )
                cursor.execute(query, (int(runid),))
                rows = cursor.fetchall()

                table = self.myTableWidget1
                table.setRowCount(0)

                if rows:
                    for r, row_data in enumerate(rows):
                        table.insertRow(r)
                        for c, data in enumerate(row_data):
                            table.setItem(r, c, QtWidgets.QTableWidgetItem(str(data)))
                    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    Config.warning_msg("No record found", "")

                pipe_ids = [str(i[0]) for i in rows]
                print("pipe_id_list:", pipe_ids)

        except Exception as e:
            print("Error in ShowWeldToPipe:", e)
            Config.warning_msg("Error fetching weld-to-pipe data", str(e))

    def DefectList(self):
        """
        Fetch and populate defect list table for the selected run ID.
        """
        main = self.parent  # main window reference
        runid = getattr(main, "runid", None)
        if runid is None:
            Config.warning_msg("No RunID loaded", "")
            return

        try:
            with connection.cursor() as cursor:
                query = (
                    "SELECT id, runid, start_observation, end_observation, "
                    "start_sensor, end_sensor, angle, length, breadth, depth, type "
                    "FROM defect_sensor_hm WHERE runid = %s"
                )
                cursor.execute(query, (int(runid),))
                rows = cursor.fetchall()

                table = self.myTableWidget2  # your FetchDefectList instance
                table.setRowCount(0)

                if rows:
                    for row_number, row_data in enumerate(rows):
                        table.insertRow(row_number)
                        for column_num, data in enumerate(row_data):
                            table.setItem(row_number, column_num, QtWidgets.QTableWidgetItem(str(data)))
                    table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                else:
                    Config.warning_msg("No record found", "")

                print(f"[DEBUG] Fetched {len(rows)} defect records for runid {runid}")

        except Exception as e:
            print("Error in DefectList:", e)
            Config.warning_msg("Error fetching defect list", str(e))


