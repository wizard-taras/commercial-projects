'''
Program file: ESP_course_certification_OT2.py

Purpose:
    This script is used for determining the number of attendees that can be certified as well as their names

Record of revisions:
    Date        Programmer      Description of change(-s)
    ----        ----------      -------------------------
    31/1/24     Koziupa Taras   Original code. Problem statement and .csv Attendee Report loading to the
working space
'''

import csv

reg_arr = []
arr_OT1 = []
arr_OT2 = []
arr_OT3 = []
arr_OT4 = []
passed_tests = []

# Ongoing test participant responses filler
def OTarrays_filler(test_index):
    emails_temp_arr = [] # Clearing temp list beore filling in
    with open(f'ESP Day {test_index} Post-webinar test responses.csv', mode='r') as report:
        csv_reader = csv.reader(report)
        for lines in csv_reader:
            emails_temp_arr.append([lines[1], test_index, lines[0]])
    
    return emails_temp_arr

## Loading the participants' emails who passed [i] test and Final test
arr_OT1 = OTarrays_filler(1)
arr_OT2 = OTarrays_filler(2)
arr_OT3 = OTarrays_filler(3)
arr_OT4 = OTarrays_filler(4)

arr_FT = []
emails_temp_arr = [] # Clearing temp list beore filling in
with open(f'ESP Final test responses.csv', mode='r') as report:
    csv_reader = csv.reader(report)
    for lines in csv_reader:
        arr_FT.append(lines)


## Loading the Registration Report
with open(f'ESP Registration form.csv', mode='r') as reg_report:
    flag = 0 # Flag used to indicate whether participant has mark for a specific test (i.e., if
    # email from "Registration.csv" is in "arr_OT{i}" list)
    csv_reg = csv.reader(reg_report)
    for lines in csv_reg:
        for participant_info_OT1 in arr_OT1:
            if lines[2] in participant_info_OT1:
                passed_tests.append(participant_info_OT1[2])
                flag = 1
        if flag == 0: passed_tests.append('-')
        flag = 0
        for participant_info_OT2 in arr_OT2:
            if lines[2] in participant_info_OT2:
                passed_tests.append(participant_info_OT2[2])
                flag = 1
        if flag == 0: passed_tests.append('-')
        flag = 0
        for participant_info_OT3 in arr_OT3:
            if lines[2] in participant_info_OT3:
                passed_tests.append(participant_info_OT3[2])
                flag = 1
        if flag == 0: passed_tests.append('-')
        flag = 0
        for participant_info_OT4 in arr_OT4:
            if lines[2] in participant_info_OT4:
                passed_tests.append(participant_info_OT4[2])
                flag = 1
        if flag == 0: passed_tests.append('-')
        flag = 0
        for participant_info_FT in arr_FT:
            if lines[2] in participant_info_FT:
                passed_tests.append([participant_info_FT[3], participant_info_FT[0]])
                flag = 1
        if flag == 0: passed_tests.append('-')
        flag = 0
        
        lines.append(passed_tests)
        reg_arr.append(lines)

        passed_tests = []

with open(f'certified_combined.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Attendee name', 'Attendee email', 'Passed test marks'])
    for line in reg_arr:
        to_add = [line[28][0], line[28][1], line[28][2], line[28][3], line[28][4]]
        line = line[:28]
        line += to_add

        writer.writerow(line)