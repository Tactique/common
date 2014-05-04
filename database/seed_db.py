#!/usr/bin/env python

import os
import csv

from engine import engine
from tables import (
    Team,
    Cell,
    WeaponType,
    Weapon,
    ArmorType,
    Armor,
    SpeedMap,
    Movement,
    Unit,
)


class Seeder:
    def __init__(self, session):
        self.session = session
        try:
            self.resource_path = '%s/common/resources/' % (os.environ['ROOTIQUE'],)
        except KeyError:
            raise Exception("Please define the $DOMOROOT environment variable to your domoco dir")

    def run(self):
        self.clearAllTables()
        self.seed_entries(Team, "Team", 'teams.csv')
        self.seed_entries(Cell, "Cell", 'terrain.csv', unique_name='cellType')
        weapon_types  = self.seed_entries(WeaponType, "WeaponType", 'weaponTypes.csv')
        weapons = self.seed_entries(Weapon, "Weapon", 'weapons.csv', reference_information={'weaponType': weapon_types})
        armor_types = self.seed_entries(ArmorType, "ArmorType", 'armorTypes.csv')
        armors = self.seed_entries(Armor, "Armor", 'armors.csv', reference_information={'armorType': armor_types})
        speed_maps = self.seed_entries(SpeedMap, "SpeedMap", 'speedMaps.csv')
        movements = self.seed_entries(Movement, "Movement", 'movements.csv', reference_information={'speedMap': speed_maps})
        self.seed_entries(Unit, "Unit", 'units.csv', reference_information={
            'attack_one': weapons,
            #'attack_two': weapons,
            'armor': armors,
            'movement': movements})

    def clearAllTables(self):
        print("Clearing all Tables")
        def delete_me(x):
            print("deleting %s" % x)
            x.delete()

        '''
        map(delete_me, Team.objects.all())
        map(delete_me, Cell.objects.all())
        map(delete_me, WeaponType.objects.all())
        map(delete_me, Weapon.objects.all())
        map(delete_me, ArmorType.objects.all())
        map(delete_me, Armor.objects.all())
        map(delete_me, SpeedMap.objects.all())
        map(delete_me, Movement.objects.all())
        map(delete_me, Unit.objects.all())
        '''

    def seed_entries(self, constructor, model_name, csv_file, reference_information={}, unique_name='name'):
        dbEntries = {}
        with open(self.resource_path + csv_file, 'r') as file_:
            reader = csv.reader(file_, quotechar='\'')
            names = next(reader, None)
            for pieces in reader:
                print(pieces)
                pieces = convert_ints(pieces)
                print(pieces)
                index = names.index(unique_name)
                kwargs = dict(zip(names, pieces))
                print(kwargs)
                for reference_name, reference_table in reference_information.items():
                    if reference_name in kwargs:
                        if kwargs[reference_name] != 'null':
                            kwargs[reference_name] = reference_table[kwargs[reference_name]]
                        else:
                            kwargs[reference_name] = None
                    else:
                        raise Exception("reference name %s was given, but is not in header of csv for %s" % (
                            reference_name, csv_file))
                print("Creating %s(%s)" % (
                    model_name, ', '.join(map(str, pieces))))
                print(kwargs)
                dbEntry = constructor(**kwargs)
                self.session.add(dbEntry)
                dbEntries[pieces[index]] = dbEntry
        return dbEntries


def convert_ints(pieces):
    ret = []
    for piece in pieces:
        if is_int(piece):
            ret.append(int(piece))
        else:
            ret.append(piece)
    return ret


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    session = engine.get_session()
    Seeder(session).run()
    session.commit()
