import time
start_time=time.time()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import final_table as ft
import math
import os


path = '//'.join(os.path.dirname(os.path.abspath(__file__)).split('//')[0:-1])

#Pull in all the inputs from csv into a df
df_inputs = pd.read_excel(path + '//input_data//inputs.xlsx', index_col=0)

#Get state data from csv into a df
df_state = pd.read_csv(path + '//input_data//state_data.csv', header=[0,1], skip_blank_lines=True, index_col=[0])

#Get module database from csv to df
df_module_db = pd.read_excel(path + '//input_data//module_database.xlsx', index_col=0)

#Get Commercial installation cost inputs csv to df
df_utility = pd.read_csv(path + '//input_data//Commercial - Material Labor Equipment.csv', index_col=0)

#Get consumer price index inflation data to df
df_cpi = pd.read_csv(path + '//input_data//consumer_price_index.csv', index_col=0)

#Get labor info to feed labor_database.py
df_labor = pd.read_excel(path + '//input_data//Labor_Info.xlsx', sheet_name='Labor', index_col=0)

#Get labor info to feed labor_database.py
df_labor_weight = pd.read_excel(path + '//input_data//Labor_Info.xlsx', sheet_name='Labor Weight', index_col=0)

df_ballasted_systems = pd.read_excel(path + '//input_data//Bill of Material Input.xlsx', sheet_name='Ballasted Systems', index_col=0)

df_bos_cost = pd.read_excel(path + '//input_data//Bill of Material Input.xlsx', sheet_name='BOS Cost Category', index_col=0)

df_labor_table = pd.read_excel(path + '//input_data//BLS Labor Database.xlsx', index_col=0)

#Get Developer Overhead info
df_dev_costs = pd.read_excel(path + '//input_data//Developer Profit & Overhead.xlsx', sheet_name='Developer Costs', index_col=0)

df_dev_business_model = pd.read_excel(path + '//input_data//Developer Profit & Overhead.xlsx', sheet_name='Developer Business Model', index_col=0)

df_profit = pd.read_excel(path + '//input_data//Developer Profit & Overhead.xlsx', sheet_name='Profit', index_col=0)

df_ancillary_exp = pd.read_excel(path + '//input_data//Developer Profit & Overhead.xlsx', sheet_name='Ancillary Expenses', index_col=0)

#Get Storage info
df_com_storage = pd.read_excel(path + '//input_data//commercial_storage.xlsx', index_col=0)

#Get Loading info
df_loading_inputs = pd.read_csv(path + '//input_data//loading_combo.csv',index_col=[0])

#Create variables for column header strings
A = 'Value A'
B = 'Value B'
C = 'Value C'
D = 'Value D'


#Intermediate Functions
#Function to get number of modules for selected Project Size
def num_of_modules(df_inputs, df_module_db, project_size):
    module = df_inputs.loc['Module Name', A]
    mod_size = df_module_db.loc[module,'Length (mm)']/1000.0*df_module_db.loc[module,'Width (mm)']/1000.0
    
    if pd.isnull(df_inputs.loc['Module Efficiency', A]):
        efficiency = df_module_db.loc[module,'Efficiency (from Specs)']
    else:
        efficiency = df_inputs.loc['Module Efficiency', A]

    watts = mod_size*efficiency*1000

    if df_inputs.loc['Fixed Acreage ?', A]:
        num_modules = math.ceil(project_size/310.4*1000000)
    else:
        num_modules = math.ceil(project_size/watts*1000000)
    
    return num_modules, watts

#Function to get inflation for materials and equipment
def get_inflation(df_cpi, year):
    df_c = pd.DataFrame(index=df_cpi.index)
    df_c['Avg'] = df_cpi.mean(axis=1)
    df_c['Change'] = df_c['Avg']/df_c.loc[2013,'Avg']
    compound = (df_c.loc[year,'Avg']/df_c.loc[2000,'Avg'])**(1/(year-2000))
    if pd.isnull(df_c.loc[year,'Change']):
        inflation = compound**(year-2013)
    else:
        inflation = df_c.loc[year,'Change']
    
    return inflation

