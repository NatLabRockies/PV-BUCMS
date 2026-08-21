import time
start_time=time.time()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import final_table as ft
import math
import os
import retrieve_datasets as rd

if os.name=="nt":
	path = '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[0:-1])

#Pull in all the inputs from csv into a df
	df_inputs = pd.read_excel(path + '\\input_data\\inputs.xlsx', index_col=0)

#Get state data from csv into a df
	df_state = pd.read_csv(path + '\\input_data\\state_data.csv', header=[0,1], skip_blank_lines=True, index_col=[0])

#Get module database from csv to df
	df_module_db = pd.read_excel(path + '\\input_data\\module_database.xlsx', index_col=0)

#Get Commercial installation cost inputs csv to df
	df_utility = pd.read_csv(path + '\\input_data\\Commercial - Material Labor Equipment.csv', index_col=0)

#Get consumer price index inflation data to df
	# df_cpi = pd.read_csv(path + '\\input_data\\consumer_price_index.csv', index_col=0)

# Get Historical Cost Index for material & equipment cost
	df_hist_cost = pd.read_csv( path + '\\input_data\\historical_cost_index.csv' )

#Get labor info to feed labor_database.py
	df_labor = pd.read_excel(path + '\\input_data\\Labor_Info.xlsx', sheet_name='Labor', index_col=0)

#Get labor info to feed labor_database.py
	df_labor_weight = pd.read_excel(path + '\\input_data\\Labor_Info.xlsx', sheet_name='Labor Weight', index_col=0)

	df_ballasted_systems = pd.read_excel(path + '\\input_data\\Bill of Material Input.xlsx', sheet_name='Ballasted Systems', index_col=0)

	df_bos_cost = pd.read_excel(path + '\\input_data\\Bill of Material Input.xlsx', sheet_name='BOS Cost Category', index_col=0)

	# df_labor_table = pd.read_excel(path + '\\input_data\\BLS Labor Database.xlsx', index_col=0)

#Get Developer Overhead info
	df_dev_costs = pd.read_excel(path + '\\input_data\\Developer Profit & Overhead.xlsx', sheet_name='Developer Costs', index_col=0)

	df_dev_business_model = pd.read_excel(path + '\\input_data\\Developer Profit & Overhead.xlsx', sheet_name='Developer Business Model', index_col=0)

	df_profit = pd.read_excel(path + '\\input_data\\Developer Profit & Overhead.xlsx', sheet_name='Profit', index_col=0)

	df_ancillary_exp = pd.read_excel(path + '\\input_data\\Developer Profit & Overhead.xlsx', sheet_name='Ancillary Expenses', index_col=0)

#Get Storage info
	df_com_storage = pd.read_excel(path + '\\input_data\\commercial_storage.xlsx', index_col=0)

#Get Loading info
	df_loading_inputs = pd.read_csv(path + '\\input_data\\loading_combo.csv',index_col=[0])

# Get inverter data from csv into a df
	df_inverter = pd.read_csv( path + '\\input_data\\inverter.csv', skip_blank_lines=True, index_col=[0] )

else:
	path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-1])

#Pull in all the inputs from csv into a df
	df_inputs = pd.read_excel(path + '/input_data/inputs.xlsx', index_col=0)

#Get state data from csv into a df
	df_state = pd.read_csv(path + '/input_data/state_data.csv', header=[0,1], skip_blank_lines=True, index_col=[0])

#Get module database from csv to df
	df_module_db = pd.read_excel(path + '/input_data/module_database.xlsx', index_col=0)

#Get Commercial installation cost inputs csv to df
	df_utility = pd.read_csv(path + '/input_data/Commercial - Material Labor Equipment.csv', index_col=0)

#Get consumer price index inflation data to df
	# df_cpi = pd.read_csv(path + '/input_data/consumer_price_index.csv', index_col=0)

# Get Historical Cost Index for material & equipment cost
	df_hist_cost = pd.read_csv( path + '/input_data/historical_cost_index.csv' )

#Get labor info to feed labor_database.py
	df_labor = pd.read_excel(path + '/input_data/Labor_Info.xlsx', sheet_name='Labor', index_col=0)

