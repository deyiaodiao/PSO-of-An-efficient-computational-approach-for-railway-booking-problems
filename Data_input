import xlrd

def fare_you(station_num,fare_rate):
    data=xlrd.open_workbook('Data_You.xlsx')
    sh=data.sheet_by_index(0)#prize
    fare_dic={}
    for i in range(0,station_num):
        for j in range(0,station_num):
            fare_dic[1,i,j]=sh.cell_value(i,j)
    for i in range(0,station_num):
        for j in range(0,station_num):
            fare_dic[0,i,j]=fare_dic[1,i,j]*fare_rate
    return  fare_dic

def fare_types(fare,fare_type_num,station_num):
    for i in range(1,fare_type_num):
        for j in range(0,station_num):
            for k in range(0,station_num):
                if i==1:
                    fare[i,j,k]=fare[0,j,k]*0.95
                if i==2:
                    fare[i,j,k]=fare[0,j,k]*0.85
    return  fare

def mean_you(station_num,fare_type,mean_rate):
    data=xlrd.open_workbook('Data_You.xlsx')
    mean_dic = {}
    sh = data.sheet_by_index(1)  # mean
    for i in range(0, station_num):
        for j in range(0, station_num):
            mean_dic[ 1, i, j] = sh.cell_value(i, j)
            mean_dic[0,i,j]=mean_dic[1,i,j]*mean_rate
    return  mean_dic

def sigma_you(station_num,sigma_rate):
    data=xlrd.open_workbook('Data_You.xlsx')
    sigma_dic = {}
    sh = data.sheet_by_index(2)  # mean
    for i in range(0, station_num):
        for j in range(0, station_num):
            sigma_dic[ 1, i, j] = sh.cell_value(i, j)
            sigma_dic[0,i,j]=sigma_dic[1,i,j]*sigma_rate
    return  sigma_dic
