#import necessary libraries
import requests
import os
import pandas as pd
from zipfile import ZipFile, BadZipFile
from io import BytesIO
import wget
import shutil
from functools import reduce
# import main_program as m
import ssl
from pandas import ExcelWriter

current_path = os.path.abspath( __file__ )
adjusted_path = '/'.join( os.path.abspath( __file__ ).split( '/' )[0:-2] )
import_path = adjusted_path + '/input_data/'
dataset_path = import_path + 'datasets/'

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:  # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:  # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

#retrive latest year labor database from bls.gov
print("Retrieving Labor data",'\n',".",'\n',".")

df_main_inputs = pd.read_excel(import_path + 'inputs.xlsx', index_col=0 )
year = '%d' % df_main_inputs.loc['Year', 'Value A']
# year = '%d' % 2021 #testing
# print("labor data year", year) #testing

while True:
    try:
        labor_data = requests.get("https://www.bls.gov/oes/special.requests/oesm"+year[-2:]+"st.zip") #only works if year value is a string in quotes
        labor_data_zip = ZipFile(BytesIO(labor_data.content))
        print("Loaded",year, " state labor data from bls.gov",'\n',".",'\n',"." )
        break
    except BadZipFile:
        print( "Year",year, "state labor data not found in bls.gov")
        previous_year = int(year) - 1
        year = str(previous_year)

while True:
    try:
        national_labor_data = requests.get("https://www.bls.gov/oes/special.requests/oesm"+year[-2:]+"nat.zip")
        labor_data_nat_zip = ZipFile(BytesIO(national_labor_data.content))
        print("Loaded",year, "national labor data from bls.gov",'\n',".",'\n',"." )
        break
    except BadZipFile:
        print( "Year",year, "national labor data not found in bls.gov")
        previous_year = int(year) - 1
        year = str(previous_year)

labor_data_year = year
zip_array = labor_data_zip.namelist()
zip_array_nat = labor_data_nat_zip.namelist()

for file in zip_array:
    if 'state' in file:
        df_full_labor_data = pd.read_excel(labor_data_zip.open(file))
for file in zip_array_nat:
    if 'national' in file:
        df_full_labor_data_nat = pd.read_excel(labor_data_nat_zip.open(file))
# df_full_labor_data = pd.read_excel(labor_data_zip.open(zip_array[0]))
df_full_labor_data.columns = [x.upper() for x in df_full_labor_data.columns]  # change all headers to upper_case
df_full_labor_data_nat.columns = [x.upper() for x in df_full_labor_data_nat.columns]  # change all headers to upper_case

if 'AREA_TITLE' in df_full_labor_data.columns:  # 2019 dataset has different column name for previously titled column 'STATE'
    df_full_labor_data = df_full_labor_data.rename(columns={'AREA_TITLE': 'STATE'})
    df_full_labor_data_nat = df_full_labor_data_nat.rename(columns={'AREA_TITLE': 'STATE'})

#extract only required labor data
df_full_labor_data = df_full_labor_data[['STATE','OCC_TITLE','H_PCT10','H_MEDIAN','H_PCT90']]
df_full_labor_data_nat = df_full_labor_data_nat[['PRIM_STATE','OCC_TITLE','H_PCT10','H_MEDIAN','H_PCT90']]

df_Electrician_labor_data = df_full_labor_data.query('OCC_TITLE == "Electricians"')
df_Construction_labor_data = df_full_labor_data.query('OCC_TITLE == "Construction Laborers"')
df_Equipment_labor_data = df_full_labor_data.query('OCC_TITLE == "Operating Engineers and Other Construction Equipment Operators"')

df_Electrician_labor_data_nat = df_full_labor_data_nat.query('OCC_TITLE == "Electricians"')
df_Construction_labor_data_nat = df_full_labor_data_nat.query('OCC_TITLE == "Construction Laborers"')
df_Equipment_labor_data_nat = df_full_labor_data_nat.query('OCC_TITLE == "Operating Engineers and Other Construction Equipment Operators"')

