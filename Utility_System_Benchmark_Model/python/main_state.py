import time
start_time=time.time()
import pandas as pd
import numpy as np
import matplotlib as plt
import final_table as ft
import inverter as inv
import os
import logging


logging.captureWarnings(capture=True)

#Get the directory where the Python folder is saved

path = '//'.join(os.path.dirname(os.path.abspath(__file__)).split('//')[0:-1])

#Grab all the user input data from the input_data folder

#Get all of the main inputs
df_inputs = pd.read_excel(path + '//input_data//inputs.xlsx', index_col=0)

#Get individual state data
df_state = pd.read_csv(path + '//input_data//state_data.csv', header=[0,1], skip_blank_lines=True, index_col=[0])

#Get module database
df_module_db = pd.read_csv(path + '//input_data//module_database.csv', index_col=0)

#Get Utility installation labor, material, and equipment costs
df_utility = pd.read_csv(path + '//input_data//Utility - Material Labor Equipment.csv', index_col=0)

#Get Consumer Price Index inflation data
df_cpi = pd.read_csv(path + '//input_data//consumer_price_index.csv', index_col=0)

#Get labor database
df_labor_table = pd.read_excel(path + '//input_data//BLS Labor Database.xlsx')

#Get labor info to feed labor_database.py
df_labor = pd.read_excel(path + '//input_data//Labor_Info.xlsx', sheet_name='Labor', index_col=0)

#Get labor info to feed labor_database.py
df_labor_weight = pd.read_excel(path + '//input_data//Labor_Info.xlsx', sheet_name='Labor Weight', index_col=0)

#Get Bill of Material data
df_torque_tube = pd.read_excel(path + '//input_data//Bill of Material Input.xlsx', sheet_name='Torque Tube Sizes', index_col=0)

df_pipe = pd.read_excel(path + '//input_data//Bill of Material Input.xlsx', sheet_name='Pipe Sizes', index_col=0)

df_rail_clamp = pd.read_excel(path + '//input_data//Bill of Material Input.xlsx', sheet_name='Rail Clamp type', index_col=0)

df_steel_price = pd.read_excel(path + '//input_data//Bill of Material Input.xlsx', sheet_name='US Steel Price Index', index_col=0)

#Get Inverter and System sizing info
df_inverter = pd.read_excel(path + '//input_data//600_1000_1500v.xlsx', sheet_name='Inverter', index_col=[0,1])

df_sys_cond = pd.read_excel(path + '//input_data//600_1000_1500v.xlsx', sheet_name='System Conditions', index_col=[0,1])


#Get Developer Overhead data
df_epc = pd.read_excel(path + '//input_data//Overhead.xlsx', sheet_name='EPC Overhead Only', index_col=0)

df_profit = pd.read_excel(path + '//input_data//Overhead.xlsx', sheet_name='Profit', index_col=0)

#Get updated Labor Database
df_labor_table = pd.read_excel(path + '//input_data//BLS Labor Database.xlsx', index_col=0)

#Get Loading info
df_loading_combo = pd.read_csv(path + '//input_data//loading_combo.csv', index_col=[0])

#Create variables for column header strings
A = 'Value A'
B = 'Value B'
C = 'Value C'
D = 'Value D'

#Intermediate Functions
#Function to get number of modules for selected Project Size
def num_of_modules(df_inputs, df_module_db, project_size):
	"""
	This function calculates the number of modules that would be needed for the given project size, type of module, and other parameters which are specified by the user in the input spreadsheets.
	
	Parameters
	----------
	df_inputs : DataFrame
		Table of all the main inputs that are specificed by the user

	df_module_db : DataFrame
		Table of different module brands and sizes along with their other specifications

	project_size : int
		The size of the solar system in MW specified by the user in the main inputs table

	Returns
	-------

	num_modules : 
	
	"""  

	module = df_inputs.loc['Module Name', A]
	mod_size = df_module_db.loc[module,'Length (mm)']/1000.0*df_module_db.loc[module,'Width (mm)']/1000.0
	
	if pd.isnull(df_inputs.loc['Module Efficiency', A]):
		efficiency = df_module_db.loc[module,'Efficiency (from Specs)']
	else:
		efficiency = df_inputs.loc['Module Efficiency', A]
	
	watts = mod_size*efficiency*1000
	if df_inputs.loc['Fixed Acreage ?', A]:
		num_modules = project_size/291*1000000
	else:
		num_modules = project_size/watts*1000000
	return num_modules