#Get labor info to feed labor_database.py
	df_labor_weight = pd.read_excel(path + '/input_data/Labor_Info.xlsx', sheet_name='Labor Weight', index_col=0)

	df_ballasted_systems = pd.read_excel(path + '/input_data/Bill of Material Input.xlsx', sheet_name='Ballasted Systems', index_col=0)

	df_bos_cost = pd.read_excel(path + '/input_data/Bill of Material Input.xlsx', sheet_name='BOS Cost Category', index_col=0)

	# df_labor_table = pd.read_excel(path + '/input_data/BLS Labor Database.xlsx', index_col=0)

#Get Developer Overhead info
	df_dev_costs = pd.read_excel(path + '/input_data/Developer Profit & Overhead.xlsx', sheet_name='Developer Costs', index_col=0)

	df_dev_business_model = pd.read_excel(path + '/input_data/Developer Profit & Overhead.xlsx', sheet_name='Developer Business Model', index_col=0)

	df_profit = pd.read_excel(path + '/input_data/Developer Profit & Overhead.xlsx', sheet_name='Profit', index_col=0)

	df_ancillary_exp = pd.read_excel(path + '/input_data/Developer Profit & Overhead.xlsx', sheet_name='Ancillary Expenses', index_col=0)

#Get Storage info
	df_com_storage = pd.read_excel(path + '/input_data/commercial_storage.xlsx', index_col=0)

#Get Loading info
	df_loading_inputs = pd.read_csv(path + '/input_data/loading_combo.csv',index_col=[0])

#Get inverter data from csv into a df
	df_inverter = pd.read_csv(path + '/input_data/inverter.csv', skip_blank_lines=True, index_col=[0])

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
		num_modules = math.ceil(project_size/310.4*1000000)
	else:
		num_modules = math.ceil(project_size/watts*1000000)
	
	return num_modules, watts

#calculates inflation based on 2019 cost data used
def get_inflation(df_cpi, year):
	df_c = df_cpi
	df_c['Change'] = df_c['cpi'] / df_c.loc[year, 'cpi']
	# compound = (df_c.loc[year,'cpi']/df_c.loc[2000,'cpi'])**(1/(year-2000))
	# if pd.isnull(df_c.loc[year,'Change']):
	# inflation = compound**(year-2019)
	# else:
	inflation = df_c.loc[year, 'Change']
	# print(inflation)

	return inflation

#Based on labor year data pulled from bls appropriate cost adjustment is made
def get_labor_inflation(year, labor_data_year, df_cpi):
 labor_inflation = df_cpi.loc[year, 'cpi']/df_cpi.loc[labor_data_year, 'cpi']
 # print(labor_inflation)
 return labor_inflation

#Calculates cost index for construction costs - material & equipment based on 2019 RS means data
def get_hist_cost_index(year, df_hist_cost):
 hist_cost_index = df_hist_cost.loc[year,'cost_index']/df_hist_cost.loc[2020,'cost_index']
 # print(hist_cost_index)
 return hist_cost_index

#Global Variables
year = df_inputs.loc['Year', A]
inflation = get_inflation(df_cpi, year)
state_input = df_inputs.loc['Location', A]
project_size_input = df_inputs.loc['Project Size (MW)', A]
hist_cost_index = get_hist_cost_index(year,df_hist_cost)
labor_inflation = get_labor_inflation(year, labor_data_year, df_cpi)
steel_inflation = df_steel_price.loc[year,'spi']/df_steel_price.loc[2012,'spi']

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

# state_list = ["California"
#   ]

nec_2017_list = ["Alaska","Connecticut","Hawaii","Kentucky","Michigan","Nevada","North Carolina","Tennessee","Utah","Wisconsin","Vermont","Arkansas","Colorado","Georgia","Idaho","Massachusetts","Iowa","Maine","Minnesota","Nebraska","New Hampshire","New Mexico","North Dakota","Ohio","Oregon","South Dakota","Texas","Washington"]

project_size_list = [0.2] #testing

df_complete_usa_table = pd.DataFrame()
df_state_results={}

#add cumulative installation number for available states to exisiting dataframe
df_states = df_state.join(commercial_installation_data['Cumulative Install'])

