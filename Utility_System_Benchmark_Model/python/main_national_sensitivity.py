import time
start_time=time.time()
import pandas as pd
import xlrd
import numpy as np
import matplotlib as plt
import final_table as ft
import inverter as inv
import os
import logging
import retrieve_datasets as rd

logging.captureWarnings(capture=True)

#Get the directory where the Python folder is saved"

if os.name=="nt":
	path = '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[0:-1])

	#Grab all the user input data from the input_data folder

	#Get all of the main inputs
	df_inputs = pd.read_excel(path + '\\input_data\\inputs.xlsx', index_col=0)

	#Get individual state data
	df_state = pd.read_csv(path + '\\input_data\\state_data.csv', header=[0,1], skip_blank_lines=True, index_col=[0])

	#Get module database
	df_module_db = pd.read_csv(path + '\\input_data\\module_database.csv', index_col=0)

	#Get Utility installation labor, material, and equipment costs
	df_utility = pd.read_csv(path + '\\input_data\\Utility - Material Labor Equipment.csv', index_col=0)

	#Get Consumer Price Index inflation data
	#df_cpi = pd.read_csv(path + '\\input_data\\consumer_price_index.csv', index_col=0)

	#Get labor database
	# df_labor_table = pd.read_excel(path + '\\input_data\\BLS Labor Database.xlsx')

	# Get Historical Cost Index for material & equipment cost
	df_hist_cost = pd.read_csv( path + '\\input_data\\historical_cost_index.csv' )

	#Get labor info to feed labor_database.py
	df_labor = pd.read_excel(path + '\\input_data\\Labor_Info.xlsx', sheet_name='Labor', index_col=0)

	#Get labor info to feed labor_database.py
	df_labor_weight = pd.read_excel(path + '\\input_data\\Labor_Info.xlsx', sheet_name='Labor Weight', index_col=0)

	#Get Bill of Material data
	df_torque_tube = pd.read_excel(path + '\\input_data\\Bill of Material Input.xlsx', sheet_name='Torque Tube Sizes', index_col=0)

	df_pipe = pd.read_excel(path + '\\input_data\\Bill of Material Input.xlsx', sheet_name='Pipe Sizes', index_col=0)

	df_rail_clamp = pd.read_excel(path + '\\input_data\\Bill of Material Input.xlsx', sheet_name='Rail Clamp type', index_col=0)

	# df_steel_price = pd.read_excel(path + '\\input_data\\Bill of Material Input.xlsx', sheet_name='US Steel Price Index', index_col=0)

	#Get Inverter and System sizing info
	df_inverter = pd.read_excel(path + '\\input_data\\600_1000_1500v.xlsx', sheet_name='Inverter', index_col=[0,1])

	df_sys_cond = pd.read_excel(path + '\\input_data\\600_1000_1500v.xlsx', sheet_name='System Conditions', index_col=[0,1])


	#Get Developer Overhead data
	df_epc = pd.read_excel(path + '\\input_data\\Overhead.xlsx', sheet_name='EPC Overhead Only', index_col=0)

	df_profit = pd.read_excel(path + '\\input_data\\Overhead.xlsx', sheet_name='Profit', index_col=0)

	df_trans = pd.read_excel(path + '\\input_data\\Overhead.xlsx', sheet_name='Transmission Line', index_col=0)

	#Get updated Labor Database
	# df_labor_table = pd.read_excel(path + '\\input_data\\BLS Labor Database.xlsx', index_col=0)

	#Get Loading info
	df_loading_combo = pd.read_csv(path + '\\input_data\\loading_combo.csv', index_col=[0])
