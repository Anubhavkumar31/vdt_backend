import json
import os
import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox, QLabel
from google.oauth2 import service_account
from google.cloud import storage
# import Components.logger as logger
from datetime import datetime
from google.cloud import bigquery
from PyQt5.QtWebEngineWidgets import QWebEngineView
xyz = QWebEngineView
no_weld_indicator = False
connection = pymysql.connect(host='localhost', user='root', password='anubhav', db='gmfldesktop12')
credentials = service_account.Credentials.from_service_account_file('./utils/Authorization.json')
storage_client = storage.Client.from_service_account_json('./utils/GCS_Auth.json')
sensor_values = json.loads(open('./utils/sensor_value_update.json').read())
## runid=2
source_dataset_id = 'Processed_data_12inch_gmfl_without_time'
source_table_id = 'Main_12_copy_x14'
# source_table_id = 'Main_copy_12_partitioned_x23'
project_id = 'quantum-theme-334609'
table_name = project_id + '.'+source_dataset_id + '.'+source_table_id

"""     
Reference value will be consider 
"""
oddo1 = 1205.894
oddo2 = 0
roll_value = 34.71
pitch_value = 2.5
yaw_value = 83.43
pipe_thickness = 5.5                    ##### pipe_thickness changed accoridng to pipes #####
positive_sigma_col = 1.70                   ##### positive sigma standard deviation for defect calculation in clock heatmap #####
positive_sigma_row = 0.45                      ##### positive sigma standard deviation for defect calculation in clock heatmap #####
negative_sigma = 3                          ##### negative sigma standard deviation for defect calculation in clock heatmap #####
defect_box_thresh = 0.25              ##### defect boxing percentage in clock heatmap calculation #####
l_per_1 = 0.76                               ##### 24% length percentage in clock heatmap calculation #####
outer_dia = 324                             ################# outer_diametere 324 for 12 inch and 355 for 14 inch pipe #################
width_angle1 = 1.7                         ################# 1.7 for 12 inch(7.1 WT) and 1.60 for 14 inch(14.3 WT) pipe #################
width_angle2 = 3.4                         ################# 3.4 for 12 inch(7.1 WT) and 3.19 for 14 inch(14.3 WT) #################
width_angle3 = 9.7                        ################# 9.7 for 12 inch(7.1 WT) and 11.32 for 14 inch(14.3 WT) #################
w_per_1 = 0.55
oddo1_ref = 0
div_factor = 1.15
slope_per = 0.65
weld_pipe_pkl = os.getcwd() + '/DataFrames1/'
clock_pkl = os.getcwd() + '/ClockDataFrames/'
roll_pkl_lc = os.getcwd() + '/DataFrames_rollLC/'
image_folder = os.getcwd() + '/Charts/'
""" <!----------    Different length percentages but not stored in db, only in front    ----------!>    """
l_per_2 = 0.74                              ##### 26% length percentage in clock heatmap calculation #####
l_per_3 = 0.72                              ##### 28% length percentage in clock heatmap calculation #####
l_per_4 = 0.70                              ##### 30% length percentage in clock heatmap calculation #####

theta_ang1 = 1.7
theta_ang2 = 3.4
theta_ang3 = 9.7

client = bigquery.Client(credentials=credentials, project=project_id)
shared_dataset_ref = client.get_dataset(source_dataset_id)
print(shared_dataset_ref)
app = QtWidgets.QApplication([])
print("generated app ")
msg = QMessageBox()
print("mssage box created ")

def error_msg(Title, Description):
    """
    Method that will show a alert box for Error
    :param Title: Title of the Box
    :param Description: Description of the Box
    :return: void type
    """
    set_msg_body(Title, Description, QMessageBox.Critical, "Critical")


def info_msg(Title, Description):
    set_msg_body(Title, Description, QMessageBox.Information, "Information")


def warning_msg(Title, Description):
    set_msg_body(Title, Description, QMessageBox.Warning, "Warning")


def set_msg_body(Title, Description, icon, WindowTitle):
    try:
        msg.setIcon(icon)
        msg.setText(Title)
        msg.setInformativeText(Description)
        msg.setWindowTitle(WindowTitle)
        msg.exec_()
        app.exec_()
    except OSError as error:
        # logger.log_error(error or "Set_msg_body method failed with unknown Error")
        pass

def print_with_time(msg):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(msg, dt_string)
