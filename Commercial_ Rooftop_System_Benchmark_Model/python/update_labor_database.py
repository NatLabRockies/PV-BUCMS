import time
start_time=time.time()
import pandas as pd
import labor_database as ld
import os

path = '//'.join(os.path.dirname(os.path.abspath(__file__)).split('//')[0:-1])

df_full = ld.get_zip('2019')

df_labor_table = ld.create_labor_table(df_full)

df_labor_table.to_excel(path + '//input_data//BLS Labor Database.xlsx')

print("--- %s seconds ---" % (time.time() - start_time))