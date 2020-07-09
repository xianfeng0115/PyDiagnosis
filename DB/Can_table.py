# coding:utf-8

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, and_, Float

from sqlalchemy.orm import relationship, backref
from Common.CommonVar import BASE
from datetime import datetime


class CanTask(BASE):
    __tablename__ = 'CanTask'  # 表格名字
    id = Column(Integer, primary_key=True, autoincrement=True)
    current = Column(DateTime, default=datetime.now)
    content = Column(String(200), nullable=False)
    can_len = Column(Integer, nullable=False)
    can_id = Column(String(20), nullable=False)
    Tx_Rx = Column(String(20), nullable=False)
    cycle_time = Column(String(20), nullable=False)
    explain = Column(String(200), nullable=False)

    def __str__(self):
        return "{'current':'%s','content':'%s','can_len':'%s','can_id':'%s','Tx_Rx':'%s','cycle_time':%s,'explain':'%s' }" % (
            self.current,
            self.content,
            self.can_len,
            self.can_id,
            self.Tx_Rx,
            self.cycle_time,
            self.explain,
        )


class EcuMsg(BASE):
    __tablename__ = 'EcuMsg'  # 表格名字
    id = Column(Integer, primary_key=True, autoincrement=True)
    ecu_name = Column(String(50), nullable=False)
    msg_id = Column(String(10), nullable=False)
    msg_name = Column(String(50), nullable=False)
    msg_value = Column(String(50), nullable=False)
    len = Column(String(10), nullable=False)
    cycle = Column(Boolean, default=0, nullable=False)
    cycle_time = Column(Integer, default=0, nullable=False)
    count = Column(Integer, default=1, nullable=False)
    Intervaltime = Column(Float, default=0, nullable=False)
    delaytime = Column(Float, default=0, nullable=False)

    # single_name = relationship("single_name", backref="EcuMsg")

    def __str__(self):
        return "{'msg_id':'%s','msg_name':'%s','msg_value':'%s','len':'%s'" \
               ",'cycle':'%s','cycle_time':'%s','count':'%s','Intervaltime':'%s,'delaytime':'%s" % (
                   self.msg_id,
                   self.msg_name,
                   self.msg_value,
                   self.len,
                   self.cycle,
                   self.cycle_time,
                   self.count,
                   self.Intervaltime,
                   self.delaytime
               )


class EcuSingle(BASE):
    __tablename__ = 'EcuSingle'  # 表格名字
    id = Column(Integer, primary_key=True, autoincrement=True)
    single_name = Column(String(50), nullable=False)
    single_unit = Column(String(10))
    single_len = Column(String(10), nullable=False)
    single_begin = Column(Boolean, default=0, nullable=False)
    # single_max = Column(String(10), nullable=False)
    # single_min = Column(String(10), nullable=False)
    single_value = Column(String(200), nullable=False)
    single_offset = Column(String(10))
    single_factor = Column(String(10))
    related_ecu_msg = Column(Integer, ForeignKey('EcuMsg.id'))

    def __str__(self):
        return "{'single_name':'%s','single_unit':'%s','single_len':'%s','single_begin':'%s'," \
               "'single_value':'%s','single_offset':'%s','single_factor':'%s','related_ecu_msg':'%s'" % (
                   self.single_name,
                   self.single_unit,
                   self.single_len,
                   self.single_begin,
                   self.single_value,
                   self.single_offset,
                   self.single_factor,
                   self.related_ecu_msg,
               )


class EcuMap(BASE):
    __tablename__ = 'EcuMap'  # 表格名字
    id = Column(Integer, primary_key=True, autoincrement=True)
    cmd_Resp = Column(String(50), nullable=False)
    map_func = Column(String(100), nullable=False)
    related_ecu_msg = Column(String(100), nullable=False)

    def __str__(self):
        return "{'msg_id':'%s','map_func':'%s','related_ecu_msg':'%s' " % (
            self.msg_id,
            self.map_func,
            self.related_ecu_msg
        )