#Global Variables
year = df_inputs.loc['Year', A]
inflation = get_inflation(df_cpi, year)
state_input = df_inputs.loc['Location', A]
project_size_input = df_inputs.loc['Project Size (MW)', A]

df_complete_usa_table = pd.DataFrame()
df_state_results={}

def final_table(project_size, state, num_modules):
    """
    This function calls a series of other functions that calculate the individual system costs and outputs a final table of all these costs. The individual system costs are calculated line by line in the table. The total system cost is also calculated and output in this table.

    Input
    -----
    project_size: int
        The size of the solar system in MW specified by the user in the main inputs table

    state: string
    	The full name of the state being analyzed

    num_moduls: int
    	Number of modules based on system size

    Output
    ------

    df_final: The final table of system costs for the location and system size specified.
    
    """

    #Function to get sales tax of selected location
    
    sales_tax = df_state.loc[state, ('Sales Tax', 'Utility')]

    #Create empty df for the final values to be graphed
    df_final = pd.DataFrame(columns = [state])

    #Get module cost into final table
    df_final.loc['Module',state] = ft.get_module_cost(df_inputs)

    #Get inverter cost into final table
    df_final.loc['Inverter Only',state] = ft.get_inverter_cost(df_inputs)

    #Get Structural BOS into final table
    df_final.loc['Structural BOS',state], df_structural_bos = ft.get_structural_bos(df_module_db, df_ballasted_systems, df_utility,project_size, num_modules, df_inputs, df_state, state, inflation, year, watts, df_loading_inputs)

    #Get Electrical BOS into final table
    #Get Install Labor & Equipment into final table
    if df_inputs.loc['Battery EPC?', A]:
        df_final.loc['Electrical BOS',state], df_electrical_bos, pv_source_conductor_job_qty, df_pre_sur, df_pre_sur_bat = ft.get_electrical_bos_battery(df_utility,project_size, num_modules, df_inputs, df_state, state, inflation, year, df_module_db, df_bos_cost, df_com_storage)
        df_final.loc['Install Labor & Equipment',state], df_install, df_wage = ft.get_install_cost_battery(df_electrical_bos, df_structural_bos, df_utility, df_labor, df_labor_weight, df_state, state, inflation, project_size, df_inputs, df_labor_table, num_modules, pv_source_conductor_job_qty, df_pre_sur, watts, df_pre_sur_bat)
    else:
        df_final.loc['Electrical BOS',state], df_electrical_bos, pv_source_conductor_job_qty, df_pre_sur = ft.get_electrical_bos(df_utility,project_size, num_modules, df_inputs, df_state, state, inflation, year, df_module_db, df_bos_cost)
        df_final.loc['Install Labor & Equipment',state], df_install, df_wage = ft.get_install_cost(df_electrical_bos, df_structural_bos, df_utility, df_labor, df_labor_weight, df_state, state, inflation, project_size, df_inputs, df_labor_table, num_modules, pv_source_conductor_job_qty, df_pre_sur, watts)
    
    #Get EPC Overhead Cost into final table
    df_final.loc['Epc Overhead',state], oh_p_cost, df_install = ft.get_oh_p_cost(df_install, project_size, df_labor_weight, df_wage)

    #Get land acquisition cost into final table
    df_final.loc['Land Acquisition',state] = ft.get_land_acq_cost(df_inputs)

    #Get Permitting Cost into final table
    df_final.loc['Permitting & Interconnection', state], permitting_cost = ft.get_permitting_cost(state, df_state, df_inputs, project_size, df_wage, df_labor_weight, df_utility, inflation)

    #   Get sales tax per watt into final table
    df_final.loc['Sale Tax (if any)',state], material_cost, equipment_cost = ft.get_sales_tax_cost(df_install, sales_tax, project_size, df_final.loc['Module',state], df_final.loc['Inverter Only',state])

    #Get Contingency Cost into final table
    df_final.loc['Contingency (4%)', state], pre_contigency_developer_oh_total = ft.get_contigency_cost(df_inputs, material_cost, equipment_cost, df_install, df_final.loc['Module',state], df_final.loc['Inverter Only',state], permitting_cost, project_size, df_final.loc['Sale Tax (if any)',state], oh_p_cost)

    #Get Contingency Cost into final table
    inflation_2015 = get_inflation(df_cpi, 2015)
    df_final.loc['Developer Overhead', state] = ft.get_developer_overhead_cost(df_dev_costs, df_dev_business_model, df_ancillary_exp, state, df_state, project_size, inflation, inflation_2015)

    #Get Net Profit into final table
    df_final.loc['EPC/Developer Net Profit', state] = ft.get_net_profit(df_final, state, df_profit)

    #Get Total System Cost final table
    df_final.loc['Total System Cost', state] = ft.get_total_cost(df_final, state)

    return df_final

