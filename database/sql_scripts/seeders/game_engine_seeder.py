import os
import csv

from tables.game_engine import (
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

from seeders.base_seeder import BaseSeeder, print_delete_count


class GameEngineSeeder(BaseSeeder):
    def clear_game_engine(self):
        print("Clearing all game engine tables")
        print_delete_count(self.session.query(Team).delete())
        print_delete_count(self.session.query(Cell).delete())
        print_delete_count(self.session.query(WeaponType).delete())
        print_delete_count(self.session.query(Weapon).delete())
        print_delete_count(self.session.query(ArmorType).delete())
        print_delete_count(self.session.query(Armor).delete())
        print_delete_count(self.session.query(SpeedMap).delete())
        print_delete_count(self.session.query(Movement).delete())
        print_delete_count(self.session.query(Unit).delete())

    def seed(self):
        self.clear_game_engine()
        self.seed_entries(Team, "Team", 'teams.csv')
        self.seed_entries(Cell, "Cell", 'terrain.csv', unique_name='cellType')
        weapon_types  = self.seed_entries(WeaponType, "WeaponType", 'weaponTypes.csv')
        weapons = self.seed_entries(Weapon, "Weapon", 'weapons.csv', custom_function=get_deferencer({'weaponType': weapon_types}))
        armor_types = self.seed_entries(ArmorType, "ArmorType", 'armorTypes.csv')
        armors = self.seed_entries(Armor, "Armor", 'armors.csv', custom_function=get_deferencer({'armorType': armor_types}))
        speed_maps = self.seed_entries(SpeedMap, "SpeedMap", 'speedMaps.csv')
        movements = self.seed_entries(Movement, "Movement", 'movements.csv', custom_function=get_deferencer({'speedMap': speed_maps}))
        self.seed_entries(Unit, "Unit", 'units.csv', custom_function=get_deferencer({
            'attack_one': weapons,
            #'attack_two': weapons,
            'armor': armors,
            'movement': movements}))

    def seed_entries(self, constructor, model_name, csv_file, custom_function=None, unique_name='name'):
        dbEntries = {}
        with open(os.path.join(self.seed_data, csv_file), 'r') as file_:
            reader = csv.reader(file_, quotechar='\'')
            names = next(reader, None)
            for pieces in reader:
                pieces = convert_ints(pieces)
                index = names.index(unique_name)
                kwargs = dict(zip(names, pieces))
                if custom_function != None:
                    kwargs = custom_function(kwargs)
                print("Creating %s(%s)" % (
                    model_name, ', '.join(map(str, pieces))))
                dbEntry = constructor(**kwargs)
                self.session.add(dbEntry)
                dbEntries[pieces[index]] = dbEntry
        return dbEntries


def get_deferencer(reference_information):
    def dereferencer(orig_kwargs):
        return dereference_column_name(orig_kwargs, reference_information)

    return dereferencer


def dereference_column_name(orig_kwargs, reference_information):
    kwargs = dict(orig_kwargs)
    for reference_name, reference_table in reference_information.items():
        if reference_name in kwargs:
            if kwargs[reference_name] != 'null':
                kwargs[reference_name] = reference_table[kwargs[reference_name]]
            else:
                kwargs[reference_name] = None
        else:
            raise Exception("reference name %s was given, but is not in header of csv for %s" % (
                reference_name, csv_file))
    return kwargs


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
