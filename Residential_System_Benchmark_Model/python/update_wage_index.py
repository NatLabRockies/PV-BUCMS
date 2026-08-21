import time
start_time=time.time()
import os
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import pandas as pd
import requests

path = '//'.join(os.path.dirname(os.path.abspath(__file__)).split('//')[0:-1])

def wage_index(df_state, df_nat):
    national_occupation_median = df_nat.loc['All Occupations','A_MEDIAN']
    
    df_occupation = df_state.loc[(df_state['OCC_TITLE']=='All Occupations')]
    
    df_occupation['Wage Index'] = df_occupation['A_MEDIAN']/national_occupation_median
    
    df_wage_index = pd.DataFrame(index=df_occupation.index, data=df_occupation['Wage Index'])
    
    return df_wage_index

def get_zip(year):
    r = requests.get("https://www.bls.gov/oes/special.requests/oesm"+year[-2:]+"st.zip")
    z = ZipFile(BytesIO(r.content))
    zip_array = z.namelist()
    df_full = pd.read_excel(z.open(zip_array[1]))
    df_full.set_index('STATE', inplace=True)
    return df_full

def get_national_zip(year):
    r = requests.get("https://www.bls.gov/oes/special.requests/oesm"+year[-2:]+"nat.zip")
    z = ZipFile(BytesIO(r.content))
    zip_array = z.namelist()
    df_full = pd.read_excel(z.open(zip_array[1]))
    df_full.set_index('OCC_TITLE', inplace=True)
    return df_full

df_state_wage = get_zip('2018')
df_nat_wage = get_national_zip('2018')

df_wage_index = wage_index(df_state_wage, df_nat_wage)

df_wage_index.to_excel(path + '//input_data//BLS Wage Index.xlsx')


print("--- %s seconds ---" % (time.time() - start_time))