# CREATING THE TABLE FOR THE STATE AND PROJECT SIZE OF INTEREST
num_modules, watts = num_of_modules(df_inputs, df_module_db, project_size_input)
print(num_modules)
print(watts)
df_state_of_interest = final_table(num_modules*watts, state_input, num_modules)
df_state_of_interest.rename(columns={state_input:(state_input + " " + str(project_size_input) + " MW")}, inplace=True)

#EXPORTING THE US AVERAGE, STATE OF INTEREST, AND ALL OTHER STATE TABLES TO EXCEL
export_path = path + "//results//Commercial Benchmark Results for Given Location.xlsx"
writer = pd.ExcelWriter(export_path, engine = 'xlsxwriter')

df_state_of_interest.to_excel(writer, sheet_name = 'State and Project of Interest')

writer.save()
writer.close()

#CREATE AND EXPORT STATE LEVEL FIGURE
import seaborn as sns

sns.set_style('whitegrid')
colors = ["#e7e34e","#1ac9e6","#eb548c","#1de4bd","#3665ff","#af4bce","#c7f9ee","#c02323","#f7f4bf","#ef7e32","#d9dbde","#3f8fc1"]

df_state_graph = df_state_of_interest.transpose().drop('Total System Cost', axis=1)

fig, ax = plt.subplots()
df_state_graph[df_state_graph.columns].plot(kind='bar', stacked = True, figsize=[5,12], ax=ax, color=colors)

plt.xticks(rotation='horizontal', fontsize=20, fontweight='bold')

total_height = 0
for n,rect in enumerate(ax.patches):
    ax.text(rect.get_x() + rect.get_width()/2, total_height+rect.get_height()/2, "%.2f" % df_state_graph.iloc[0,n], ha='center', va='center', fontsize = 16)
    total_height = rect.get_height() + total_height

ax.text(ax.patches[0].get_x()+ax.patches[0].get_width()/2, total_height+0.1, 'Total System Cost = ' + str("%.2f" % df_state_of_interest.loc['Total System Cost',(state_input + " " + str(project_size_input) + " MW")]), ha='center', va='center', fontsize = 16)

handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles), reversed(labels),fontsize = 16, bbox_to_anchor=(1.01, 1))

plt.ylim(top= df_state_of_interest.loc['Total System Cost',(state_input + " " + str(project_size_input) + " MW")]+0.2)
plt.yticks(fontsize=20, fontweight='bold')
plt.ylabel('$/W', fontsize=20, fontweight='bold')
plt.title('Commercial Benchmark of Input Location', fontsize=24, fontweight='bold')
plt.savefig(path + "//results//Figure for Given Location.png", bbox_inches='tight')

#FINISH
print('done')
print("--- %s seconds ---" % (time.time() - start_time))