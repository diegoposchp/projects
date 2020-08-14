#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 21:05:58 2020

@author: Diego
"""


import sys
import pandas as pd
sys.path.insert(0, '/Users/Diego/Developer/desarrollos/librerias')
import utiles

def fetch_fyf():
    
    
    wb = utiles.open_workbook("./fyf.xlsx", True, True)
    fyf = utiles.get_frame_xl(wb, "BD", (1, 1), [0])
    fyf.reset_index(inplace=True)
    fyf.sort_values(by = ["Fecha_inicio"], inplace = True)
    fyf.fillna(0, inplace = True)
    
    min_date = utiles.convert_date_to_string(fyf["Fecha_inicio"].min())
    max_date = utiles.convert_date_to_string(fyf["Fecha_fin"].max())
    working_days = utiles.get_working_dates(min_date, max_date)
    validate_data = fyf.merge(working_days, how = 'left', left_on = "Fecha_fin", right_on = "fecha")
    nulls_number = validate_data["fecha"].isnull().sum()
    if nulls_number==0:
        upload_dataset_db(fyf)
    else:
        print("No se subirá la data porque no todas las fechas son habiles")

    
def upload_dataset_db(dataset):
    '''
    UPLOAD DATASET BBDD

    '''
    dataset_tuplas = utiles.format_tuples(df = dataset)
    print(dataset.head())
    print(dataset_tuplas)
    conn = utiles.connect_database_user(server="localhost",
                                    database="fintech",
                                    username="sa",
                                    password="usuariosql")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO FyF (fecha_inicio,fecha_fin,A,B,C,D,E) VALUES (%s,%s,%d,%d,%d,%d,%d)", dataset_tuplas)
    conn.commit()
    utiles.disconnect_database(conn)
    
    
    
fetch_fyf()

    
    

