#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import xlwings as xw
import pymssql
import datetime as dt
#from win32com import client
#import win32com.client
import numpy as np
import pandas as pd


def open_workbook(path, screen_updating, visible):
	'''
	Abre un workbook y retorna un objecto workbook de xlwings. Sin screen_updating es false es mas rapido.
	'''
	
	wb = xw.Book(path)
	if screen_updating == False:		
		wb.app.screen_updating = False
	else:
		wb.app.screen_updating = True
	if visible == False:
		wb.app.visible = False
	else:
		wb.app.visible = True
	return wb

def get_table_xl(wb, sheet, tupla):
	'''
	Retorna la tabla en un arreglo, dado un rango y la hoja.
	'''
	return wb.sheets[sheet].range(tupla).expand('table').value

def get_frame_xl(wb, sheet, tupla, index_pos):
	'''
	Retorna la tabla en un dataframe, dado un rango y la hoja.
	Ademas se le da la posicion de las columnas a indexar
	'''
	table = get_table_xl(wb, sheet, tupla)
	data = table[1:]
	columns = np.array(table[0])
	table = pd.DataFrame(data, columns=columns)
	table.set_index(columns[index_pos].tolist(), inplace=True)
	return table

def format_tuples(df):
    '''
    Transforma un dataframe en una lista de tuplas.
    '''
    serie_tuplas = [tuple(x) for x in df.values]
    return serie_tuplas

def connect_database_user(server, database, username, password):
	'''
	Se conecta a una base de datos y retorna el objecto de la conexion, usando un usuario.
	'''
	conn= pymssql.connect(host=server, database=database, user=username, password=password)
	return conn

def disconnect_database(conn):
	'''
	Se deconecta a una base de la datos.
	'''
	conn.close()
    
def convert_date_to_string(date):
	'''
	Retorna la fecha en formato de string, dado el objeto date.
	'''
	date_string=str(date.strftime('%Y-%m-%d'))
	return date_string

def get_working_dates(start_date, end_date):
    
    query_wdays = "Select fecha from fechas_habiles where fecha>='start_date' and fecha<='end_date' order by fecha"
    query_wdays = query_wdays.replace('start_date', start_date).replace('end_date',end_date)
    df_wdays = get_frame_sql_user(server="localhost",
                               database="fintech",
                               username="sa",
                               password="usuariosql",
                               query=query_wdays)
    return df_wdays

def query_database(conn, query):
	'''
	Consulta la la base de datos(conn) y devuelve el cursor asociado a la consulta.
	'''
	cursor=conn.cursor()
	cursor.execute(query)
	return cursor

def get_table_sql(cursor):
	'''
	Recibe un cursor asociado a una consulta en la BDD y la transforma en una matriz.
	'''
	table=[]
	row = cursor.fetchone()
	ncolumns=len(cursor.description)
	while row:
		col=0	
		vect=[]
		while col<ncolumns:
			vect.append(row[col])
			col=col+1
		row = cursor.fetchone()
		table.append(vect)
	return table

def get_frame_sql_user(server, database, username, password, query):
    '''
    Retorna el resultado de la query en un panda's dataframe con usuario y clave. 
    '''
    conn = connect_database_user(server = server, database = database, username = username, password = password)
    cursor = query_database(conn, query)
    schema = get_schema_sql(cursor = cursor)
    table = get_table_sql(cursor)
    dataframe = pd.DataFrame(data = table, columns = schema)
    disconnect_database(conn)
    return dataframe

def get_schema_sql(cursor):
	'''
	Recibe un cursor asociado a una consulta en la BDD y retorna el esquema de la relacion en una lista.
	'''
	schema = []
	for i in range(len(cursor.description)):
		prop = cursor.description[i][0]
		schema.append(prop)
	return schema

def print_full(x):
    '''
    Imprime un dataframe entero
    '''
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
    
def clear_sheet_xl(wb, sheet):
	'''
	Borra todos los contenidos de una hoja de excel.
	'''
	return wb.sheets[sheet].clear_contents()

def paste_val_xl(wb, sheet, tupla, value):
	'''
	a un valor en una celta de excel dada la hoja. 
	'''
	wb.sheets[sheet].range(tupla).value = value

def convert_string_to_datetime(date_string):
	'''
	Retorna la fecha en formato date.
	'''
	date_formated=dt.datetime.strptime(date_string, '%Y-%m-%d')
	return date_formated

def convert_string_to_date(date_string):
	'''
	Retorna la fecha en formato date.
	'''
	date_formated=dt.datetime.strptime(date_string, '%Y-%m-%d').date()
	return date_formated

def get_ndays_from_date(days, date_string):
	'''
	Retorna la fecha n dias desde hoy.
	'''
	date = convert_string_to_date(date_string) - dt.timedelta( days = days )
	date=str(date.strftime('%Y-%m-%d'))
	return date

