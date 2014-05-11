import sqlalchemy as sqla
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

MAX_CHAR_LENGTH = 128
MAX_JSON_LENGTH = 512

Base = declarative_base()


class Team(Base):
    __tablename__ = 'team'

    id = sqla.Column(sqla.Integer, primary_key=True)
    nationType = sqla.Column(sqla.Integer)
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))


class Cell(Base):
    __tablename__ = 'cell'

    id = sqla.Column(sqla.Integer, primary_key=True)
    cellType = sqla.Column(sqla.Integer)
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))


class WeaponType(Base):
    __tablename__ = 'weapontype'

    id = sqla.Column(sqla.Integer, primary_key=True)
    weaponType = sqla.Column(sqla.Integer)
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))


class Weapon(Base):
    __tablename__ = 'weapon'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))
    power = sqla.Column(sqla.Integer)
    minRange = sqla.Column(sqla.Integer)
    maxRange = sqla.Column(sqla.Integer)

    weaponTypeId = sqla.Column(sqla.Integer, sqla.ForeignKey('weapontype.id'))
    weaponType = relationship(
        'WeaponType',
        backref=backref('weapon'))


class ArmorType(Base):
    __tablename__ = 'armortype'

    id = sqla.Column(sqla.Integer, primary_key=True)
    armorType = sqla.Column(sqla.Integer)
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))


class Armor(Base):
    __tablename__ = 'armor'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))
    strength = sqla.Column(sqla.Integer)

    armorTypeId = sqla.Column(sqla.Integer, sqla.ForeignKey('armortype.id'))
    armorType = relationship(
        'ArmorType',
        backref=backref('armor'))


class SpeedMap(Base):
    __tablename__ = 'speedmap'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))
    speeds = sqla.Column(sqla.String(MAX_JSON_LENGTH))


class Movement(Base):
    __tablename__ = 'movement'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))
    distance = sqla.Column(sqla.Integer)

    speedMapId = sqla.Column(sqla.Integer, sqla.ForeignKey('speedmap.id'))
    speedMap = relationship(
        'SpeedMap',
        backref=backref('movement'))


class Unit(Base):
    __tablename__ = 'unit'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))
    health = sqla.Column(sqla.Integer)

    attack_oneId  = sqla.Column(sqla.Integer, sqla.ForeignKey('weapon.id'))
    attack_one = relationship(
        'Weapon',
        backref=backref('unit'))

    armorId = sqla.Column(sqla.Integer, sqla.ForeignKey('armor.id'))
    armor = relationship(
        'Armor',
        backref=backref('unit'))

    movementId = sqla.Column(sqla.Integer, sqla.ForeignKey('movement.id'))
    movement = relationship(
        'Movement',
        backref=backref('unit'))


class World(Base):
    __tablename__ = 'world'

    id = sqla.Column(sqla.Integer, primary_key=True)
    worldId = sqla.Column(sqla.String(MAX_CHAR_LENGTH))
    name = sqla.Column(sqla.String(MAX_CHAR_LENGTH))
    numPlayers = sqla.Column(sqla.Integer)
    cellData = sqla.Column(sqla.String(MAX_CHAR_LENGTH))