else:
	path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-1])

	#Grab all the user input data from the input_data folder

	#Get all of the main inputs
	df_inputs = pd.read_excel(path + '/input_data/inputs.xlsx', index_col=0)

	#Get individual state data
	df_state = pd.read_csv(path + '/input_data/state_data.csv', header=[0,1], skip_blank_lines=True, index_col=[0])

	#Get module database
	df_module_db = pd.read_csv(path + '/input_data/module_database.csv', index_col=0)

	#Get Utility installation labor, material, and equipment costs
	df_utility = pd.read_csv(path + '/input_data/Utility - Material Labor Equipment.csv', index_col=0)

	#Get Consumer Price Index inflation data
	#df_cpi = pd.read_csv(path + '/input_data/consumer_price_index.csv', index_col=0)

	#Get labor database
	# df_labor_table = pd.read_excel(path + '/input_data/BLS Labor Database.xlsx')

	#Get Historical Cost Index for material & equipment cost
	df_hist_cost = pd.read_csv(path + '/input_data/historical_cost_index.csv')

	#Get labor info to feed labor_database.py
	df_labor = pd.read_excel(path + '/input_data/Labor_Info.xlsx', sheet_name='Labor', index_col=0)

	#Get labor info to feed labor_database.py
	df_labor_weight = pd.read_excel(path + '/input_data/Labor_Info.xlsx', sheet_name='Labor Weight', index_col=0)

	#Get Bill of Material data
	df_torque_tube = pd.read_excel(path + '/input_data/Bill of Material Input.xlsx', sheet_name='Torque Tube Sizes', index_col=0)

	df_pipe = pd.read_excel(path + '/input_data/Bill of Material Input.xlsx', sheet_name='Pipe Sizes', index_col=0)

	df_rail_clamp = pd.read_excel(path + '/input_data/Bill of Material Input.xlsx', sheet_name='Rail Clamp type', index_col=0)

	# df_steel_price = pd.read_excel(path + '/input_data/Bill of Material Input.xlsx', sheet_name='US Steel Price Index', index_col=0)

	#Get Inverter and System sizing info
	df_inverter = pd.read_excel(path + '/input_data/600_1000_1500v.xlsx', sheet_name='Inverter', index_col=[0,1])

	df_sys_cond = pd.read_excel(path + '/input_data/600_1000_1500v.xlsx', sheet_name='System Conditions', index_col=[0,1])


	#Get Developer Overhead data
	df_epc = pd.read_excel(path + '/input_data/Overhead.xlsx', sheet_name='EPC Overhead Only', index_col=0)

	df_profit = pd.read_excel(path + '/input_data/Overhead.xlsx', sheet_name='Profit', index_col=0)

	df_trans = pd.read_excel(path + '/input_data/Overhead.xlsx', sheet_name='Transmission Line', index_col=0)

	#Get updated Labor Database
	#df_labor_table = pd.read_excel(path + '/input_data/BLS Labor Database.xlsx', index_col=0)

	#Get Loading info
	df_loading_combo = pd.read_csv(path + '/input_data/loading_combo.csv', index_col=[0])

#call retreive_datset and store all dataframes

dataset = rd.get_datasets()
cpi_data = dataset[0]
spi_data = dataset[1]
utility_installation_data = dataset[2]
commercial_installation_data = dataset[3]
residential_installation_data = dataset[4]
labor_installation_data = dataset[5]
labor_data_year = int(dataset[6])
labor_installation_data_nat = dataset[7]

# Add United States to the existing list
labor_installation_data.loc['United States'] = labor_installation_data_nat.iloc[0]
utility_installation_data.loc['United States'] = utility_installation_data.sum()
commercial_installation_data.loc['United States'] = commercial_installation_data.sum()
residential_installation_data.loc['United States'] = residential_installation_data.sum()

#assign retrieved datasets to existing dataframes
df_labor_table = labor_installation_data
df_cpi = cpi_data

df_hist_cost = df_hist_cost.set_index('Year', drop=True)
df_steel_price = spi_data

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

def watt_calc(df_inputs, df_module_db, project_size):
	module = df_inputs.loc['Module Name', A]
	mod_size = df_module_db.loc[module, 'Length (mm)'] / 1000.0 * df_module_db.loc[module, 'Width (mm)'] / 1000.0

	length_m = df_module_db.loc[module, 'Length (mm)'] / 1000.0
	width_m = df_module_db.loc[module, 'Width (mm)'] / 1000.0

	if pd.isnull( df_inputs.loc['Module Efficiency', A] ):
		efficiency = df_module_db.loc[module, 'Efficiency (from Specs)']
	else:
		efficiency = df_inputs.loc['Module Efficiency', A]

	watts = mod_size * efficiency * 1000
	# if df_inputs.loc['Fixed Acreage ?', A]:
	# 	num_modules = project_size / 291 * 1000000
	# else:
	# 	num_modules = project_size / watts * 1000000

	return watts, length_m, width_m