def get_inflation(df_cpi, year):
	"""
	This function calculates the inflation value for the specified year from the consumer price index
	
	Input
	-----
	df_cpi: A table of consumer price index values that are manually input by the user

	state: The full name of the state being analyzed

	Output
	------

	df_final: The final table of system costs for the location and system size specified.
	
	"""    

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
steel_inflation = df_steel_price.loc['price',year]/df_steel_price.loc['price',2012]
state_input = df_inputs.loc['Location', A]
project_size_input = df_inputs.loc['Project Size (MW)', A]
tracker_input = df_inputs.loc['Tracker?', A]


#FUNCTION TO COMPUTE EACH ITEM IN THE FINAL TABLE
def final_table(project_size, state, df_inv_calc, num_modules):
	"""
	This function calls a series of other functions that calculate the individual system costs and outputs a final table of all these costs. The individual system costs are calculated line by line in the table. The total system cost is also calculated and output in this table.

	Input
	-----
	project_size: int
		The size of the solar system in MW specified by the user in the main inputs table

	state: The full name of the state being analyzed

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
	df_final.loc['Structural BOS',state], df_structural_bos, df_bom, size_factor = ft.get_structural_bos(df_utility,project_size, num_modules, df_inputs, df_state, state, inflation, df_module_db, year, df_torque_tube, df_pipe, df_rail_clamp, steel_inflation, df_inv_calc, df_loading_combo)

	#Get Electrical BOS into final table
	df_final.loc['Electrical BOS',state], df_electrical_bos = ft.get_electrical_bos(df_structural_bos, df_utility, inflation, df_state, state, df_bom, size_factor, num_modules, df_inv_calc, df_inputs, project_size)

	#Get Install Labor & Equipment into final table
	df_final.loc['Install Labor & Equipment',state], df_install, df_wage = ft.get_install_cost(df_electrical_bos, df_structural_bos, df_utility, df_labor, df_labor_weight, df_state, state, project_size, df_inputs, df_labor_table)
	
	#Get EPC Overhead Cost into final table
	df_final.loc['Epc Overhead',state], df_total_installed_cost, df_bare_cost, trans_dist_list = ft.get_oh_p_cost(df_inputs, df_install, df_utility, df_state, state, inflation, project_size, df_labor_weight, df_wage, df_epc)

	#Get land acquisition cost into final table
	df_final.loc['Land Acquisition',state] = ft.get_land_acq_cost(df_inputs)

	#Get Permitting Cost into final table
	df_final.loc['Permitting Fee (if any)', state] = ft.get_permitting_cost(state, df_state, df_inputs, project_size)

	#Get Interconnection Fee Cost into final table
	df_final.loc['Interconnection Fee', state] = ft.get_interconnection_cost(df_utility, df_state, state, inflation, project_size, df_inputs)

	#Get Transmission Line cost into final table
	df_final.loc['Transmission Line (if any)', state], other_eng = ft.get_transmission_cost(df_bare_cost, trans_dist_list, project_size)

	#Get Contingency Cost into final table
	df_final.loc['Contingency (3%)', state], material_cost, equipment_cost, pre_contigency_developer_oh_total = ft.get_contigency_cost(df_inputs, df_bare_cost, other_eng, df_final.loc['Module',state], df_final.loc['Inverter Only',state], df_final.loc['Land Acquisition',state], project_size, sales_tax, df_final.loc['Epc Overhead',state], df_final.loc['Permitting Fee (if any)', state])

	#Get sales tax per watt into final table
	df_final.loc['Sale Tax (if any)',state] = ft.get_sales_tax_cost(material_cost, equipment_cost, sales_tax, project_size)

	#Get Contingency Cost into final table
	df_final.loc['Developer Overhead', state] = ft.get_developer_overhead_cost(pre_contigency_developer_oh_total, project_size)

	#Get Net Profit into final table
	df_final.loc['EPC/Developer Net Profit', state] = ft.get_net_profit(df_final,state,project_size, df_profit)

	#Get Total System Cost final table
	df_final.loc['Total System Cost', state] = ft.get_total_cost(df_final, state)

	return df_final, df_total_installed_cost


#LOOPING THROUGH FIXED TILT AND ONE AXIS, ALL PROJECT SIZES, AND ALL STATES TO CREATE THE FINAL TABLE FOR THE MAIN FIGURE
# for tracker in tracker_list:
# 	df_inputs.at['Tracker?', A] = tracker
	
# 	if tracker.lower()=='true':
# 		axis = 'One-Axis Tracker'
# 	else:
# 		axis = 'Fixed-Tilt'
	
# 	df_all_sizes = pd.DataFrame()
	
# 	for project_size in project_size_list:
# 		num_modules = num_of_modules(df_inputs, df_module_db, project_size)

# 		df_inv_calc = inv.inverter_calculations(num_modules, df_inverter, df_sys_cond)
# 		df_all_states = pd.DataFrame()
# 		for state in state_list:

# 			df_final = final_table(project_size, state, df_inv_calc, num_modules)

# 			df_final.loc['Weight'] = df_state.loc[state,('State Weight','Utility Weight')]

# 			df_all_states[state] = df_final[state]

# 		df_all_states.loc['Weight'] = df_all_states.apply(lambda x:df_state.loc[x.name,('State Weight','Utility Weight')], axis=0)
# 		df_all_states = df_all_states.fillna(0)
# 		df_state_results[axis+" "+str(project_size)+" MW"] = df_all_states
		
# 		weight_sum = df_all_states.loc['Weight'].sum()
# 		df_us_avg = df_all_states.apply(lambda x: x.dot(df_all_states.loc['Weight'])/weight_sum, axis = 1)                                       
# 		df_us_avg = df_us_avg.drop('Weight', axis=0)
# 		df_all_sizes[project_size]= df_us_avg
# 	keys_list.append(axis)
# 	tracker_df_list.append(df_all_sizes)

# df_complete_usa_table = pd.concat(tracker_df_list, keys=keys_list, axis = 1, sort = True)

#CREATING THE TABLE FOR THE STATE AND PROJECT SIZE OF INTEREST
num_modules = num_of_modules(df_inputs, df_module_db, project_size_input)
df_inv_calc = inv.inverter_calculations(num_modules, df_inverter, df_sys_cond)
df_state_of_interest, df_total_installed_cost = final_table(project_size_input, state_input, df_inv_calc, num_modules)
if tracker_input:
	axis = 'One-Axis Tracker'
else:
	axis = 'Fixed-Tilt'
df_state_of_interest.rename(columns={state_input:(state_input + " " + axis + " " + str(project_size_input) + " MW")}, inplace=True)

# if project_size_input in project_size_list:
# 	if tracker_input:
# 		axis = 'One-Axis Tracker'
# 	else:
# 		axis = 'Fixed-Tilt'
# 	df_state_of_interest = df_state_results[axis + " " + str(project_size_input) + " MW"][state_input]
# 	df_state_of_interest.rename((state_input + " " + axis + " " + str(project_size_input) + " MW"), inplace=True)
# else:
# 	df_inputs.at['Tracker?', A] = tracker_input
	


#EXPORTING THE US AVERAGE, STATE OF INTEREST, AND ALL OTHER STATE TABLES TO EXCEL
export_path = path + "//results//Utility Benchmark Results for Given Location.xlsx"
writer = pd.ExcelWriter(export_path, engine = 'xlsxwriter')

df_state_of_interest.to_excel(writer, sheet_name = 'State and Project of Interest')
df_total_installed_cost.to_excel(path + "//results//test.xlsx", sheet_name = 'State and Project of Interest')
writer.save()
writer.close()

#CREATE AND EXPORT STATE LEVEL FIGURE
# df_state_graph = df_state_of_interest.transpose().drop('Total System Cost', axis=1)
# fig, ax = plt.subplots()
# df_state_graph[df_state_graph.columns].plot(kind='bar', stacked = True, figsize=[5,12], ax=ax)
# plt.xticks(rotation='horizontal', fontsize=20)
# total_height = 0
# for n,rect in enumerate(ax.patches):
#     ax.text(rect.get_x() + rect.get_width()/2, total_height+rect.get_height()/2, "%.2f" % df_state_graph.iloc[0,n], ha='center', va='center', fontsize = 16)
#     total_height = rect.get_height() + total_height

# ax.text(ax.patches[0].get_x()+ax.patches[0].get_width()/2, total_height+0.1, 'Total System Cost = ' + str("%.2f" % df_state_of_interest.loc['Total System Cost',(state_input + " " + str(project_size_input) + " MW")]), ha='center', va='center', fontsize = 16)

# plt.legend(fontsize = 16, bbox_to_anchor=(1.01, 1))
# plt.ylim(top= df_state_of_interest.loc['Total System Cost',(state_input + " " + str(project_size_input) + " MW")]+0.2)
# plt.yticks(fontsize=20)
# plt.savefig(path + "//results//Figure for Given Location.png", bbox_inches='tight')

print('done')
print("--- %s seconds ---" % (time.time() - start_time))