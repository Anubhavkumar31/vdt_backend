import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, QtWebEngineWidgets
from GMFL_12_Inch_Desktop.Tabs.Line_plot_tab_4.widgets.helper_functions import Line_chart1
from google.cloud import bigquery
import json
import os
import pandas as pd
import GMFL_12_Inch_Desktop.Components.config as Config
from PyQt5.QtWidgets import QMessageBox
from scipy.signal import savgol_filter, lfilter
from matplotlib.widgets import RectangleSelector
from matplotlib.transforms import Bbox
from sklearn.preprocessing import MinMaxScaler
from PyQt5.QtCore import QUrl
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# Dynamically locate the GMFL root (2 levels above this file)
GMFL_ROOT = Path(__file__).resolve().parents[2]


def gmfl_path(relative):
    """Return absolute path inside GMFL backend_data/temp folder."""
    temp_dir = GMFL_ROOT / "backend_data" / "data_generated" / "temp"
    os.makedirs(temp_dir, exist_ok=True)  # make sure folder exists
    return str(temp_dir / relative)

connection = Config.connection
credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
config = json.loads(open('./utils/proximity_base_value.json').read())



class LinePlotTab:
    """
    Line Plotting Tab (PyQt5 Version)
    ---------------------------------
    - Child UI class that delegates all event handlers to the parent main window.
    - Keeps logic identical to the procedural version.
    """

    def __init__(self, parent=None):
        self.parent = parent
        self._setup_tab()

    # =====================================================
    # ----------------- UI SETUP --------------------------
    # =====================================================
    def _setup_tab(self):
        """Sets up all widgets and layouts (logic unchanged)."""

        # ---- Create Tab Widget ----
        self.tab_line1 = QtWidgets.QWidget()
        self.tab_line1.setObjectName("tab_4")
        self.tab_line1.setStyleSheet("background-color: #EDF6FF;")

        # ---- Layouts ----
        self.hb5 = QtWidgets.QHBoxLayout(self.tab_line1)
        self.vb5 = QtWidgets.QVBoxLayout()

        # ---- Matplotlib Canvas ----
        self.figure_x5 = plt.figure(figsize=(25, 8))
        self.canvas_x5 = FigureCanvas(self.figure_x5)
        self.toolbar_x5 = NavigationToolbar(self.canvas_x5, self.tab_line1)

        # ---- Combo Box ----
        self.combo = QtWidgets.QComboBox()
        self.combo.setObjectName("Pipe_id")
        self.combo.setCurrentText("pipe_id")

        # ---- Reset Button ----
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.reset_btn.clicked.connect(self.parent.reset_btn_fun)

        # ---- Latitude / Longitude ----
        self.latitude = QtWidgets.QLineEdit()
        self.latitude.setFixedWidth(100)
        self.logitude = QtWidgets.QLineEdit()
        self.logitude.setFixedWidth(100)

        # ---- Marker Buttons ----
        self.selection_mark_lat_long = QtWidgets.QPushButton("Mark Lat Long")
        self.selection_mark_lat_long.clicked.connect(self.mark_lat_long)

        self.selection_mark_base_value = QtWidgets.QPushButton("Mark Base Value")
        self.selection_mark_base_value.clicked.connect(self.parent.basevalue)

        self.feature_selection = QtWidgets.QPushButton("Mark Feature")
        self.feature_selection.clicked.connect(self.parent.feature_selection_func)

        # ---- Internal State ----
        self.rect_start_1 = None
        self.rect_end_1 = None

        # ---- Line Chart + Navigation Buttons ----
        self.button_x5 = QtWidgets.QPushButton("Line Chart")
        self.button_x5.clicked.connect(lambda: Line_chart1(self))
        self.button_x5.resize(50, 50)

        self.next_btn_lc = QtWidgets.QPushButton("Next")
        self.next_btn_lc.setStyleSheet("background-color: white; color: black;")
        self.next_btn_lc.clicked.connect(self.parent.Line_chart1_next)

        self.prev_btn_lc = QtWidgets.QPushButton("Previous")
        self.prev_btn_lc.setStyleSheet("background-color: white; color: black;")
        self.prev_btn_lc.clicked.connect(self.parent.Line_chart1_previous)

        # ---- Navigation Layout ----
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.prev_btn_lc)
        button_layout.addStretch(1)
        button_layout.addWidget(self.next_btn_lc)
        button_layout_widget = QtWidgets.QWidget()
        button_layout_widget.setLayout(button_layout)

        # ---- Web Output View ----
        self.m_output_proxi = QtWebEngineWidgets.QWebEngineView(self.tab_line1)

        # ---- Main Layout Hierarchy ----
        self.hb5.addLayout(self.vb5, 75)

        self.hbox_5 = QtWidgets.QHBoxLayout()
        self.hbox_6 = QtWidgets.QHBoxLayout()
        self.hbox_7 = QtWidgets.QHBoxLayout()

        self.vb5.addLayout(self.hbox_5)
        self.vb5.addLayout(self.hbox_6, 60)
        self.vb5.addLayout(self.hbox_7, 40)
        self.vb5.addWidget(button_layout_widget)

        # ---- Top Toolbar Section ----
        self.hbox_5.addWidget(self.toolbar_x5)
        self.hbox_5.addWidget(self.combo)
        self.hbox_5.addWidget(self.button_x5)
        self.hbox_5.addWidget(self.latitude)
        self.hbox_5.addWidget(self.logitude)
        self.hbox_5.addWidget(self.selection_mark_lat_long)
        self.hbox_5.addWidget(self.selection_mark_base_value)
        self.hbox_5.addWidget(self.feature_selection)
        self.hbox_5.addWidget(self.reset_btn)

        # ---- Chart and Output ----
        self.hbox_6.addWidget(self.canvas_x5)
        self.hbox_7.addWidget(self.m_output_proxi)

        self.tab_line1.setLayout(self.hb5)

        """
        -------> End of fourth tab (Line Plotting)
        """

    def mark_lat_long(self):
        try:
            print("[DEBUG] mark_lat_long called")
            print(f"[DEBUG] rect_start_1={self.rect_start_1}, rect_end_1={self.rect_end_1}")

            if self.rect_start_1 is not None and self.rect_end_1 is not None:
                x1, y1 = min(self.rect_start_1[0], self.rect_end_1[0]), \
                         min(self.rect_start_1[1], self.rect_end_1[1])
                x2, y2 = x1 + abs(self.rect_end_1[0] - self.rect_start_1[0]), \
                         y1 + abs(self.rect_end_1[1] - self.rect_start_1[1])
                lat_mark = self.latitude.text().strip()
                long_mark = self.logitude.text().strip()
                print(f"[DEBUG] lat_mark={lat_mark}, long_mark={long_mark}")

                if lat_mark and long_mark:
                    print("[DEBUG] Entering DB logic")
                    index = getattr(self, "index", None)
                    if index is None:
                        raise ValueError("self.index not found in class scope")

                    start_index = index.iloc[int(self.rect_start_1[0])]
                    end_index = index.iloc[int(self.rect_end_1[0])]
                    runid = getattr(self.parent, "runid", None)
                    weld_id = getattr(self.parent, "weld_id", None)

                    if runid is None or weld_id is None:
                        raise ValueError("Missing runid or weld_id in class")

                    print(f"[DEBUG] runid={runid}, weld_id={weld_id}")
                    print(f"[DEBUG] start_index={start_index}, end_index={end_index}")

                    query_for_start = 'SELECT * FROM ' + Config.table_name + ' WHERE index={}'
                    query_job = client.query(query_for_start.format(start_index))
                    results_1 = query_job.result()

                    oddo1, oddo2 = [], []
                    for row1 in results_1:
                        oddo1.append(row1['ODDO1'])
                        oddo2.append(row1['ODDO2'])
                    print(f"[DEBUG] Raw oddo1={oddo1}, oddo2={oddo2}")

                    if not oddo1 or not oddo2:
                        raise ValueError("Empty oddo1/oddo2 fetched from query")

                    oddo1 = oddo1[0] - Config.oddo1
                    oddo2 = oddo2[0] - Config.oddo2
                    print(f"[DEBUG] Adjusted oddo1={oddo1}, oddo2={oddo2}")

                    with connection.cursor() as cursor:
                        same_lw_up_check = cursor.execute(
                            'SELECT absolute_distance_oddo1, absolute_distance_oddo2 FROM dgps_segment '
                            'WHERE absolute_distance_oddo1=%s AND absolute_distance_oddo2=%s',
                            (oddo1, oddo2)
                        )

                        print(f"[DEBUG] same_lw_up_check={same_lw_up_check}")

                        if same_lw_up_check:
                            print("[DEBUG] Duplicate entry found, skipping insert.")
                            return 'HII'

                        query_pipe_insert = (
                            "INSERT INTO dgps_segment (runid, pipe_id, start_index, "
                            "absolute_distance_oddo2, absolute_distance_oddo1, Latitude, Longitude) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        )
                        cursor.execute(query_pipe_insert, (
                            int(runid), int(weld_id), int(start_index),
                            oddo2, oddo1, lat_mark, long_mark
                        ))
                        connection.commit()
                        print("[DEBUG] Data inserted successfully.")

                    QMessageBox.information(self.tab_line1, 'Success', 'Data saved')

                else:
                    QMessageBox.warning(self.tab_line1, 'Invalid Input', 'Enter any value')

            else:
                QMessageBox.warning(
                    self.tab_line1,
                    'Invalid Input',
                    'Select RectangleSelection of Marking, then press the button for Lat And Long'
                )

        except Exception as e:
            import traceback
            err_details = traceback.format_exc()
            print("========== [DEBUG] mark_lat_long ERROR ==========")
            print(err_details)
            print("==================================================")
            QMessageBox.critical(self.tab_line1, 'Error', f'Error in mark_lat_long:\n{str(e)}')

    def line_selection5(self, eclick, erelease):
        """Handles rectangular selection and saves start/end coords."""
        try:
            if abs(eclick.x - erelease.x) >= 3 and abs(eclick.y - erelease.y) >= 3:
                self.rect_start_1 = (eclick.xdata, eclick.ydata)
                self.rect_end_1 = (erelease.xdata, erelease.ydata)

                ax = self.figure_x5.gca()
                for patch in list(ax.patches):  # clear existing rectangles
                    patch.remove()

                rect = plt.Rectangle(
                    (min(self.rect_start_1[0], self.rect_end_1[0]),
                     min(self.rect_start_1[1], self.rect_end_1[1])),
                    abs(self.rect_end_1[0] - self.rect_start_1[0]),
                    abs(self.rect_end_1[1] - self.rect_start_1[1]),
                    edgecolor='black',
                    linewidth=1,
                    fill=False
                )
                ax.add_patch(rect)
                self.canvas_x5.draw()

                print(f"[DEBUG] Rectangle selected: {self.rect_start_1} → {self.rect_end_1}")
            else:
                print("[DEBUG] Too small to select.")
        except Exception as e:
            import traceback
            print(f"[ERROR] line_selection5 failed: {e}")
            traceback.print_exc()


    def plot_linechart_sensor(self, df_pipe):
        print("hi sensor linechart")
        self.index = df_pipe['index']
        oddo1 = (df_pipe['ODDO1'] - Config.oddo1) / 1000

        self.figure_x5.clear()
        self.ax5 = self.figure_x5.add_subplot(111)
        self.ax5.figure.subplots_adjust(bottom=0.085, left=0.055, top=0.930, right=0.920)
        self.ax5.clear()

        res = [f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]
        df1 = df_pipe[res].apply(pd.to_numeric, errors='coerce')

        # ------------------- Denoising -------------------
        window_length = 15
        polyorder = 2
        for col in res:
            data = df1[col].values
            time_index = np.arange(len(df1))
            coefficients = np.polyfit(time_index, data, polyorder)
            trend = np.polyval(coefficients, time_index)
            data_dettrended = data - trend
            data_denoised = savgol_filter(data_dettrended, window_length, polyorder)
            df1.loc[:len(df1), col] = data_denoised

        for i, data in enumerate(res):
            df1[data] = df1[data] + i * 1400

        n = 15
        b = [1.0 / n] * n
        a = 1

        for i, data in enumerate(res):
            filtered_data = lfilter(b, a, df1[data])
            self.ax5.plot(self.index, filtered_data, label=i)

        self.ax5.margins(x=0, y=0)
        oddo_val = list(oddo1)
        num_ticks1 = len(self.ax5.get_xticks())
        tick_positions1 = [int(i) for i in np.linspace(0, len(oddo_val) - 1, num_ticks1)]

        ax4 = self.ax5.twiny()
        ax4.set_xticks(tick_positions1)
        ax4.set_xticklabels([f'{oddo_val[i]:.2f}' for i in tick_positions1], size=8)
        ax4.set_xlabel("Absolute Distance (m)", size=8)

        def on_hover(event):
            if event.inaxes:
                try:
                    x, y = event.xdata, event.ydata
                    if x is not None:
                        x = int(event.xdata)
                        y = int(event.ydata)
                        z = (df_pipe.loc[df_pipe.index == x, 'ODDO1']) - Config.oddo1
                        Abs_distance = int(z.values[0])
                        index_value = df_pipe.loc[df_pipe.index == x, 'index']
                        index_value_1 = int(index_value.values[0])
                        self.toolbar_x5.set_message(
                            f"Index_Value={index_value_1}, Abs.Distance(mm)={Abs_distance / 1000:.2f},\nSensor_offset_Values={y}"
                        )
                except (IndexError, ValueError):
                    print("Hovering outside valid data range.")

        self.canvas_x5.mpl_connect('motion_notify_event', on_hover)

        legend = self.ax5.legend(res, loc="upper left", bbox_to_anchor=(1.02, 0, 0.07, 1))
        d = {"down": 30, "up": -30}

        def func_scroll(evt):
            if legend.contains(evt):
                bbox = legend.get_bbox_to_anchor()
                bbox = Bbox.from_bounds(bbox.x0, bbox.y0 + d[evt.button], bbox.width, bbox.height)
                tr = legend.axes.transAxes.inverted()
                legend.set_bbox_to_anchor(bbox.transformed(tr))
                self.canvas_x5.draw_idle()

        self.canvas_x5.mpl_connect("scroll_event", func_scroll)

        # ------------------- Proximity Plot -------------------
        df_proxi_data = [
            'F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3', 'F8P4', 'F9P1', 'F10P2',
            'F11P3', 'F12P4', 'F13P1', 'F14P2', 'F15P3', 'F16P4', 'F17P1', 'F18P2', 'F19P3',
            'F20P4', 'F21P1', 'F22P2', 'F23P3', 'F24P4', 'F25P1', 'F26P2', 'F27P3', 'F28P4',
            'F29P1', 'F30P2', 'F31P3', 'F32P4', 'F33P1', 'F34P2', 'F35P3', 'F36P4'
        ]

        scaler = MinMaxScaler()
        scaled_values = scaler.fit_transform(df_pipe[df_proxi_data])
        for i, col in enumerate(df_proxi_data):
            df_pipe[col] = scaled_values[:, i]

        n = 15
        b = [1.0 / n] * n
        a = 1
        ls = [round(i * 0.3, 1) for i in range(1, 37)]

        for j1, column2 in enumerate(df_proxi_data):
            df_pipe[column2] = df_pipe[column2] + ls[j1]

        fig = go.Figure()
        for i1, column1 in enumerate(df_proxi_data):
            yy = lfilter(b, a, df_pipe[column1])
            fig.add_trace(go.Scatter(x=df_pipe.index, y=yy, name=column1))

        fig.update_layout(
            width=1800,
            height=400,
            title={'x': 0.5},
            font={"family": "courier"},
        )
        fig.update_xaxes(
            title_text="ODDO1(Absolute Distance(m))",
            tickfont=dict(size=11),
            dtick=1000,
            tickangle=0,
            showticklabels=True,
            ticklen=0,
        )

        file_path = gmfl_path("h_line_chart_proxi.html")
        pio.write_html(fig, file=file_path, auto_open=False)
        self.m_output_proxi.load(QUrl.fromLocalFile(file_path))

        self.canvas_x5.draw()
        Config.print_with_time("End plotting at : ")

        # --- Rectangle Selector (same as original logic) ---
        self.rs1 = RectangleSelector(self.figure_x5.gca(), self.line_selection5, useblit=True)
        plt.connect('key_press_event', self.rs1)




