from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    Sequence,
    ForeignKey,
    UniqueConstraint
)
from app.db.database_conect import Base


class RealTimeQueue(Base):

    __tablename__ = 'REALTIMEQUEUE'

    id_seq = Sequence('REALTIMEQUEUE_SEQ', metadata=Base.metadata, start=1)
    id = Column(Integer, id_seq,  primary_key=True)
    type_import = Column(Integer, ForeignKey('TYPEIMPORT.id'))
    source_folder = Column(String(64), nullable=False, index=True)
    filename = Column(String(64), nullable=False, index=True, unique=True)
    created_date = Column(DateTime, nullable=False)
    saved_in_db_date = Column(DateTime, nullable=False)
    is_locked = Column(Boolean, default=False)
    locked_date = Column(DateTime)

    def __repr__(self):
        return f'id: {self.id} folder: {self.source_folder} ' \
               f'filename: {self.filename} saved: {self.saved_in_db_date}'

    # create sequence REALTIMEQUEUE_SEQ start with 1 increment by 1 nocache nocycle;


class HistoricQueue(Base):

    __tablename__ = 'HISTORICQUEUE'

    __table_args__ = (
        UniqueConstraint('filename', 'to_reko', name='historicQueue_filename_to_reko'),
        UniqueConstraint('filename', 'to_kofax', name='historicQueue_filename_to_kofax'),
    )

    id_seq = Sequence('REALTIMEQUEUE_SEQ', metadata=Base.metadata, start=1)
    id = Column(Integer, id_seq, primary_key=True)
    type_import = Column(Integer, ForeignKey('TYPEIMPORT.id'))
    source_folder = Column(String(64), nullable=False)
    filename = Column(String(64), nullable=False, index=True)
    created_date = Column(DateTime, nullable=False)
    saved_in_db_date = Column(DateTime, nullable=False)
    locked_date = Column(DateTime)
    finish_transfer_date = Column(DateTime)
    to_reko = Column(Boolean, default=False)
    to_kofax = Column(Boolean, default=False)

    def __repr__(self):
        return f'id: {self.id} folder: {self.source_folder} ' \
               f'filename: {self.filename} saved: {self.saved_in_db}'

    # create sequence HISTORIQUEUE_SEQ start with 1 increment by 1 nocache nocycle;


class TypeImport(Base):

    __tablename__ = 'TYPEIMPORT'

    id_seq = Sequence('TYPEIMPORT_SEQ', metadata=Base.metadata, start=1)
    id = Column(Integer, id_seq, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    description = Column(String(128))

    # create sequence TYPEIMPORT_SEQ start with 1 increment by 1 nocache nocycle;
