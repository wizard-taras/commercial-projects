import csv

arr = []
att_dict = {}

for i in range(1, 4):
    
    ## Loading the 'FINAL_certified_att-s_b{i}' Reports
    with open(f'FINAL_certified_att-s_b{i}.csv', mode='r') as report:
        csv_fl = csv.reader(report)
        for lines in csv_fl:
            arr.append(lines)

    ## Looping through the Attendee Report from 2nd line (starting position of the attendees data) to the end of
    # the Report and copying the data of attendees (email, name) into the dictionary 'att_dict'
    for line in arr[1:]:
        if line[0] in att_dict.keys() and int(line[2]) > 2:
            temp = att_dict[line[0]][1]
            att_dict.update({line[0]: [line[1], f'{temp} + {i}']})
        elif int(line[2]) > 2: att_dict[line[0]] = [line[1], i]

    arr.clear()

with open(f'FINAL_certified_att-s.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Attendee email', 'Attendee name', 'Blocks'])
        for key, value in att_dict.items():
            writer.writerow([key, value[0], value[1]])

arr.clear()

## Loading the 'FINAL_certified_att-s_b{i}' Reports
with open('FINAL_certified_att-s_b4.csv', mode='r') as report:
    csv_fl = csv.reader(report)
    for lines in csv_fl:
        arr.append(lines)

## Looping through the Attendee Report from 2nd line (starting position of the attendees data) to the end of
# the Report and copying the data of attendees (email, name) into the dictionary 'att_dict'
for line in arr[1:]:
    if line[0] in att_dict.keys():
        temp = att_dict[line[0]][1]
        att_dict.update({line[0]: [line[1], f'{temp} + 4']})
    else: att_dict[line[0]] = [line[1], i]

with open(f'FINAL_certified_att-s.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Attendee email', 'Attendee name', 'Blocks'])
    for key, value in att_dict.items():
        writer.writerow([key, value[0], value[1]])