df_Electrician_labor_data = df_Electrician_labor_data.rename(columns={'H_PCT10':'Electricians - 10', 'H_MEDIAN':'Electricians - 50', 'H_PCT90':'Electricians - 90'})
df_Construction_labor_data = df_Construction_labor_data.rename(columns={'H_PCT10':'Construction Laborers - 10', 'H_MEDIAN':'Construction Laborers - 50', 'H_PCT90':'Construction Laborers - 90'})
df_Equipment_labor_data = df_Equipment_labor_data.rename(columns={'H_PCT10':'Operating Engineers and Other Construction Equipment Operators - 10', 'H_MEDIAN':'Operating Engineers and Other Construction Equipment Operators - 50', 'H_PCT90':'Operating Engineers and Other Construction Equipment Operators - 90'})

df_Electrician_labor_data_nat = df_Electrician_labor_data_nat.rename(columns={'H_PCT10':'Electricians - 10', 'H_MEDIAN':'Electricians - 50', 'H_PCT90':'Electricians - 90'})
df_Construction_labor_data_nat = df_Construction_labor_data_nat.rename(columns={'H_PCT10':'Construction Laborers - 10', 'H_MEDIAN':'Construction Laborers - 50', 'H_PCT90':'Construction Laborers - 90'})
df_Equipment_labor_data_nat = df_Equipment_labor_data_nat.rename(columns={'H_PCT10':'Operating Engineers and Other Construction Equipment Operators - 10', 'H_MEDIAN':'Operating Engineers and Other Construction Equipment Operators - 50', 'H_PCT90':'Operating Engineers and Other Construction Equipment Operators - 90'})

df_Electrician_labor_data.drop('OCC_TITLE', axis=1, inplace=True)
df_Construction_labor_data.drop('OCC_TITLE', axis=1, inplace=True)
df_Equipment_labor_data.drop('OCC_TITLE', axis=1, inplace=True)

df_Electrician_labor_data_nat.drop('OCC_TITLE', axis=1, inplace=True)
df_Construction_labor_data_nat.drop('OCC_TITLE', axis=1, inplace=True)
df_Equipment_labor_data_nat.drop('OCC_TITLE', axis=1, inplace=True)

df_all_labor_data = [df_Electrician_labor_data, df_Construction_labor_data, df_Equipment_labor_data]
df_all_labor_data_nat = [df_Electrician_labor_data_nat, df_Construction_labor_data_nat, df_Equipment_labor_data_nat]

labor_data = reduce(lambda left,right: pd.merge(left,right,on='STATE'), df_all_labor_data)
labor_data = labor_data.reset_index(drop=True)
labor_data = labor_data.set_index('STATE', drop=True)
labor_data.rename(index={'District of Columbia':'DC'},inplace=True)

labor_data_nat = reduce(lambda left,right: pd.merge(left,right,on='PRIM_STATE'), df_all_labor_data_nat)
labor_data_nat = labor_data_nat.reset_index(drop=True)
labor_data_nat = labor_data_nat.set_index('PRIM_STATE', drop=True)

labor_data.to_excel(dataset_path + 'bls_labor_database.xlsx', index=True)
labor_data_nat.to_excel(dataset_path + 'bls_labor_database_national.xlsx', index=True)

#retrieve project installation data from NREL library
print("Retrieving Project Installation data")

# installation_data_url = "https://nrellibrary.nrel.gov/store/WoodMackenzie/2019/WM_USSMI_2019.xlsx"
# installation_data_file_path = dataset_path + 'WM_USSMI_2019.xlsx'
# installation_data_file = wget.download(installation_data_url, dataset_path)
#
# if os.path.exists(installation_data_file_path): #Overwrite file if already exists
#     print("Overwriting Existing Installation Data File",'\n',".",'\n',".")
#     shutil.move(installation_data_file,installation_data_file_path)

installation_data = pd.read_excel(dataset_path + 'WM_USSMI_2019.xlsx', sheet_name='Annual Capacity and Forecasts')

#structure installation data and split into respective data frames
residential_row_num = installation_data.loc[installation_data['Unnamed: 1'] == 'Residential PV'].index[0] #grabs index number
commercial_row_num = installation_data.loc[installation_data['Unnamed: 1'] == 'Non-Residential PV'].index[0]
utility_row_num = com_row_num = installation_data.loc[installation_data['Unnamed: 1'] == 'Utility PV'].index[0]

