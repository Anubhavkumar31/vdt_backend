from google.cloud import bigquery
import json
import os
import pandas as pd
import GMFL_12_Inch_Desktop.Components.config as Config



connection = Config.connection
credentials = Config.credentials
project_id = Config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
config = json.loads(open('./utils/proximity_base_value.json').read())

"""
----->Line chart tab(4) all functions starts from here
"""
# def Line_chart1(self):
#     runid = self.parent.runid
#     weld_id = self.combo.currentText()
#     self.parent.weld_id = int(weld_id)
#     p = self.parent.project_name
#
#     print("Project:", p)
#
#     with connection.cursor() as cursor:
#         query = """
#             SELECT start_index, end_index, start_oddo1, end_oddo1
#             FROM welds
#             WHERE runid=%s AND id IN (
#                 %s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)
#             )
#             ORDER BY id
#         """
#         cursor.execute(query, (runid, self.parent.weld_id, runid, self.parent.weld_id))
#         result = cursor.fetchall()
#
#         if result:
#             path = os.path.join(Config.weld_pipe_pkl, p, f"{weld_id}.pkl")
#             print("Path:", path)
#
#             if os.path.isfile(path):
#                 Config.print_with_time("File exists")
#                 df_pipe = pd.read_pickle(path)
#                 self.plot_linechart_sensor(df_pipe)
#                 return
#
#             folder_path = os.path.join(Config.weld_pipe_pkl, p)
#             Config.print_with_time("File not exist")
#
#             os.makedirs(folder_path, exist_ok=True)
#             start_index, end_index = result[0][0], result[1][1]
#             Config.print_with_time(f"Start fetching at: {start_index}–{end_index}")
#
#             query_for_start = f"""
#                 SELECT index, ROLL, ODDO1, ODDO2,
#                        [F1H1, F1H2, F1H3, F1H4, ..., F36H1, F36H2, F36H3, F36H4],
#                        PITCH, YAW
#                 FROM {Config.table_name}
#                 WHERE index>{{}} AND index<{{}} ORDER BY index
#             """
#             query_job = client.query(query_for_start.format(start_index, end_index))
#             results = query_job.result()
#
#             data = []
#             index_t4, oddo_1, oddo_2 = [], [], []
#             roll1, pitch1, yaw1 = [], [], []
#
#             for row in results:
#                 index_t4.append(row[0])
#                 roll1.append(row[1])
#                 oddo_1.append(row[2])
#                 oddo_2.append(row[3])
#                 data.append(row[4])
#                 pitch1.append(row[5])
#                 yaw1.append(row[6])
#
#             # Apply reference adjustments
#             oddo1_t4 = [x - Config.oddo1 for x in oddo_1]
#             oddo2_t4 = [x - Config.oddo2 for x in oddo_2]
#             roll_t4 = [x - Config.roll_value for x in roll1]
#             pitch_t4 = [x - Config.pitch_value for x in pitch1]
#             yaw_t4 = [x - Config.yaw_value for x in yaw1]
#
#             # Proximity query
#             query_for_prox = f"""
#                 SELECT index, [F1P1, F2P2, ..., F36P4]
#                 FROM {Config.table_name}
#                 WHERE index>{{}} AND index<{{}} ORDER BY index
#             """
#             query_job = client.query(query_for_prox.format(start_index, end_index))
#             results_1 = query_job.result()
#
#             data1, index_lc = [], []
#             for row1 in results_1:
#                 index_lc.append(row1[0])
#                 data1.append(row1[1])
#
#             df_new_proximity_lc = pd.DataFrame(
#                 data1, columns=[f"F{i}P{j}" for i in range(1, 37) for j in range(1, 5)]
#             )
#             df_new_t4 = pd.DataFrame(
#                 data, columns=[f"F{i}H{j}" for i in range(1, 37) for j in range(1, 5)]
#             )
#             df_elem = pd.DataFrame({
#                 "index": index_t4,
#                 "ODDO1": oddo_1,
#                 "ROLL": roll_t4,
#                 "PITCH": pitch_t4,
#                 "YAW": yaw_t4
#             })
#
#             frames = [df_elem, df_new_t4]
#             df_pipe = pd.concat(frames, axis=1, join="inner")
#
#             for col in df_new_proximity_lc.columns:
#                 df_pipe[col] = df_new_proximity_lc[col]
#
#             df_pipe.to_pickle(os.path.join(folder_path, f"{weld_id}.pkl"))
#             Config.print_with_time("Successfully saved to pickle file")
#             Config.print_with_time("End fetching at:")
#             self.parent.plot_linechart_sensor(df_pipe)
#
#         else:
#             Config.print_with_time("No data found for this pipe ID.")