#calculates inflation based on 2019 cost data used
def get_inflation(df_cpi, year):
	df_c = df_cpi
	df_c['Change'] = df_c['cpi']/df_c.loc[2020,'cpi']
	# compound = (df_c.loc[year,'cpi']/df_c.loc[2000,'cpi'])**(1/(year-2000))
	# if pd.isnull(df_c.loc[year,'Change']):
	# 	inflation = compound**(year-2019)
	# else:
	inflation = df_c.loc[year,'Change']
	# print(inflation)
	return inflation

#Based on labor year data pulled from bls appropriate cost adjustment is made
def get_labor_inflation(year, labor_data_year, df_cpi):
	labor_inflation = df_cpi.loc[year, 'cpi']/df_cpi.loc[labor_data_year, 'cpi']
	print("labor inflation",labor_inflation)
	return labor_inflation

#Calculates cost index for construction costs - material & equipment based on 2019 RS means data
def get_hist_cost_index(year, df_hist_cost):
	hist_cost_index = df_hist_cost.loc[year,'cost_index']/df_hist_cost.loc[2020,'cost_index']
	# print(hist_cost_index)
	return hist_cost_index

#Global Variables
year = df_inputs.loc['Year', A]
inflation = get_inflation(df_cpi, year)
hist_cost_index = get_hist_cost_index(year,df_hist_cost)
labor_inflation = get_labor_inflation(year, labor_data_year, df_cpi)
steel_inflation = df_steel_price.loc[year,'spi']/df_steel_price.loc[2012,'spi']
state_input = df_inputs.loc['Location', A]
project_size_input = df_inputs.loc['Project Size (MW)', A]
tracker_input = df_inputs.loc['Tracker?', A]

#adjust labor table with inflation before calculations
df_labor_table = df_labor_table[["Electricians - 10","Electricians - 50","Electricians - 90",
								 "Construction Laborers - 10","Construction Laborers - 50","Construction Laborers - 90",
								 "Operating Engineers and Other Construction Equipment Operators - 10","Operating Engineers and Other Construction Equipment Operators - 50","Operating Engineers and Other Construction Equipment Operators - 90"]] * labor_inflation


state_list = ["United States"]
# state_list = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
#   "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
#   "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
#   "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
#   "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
#   "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
#   "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
#   "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming","DC","Puerto Rico"
#   ]
project_size_list = [100]

tracker_list = [True]


tracker_df_list =[]
keys_list=[]
df_complete_usa_table = pd.DataFrame()
df_state_results={}

#add cumulative installation number for available states to exisiting dataframe
df_states = df_state.join(utility_installation_data['Cumulative Install'])

#FUNCTION TO COMPUTE EACH ITEM IN THE FINAL TABLE
def final_table(project_size, poi, state, df_inv_calc, num_modules):
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
	df_final.loc['Structural BOS',state], df_structural_bos, df_bom, size_factor = ft.get_structural_bos(df_utility,project_size, num_modules, df_inputs, df_state, state, hist_cost_index, df_module_db, year, df_torque_tube, df_pipe, df_rail_clamp, steel_inflation, df_inv_calc, df_loading_combo)

	#Get Electrical BOS into final table
	df_final.loc['Electrical BOS',state], df_electrical_bos = ft.get_electrical_bos(df_structural_bos, df_utility, hist_cost_index, df_state, state, df_bom, size_factor, num_modules, df_inv_calc, df_inputs, project_size)

	#Get Install Labor & Equipment into final table
	df_final.loc['Install Labor & Equipment',state], df_install, df_wage = ft.get_install_cost(df_electrical_bos, df_structural_bos, df_utility, df_labor, df_labor_weight, df_state, state, project_size, df_inputs, df_labor_table)


	#Get EPC Overhead Cost into final table
	df_final.loc['Epc Overhead',state], df_total_installed_cost, df_bare_cost, trans_dist_list = ft.get_oh_p_cost(df_inputs, df_install, df_utility, df_state, state, inflation, hist_cost_index, project_size, poi, df_labor_weight, df_wage, df_epc, df_trans)


	#Get land acquisition cost into final table
	df_final.loc['Land Acquisition',state] = ft.get_land_acq_cost(df_inputs)

	#Get Permitting Cost into final table
	df_final.loc['Permitting Fee (if any)', state] = ft.get_permitting_cost(state, df_state, df_inputs, project_size)

	#Get Interconnection Fee Cost into final table
	df_final.loc['Interconnection Fee', state] = ft.get_interconnection_cost(df_utility, df_state, state, inflation, project_size, poi, df_inputs)

	#Get Transmission Line cost into final table
	df_final.loc['Transmission Line (if any)', state], other_eng = ft.get_transmission_cost(df_bare_cost, trans_dist_list, project_size, poi)

	#Get Contingency Cost into final table
	df_final.loc['Contingency (3%)', state], material_cost, equipment_cost, pre_contigency_developer_oh_total = ft.get_contigency_cost(df_inputs, df_bare_cost, other_eng, df_final.loc['Module',state], df_final.loc['Inverter Only',state], df_final.loc['Land Acquisition',state], project_size, sales_tax, df_final.loc['Epc Overhead',state],df_final.loc['Permitting Fee (if any)', state])

	#Get sales tax per watt into final table
	df_final.loc['Sale Tax (if any)',state] = ft.get_sales_tax_cost(material_cost, equipment_cost, sales_tax, project_size)

	#Get Contingency Cost into final table
	df_final.loc['Developer Overhead', state] = ft.get_developer_overhead_cost(pre_contigency_developer_oh_total, project_size)

	#Get Net Profit into final table
	df_final.loc['EPC/Developer Net Profit', state] = ft.get_net_profit(df_final,state,project_size, df_profit)

	#Get Total System Cost final table
	df_final.loc['Total System Cost', state] = ft.get_total_cost(df_final, state)

	return df_final