residential_installation_data = installation_data[residential_row_num:(residential_row_num+55)].drop(columns='Unnamed: 0') #grabs right data and assign it to a df
commercial_installation_data = installation_data[commercial_row_num:(commercial_row_num+55)].drop(columns='Unnamed: 0')
utility_installation_data = installation_data[utility_row_num:(utility_row_num+55)].drop(columns='Unnamed: 0')

residential_installation_data.columns = residential_installation_data.iloc[1] #reassign header, keep only required data and change index to state
residential_installation_data = residential_installation_data[2:]
residential_installation_data = residential_installation_data.set_index('State')

commercial_installation_data.columns = commercial_installation_data.iloc[1]
commercial_installation_data = commercial_installation_data[2:]
commercial_installation_data = commercial_installation_data.set_index('State')

utility_installation_data.columns = utility_installation_data.iloc[1]
utility_installation_data = utility_installation_data[2:]
utility_installation_data = utility_installation_data.set_index('State')

year = df_main_inputs.loc['Year', 'Value A']
residential_installation_data['Cumulative Install'] = residential_installation_data[:year].sum(axis=1) #calculate cumulative total of all years
commercial_installation_data['Cumulative Install'] = commercial_installation_data[:year].sum(axis=1)
utility_installation_data['Cumulative Install'] = utility_installation_data[:year].sum(axis=1)

residential_installation_data = residential_installation_data[:-1] #drop last row for cumulative weight calc
commercial_installation_data = commercial_installation_data[:-1]
utility_installation_data = utility_installation_data[:-1]

residential_installation_data.rename( index={'Washington DC': 'DC'}, inplace=True )
commercial_installation_data.rename( index={'Washington DC': 'DC'}, inplace=True )
utility_installation_data.rename( index={'Washington DC': 'DC'}, inplace=True )

residential_installation_data['Weight'] = residential_installation_data['Cumulative Install']/residential_installation_data['Cumulative Install'].sum()  #calculate cumulative weight
commercial_installation_data['Weight'] = commercial_installation_data['Cumulative Install']/commercial_installation_data['Cumulative Install'].sum()
utility_installation_data['Weight'] = utility_installation_data['Cumulative Install']/utility_installation_data['Cumulative Install'].sum()

#retrieve steel price index data from external source
print("Retrieving Steel Price Index data")

spi_data_url = "https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=WPU101704&scale=left&cosd=1982-06-01&coed=2022-03-01"
spi_data_file_path = dataset_path + 'WPU101704.xls'
spi_data_file = wget.download(spi_data_url, dataset_path)

if os.path.exists(spi_data_file_path): #Overwrite file if already exists
    print("Overwriting Existing SPI Data File",'\n',".",'\n',".")
    shutil.move(spi_data_file, spi_data_file_path)

spi_data = pd.read_excel(dataset_path + 'WPU101704.xls')

spi_data = spi_data[9:]
spi_data.columns = spi_data.iloc[0]
spi_data.rename(columns={'WPU101704':'spi'}, inplace=True)
spi_data = spi_data[1:]
spi_data['year'] = pd.to_datetime(spi_data['observation_date']).dt.year
spi_data = spi_data[['year','spi']].astype(int)
spi_data = spi_data.groupby('year').mean()

#retrieve consumer price index data from external source
print( "Retrieving Consumer Price Index data")

cpi_data_url = "https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CPIAUCSL&scale=left&cosd=1947-01-01&coed=2022-03-01"
cpi_data_file_path = dataset_path + 'CPIAUCSL.xls'
cpi_data_file = wget.download(cpi_data_url, dataset_path)

if os.path.exists(cpi_data_file_path): #Overwrite file if already exists
    print("Overwriting Existing CPI Data File",'\n',".",'\n',".")
    shutil.move(cpi_data_file, cpi_data_file_path)

cpi_data = pd.read_excel(dataset_path + 'CPIAUCSL.xls')
cpi_data = cpi_data[9:]
cpi_data.columns = cpi_data.iloc[0]
cpi_data.rename(columns={'CPIAUCSL': 'cpi'}, inplace=True )
cpi_data = cpi_data[1:]
cpi_data['year'] = pd.to_datetime( cpi_data['observation_date'] ).dt.year
cpi_data['month'] = pd.to_datetime( cpi_data['observation_date'] ).dt.month
cpi_data = cpi_data[['year', 'cpi']].astype(int)
cpi_annual_avg = cpi_data.groupby('year').mean()
