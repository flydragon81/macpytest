from function.file_function.SpsParser import Sps21Parser
from configure import config
from function.file_function import check
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from sqlalchemy import and_
from function.db_function.dbtable import Template, Xps
from function.db_function.dbtable import choose_table
import os


class PointDbUpdate(QRunnable):
    def __init__(self, sess, file_name):
        super().__init__()
        self.sess = sess
        self.file_name = file_name
        self.signals = WorkerSignal()
        self.parser = Sps21Parser()
        self.commit_every = 5000

    @pyqtSlot()
    def run(self):
        self.signals.start.emit(False)
        line_numbers = check.iter_count(self.file_name)
        self.signals.process_max.emit(line_numbers)
        table_name = choose_table(self.file_name)
        counter = 0
        try:
            _session = self.sess()
            with open(self.file_name) as fr:
                for line in fr:
                    parsed = self.parser.parse_point(line)
                    if parsed:
                        tc = config.table_class[table_name]
                        query = _session.query(tc).filter(
                            and_(tc.line == parsed[1],
                                 tc.point == parsed[2],
                                 tc.idx == parsed[3]))
                        exsit_obj = _session.query(query.exists()).scalar()
                        if exsit_obj:
                            p = query.first()
                            p.x = parsed[10]
                            p.y = parsed[11]
                            p.z = parsed[12]
                        else:
                            p = tc(line=parsed[1], point=parsed[2], idx=parsed[3],
                                   x=parsed[10],
                                   y=parsed[11], z=parsed[12])
                            _session.add(p)
                    counter += 1
                    if counter % self.commit_every == 0:
                        self.signals.process.emit(counter)
                        _session.commit()
            self.signals.process.emit(counter)
            self.signals.finished.emit(True)
            _session.commit()
        except Exception as e:
            print('1' + str(e))
            self.signals.error.emit(str(e))


class XDbUpdate(QRunnable):
    def __init__(self, sess, file_name):
        super().__init__()
        self.sess = sess
        self.file_name = file_name
        self.signals = WorkerSignal()
        self.parser = Sps21Parser()
        self.commit_every = 10000

    @pyqtSlot()
    def run(self):
        self.signals.start.emit(False)
        line_numbers = check.iter_count(self.file_name)
        self.signals.process_max.emit(line_numbers)
        self.commit_every = int(line_numbers/20)
        # table_name = choose_table(self.file_name)
        counter = 0
        xid = 0
        tcounter = 0
        osln = 0.0
        ospn = 0.0
        osidx = 0
        try:
            _session = self.sess()
            with open(self.file_name) as fr:
                for line in fr:
                    counter += 1
                    parsed = self.parser.parse_relation(line)
                    tc = config.table_class['template']
                    if parsed:
                        xid += 1
                        sln = parsed[5]
                        spn = parsed[6]
                        spidx = parsed[7]

                        if sln == osln and spn == ospn and spidx == osidx:
                            pass
                        else:
                            if osln != 0.0:
                                xps = Xps(sline=osln, spoint=ospn, sidx=osidx, template_id=tcounter)
                                _session.add(xps)
                            xps = Xps()
                            tcounter += 1
                            xps.sline = sln
                            xps.spoint = spn
                            xps.sidx = spidx
                            xps.template_id = tcounter

                        template = tc(id=xid, sline=parsed[5], spoint=parsed[6], sidx=parsed[7],
                                      from_ch=parsed[8],
                                      to_ch=parsed[9], rline=parsed[11], from_rp=parsed[12],
                                      to_rp=parsed[13], ridx=parsed[14], temp_id=tcounter)
                        _session.add(template)
                        osln = sln
                        ospn = spn
                        osidx = spidx

                    if tcounter % self.commit_every == 0:
                        self.signals.process.emit(counter)
                        _session.commit()
                if template is not None:
                    _session.add(xps)

            self.signals.process.emit(counter)
            self.signals.finished.emit(True)
            _session.commit()
        except Exception as e:
            print('1' + str(e))
            self.signals.error.emit(str(e))