def Line_chart1(self):
    runid = self.parent.runid
    weld_id = self.combo.currentText()
    self.parent.weld_id = int(weld_id)
    p = self.parent.project_name

    print("Project:", p)

    with connection.cursor() as cursor:
        query = """
            SELECT start_index, end_index, start_oddo1, end_oddo1
            FROM welds
            WHERE runid=%s AND id IN (
                %s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s)
            )
            ORDER BY id
        """
        cursor.execute(query, (runid, self.parent.weld_id, runid, self.parent.weld_id))
        result = cursor.fetchall()

        if result:
            path = os.path.join(Config.weld_pipe_pkl, p, f"{weld_id}.pkl")
            print("Path:", path)

            if os.path.isfile(path):
                Config.print_with_time("File exists")
                df_pipe = pd.read_pickle(path)
                self.plot_linechart_sensor(df_pipe)
                return

            folder_path = os.path.join(Config.weld_pipe_pkl, p)
            Config.print_with_time("File not exist")

            os.makedirs(folder_path, exist_ok=True)
            start_index, end_index = result[0][0], result[1][1]
            Config.print_with_time(f"Start fetching at: {start_index}–{end_index}")

            # ✅ FIXED QUERY: removed square brackets, added proper columns
            hall_sensors = ', '.join([f"F{i}H{j}" for i in range(1, 37) for j in range(1, 5)])
            query_for_start = f"""
                SELECT index, ROLL, ODDO1, ODDO2,
                       {hall_sensors},
                       PITCH, YAW
                FROM `{Config.table_name}`
                WHERE index>{start_index} AND index<{end_index}
                ORDER BY index
            """
            query_job = client.query(query_for_start)
            results = query_job.result()

            data = []
            index_t4, oddo_1, oddo_2 = [], [], []
            roll1, pitch1, yaw1 = [], [], []

            for row in results:
                index_t4.append(row[0])
                roll1.append(row[1])
                oddo_1.append(row[2])
                oddo_2.append(row[3])
                # collect hall-sensor array from row[4:-2]
                data.append(list(row[4:-2]))
                pitch1.append(row[-2])
                yaw1.append(row[-1])

            # Apply reference adjustments
            oddo1_t4 = [x - Config.oddo1 for x in oddo_1]
            oddo2_t4 = [x - Config.oddo2 for x in oddo_2]
            roll_t4 = [x - Config.roll_value for x in roll1]
            pitch_t4 = [x - Config.pitch_value for x in pitch1]
            yaw_t4 = [x - Config.yaw_value for x in yaw1]

            # ✅ FIXED QUERY for proximity columns
            prox_sensors = ', '.join([f"F{i}P{j}" for i in range(1, 37) for j in range(1, 5)])
            query_for_prox = f"""
                SELECT index, {prox_sensors}
                FROM `{Config.table_name}`
                WHERE index>{start_index} AND index<{end_index}
                ORDER BY index
            """
            query_job = client.query(query_for_prox)
            results_1 = query_job.result()

            data1, index_lc = [], []
            for row1 in results_1:
                index_lc.append(row1[0])
                data1.append(list(row1[1:]))

            df_new_proximity_lc = pd.DataFrame(
                data1, columns=[f"F{i}P{j}" for i in range(1, 37) for j in range(1, 5)]
            )
            df_new_t4 = pd.DataFrame(
                data, columns=[f"F{i}H{j}" for i in range(1, 37) for j in range(1, 5)]
            )
            df_elem = pd.DataFrame({
                "index": index_t4,
                "ODDO1": oddo_1,
                "ROLL": roll_t4,
                "PITCH": pitch_t4,
                "YAW": yaw_t4
            })

            frames = [df_elem, df_new_t4]
            df_pipe = pd.concat(frames, axis=1, join="inner")

            for col in df_new_proximity_lc.columns:
                df_pipe[col] = df_new_proximity_lc[col]

            df_pipe.to_pickle(os.path.join(folder_path, f"{weld_id}.pkl"))
            Config.print_with_time("Successfully saved to pickle file")
            Config.print_with_time("End fetching at:")
            self.parent.plot_linechart_sensor(df_pipe)

        else:
            Config.print_with_time("No data found for this pipe ID.")
