import csv
import os

def get_artikel_data_by_id(id):
    if os.path.isfile('artikel.csv'):
        with open('artikel.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['id'] == id:
                    return row
    return None

def get_all_artikel_data():
    if os.path.isfile('artikel.csv'):
        with open('artikel.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            artikel_list = []
            for row in reader:
                artikel_list.append(row)
        return artikel_list
    return []