#Sensitivity Loop with values [low, high, basecase]

sensitivity_dict = {
	'Module Efficiency': {
		'location': df_inputs,
		'column': 'Value A',
		'sensitivity_value_list': [0.194,0.206, 0.199],
	},
	'Module Price ($/W)': {
		'location': df_inputs,
		'column': 'Value A',
		'sensitivity_value_list': [0.35,0.47,0.37],
	},
	'United States A': {
		'location': df_state,
		'column': ('ASCE 7-05 Design Criteria', 'Wind'),
		'sensitivity_value_list': [85, 145, 90],
	},
	'United States B': {
		'location': df_state,
		'column': ('ASCE 7-05 Design Criteria', 'Snow'),
		'sensitivity_value_list': [0, 60, 20],
	},
	'United States C': {
		'location': df_state,
		'column': ('Sales Tax', 'Utility'),
		'sensitivity_value_list': [0, 0.075, 0.058],
	},
	'United States D': {
		'location': df_state,
		'column': ('Location Factor', 'Material'),
		'sensitivity_value_list': [91.3, 117.8, 98.1],
	},
	'United States E': {
		'location': df_state,
		'column': ('Location Factor', 'Equipment'),
		'sensitivity_value_list': [27.2, 176.2, 83.7],
	},
	'United States F': {
		'location': df_labor_table,
		'column': ('Electricians - 50'),
		'sensitivity_value_list': [11.68, 41.01, 27.36],
	},
	'United States G': {
		'location': df_labor_table,
		'column': ('Construction Laborers - 50'),
		'sensitivity_value_list': [8.8, 28.11, 18.22],
	},
	'United States H': {
		'location': df_labor_table,
		'column': ('Operating Engineers and Other Construction Equipment Operators - 50'),
		'sensitivity_value_list': [9.65, 40.13, 23.93],
	},
}

# sensitivity_percent_list = [1.5,1, 0.5]


