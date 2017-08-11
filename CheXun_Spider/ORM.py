from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Serie(Base):

    __tablename__ = 'BDCI_CHEXUN.stg.CONFIG_SERIES'

    serie_id = Column(String(500), primary_key=True)
    serie_name_cn = Column(String(500))
    serie_name_en = Column(String(500))
    serie_url = Column(String(500))
    create_time = Column(DateTime)
    last_update_time = Column(DateTime)