#adjust labor table with inflation before calculations
df_labor_table = df_labor_table[["Electricians - 10","Electricians - 50","Electricians - 90",
								 "Construction Laborers - 10","Construction Laborers - 50","Construction Laborers - 90",
								 "Operating Engineers and Other Construction Equipment Operators - 10","Operating Engineers and Other Construction Equipment Operators - 50","Operating Engineers and Other Construction Equipment Operators - 90"]] * labor_inflation


#FUNCTION TO COMPUTE EACH ITEM IN THE FINAL TABLE
def final_table(project_size, poi, state, num_modules, inv_cost):
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
	df_final.loc['Inverter Only',state] = inv_cost

	#Get Structural BOS into final table
	df_final.loc['Structural BOS',state], df_structural_bos = ft.get_structural_bos(df_module_db, df_ballasted_systems, df_utility,project_size, num_modules, df_inputs, df_state, state, hist_cost_index, year, watts, df_loading_inputs)

	#Get Electrical BOS into final table
	#Get Install Labor & Equipment into final table
	if df_inputs.loc['Battery EPC?', A]:
		df_final.loc['Electrical BOS',state], df_electrical_bos, pv_source_conductor_job_qty, df_pre_sur, df_pre_sur_bat = ft.get_electrical_bos_battery(df_utility,project_size, num_modules, df_inputs, df_state, state, hist_cost_index, year, df_module_db, df_bos_cost, df_com_storage)
		df_final.loc['Install Labor & Equipment',state], df_install, df_wage = ft.get_install_cost_battery(df_electrical_bos, df_structural_bos, df_utility, df_labor, df_labor_weight, df_state, state, inflation, project_size, df_inputs, df_labor_table, num_modules, pv_source_conductor_job_qty, df_pre_sur, watts, df_pre_sur_bat)
	else:
		df_final.loc['Electrical BOS',state], df_electrical_bos, pv_source_conductor_job_qty, df_pre_sur = ft.get_electrical_bos(df_utility,project_size, num_modules, df_inputs, df_state, state, hist_cost_index, year, df_module_db, df_bos_cost,dc_ac_ratio)
		df_final.loc['Install Labor & Equipment',state], df_install, df_wage = ft.get_install_cost(df_electrical_bos, df_structural_bos, df_utility, df_labor, df_labor_weight, df_state, state, inflation, project_size, df_inputs, df_labor_table, num_modules, pv_source_conductor_job_qty, df_pre_sur, watts)

	# testing
	# df_electrical_bos.to_csv('electrical_bos.csv')
	# df_install.to_csv('install_cost.csv')

	#Get EPC Overhead Cost into final table
	df_final.loc['Epc Overhead',state], oh_p_cost, df_install = ft.get_oh_p_cost(df_install, project_size, df_labor_weight, df_wage)

	#Get land acquisition cost into final table
	df_final.loc['Land Acquisition',state] = ft.get_land_acq_cost(df_inputs)

	#Get Permitting Cost into final table
	df_final.loc['Permitting & Interconnection', state], permitting_cost = ft.get_permitting_cost(state, df_state, df_inputs, project_size, poi, df_wage, df_labor_weight, df_utility, inflation)

	#   Get sales tax per watt into final table
	df_final.loc['Sale Tax (if any)',state], material_cost, equipment_cost = ft.get_sales_tax_cost(df_install, sales_tax, project_size, df_final.loc['Module',state], df_final.loc['Inverter Only',state])

	#Get Contingency Cost into final table
	df_final.loc['Contingency (4%)', state], pre_contigency_developer_oh_total = ft.get_contigency_cost(df_inputs, material_cost, equipment_cost, df_install, df_final.loc['Module',state], df_final.loc['Inverter Only',state], permitting_cost, project_size, df_final.loc['Sale Tax (if any)',state], oh_p_cost)

	#Get Contingency Cost into final table
	inflation_2015 = get_inflation(df_cpi, 2015)
	# df_final.loc['Developer Overhead', state] = ft.get_developer_overhead_cost(df_dev_costs, df_dev_business_model, df_ancillary_exp, state, df_state, project_size, inflation, inflation_2015)
	df_final.loc['Developer Overhead', state] = ft.get_developer_overhead_cost(pre_contigency_developer_oh_total,project_size)

	#Get Net Profit into final table
	df_final.loc['EPC/Developer Net Profit', state] = ft.get_net_profit(df_final, state, df_profit)

	#Get Total System Cost final table
	df_final.loc['Total System Cost', state] = ft.get_total_cost(df_final, state)

	return df_final