for variable in sensitivity_dict.keys():
	if 'United States' in variable:
		loc_variable = 'United States'
	else:
		loc_variable = variable

	for sensitivity_value in sensitivity_dict[variable]['sensitivity_value_list']:

		original_variable_value = sensitivity_dict[variable]['location'].loc[loc_variable, sensitivity_dict[variable]['column']]
		sensitivity_dict[variable]['location'].loc[loc_variable, sensitivity_dict[variable]['column']] = sensitivity_value

		#LOOPING THROUGH FIXED TILT AND ONE AXIS, ALL PROJECT SIZES, AND ALL STATES TO CREATE THE FINAL TABLE FOR THE MAIN FIGURE
		for tracker in tracker_list:
			df_inputs.at['Tracker?', A] = tracker

			if tracker:
				axis = 'One-Axis Tracker'
			else:
				axis = 'Fixed-Tilt'

			df_all_sizes = pd.DataFrame()

			for project_size in project_size_list:

				num_modules = num_of_modules(df_inputs, df_module_db, project_size)

				df_inv_calc = inv.inverter_calculations(num_modules, df_inverter, df_sys_cond)
				df_all_states = pd.DataFrame()
				if df_inputs.loc['Tracker?', A]:
					dc_ac_ratio = df_inputs.loc['DC to AC Ratio', A]
				else:
					dc_ac_ratio = df_inputs.loc['DC to AC Ratio', B]
				poi = round(project_size/dc_ac_ratio,2)

				for state in state_list:

					df_final = final_table(project_size, poi, state, df_inv_calc, num_modules)
					total_cost = df_final.loc['Total System Cost', state]
					watt = watt_calc(df_inputs, df_module_db, project_size)[0]
					length = watt_calc(df_inputs, df_module_db, project_size)[1]
					width = watt_calc( df_inputs, df_module_db, project_size )[2]

					print(loc_variable, ';', sensitivity_dict[variable]['column'], ';', watt, ';', length, ';', width, ';', project_size, ';', poi, ';', tracker,';', (sensitivity_value), ';', total_cost)
		sensitivity_dict[variable]['location'].loc[loc_variable, sensitivity_dict[variable]['column']] = original_variable_value

# 			# df_final.loc['Weight'] = df_state.loc[state,('State Weight','Utility Weight')]
# 			df_final.loc['Weight'] = df_states.loc[state, 'Cumulative Install']
# 			# print(df_final.loc['Weight'])
# 			df_all_states[state] = df_final[state]
# 		# df_all_states.loc['Weight'] = df_all_states.apply(lambda x:df_state.loc[x.name,('State Weight','Utility Weight')], axis=0)
# 		df_all_states.loc['Weight'] = df_all_states.apply(lambda x: df_states.loc[x.name, 'Cumulative Install'], axis=0 )
# 		df_all_states = df_all_states.fillna(0)
# 		df_state_results[axis+" "+str(project_size)+" MW"] = df_all_states
#
# 		weight_sum = df_all_states.loc['Weight'].sum()
# 		df_us_avg = df_all_states.apply(lambda x: x.dot(df_all_states.loc['Weight'])/weight_sum, axis = 1)
# 		df_us_avg = df_us_avg.drop('Weight', axis=0)
# 		df_all_sizes[project_size]= df_us_avg
#
# 	keys_list.append(axis)
# 	tracker_df_list.append(df_all_sizes)
#
# df_complete_usa_table = pd.concat(tracker_df_list, keys=keys_list, axis = 1, sort = True)


#CREATING THE TABLE FOR THE STATE AND PROJECT SIZE OF INTEREST
# if project_size_input in project_size_list:
# 	if tracker_input:
# 		axis = 'One-Axis Tracker'
# 	else:
# 		axis = 'Fixed-Tilt'
# 	df_state_of_interest = df_state_results[axis + " " + str(project_size_input) + " MW"][state_input]
# 	df_state_of_interest.rename((state_input + " " + axis + " " + str(project_size_input) + " MW"), inplace=True)
# else:
# 	df_inputs.at['Tracker?', A] = tracker_input
# 	num_modules = num_of_modules(df_inputs, df_module_db, project_size_input)
# 	df_inv_calc = inv.inverter_calculations(num_modules, df_inverter, df_sys_cond)
# 	df_state_of_interest = final_table(project_size_input, state_input, df_inv_calc, num_modules)
# 	df_state_of_interest.rename(columns={state_input:(state_input + " " + axis + " " + str(project_size_input) + " MW")}, inplace=True)

#EXPORTING THE US AVERAGE, STATE OF INTEREST, AND ALL OTHER STATE TABLES TO EXCEL

# if os.name=="nt":
# 	export_path = path + '\\results\\Utility Benchmark National Results.xlsx'
# else:
# 	export_path = path + '/results/Utility Benchmark National Results.xlsx'
#
# writer = pd.ExcelWriter(export_path, engine = 'xlsxwriter')
#
# df_complete_usa_table.to_excel(writer, sheet_name = 'US Weighted Average Results')
# # df_state_of_interest.to_excel(writer, sheet_name = 'State and Project of Interest')
# [df.to_excel(writer, sheet_name = key) for key, df in df_state_results.items()]
# #
# # print(df_complete_usa_table['Total System Cost'])
# writer.save()
# writer.close()
print('done')
print("--- %s seconds ---" % (time.time() - start_time))

