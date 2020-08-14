#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 16:57:37 2020

@author: Diego
"""

import sys
import pandas as pd
sys.path.insert(0, '/Users/Diego/Developer/desarrollos/librerias')
import utiles

def fetch_valores_cuota(fund_type):
    
    fund_type = str(fund_type)
    wb = utiles.open_workbook("./afps_vc.xlsx", True, True)
    valores_cuota = utiles.get_frame_xl(wb, fund_type, (1, 1), [0])
    valores_cuota.reset_index(inplace=True)
    valores_cuota.sort_values(by = ["Fecha"], inplace = True)
    valores_cuota.bfill(inplace = True)
    upload_dataset_db(fund_type,valores_cuota)

    
def upload_dataset_db(fund_type,dataset):
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
    cursor.executemany("INSERT INTO AFPs_"+fund_type+"(Fecha,Capital,Cuprum,Habitat,Modelo,Planvital,Provida) VALUES (%s,%d,%d,%d,%d,%d,%d)", dataset_tuplas)
    conn.commit()
    utiles.disconnect_database(conn)
    
    
    
fetch_valores_cuota("D")

    
    

