from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData
from configure import config
import sqlite3

Base = declarative_base()


# 类相当于在sql中创建的一张表
class Rps(Base):
    __tablename__ = "R"
    line = Column(Float(10.2), primary_key=True)
    point = Column(Float(10.2), primary_key=True)
    idx = Column(Integer, primary_key=True)
    x = Column(Float(10.2))
    y = Column(Float(10.2))
    z = Column(Float(10.2))

    def __repr__(self):
        return "R %10.1f %10.1f %d %10.1f %10.1f %10.1f" \
               % (self.line, self.point, self.idx, self.x, self.y, self.z)


class Sps(Base):
    __tablename__ = "S"
    line = Column(Float(10.2), primary_key=True)
    point = Column(Float(10.2), primary_key=True)
    idx = Column(Integer, primary_key=True)
    x = Column(Float(10.2))
    y = Column(Float(10.2))
    z = Column(Float(10.2))

    def __repr__(self):
        return "S %10.1f %10.1f %d %10.1f %10.1f %10.1f" \
               % (self.line, self.point, self.idx, self.x, self.y, self.z)


class Xps(Base):
    __tablename__ = 'X'
    sline = Column(Float, primary_key=True)
    spoint = Column(Float, primary_key=True)
    sidx = Column(Integer, primary_key=True)
    # relations = Column()
    template_id = Column(Integer)

    def __repr__(self):
        return "X sline:%10.1f spoint:%10.1f sidx:%d template_id:%d" \
               % (self.sline, self.spoint, self.sidx, self.template_id)


class Template(Base):
    __tablename__ = 'template'
    id = Column(Integer, primary_key=True)
    sline = Column(Float)
    spoint = Column(Float)
    sidx = Column(Integer)
    from_ch = Column(Integer)
    to_ch = Column(Integer)
    rline = Column(Float)
    from_rp = Column(Float)
    to_rp = Column(Float)
    ridx = Column(Integer)
    temp_id = Column(Integer, ForeignKey("X.template_id"))

    xps = relationship("Xps", backref="point_template")

    def __repr__(self):
        return "X %d %10.1f %10.1f %1d %5d %5d %10.1f %10.1f %10.1f %1d temp_id:%d \n" \
               % (self.id, self.sline, self.spoint, self.sidx, self.from_ch, self.to_ch, self.rline, self.from_rp,
                  self.to_rp, self.ridx, self.temp_id)

class Valid(Base):
    __tablename__ = 'Valid'
    sline = Column(Float, primary_key=True)
    spoint = Column(Float, primary_key=True)
    sidx = Column(Integer)
    ffid = Column(Integer)

    def __repr__(self):
        return "X sline:%10.1f spoint:%10.1f sidx:%d ffid:%d" \
               % (self.sline, self.spoint, self.sidx, self.ffid)


def table_create(engine):
    try:
        Base.metadata.create_all(engine, checkfirst=True)
    except Exception as e:
        print(str(e))


def choose_table(data_file):
    with open(data_file) as sps:
        line = sps.readline()
        while line:
            if line[0:1] not in config.table_dict.keys():
                pass
            else:
                break
            line = sps.readline()
    sps.close()
    return line[0:1]


def truncate_db(engine):
    # delete all table data (but keep tables)
    # we do cleanup before test 'cause if previous test errored,
    # DB can contain dust
    meta = MetaData(bind=engine)
    con = engine.connect()
    trans = con.begin()
    # con.execute('SET FOREIGN_KEY_CHECKS = False;')
    for table in meta.sorted_tables:
        print(table)
        con.execute(table.delete())
    # con.execute('SET FOREIGN_KEY_CHECKS = Ture;')
    trans.commit()


def GetTables(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("select name from sqlite_master where type='table' order by name")
        print(cur.fetchall())
    except Exception as e:
        print(str(e))
'''
#查看表结构
cur.execute("PRAGMA table_info(T_Person)")
print cur.fetchall()
'''
