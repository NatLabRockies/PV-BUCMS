import time
start_time=time.time()
import os
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import pandas as pd
import requests

path = '//'.join(os.path.dirname(os.path.abspath(__file__)).split('//')[0:-1])
# or: requests.get(url).content

# def get_zip(year):
#     r = requests.get("https://www.bls.gov/oes/special.requests/oesm"+year[-2:]+"st.zip")
#     z = ZipFile(BytesIO(r.content))
#     zip_array = z.namelist()
#     df_full = pd.read_excel(z.open(zip_array[1]))
#     df_full.set_index('STATE', inplace=True)
#     return df_full
#
# def create_labor_table(df_full):
#     columns_list = ['H_PCT10', 'H_MEDIAN', 'H_PCT90']
#     occup_list = ["Electricians", "Construction Laborers", "Operating Engineers and Other Construction Equipment Operators"]
#     quart_list = [' - 10', ' - 50', ' - 90']
#     df_labor_table = pd.DataFrame(index=df_full[(df_full['OCC_TITLE']==occup_list[0])].index)
#     for n in range(0,3):
#         df = df_full[(df_full['OCC_TITLE']==occup_list[n])]
#         for i in range(0,3):
#             df_labor_table[occup_list[n]+quart_list[i]] = df[columns_list[i]]
#     index_list = df_labor_table.index.tolist()
#     index_list[index_list.index('District of Columbia')] = 'DC'
#     df_labor_table.index = index_list
#     return df_labor_table

def average_wage_by_state(df_inputs, state, df_labor_table, df_labor, project_size, df_state):
    
    df_wage = pd.DataFrame(index=['Common Laborers', 'Electricians', 'Equipment Operators'])
    
    df_wage.loc['Common Laborers','BLS Survey']= df_labor_table.loc[state, 'Construction Laborers - 50']
    df_wage.loc['Electricians','BLS Survey']= df_labor_table.loc[state, 'Electricians - 50']
    df_wage.loc['Equipment Operators','BLS Survey']= df_labor_table.loc[state, 'Operating Engineers and Other Construction Equipment Operators - 50']
    
    if df_inputs.loc['Improved Logistics', 'Value A']:
        save = 0.2
    else:
        save = 0
        
    if project_size<5:
        df_wage['Base Hourly'] = df_wage['BLS Survey']*(1-save)
    elif project_size>100:
        df_wage['Base Hourly'] = df_wage['BLS Survey']*(1-save)*0.8
    else:
        df_wage['Base Hourly'] = df_wage['BLS Survey']*(1-save)*((100-project_size)*(0.2/95)+0.8)
    ""
    df_wage['Overhead & Profit %'] = float(df_state.loc[state, ('Labor','Workers Compensation Insurance Rates')].strip('%'))/100 + float(df_labor.loc['Federal and State Unemployment Cost','Value']) +\
    float(df_labor.loc['Social Security Taxes (FICA)','Value']) + float(df_labor.loc["Builder's Risk Insurance Cost",'Value']) + \
    float(df_labor.loc['Public Liability Cost','Value']) + float(df_labor.loc['Profit','Value'])
    
    df_wage.loc['Common Laborers','Overhead & Profit %']= df_wage.loc['Common Laborers','Overhead & Profit %'] + float(df_labor.loc['Common Laborers Overhead','Value'])
    df_wage.loc['Electricians','Overhead & Profit %']= df_wage.loc['Electricians','Overhead & Profit %']+float(df_labor.loc['Electricians Overhead','Value'])
    df_wage.loc['Equipment Operators','Overhead & Profit %']= df_wage.loc['Equipment Operators','Overhead & Profit %'] + +float(df_labor.loc['Equipment Operators Overhead','Value'])
    
    df_wage['Total Hourly']=df_wage['Base Hourly']*(1+df_wage['Overhead & Profit %'])

    return df_wage

