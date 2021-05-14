"""
name
"""
from function.db_function.dbtable import Rps, Sps, Xps, Template

x_file_pattern = '"XPS (*.xps, *.x, *.XPS, *.X )"'
s_file_pattern = '"SPS (*.sps, *.s, *.SPS, *.S )"'
r_file_pattern = '"RPS (*.rps, *.r, *.RPS, *.R )"'
db_file_pattern = '"SQLite (*.sqlite )"'
sps_file_pattern = '"RPS (*.rps, *.r, *.RPS, *.R )";;"SPS (*.sps, *.s, *.SPS, *.S )";;"XPS (*.xps, *.x, *.XPS, *.X )"'
'''
table config
'''
point_table_content = '''(
                        line real NOT NULL,
                        point real NOT NULL,
                        idx int NOT NULL,
                        easting real NOT NULL,
                        northing real NOT NULL,
                        elevation real NOT NULL,
                        PRIMARY KEY(line, point, idx)'''

table_dict = {'R': point_table_content,
              'S': point_table_content,
              'X': point_table_content,
              }

table_class = {'R': Rps,
               'S': Sps,
               'X': Xps,
               'template': Template
               }
point_table = ['R', 'S']

colspecsp = [(0, 1), (1, 11), (11, 21), (21, 24), (24, 26), (26, 30), (30, 34),
             (34, 38), (38, 40), (40, 46), (46, 55), (55, 65), (65, 71), (71, 74), (74, 80)]
colspecsx = [(0, 1), (1, 7), (7, 15), (15, 16), (16, 17), (17, 27), (27, 37), (37, 38), (38, 43), (43, 48), (48, 49),
             (49, 59), (59, 69), (69, 79), (79, 80)]
# SQL_CREATE_TABLE = """ CREATE TABLE IF NOT EXISTS  {}{}
# ); """.format(list(table_dict.keys())[0], table_dict[list(table_dict.keys())[0]])
#
# print(SQL_CREATE_TABLE)