class DbSelectPoint(QRunnable):
    def __init__(self, sess, from_file_name, to_file_name):
        super().__init__()
        self.sess = sess
        self.from_file_name = from_file_name
        self.to_file_name = to_file_name

        self.signals = WorkerSignal()
        self.parser = Sps21Parser()
        self.commit_every = 5000

    @pyqtSlot()
    def run(self):
        try:
            self.signals.start.emit(False)
            line_numbers = check.iter_count(self.from_file_name)
            self.signals.process_max.emit(line_numbers)
            table_name = choose_table(self.from_file_name)
            file_suffix = file_type(self.from_file_name)
            _session = self.sess()
            counter = 0
            vcounter = 0
            ncounter = 0
            with open(self.from_file_name) as ff:
                with open(self.to_file_name, 'w') as tf:
                    for line in ff:
                        if file_suffix in config.point_table:
                            dat = select_from_sps(line, _session, table_name)
                        else:
                            dat = select_from_csv(line, _session, table_name)
                        vcounter += dat[1]
                        ncounter += dat[2]
                        if dat[0]:
                            for d in dat[0]:
                                print(d, end='\n', file=tf, flush=False)
                        counter += 1
                        if counter % self.commit_every == 0:
                            self.signals.process.emit(counter)
                    print(vcounter, ncounter)
                    self.signals.message.emit((vcounter, ncounter))
        except Exception as e:
            print(str(e))
        self.signals.process.emit(counter)
        self.signals.finished.emit(True)


class WorkerSignal(QObject):
    start = pyqtSignal(bool)
    process = pyqtSignal(int)
    process_max = pyqtSignal(int)
    message = pyqtSignal(tuple)
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)


def select_from_csv(line, session, table):
    line_interval = 16
    point_interval = 2
    data = []
    vcounter = 0
    ncounter = 0
    parsed = line.split(',')
    fl = int(parsed[1].strip())
    tl = int(parsed[2].strip())
    fp = int(parsed[3].strip())
    tp = int(parsed[4].strip())
    tc = config.table_class[table]
    for l in range(fl, tl + 1, line_interval):
        for p in range(fp, tp + 1, point_interval):
            query = session.query(tc).filter(and_(tc.line == float(l), tc.point == float(p)))
            exsit_obj = session.query(query.exists()).scalar()
            if exsit_obj:
                d = session.query(tc).filter(
                    and_(tc.line == float(l), tc.point == float(p))).first()
                data.append(d)
                vcounter += 1
            else:
                ncounter += 1
    return data, vcounter, ncounter


def select_from_sps(line, session, table):
    parser = Sps21Parser()
    parsed = parser.parse_point(line)
    tc = config.table_class[table]
    vcounter = 0
    ncounter = 0
    data = []
    if parsed:
        query = session.query(tc).filter(and_(tc.line == parsed[1], tc.point == parsed[2], tc.idx == parsed[3]))
        exsit_obj = session.query(query.exists()).scalar()
        if exsit_obj:
            d = session.query(tc).filter(
                and_(tc.line == parsed[1], tc.point == parsed[2], tc.idx == parsed[3])).first()
            data.append(d)
            vcounter += 1
        else:
            ncounter += 1
    return data, vcounter, ncounter


def select_from_xps():
    pass


def search_from_point_table(session, table, key1, key2):
    tc = config.table_class[table]
    if key1 > 0 and key2 > 0:
        data = session.query(tc).filter(
            and_(tc.line == key1, tc.point == key2)).all()
    else:
        data = session.query(tc).all()
    return data


def search_from_relation_table(session, table, key1, key2):
    tc = config.table_class['X']
    data = session.query(tc).filter(
        and_(tc.sline == key1, tc.spoint == key2)).all()
    # if len(data) > 0:
    #     for row in data:
    #         self.ui.output_text.append(str(row.point_template))
    # else:
    #     self.ui.output_text.setText('Not exist')

    return data


def file_type(file_name):
    file_end = os.path.splitext(file_name)[-1][1:].upper()
    return file_end

