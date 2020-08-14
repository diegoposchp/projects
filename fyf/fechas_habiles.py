# -*- coding: utf-8 -*-


from workalendar.america import Chile
import datetime as dt
import pandas as pd
import sys
sys.path.insert(0, '/Users/Diego/Developer/desarrollos/librerias')
import utiles
import pymssql


def complete_working_days(year):

    start_date = "01-01-"+str(year)
    end_date = "31-12-"+str(year)
    cal = Chile()
    list_holidays = cal.holidays(year)
    df_holidays = pd.DataFrame(list_holidays, columns=["Fecha","Feriado"])
    #utiles.print_full(df_holidays)
    df_dates = pd.DataFrame(pd.bdate_range(start = start_date, end = end_date), columns=["Fecha"])
    df_dates = df_dates[df_dates["Fecha"].isin(df_holidays["Fecha"])==False]
    df_dates["Fecha"] = df_dates["Fecha"].astype(str)
    df_dates = special_cases(df_dates, year)
    
    
    upload_dataset_db(df_dates)

def special_cases(dates, year): #aca es para que pongamos fechas que estan mal en workalendar
    
    if year == 2011:
        remove_list = ["2011-10-10"]
        add_list = ["2011-10-12"] #lo ideal seria que si esto no está ahí se mete
    else:
        return dates
        
    dates = dates[~dates['Fecha'].isin(remove_list)]
    d = {'Fecha': add_list}
    df_add = pd.DataFrame(data=d)
    dates = pd.concat([dates, df_add])
    dates.sort_values(by = ["Fecha"], inplace = True)
    
    return dates
    
    

def upload_dataset_db(dataset):
    '''
    UPLOAD DATASET BBDD

    '''
    print("uploading...")
    dataset_tuplas = utiles.format_tuples(df = dataset)
    print(dataset.head())
    print(dataset_tuplas)
    conn = utiles.connect_database_user(server="localhost",
                                    database="fintech",
                                    username="sa",
                                    password="usuariosql")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO fechas_habiles(Fecha) VALUES (%s)", dataset_tuplas)
    conn.commit()
    utiles.disconnect_database(conn)




start_year = 2011
end_year = 2020



for x in range(start_year, end_year+1):
    print("starting "+str(x))
    complete_working_days(x)
