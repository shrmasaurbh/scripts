import csv
import json
import os

loc = 'SearchEngineScrapy/toyota/ciaz'
file_to_write = "ciaz1.csv"
sheet = loc
for root, dirnames, filenames in os.walk(sheet):
    file = sorted(filenames)
    data = ''
    for i in file:
        sheet_file = root + '/' + i
        print(sheet_file)
        with open(sheet_file, 'r') as f:
            data = json.loads(f.read())
        csv_columns = []
        max1 = 0
        for i in data:
            if len(i.keys()) > max1:
                csv_columns = []
                csv_columns.extend((i.keys()))

        print(len(csv_columns))
        if os.path.isfile(file_to_write) == False:
            try:
                with open(file_to_write, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    writer.writeheader()
            except Exception as e:
                print(str(e))
        for i in data:
            try:
                with open(file_to_write, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    # writer.writeheader()
                    writer.writerow(i)
            except Exception as e:
                import pdb

                pdb.set_trace()
                print(i)

# print(data)
# csv_columns=[]
# max1=0
# for i in data:
#     if len(i.keys())>max1:
#         csv_columns=[]
#         csv_columns.extend((i.keys()))
#
# print(len(csv_columns))
# try:
#     with open('ciaz1.csv', 'a') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#         writer.writeheader()
# except Exception as e:
#     print(str(e))
#
# $$$$$$$$$$$$$$$$


# print(csv_columns)

# for i in data:
#     try:
#         with open('ciaz1.csv', 'a') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#             # writer.writeheader()
#             writer.writerow(i)
#     except Exception as e:
#         import pdb
#         pdb.set_trace()
#         print(i)
