import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base

MAX_CHAR_LENGTH = 128
MAX_JSON_LENGTH = 512

Base = declarative_base()


class ResponseTemplate(Base):
    __tablename__ = 'response_template'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))
    json = sqla.Column(sqla.String(MAX_JSON_LENGTH))
