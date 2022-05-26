# CT3 BRT


import datetime
import pathlib
from statistics import mean
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from pathlib import Path


# MAKE SURE PATH & FILE IS CORRECT
begin_time = datetime.datetime.now()
# path = 'C:/Users/wgately/Documents/00 Python/M2LP32 10 MAY 2022/'
path = '/Users/jilinus/Documents/EsteeLaunder/ELC/M2LP32 10 MAY 2022/'



file = '*MAY.xlsx'
report = 'reportct3_SCN*'


def CT3():
    base_path = pathlib.Path(path)
    num_spreadsheets = len(list(base_path.glob(file)))
    for i in range(num_spreadsheets):
        file_name = 'M2LP32C04U 5833129 SCN 1.'+str(i+1)+' 11 MAY.xlsx'

        for j in range(5):
            
            #load sheet
            sheet_name = j+1
            sheet_name = 'Sheet'+str(sheet_name)
            sheet = pd.read_excel(path + file_name, sheet_name= ''+ sheet_name +'', usecols="A:N" )
            sheet = np.array(sheet)

            #label stuff
            product_name = sheet[2,2]
            batch_name = sheet[3,2]
            sample_number = sheet[4,2]
            test_speed = sheet[17,2]
            data_rate = sheet[15,11]

            #build distance arrays and set start/stop
            distance_column = sheet[24:,2]
            distance_start = distance_column[0]
            distance_max = max(distance_column)
            distance_max_row = (distance_column).argmax()+1

            #set normal distance
            norm_distance_array = distance_column[0:distance_max_row]
            normal_distance = []
            for k in range(len(norm_distance_array)):
                normal_distance.append((norm_distance_array[k] - distance_start)/(distance_max - distance_start))


            #set y axis
            force_column = sheet[24:,3]
            force_array = force_column[:len(normal_distance)]

            #set variables for slope calcualtions
            normal_distance = np.array(normal_distance[:(force_array).argmax()+1])
            force = np.array(force_array[:(force_array).argmax()+1])
            normal_distance = normal_distance.tolist()
            force =force.tolist()
            slope , intercept = np.polyfit(normal_distance, force,1)
            col1 = 'Normal Distance (mm)'
            col2 = 'Force (g)'

            #temp file for data organization
            data = pd.DataFrame({col1:normal_distance, col2:force})
            data.to_excel(path+'sample_data.xlsx', sheet_name= '' + sheet_name + '', index=False ,startrow=8)

            #build temp report for final file
            file_path = path+'sample_data.xlsx'
            wb = load_workbook(file_path)
            sheet = wb['' + sheet_name + '']
            sheet['A1'] = 'Product Name'
            sheet['A2'] = 'Batch Name'
            sheet['A3'] = 'Sample Number'
            sheet['A4'] = 'Test Speed mm/s'
            sheet['A5'] = 'Data Rate pts/s'
            sheet['A6'] = 'Slope of Linear Region'
            sheet['A7'] = 'Peak Distance Normalized'
            sheet['B1'] = product_name
            sheet['B2'] = batch_name
            sheet['B3'] = sample_number
            sheet['B4'] = test_speed
            sheet['B5'] = data_rate
            sheet['B6'] = slope
            sheet['B7'] = max(normal_distance)

            #delete temp file for data organization
            dir_path = Path.home() / path
            file_path = dir_path / 'sample_data.xlsx'
            file_path.unlink()

            #make temp report files
            wb.save(path + file_name + f'report_ct3_{j+1}.xlsx')


        # collect reports TODO LINK TO j loop
        x1 = pd.read_excel(path + file_name +'report_ct3_1.xlsx')
        x2 = pd.read_excel(path + file_name +'report_ct3_2.xlsx')
        x3 = pd.read_excel(path + file_name +'report_ct3_3.xlsx')
        x4 = pd.read_excel(path + file_name +'report_ct3_4.xlsx')
        x5 = pd.read_excel(path + file_name +'report_ct3_5.xlsx')

        #manipulations for final report TODO create array based on size of j loop
        mod_array = x1.values[4][1], x2.values[4][1], x3.values[4][1], x4.values[4][1], x5.values[4][1]
        min_mod = min(mod_array)
        max_mod = max(mod_array)
        range_mod = max_mod - min_mod
        mean_mod = mean(mod_array)
        x6 = (min_mod, max_mod, mean_mod, range_mod)

        adh_array = x1.values[5][1], x2.values[5][1], x3.values[5][1], x4.values[5][1], x5.values[5][1]
        min_adh = min(adh_array)
        max_adh = max(adh_array)
        mean_adh = mean(adh_array)
        range_adh = max_adh - min_adh
        x7 = (min_adh, max_adh, mean_adh, range_adh)

        label = ('min','max','mean','range')
        label = pd.DataFrame({label})
        data = pd.DataFrame({x6, x7})

        # write/consolidate reports
        report_path = (path + f'reportct3_SCN1.{i+1}.xlsx')
        # Changes Here
        writer = pd.ExcelWriter(report_path)
        x1.to_excel(writer, sheet_name = 'SCN 1.'+str(i+1), startcol=0, index= None)
        x2.to_excel(writer, sheet_name = 'SCN 1.'+str(i+1), startcol=2, index= None)
        x3.to_excel(writer, sheet_name = 'SCN 1.'+str(i+1), startcol=4, index= None)
        x4.to_excel(writer, sheet_name = 'SCN 1.'+str(i+1), startcol=6, index= None)
        x5.to_excel(writer, sheet_name = 'SCN 1.'+str(i+1), startcol=8, index= None)
        label.to_excel(writer, sheet_name = 'SCN 1.'+str(i+1), startcol=10, startrow= 4, index= None, header= None )
        data.to_excel(writer, sheet_name = 'SCN 1.'+str(i+1), startcol=10, startrow= 5, index= None, header= None )
        writer.save()

        # Delete Temp Report Files
        for j in range(5):
            temp_name = j+1
            temp_name = path + file_name +'report_ct3_'+str(temp_name)+'.xlsx'
            dir_path = Path.home() / path
            file_path = dir_path / temp_name
            file_path.unlink()

    #consolidate reports
    num_reports = len(list(base_path.glob('*reportct3_SCN1*')))
    consolidated_path = (path + 'consolidated_report.xlsx')
    writer = pd.ExcelWriter(consolidated_path)

    for i in range(num_reports):
        #load individual reports
        report = pd.read_excel(path + 'reportct3_SCN1.'+str(i+1)+'.xlsx')
        for j in range(num_reports):
            #save reports consolidated
            report.to_excel(writer, sheet_name = 'SCN 1.'+str(i+1), startcol=0, index= None)

    writer.save()

    #delete individual reports
    for j in range(num_reports):
        temp_name = j+1
        temp_name = path + 'reportct3_SCN1.'+str(temp_name)+'.xlsx'
        dir_path = Path.home() / path
        file_path = dir_path / temp_name
        file_path.unlink()

    duration = datetime.datetime.now() - begin_time
    print('this took',duration,'s....way faster than manual manipulation')

    return


CT3 = CT3()