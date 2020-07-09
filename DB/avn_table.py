# coding:utf-8

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,Text
from sqlalchemy.orm import relationship, backref
from Common.CommonVar import BASE


class AvnSimu(BASE):
    __tablename__ = 'avnsimu'  # 表格名字
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(500), nullable=False, unique=True)
    content = Column(Text(), default='')
    count = Column(Integer(), default=0)
    current = Column(String(500), default=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    creatime = Column(String(500), default=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    _locked = Column(Boolean, default=0, nullable=False)
    #simu_para = relationship("AvnPara", backref="avnsimu")

    def __str__(self):
        return "{'id':'%s','type':'%s','content':'%s','count':'%s','current':'%s','creatime':'%s','_locked':'%s'}" % (
            self.id,
            self.type,
            self.content,
            self.count,
            self.current,
            self.creatime,
            self._locked
        )

    def to_json(self):
        return {
                'id':self.id,
                'type': self.type,
                'content':      self.content,
                'count':     self.count,
                'current':     self.current,
                'creatime':     self.creatime,
                '_locked':      self._locked

        }
class AvnSimu5G(BASE):
    __tablename__ = 'avnsimu5g'  # 表格名字
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(500), nullable=False, unique=True)
    content = Column(Text(), default='')
    count = Column(Integer(), default=0)
    current = Column(String(500), default=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    creatime = Column(String(500), default=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    _locked = Column(Boolean, default=0, nullable=False)
    #simu_para = relationship("AvnPara", backref="avnsimu")

    def __str__(self):
        return "{'id':'%s','type':'%s','content':'%s','count':'%s','current':'%s','creatime':'%s','_locked':'%s'}" % (
            self.id,
            self.type,
            self.content,
            self.count,
            self.current,
            self.creatime,
            self._locked
        )
    def to_json(self):
        return {
                'id':self.id,
                'type': self.type,
                'content':      self.content,
                'count':     self.count,
                'current':     self.current,
                'creatime':     self.creatime,
                '_locked':      self._locked

        }
#
# class AvnPara(BASE):
#     __tablename__ = 'avnpara'  # 表格名字
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     parakey = Column(String(80), nullable=False, unique=True)
#     paravalue = Column(String(100), default='')
#     related_avn_id = Column(Integer(), ForeignKey('avnsimu.id'))
#     related_para_id = Column(Integer(), ForeignKey('avnpara.id'))
#     count = Column(Integer(), default=0)
#     current = Column(DateTime, default=datetime.now)
#     creatime = Column(DateTime, default=datetime.now)
#     _locked = Column(Boolean, default=0, nullable=False)
#     para_para = relationship("AvnPara", remote_side=[id], backref="avnpara"