#
# class SpsDataDb:
#     COMMIT_X_EVERY = 100000
#
#     def __init__(self, parser: SpsParser, ses: session):
#         self.__session = ses
#         self.__parser = parser
#
#     def load_x(self, filename):
#         osln = 0.0
#         ospn = 0.0
#         osidx = 0
#
#         counter = 0
#         with open(filename, mode='r', buffering=(2 << 16) + 8) as sps:
#             line = sps.readline()
#             while line:
#                 counter += 1
#                 parsed = self.__parser.parse_relation(line)
#                 if parsed is not None:
#                     r = Relation(parsed)
#                     xps = Xps(sline=r.line, spoint=r.point, sidx=r.point_idx, from_ch=r.from_channel,
#                               to_ch=r.to_channel, rline=r.rcv_line, from_rp=r.from_rcv, to_rp=r.to_rcv, ridx=r.rcv_idx)
#                     self.__session.add(xps)
#                     sln = r.line
#                     spn = r.point
#                     spidx = r.point_idx
#
#                     if sln == osln and spn == ospn and spidx == osidx:
#                         template.relations.append(xps)
#                     else:
#                         template = Template()
#                         template.sline = sln
#                         template.spoint = spn
#                         template.sidx = spidx
#                         template.relations.append(xps)
#                         self.__session.add(template)
#
#                     osln = sln
#                     ospn = spn
#                     osidx = spidx
#                 line = sps.readline()
#
#                 if self.COMMIT_X_EVERY == counter:
#                     self.__session.commit()
#                     counter = 0
#
#         self.__session.commit()
#
#         # last template
#         # if template is not None:
#         #     templates.append(template)
#
#     def load_s(self, filename):
#         points = self.__load_points(filename)
#         # p: Point
#         for p in points:
#             point = Sps(line=p.line, point=p.point, idx=p.point_idx, easting=p.easting, northing=p.northing)
#             self.__session.add(point)
#
#         self.__session.commit()
#
#     def load_r(self, filename):
#         points = self.__load_points(filename)
#         # p: Point
#         for p in points:
#             point = Rps(line=p.line, point=p.point, idx=p.point_idx, easting=p.easting, northing=p.northing)
#             self.__session.add(point)
#
#         self.__session.commit()
#
#     def __load_points(self, filename):
#         points = []
#         with open(filename) as handle:
#             line = handle.readline()
#             while line:
#                 parsed = self.__parser.parse_point(line)
#                 if parsed is not None:
#                     points.append(Point(parsed))
#                 line = handle.readline()
#         return points
#
#     def get_all_s(self):
#         return self.__session.query(Sps).all()
#
#     def get_all_x(self):
#         return self.__session.query(Template).all()
#
#     def get_all_r(self):
#         return self.__session.query(Rps).all()
#
#     def get_all_r4line(self, line: float):
#         return self.__session.query(Rps).filter_by(line=line)
#
#     def get_r4line_range_points(self, line: float, frp: float, trp: float):
#         return self.__session.query(Rps).filter(Rps.line == line, Rps.point >= frp, Rps.point <= trp)
#
#     def get_s(self, line: float, point: float, idx: int) -> Sps:
#         return self.__session.query(Sps).filter_by(line=line, point=point, idx=idx).first()
#
#     def get_r(self, line: float, point: float, idx: int) -> Rps:
#         return self.__session.query(Rps).filter_by(line=line, point=point, idx=idx).first()
#
#
#
#
#
#
#


# import db_function
# from function.SpsParser import Sps21Parser
# import os
#
#
# def process(db_file, DB_TABLE, sps_file):
#     connection = db_function.create_connection(db_file)
#     parser = Sps21Parser()
#     print(DB_TABLE)
#     connection.execute("PRAGMA synchronous=OFF")  # 关闭同步
#     connection.execute("BEGIN TRANSACTION")  # 显式开启事务
#     print(connection)
#     with open(sps_file) as sps:
#         line = sps.readline()
#         print(line)
#         sps_counter = 0
#         while line:
#             print(line[0:1])
#             if line[0:1] not in db_function.table_list():
#                 #print(db.table_list())
#                 pass
#             else:
#                 print(db_function.table_list())
#                 parsed = parser.parse_point(line)
#                 db_function.insert_record_from_parsed_sps(connection, DB_TABLE, parsed)
#                 print(parsed)
#                 sps_counter += 1
#             line = sps.readline()
#
#             #progress_bar.setValue(sps_counter)
#     sps.close()
#     connection.commit()
#     #print(connection)
#     connection.close()
#     return sps_counter
#
#
# def find_data(db_file, DB_TABLE, sps_file):
#     connection = db_function.create_connection(db_file)
#     parser = Sps21Parser()
#     filePath = os.path.splitext(sps_file)[0] + "post.csv"
#     spsline=0
#     dataline=0
#
#     #print(DB_TABLE)
#     #connection.execute("PRAGMA synchronous=OFF")  # 关闭同步
#     #connection.execute("BEGIN TRANSACTION")  # 显式开启事务
#     with open(sps_file) as sps, open(filePath, 'w') as save :
#
#         line = sps.readline()
#         #print(line)
#         sps_counter = 0
#         while line:
#             if line[0:1] not in db_function.table_list():
#                 pass
#             else:
#                 spsline += 1
#                 parsed = parser.parse_point(line)
#                 #print(parsed)
#                 db_function.get_record_for_point(connection, DB_TABLE, parsed)
#                 data=db_function.get_record_for_point(connection, DB_TABLE, parsed)
#                 #print(data)
#                 if data:
#                     dataline += 1
#                     for da in data:
#                         print(da, file=save,end=""),
#                         print(',', file=save,end=""),
#                     print(file=save)
#                 #save.write(str(data[0]) + '\n')
#                 #return data
#                 #sps_counter += 1
#             line = sps.readline()
#
#             #progress_bar.setValue(sps_counter)
#     sps.close()
#     save.close()
#     #connection.commit()
#     #print(connection)
#     connection.close()
#     return str(spsline)+ str(dataline)