sensitivity_dict = {
	'Module Efficiency': {
		'location': df_inputs,
		'column': 'Value A',
		'sensitivity_value_list': [0.194, 0.206,0.199],
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
inverter_dict = {
	'String Inverter':{
		'Inverter $/Wac':float(df_inverter.loc['Inverter $/Wac','String Inverter']),
		'DC:AC ratio':float(df_inverter.loc['DC:AC ratio','String Inverter']),
		'Market Share':float(df_inverter.loc['Market Share','String Inverter']),
	},
	'DC-Opt':{
		'Inverter $/Wac':float(df_inverter.loc['Inverter $/Wac','DC-Opt']),
		'DC:AC ratio':float(df_inverter.loc['DC:AC ratio','DC-Opt']),
		'Market Share':float(df_inverter.loc['Market Share','DC-Opt']),
	},
	'Microinverter':{
		'Inverter $/Wac':float(df_inverter.loc['Inverter $/Wac','Microinverter']),
		'DC:AC ratio':float(df_inverter.loc['DC:AC ratio','Microinverter']),
		'Market Share':float(df_inverter.loc['Market Share','Microinverter']),
	},
}

for variable in sensitivity_dict.keys():
	if 'United States' in variable:
		loc_variable = 'United States'
	else:
		loc_variable = variable

	for sensitivity_value in sensitivity_dict[variable]['sensitivity_value_list']:

		original_variable_value = sensitivity_dict[variable]['location'].loc[loc_variable, sensitivity_dict[variable]['column']]
		sensitivity_dict[variable]['location'].loc[loc_variable, sensitivity_dict[variable]['column']] = sensitivity_value

		#LOOPING THROUGH FIXED TILT AND ONE AXIS, ALL PROJECT SIZES, AND ALL STATES TO CREATE THE FINAL TABLE FOR THE MAIN FIGURE
		df_all_sizes = pd.DataFrame()

		for project_size in project_size_list:

			num_modules, watts = num_of_modules(df_inputs, df_module_db, project_size)
			df_all_states = pd.DataFrame()


			for state in state_list:
				total_cost_inverter_share = 0
				for inverter_type in inverter_dict: #update inverter.csv sheet
					dc_ac_ratio = inverter_dict[inverter_type]['DC:AC ratio']
					poi = round(project_size / dc_ac_ratio, 2)
					inv_cost = inverter_dict[inverter_type]['Inverter $/Wac']/inverter_dict[inverter_type]['DC:AC ratio']
					df_final = final_table(num_modules*watts, poi, state, num_modules,inv_cost)
					total_cost = df_final.loc['Total System Cost', state]
					total_cost_inverter_share = total_cost * inverter_dict[inverter_type]['Market Share'] + total_cost_inverter_share
				print( loc_variable, ';', sensitivity_dict[variable]['column'], ';', project_size, ';', 'dummy', ';',(sensitivity_value), ';', total_cost_inverter_share)
		sensitivity_dict[variable]['location'].loc[loc_variable, sensitivity_dict[variable]['column']] = original_variable_value

		# 		# df_final.loc['Weight'] = df_state.loc[state,('State Weight','Commercial Weight')]
		# 		df_final.loc['Weight'] = df_states.loc[state, 'Cumulative Install']
		# 		df_all_states[state] = df_final[state]
		#
		# 	# df_all_states.loc['Weight'] = df_all_states.apply(lambda x:df_state.loc[x.name,('State Weight','Commercial Weight')], axis=0)
		# 	df_all_states.loc['Weight'] = df_all_states.apply( lambda x: df_states.loc[x.name, 'Cumulative Install'], axis=0 )
		# 	df_all_states = df_all_states.fillna(0)
		# 	df_state_results[str(project_size)+" MW"] = df_all_states
		#
		# 	weight_sum = df_all_states.loc['Weight'].sum()
		# 	df_us_avg = df_all_states.apply(lambda x: x.dot(df_all_states.loc['Weight'])/weight_sum, axis = 1)
		# 	df_us_avg = df_us_avg.drop('Weight', axis=0)
		# 	df_all_sizes[str(project_size) + ' MW']= df_us_avg
		#
		#
		# df_complete_usa_table = df_all_sizes


#CREATING THE TABLE FOR THE STATE AND PROJECT SIZE OF INTEREST
# if project_size_input in project_size_list:
# 	df_state_of_interest = df_state_results[str(project_size_input) + " MW"][state_input]
# 	df_state_of_interest.rename((state_input + " " + str(project_size_input) + " MW"), inplace=True)
# else:
# 	num_modules, watts = num_of_modules(df_inputs, df_module_db, project_size_input)
# 	df_state_of_interest = final_table(num_modules*watts, state_input, num_modules)
# 	df_state_of_interest.rename(columns={state_input:(state_input + " " + str(project_size_input) + " MW")}, inplace=True)

#EXPORTING THE US AVERAGE, STATE OF INTEREST, AND ALL OTHER STATE TABLES TO EXCEL
# if os.name=="nt":
# 	export_path = '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[0:-1]) + "\\results\\Commercial Rooftop PV Benchmark National Average.xlsx"
# else:
# 	export_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-1]) + "/results/Commercial Rooftop PV Benchmark National Average.xlsx"
# writer = pd.ExcelWriter(export_path, engine = 'xlsxwriter')
#
# df_complete_usa_table.to_excel(writer, sheet_name = 'US Weighted Average Results')
# # df_state_of_interest.to_excel(writer, sheet_name = 'State and Project of Interest')
# [df.to_excel(writer, sheet_name = key) for key, df in df_state_results.items()]
#
# writer.save()
# writer.close()

#CREATE AND EXPORT NATIONAL LEVEL FIGURE
# import seaborn as sns

# figure_states = ['Hawaii','Connecticut','New Jersey','Massachusetts','Florida','California','New York','Maryland','Colorado','Arizona','Texas']
# df_national_graph = pd.DataFrame()
# for state in figure_states:
#     df_national_graph = pd.concat([df_national_graph, df_state_results['0.2 MW'][state]], axis=1, sort = False)
    
# df_national_graph['USA'] = df_complete_usa_table['0.2 MW']    
# df_national_fig = df_national_graph.transpose().drop(['Total System Cost','Weight'], axis = 1)
# sns.set_style("whitegrid")
# colors = ["#e7e34e","#1ac9e6","#eb548c","#1de4bd","#3665ff","#af4bce","#c7f9ee","#c02323","#f7f4bf","#ef7e32","#d9dbde","#3f8fc1"]

# fig, ax1 = plt.subplots()
# df_national_fig[df_national_fig.columns].plot(kind='bar', stacked = True, figsize=[30,20], ax=ax1, color=colors,legend='reverse')

# total_height = 0
# for n,rect in enumerate(ax1.patches):
#     x = int(n/len(df_national_fig.columns))
#     m = n-x*len(df_national_fig.columns)
#     if x==0:
#         total_height=0
#     else:
#         total_height = 0
#         for i in range(n-len(df_national_fig.columns),-1,-len(df_national_fig.columns)):
#             total_height = total_height + ax1.patches[i].get_height()
#     ax1.text(rect.get_x() + rect.get_width()/2, total_height+rect.get_height()/2, "%.2f" % df_national_fig.iloc[m,x], ha='center', va='center', fontsize = 20)
# for n,state in enumerate(df_national_graph.columns):
#     ax1.text(ax1.patches[n].get_x()+ax1.patches[n].get_width()/2, df_national_graph.loc['Total System Cost',state]+0.05, "%.2f" % df_national_graph.loc['Total System Cost',state], ha='center', va='center', fontsize = 24)

# plt.xticks(rotation='horizontal', fontsize=20, fontweight='bold')
# handles, labels = ax1.get_legend_handles_labels()
# ax1.legend(reversed(handles), reversed(labels),fontsize = 22, bbox_to_anchor=(1.01, 1))
# plt.yticks(fontsize=20, fontweight='bold')
# plt.ylabel('$/W', fontsize=24, fontweight='bold')
# plt.title('Benchmark by Location: Commercial System Cost for 0.2 MW System',fontsize=30, fontweight='bold')
# plt.savefig(path + "\\results\\Benchmark by Location Figure.png", bbox_inches='tight')

print('done')
print("--- %s seconds ---" % (time.time() - start_time))