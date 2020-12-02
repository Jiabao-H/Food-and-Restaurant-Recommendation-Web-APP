import csv
import json

csvFilePath = 'covid.csv'
jsonFilePath = 'covid.json'

data = {}


with open(csvFilePath,encoding='utf-8') as csvf:
    csvReader = csv.DictReader(csvf)

    for rows in csvReader:

        if rows['city'][:7] == 'City of': area = rows['city'][8:]
        elif rows['city'][:11] == 'Los Angeles': area = rows['city'][14:]
        elif rows['city'][:14] == 'Unincorporated': area = rows['city'][17:]+'-Uni'

        key = area
        del rows['city']
        data[key] = rows

print(data)
with open(jsonFilePath, 'w',encoding='utf-8') as jsonf:
    jsonf.write(json.dumps(data, indent=4))
