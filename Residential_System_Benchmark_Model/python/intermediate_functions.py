import pandas as pd
import numpy as np
import retrieve_datasets as rd

#call retreive_datset and store all dataframes
update_dataset = 0

if update_dataset == 1:
	dataset = rd.get_datasets()
else:
	dataset = rd.get_local_datasets()

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

def read_in_input_data_mac(path):
	#Pull in all the inputs from csv into a df
	df_inputs = pd.read_excel(path + '/input_data/inputs.xlsx', index_col=0)

	# df_cpi = pd.read_csv(path + '/input_data/consumer_price_index.csv', index_col=0)
	df_cpi = cpi_data

	df_state = pd.read_csv(path + '/input_data/state_data.csv', header=[0,1], skip_blank_lines=True, index_col=[0])

	df_inverter_ship = pd.read_excel(path + '/input_data/Inverter Shipments.xlsx', index_col=0)

	df_racking = pd.read_excel(path + '/input_data/Bill of Material Input.xlsx', sheet_name='Racking', index_col=0)

	df_wiring = pd.read_excel(path + '/input_data/Bill of Material Input.xlsx', sheet_name='Wiring', index_col=[0,1])

	df_soft = pd.read_excel(path + '/input_data/Soft Costs.xlsx', index_col=0)

	df_electrical_comp = pd.read_excel(path + '/input_data/Bill of Material Input.xlsx', sheet_name='Electrical Components', index_col=0)

	df_electrical_labor_hours = pd.read_excel(path + '/input_data/Labor Hours.xlsx', sheet_name='Electrical', index_col=0)

	df_hardware_labor_hours = pd.read_excel(path + '/input_data/Labor Hours.xlsx', sheet_name='Hardware', index_col=0)

	# df_labor_cost = pd.read_excel(path + '/input_data/BLS Labor Database.xlsx', index_col=0)
	df_labor_cost = labor_installation_data
	# df_labor_cost = df_labor_cost.drop( ['Guam', 'Virgin Islands'], axis=0 )

	df_wage_index = pd.read_excel(path + '/input_data/BLS Wage Index.xlsx', index_col=0)
	# df_wage_index = df_wage_index.drop(['Guam','Virgin Islands'],axis=0)

	df_integrator_market_share = pd.read_excel(path + '/input_data/Integrator Market Share.xlsx', index_col=0)

	df_single_inverter = pd.read_excel(path + '/input_data/Inverter Cost Kelsey.xlsx', sheet_name='Single Phase Inverter', index_col=0)
	df_dc_optimizer = pd.read_excel(path + '/input_data/Inverter Cost Kelsey.xlsx', sheet_name='DC Power Optimizer', index_col=0)
	df_microinverter = pd.read_excel(path + '/input_data/Inverter Cost Kelsey.xlsx', sheet_name='Microinverter', index_col=0)

	inputs_dict = {
	"Main Inputs": df_inputs,
	"Inflation": df_cpi,
	"State Data": df_state,
	"Inverter Shipments":df_inverter_ship,
	"Racking BoM": df_racking,
	"Wiring BoM": df_wiring,
	"Electrical BoM": df_electrical_comp,
	"Soft Costs": df_soft,
	"Electrical Labor Hours": df_electrical_labor_hours,
	"Hardware Labor Hours": df_hardware_labor_hours,
	"Labor Costs": df_labor_cost,
	"Wage Index": df_wage_index,
	"Integrator Market Share": df_integrator_market_share,
	"String Inverter Calculation": df_single_inverter,
	"DC Optimizer Calculation": df_dc_optimizer,
	"Microinverter Calculation":df_microinverter
	}

	return inputs_dict

def read_in_input_data_windows(path):
	#Pull in all the inputs from csv into a df
	df_inputs = pd.read_excel(path + '//input_data//inputs.xlsx', index_col=0)

	# df_cpi = pd.read_csv(path + '//input_data//consumer_price_index.csv', index_col=0)
	df_cpi = cpi_data

	df_state = pd.read_csv(path + '//input_data//state_data.csv', header=[0,1], skip_blank_lines=True, index_col=[0])

	df_inverter_ship = pd.read_excel(path + '//input_data//Inverter Shipments.xlsx', index_col=0)

	df_racking = pd.read_excel(path + '//input_data//Bill of Material Input.xlsx', sheet_name='Racking', index_col=0)

	df_wiring = pd.read_excel(path + '//input_data//Bill of Material Input.xlsx', sheet_name='Wiring', index_col=[0,1])

	df_soft = pd.read_excel(path + '//input_data//Soft Costs.xlsx', index_col=0)

	df_electrical_comp = pd.read_excel(path + '//input_data//Bill of Material Input.xlsx', sheet_name='Electrical Components', index_col=0)

	df_electrical_labor_hours = pd.read_excel(path + '//input_data//Labor Hours.xlsx', sheet_name='Electrical', index_col=0)

	df_hardware_labor_hours = pd.read_excel(path + '//input_data//Labor Hours.xlsx', sheet_name='Hardware', index_col=0)

	# df_labor_cost = pd.read_excel(path + '//input_data//BLS Labor Database.xlsx', index_col=0)
	df_labor_cost = labor_installation_data
	# df_labor_cost = df_labor_cost.drop( ['Guam', 'Virgin Islands'], axis=0 )

	df_wage_index = pd.read_excel(path + '//input_data//BLS Wage Index.xlsx', index_col=0)
	# df_wage_index = df_wage_index.drop(['Guam','Virgin Islands'],axis=0)

	df_integrator_market_share = pd.read_excel(path + '//input_data//Integrator Market Share.xlsx', index_col=0)

	df_single_inverter = pd.read_excel(path + '//input_data//Inverter Cost Kelsey.xlsx', sheet_name='Single Phase Inverter', index_col=0)
	df_dc_optimizer = pd.read_excel(path + '//input_data//Inverter Cost Kelsey.xlsx', sheet_name='DC Power Optimizer', index_col=0)
	df_microinverter = pd.read_excel(path + '//input_data//Inverter Cost Kelsey.xlsx', sheet_name='Microinverter', index_col=0)

	inputs_dict = {
	"Main Inputs": df_inputs,
	"Inflation": df_cpi,
	"State Data": df_state,
	"Inverter Shipments":df_inverter_ship,
	"Racking BoM": df_racking,
	"Wiring BoM": df_wiring,
	"Electrical BoM": df_electrical_comp,
	"Soft Costs": df_soft,
	"Electrical Labor Hours": df_electrical_labor_hours,
	"Hardware Labor Hours": df_hardware_labor_hours,
	"Labor Costs": df_labor_cost,
	"Wage Index": df_wage_index,
	"Integrator Market Share": df_integrator_market_share,
	"String Inverter Calculation": df_single_inverter,
	"DC Optimizer Calculation": df_dc_optimizer,
	"Microinverter Calculation":df_microinverter
	}

	return inputs_dict



def variable_prep_for_main(inputs_dict, states):
	#Get inflation value for soft cost adjustment
	quarter = inputs_dict['Main Inputs'].loc['Quarter','Value A']
	year = inputs_dict['Main Inputs'].loc['Year','Value A']
	quarter_year = quarter + ' ' + str(year)

	inflation = get_inflation(inputs_dict['Inflation'], year, 2019)  #,quarter, "Q1"
	inputs_dict['Soft Costs'].loc['Engineering Costs ($/Install)':'Total Other Overhead Costs (Excluding Sales, Marketing, and Customer Service)']*=inflation

	#Create empty df and dict for results
	df_states = pd.DataFrame(columns=states)
	midx = pd.MultiIndex(levels=[['String Inverter Option','Power Optimizer Option','Microinverter Option'],['Small Installer','Large Installer','Weighted Average']], codes=[[0,0,0,1,1,1,2,2,2],[0,1,2,0,1,2,0,1,2]])
	df_final_table = pd.DataFrame(columns=midx) 
	df_final_tables = {}

	dc_ac_ratio_string = inputs_dict['Main Inputs'].loc['DC to AC Ratio (String Inverter)', 'Value A']
	dc_ac_ratio_micro = inputs_dict['Main Inputs'].loc['DC to AC Ratio (Microinverter)', 'Value A']
	dc_ac_ratio_optimizer = inputs_dict['Main Inputs'].loc['DC to AC Ratio (DC Optimizer)', 'Value A']

	string_invert_wac = inputs_dict['Main Inputs'].loc['String Inverter Cost ($/Wac)', 'Value A']
	micro_wac = inputs_dict['Main Inputs'].loc['Microinverter Cost ($/Wac)', 'Value A']
	optimizer_wac = inputs_dict['Main Inputs'].loc['DC Optimizer Cost ($/Wac)', 'Value A']

	racking_discount = inputs_dict['Main Inputs'].loc['Discount on Racking','Value B']
	inputs_dict['Racking BoM']['Total Price'] = inputs_dict['Racking BoM']['Unit Price']*inputs_dict['Racking BoM']['Quantity']*(1-racking_discount)

	labor_burden = (inputs_dict['Main Inputs'].loc['Workers Comp Insurance','Value A']
					+inputs_dict['Main Inputs'].loc['Federal and State Unemployment Insurance','Value A']
					+inputs_dict['Main Inputs'].loc['Social Security Taxes (FICA)','Value A']
					+inputs_dict['Main Inputs'].loc["Builder's Risk Insurance",'Value A']
					+inputs_dict['Main Inputs'].loc["Public Liability",'Value A'])


	interconnection_non_labor_soft_cost_small = inputs_dict['Soft Costs'].loc['Interconnection Non-Labor Costs ($/Install)','Small Installers']
	interconnection_non_labor_soft_cost_large = inputs_dict['Soft Costs'].loc['Interconnection Non-Labor Costs ($/Install)','Large Installers']
	permitting_non_labor_soft_cost_small = inputs_dict['Soft Costs'].loc['Permitting Non-Labor Costs ($/Install)','Small Installers']
	permitting_non_labor_soft_cost_large = inputs_dict['Soft Costs'].loc['Permitting Non-Labor Costs ($/Install)','Large Installers']
	engineering_soft_cost_small = inputs_dict['Soft Costs'].loc['Engineering Costs ($/Install)','Small Installers']
	engineering_soft_cost_large = inputs_dict['Soft Costs'].loc['Engineering Costs ($/Install)','Large Installers']
	interconnection_labor_soft_cost_small = inputs_dict['Soft Costs'].loc['Interconnection Labor Costs ($/Install)','Small Installers']
	interconnection_labor_soft_cost_large = inputs_dict['Soft Costs'].loc['Interconnection Labor Costs ($/Install)','Large Installers']
	permitting_labor_soft_cost_small = inputs_dict['Soft Costs'].loc['Permitting Labor Costs ($/Install)','Small Installers']
	permitting_labor_soft_cost_large = inputs_dict['Soft Costs'].loc['Permitting Labor Costs ($/Install)','Large Installers']

	customer_acq_labor_soft_cost_small = inputs_dict['Soft Costs'].loc['Customer Acquisition Labor Costs ($/Install)','Small Installers']
	customer_acq_labor_soft_cost_large = inputs_dict['Soft Costs'].loc['Customer Acquisition Labor Costs ($/Install)','Large Installers']
	customer_acq_non_labor_soft_cost_small = inputs_dict['Soft Costs'].loc['Customer Acquisition Non-Labor Costs ($/Install)','Small Installers']
	customer_acq_non_labor_soft_cost_large = inputs_dict['Soft Costs'].loc['Customer Acquisition Non-Labor Costs ($/Install)','Large Installers']

	overhead_cost_rent_small = inputs_dict['Soft Costs'].loc['Total Overhead Costs (Rent)','Small Installers']
	overhead_cost_rent_large = inputs_dict['Soft Costs'].loc['Total Overhead Costs (Rent)','Large Installers']
	overhead_cost_labor_small = inputs_dict['Soft Costs'].loc['Total Overhead Costs (Labor)','Small Installers']
	overhead_cost_labor_large = inputs_dict['Soft Costs'].loc['Total Overhead Costs (Labor)','Large Installers']
	overhead_cost_other_small = inputs_dict['Soft Costs'].loc['Total Other Overhead Costs (Excluding Sales, Marketing, and Customer Service)','Small Installers']
	overhead_cost_other_large = inputs_dict['Soft Costs'].loc['Total Other Overhead Costs (Excluding Sales, Marketing, and Customer Service)','Large Installers']

	number_of_installs_small = inputs_dict['Soft Costs'].loc['Assumed number of annual installs','Small Installers']
	number_of_installs_large = inputs_dict['Soft Costs'].loc['Assumed number of annual installs','Large Installers']

	if inputs_dict['Main Inputs'].loc['Area Constrained', 'Value A']:
		avg_system_size_soft_costs_small = inputs_dict['Soft Costs'].loc['Average system size: original (kW)', 'Small Installers']*1000
		avg_system_size_soft_costs_large = inputs_dict['Soft Costs'].loc['Average system size: original (kW)', 'Large Installers']*1000
	else:
		avg_system_size_soft_costs_small = inputs_dict['Main Inputs'].loc['Desired Power (W)','Value A']
		avg_system_size_soft_costs_large = inputs_dict['Main Inputs'].loc['Desired Power (W)','Value A']

	market_share_small_installer = inputs_dict['Main Inputs'].loc['Market Share','Value A']
	market_share_large_installer = inputs_dict['Main Inputs'].loc['Market Share','Value B']

	pre_loop_variables = {
		"Quarter":quarter,
		"Year":year,
		"Fiscal Year":quarter_year,
		"State Results Table": df_states,
		"Final Table": df_final_table,
		"Compiled Result Table": df_final_tables,
		"String DC AC Ratio": dc_ac_ratio_string,
		"Microinverter DC AC Ratio": dc_ac_ratio_micro,
		"DC Optimizer DC AC Ratio": dc_ac_ratio_optimizer,
		"String Inverter $/Wac":string_invert_wac,
		"Microinverter $/Wac": micro_wac,
		"DC Optimizer $/Wac": optimizer_wac,
		"Racking Cost Table": inputs_dict['Racking BoM'],
		"Labor Burden":labor_burden,
		"interconnection_non_labor_soft_cost_small":interconnection_non_labor_soft_cost_small,
		"interconnection_non_labor_soft_cost_large":interconnection_non_labor_soft_cost_large,
		"permitting_non_labor_soft_cost_small":permitting_non_labor_soft_cost_small,
		"permitting_non_labor_soft_cost_large":permitting_non_labor_soft_cost_large,
		"engineering_soft_cost_small":engineering_soft_cost_small,
		"engineering_soft_cost_large":engineering_soft_cost_large,
		"interconnection_labor_soft_cost_small":interconnection_labor_soft_cost_small,
		"interconnection_labor_soft_cost_large":interconnection_labor_soft_cost_large,
		"permitting_labor_soft_cost_small":permitting_labor_soft_cost_small,
		"permitting_labor_soft_cost_large":permitting_labor_soft_cost_large,
		"customer_acq_labor_soft_cost_small":customer_acq_labor_soft_cost_small,
		"customer_acq_labor_soft_cost_large":customer_acq_labor_soft_cost_large,
		"customer_acq_non_labor_soft_cost_small":customer_acq_non_labor_soft_cost_small,
		"customer_acq_non_labor_soft_cost_large":customer_acq_non_labor_soft_cost_large,
		"overhead_cost_rent_small":overhead_cost_rent_small,
		"overhead_cost_rent_large":overhead_cost_rent_large,
		"overhead_cost_labor_small":overhead_cost_labor_small,
		"overhead_cost_labor_large":overhead_cost_labor_large,
		"overhead_cost_other_small":overhead_cost_other_small,
		"overhead_cost_other_large":overhead_cost_other_large,
		"number_of_installs_small":number_of_installs_small,
		"number_of_installs_large":number_of_installs_large,
		"market_share_small_installer":market_share_small_installer,
		"market_share_large_installer":market_share_large_installer,
		"avg_size_soft_cost_small_installer":avg_system_size_soft_costs_small,
		"avg_size_soft_cost_large_installer":avg_system_size_soft_costs_large
	}

	return pre_loop_variables

def get_inflation(df_cpi, year, reference_year): #quarter, reference_quarter
	dict_end_year={
	"Q1":'Mar',
	"Q2":'Jun',
	"Q3":'Sep',
	"Q4":'Dec'
	}

	# ref_year_row_avg = df_cpi.loc[reference_year,:dict_end_year[reference_quarter]].mean()
	# year_row_avg = df_cpi.loc[year,:dict_end_year[quarter]].mean()
	df_c = df_cpi
	df_c['Change'] = df_c['cpi'] / df_c.loc[2019, 'cpi']

	inflation = df_c.loc[year,'Change']
	# compound = (df_c.loc[year,'Avg']/df_c.loc[2000,'Avg'])**(1/(year-2000))
	# if pd.isnull(df_c.loc[year,'Change']):
	#     inflation = compound**(year-2013)
	# else:
	#     inflation = df_c.loc[year,'Change']
	
	return inflation

# def get_hist_cost_index(year, df_hist_cost):
# 	hist_cost_index = df_hist_cost.loc[year,'cost_index']/df_hist_cost.loc[2019,'cost_index']
# 	# print(hist_cost_index)
# 	return hist_cost_index

def single_inverter(power, df_single_inverter):
	inverter_power = np.around(power, decimals=-3)
	if power>13200:
		single_inverter_cost = df_single_inverter.loc['13200','Inverter Cost ($/Wdc)']
	else:
		single_inverter_cost = df_single_inverter.loc[inverter_power,'Inverter Cost ($/Wdc)']

	return single_inverter_cost

def dc_optimizer(power, df_dc_optimizer, dc_ac_ratio):
	ac_power = power/dc_ac_ratio
	
	a = df_dc_optimizer.loc['a','Polynomial Value']
	b = df_dc_optimizer.loc['b','Polynomial Value']
	c = df_dc_optimizer.loc['c','Polynomial Value']

	dc_cost = a*(ac_power*ac_power)+b*ac_power+c

	return dc_cost

def microinverter(system_size_dict, df_microinverter,dc_ac_ratio):

	power = system_size_dict['System Size']
	module_power = system_size_dict['Module Power']
	module_count = system_size_dict['Module Count']

	a = df_microinverter.loc['a','Coefficients']
	b = df_microinverter.loc['b','Coefficients']

	price_per_unit = a*(module_power/dc_ac_ratio)+b 
	microinverter_cost = (module_count*price_per_unit)/power #I don't remember what the 0.95 was, deleted

	return microinverter_cost

def power(df_inputs,desired_power_override=0):
	roofspace= df_inputs.loc['Available Roof Space (m^2)', 'Value B']
	active_area = roofspace*df_inputs.loc['Module Packing Efficiency', 'Value B']
	module_efficiency = df_inputs.loc['Module Efficiency', 'Value A']
	module_area = df_inputs.loc['Module Length (m)', 'Value A']*df_inputs.loc['Module Width (m)', 'Value A']
	module_power = 1000*module_efficiency*module_area
	#module_count = 22
	#power = module_count*module_power
	# if np.isnan(df_inputs.loc['Module Count', 'Value A']):
	# 	# print('popo')
	# 	if df_inputs.loc['Area Constrained', 'Value A']:
	# 		module_count = np.trunc(active_area/module_area)
	# 		# module_count = df_inputs.loc['Module Count', 'Value A']
	# 		if df_inputs.loc['Power Limited', 'Value A']:
	# 			max_power_ac = df_inputs.loc['Max System Size (AC W)', 'Value A']
	# 			if (module_count*module_power)<max_power_ac:
	# 				power = module_count*module_power
	# 			else:
	# 				power = max_power_ac
	# 		else:
	# 			power = module_count*module_power
	# 	else:
	# 		if desired_power_override == 0:
	# 			desired_power = df_inputs.loc['Desired Power (W)', 'Value A']
	# 		else:
	# 			desired_power = desired_power_override
	# 		module_count = np.ceil(desired_power/module_power)
	# 		if df_inputs.loc['Power Limited', 'Value A']:
	# 			max_power_ac = df_inputs.loc['Max System Size (AC W)', 'Value A']
	# 			if (module_count*module_power)<max_power_ac:
	# 				power = module_count*module_power
	# 			else:
	# 				power = max_power_ac
	# 		else:
	# 			power = module_count*module_power
	# else:
	# 	# print('pepe')
	# 	module_count = df_inputs.loc['Module Count', 'Value A']
	# 	power = module_count*module_power
	if df_inputs.loc['Area Constrained', 'Value A']:
		module_count = df_inputs.loc['Module Count', 'Value A']
		# module_count = np.trunc(active_area/module_area)
		power = module_count*module_power
	else:
		power = df_inputs.loc['Desired Power (W)', 'Value A']
		module_count = np.trunc(power/module_power)
		active_area = module_count*module_area
		roofspace = active_area/df_inputs.loc['Module Packing Efficiency', 'Value B']
	# print('System Size', power/1000)

	system_size_dict ={
	"System Size":power,
	"Module Count":module_count,
	"Module Power":module_power,
	"Active Area":active_area,
	"Roofspace":roofspace,
	"Module Efficiency":module_efficiency
	}

	# print("Module Efficiency ",module_efficiency)
	return system_size_dict

def benchmark_power(df_inputs):
	roofspace= df_inputs.loc['Available Roof Space (m^2)', 'Value B']
	active_area = roofspace*df_inputs.loc['Module Packing Efficiency', 'Value B']
	module_efficiency = df_inputs.loc['Module Efficiency', 'Value A']
	module_area = df_inputs.loc['Module Length (m)', 'Value A']*df_inputs.loc['Module Width (m)', 'Value A']
	module_power = 1000*module_efficiency*module_area
	module_count = df_inputs.loc['Module Count', 'Value A']
	power = module_count*module_power

	system_size_dict ={
	"System Size":power,
	"Module Count":module_count,
	"Module Power":module_power,
	"Active Area":active_area,
	"Roofspace":roofspace,
	"Module Efficiency":module_efficiency
	}
	
	return system_size_dict

def installer_vs_integrator(inputs_dict, state):

	df_inputs = inputs_dict['Main Inputs']
	df_state = inputs_dict['State Data']
	df_cumulative_installs = df_state.join(residential_installation_data['Cumulative Install'])
	df_wage_index=inputs_dict['Wage Index']

	df_versus = pd.DataFrame(index = ['Residential PV, small installers','Residential PV, national integrators'])
	if(state=='United States'):
		# codb = np.dot(df_state[('State Weight','Residential Cost of Doing Business Index')], df_state['Cumulative Install'])/df_state['Cumulative Install'].sum()/100
		codb = 1
		# sales_tax =np.dot(df_state[('Sales Tax','Residential')], df_cumulative_installs['Cumulative Install'])/df_cumulative_installs['Cumulative Install'].sum()
		# sales_tax = ((df_state[('Sales Tax', 'Residential')] * df_cumulative_installs['Cumulative Install']).sum()) / df_cumulative_installs['Cumulative Install'].sum()
		sales_tax = df_state.loc[state,('Sales Tax','Residential')]

	else:
		codb = df_wage_index.loc[state,'Wage Index']
		sales_tax = df_state.loc[state,('Sales Tax','Residential')]
		
	module_price= df_inputs.loc['Module Price ($/W)', 'Value A']
	supply_chain = df_inputs.loc['Supply Chain Costs', 'Value B']*codb 
	# supply_chain_instal = df_inputs.loc['Supply Chain Costs - Module', 'Value A'] + supply_chain
	# supply_chain_integ = df_inputs.loc['Supply Chain Costs - Module', 'Value B'] + supply_chain
	
	df_versus['Module ex-factor gate price (or spot price)'] = module_price
	
	# df_versus.loc['Residential PV, small installers','Module-related supply-chain costs'] = module_price*supply_chain_instal
	# df_versus.loc['Residential PV, national integrators','Module-related supply-chain costs'] = module_price*supply_chain_integ
	
	historical_inventory_instal = df_inputs.loc['Supply Chain Costs - Module Price Premium due to historical inventory', 'Value A']
	historical_inventory_integ = df_inputs.loc['Supply Chain Costs - Module Price Premium due to historical inventory', 'Value B']
	small_scale_procurement_instal = df_inputs.loc['Supply Chain Costs - Module due to small-scall procurement', 'Value A']
	ship_handling_instal = df_inputs.loc['Supply Chain Costs - Module shipping and handling', 'Value A']*codb
	ship_handling_integ = df_inputs.loc['Supply Chain Costs - Module shipping and handling', 'Value B']*codb

	df_versus.loc['Residential PV, small installers','Module Premium due to Historical Inventory'] = historical_inventory_instal*module_price
	df_versus.loc['Residential PV, national integrators','Module Premium due to Historical Inventory'] = historical_inventory_integ*module_price

	df_versus.loc['Residential PV, small installers','Supply chain cost (module price premium due to small-scale procurement)'] = small_scale_procurement_instal*(df_versus.loc['Residential PV, small installers','Module Premium due to Historical Inventory']+module_price)
	df_versus.loc['Residential PV, national integrators','Supply chain cost (module price premium due to small-scale procurement)'] = 0

	df_versus.loc['Residential PV, small installers','Supply chain cost (shipping and handling)'] = ship_handling_instal*(df_versus.loc['Residential PV, small installers','Module Premium due to Historical Inventory']+module_price)
	df_versus.loc['Residential PV, national integrators','Supply chain cost (shipping and handling)'] = ship_handling_integ*(df_versus.loc['Residential PV, national integrators','Module Premium due to Historical Inventory']+module_price)

	df_versus['Module-related sales tax'] = sales_tax*(df_versus['Module ex-factor gate price (or spot price)']+df_versus['Module Premium due to Historical Inventory']+df_versus['Supply chain cost (module price premium due to small-scale procurement)']+df_versus['Supply chain cost (shipping and handling)'])
   
	supply_chain_instal = historical_inventory_instal+small_scale_procurement_instal+ship_handling_instal
	supply_chain_integ = historical_inventory_integ+ship_handling_integ
	
	# df_versus = df_versus.drop('Module-related supply-chain costs', axis=1)
	# fig, ax1 = plt.subplots()
	# df_versus.plot(kind='bar', stacked = True, figsize=[30,20], ax=ax1,legend='reverse')
	# plt.xticks(rotation='horizontal', fontsize=20, fontweight='bold')
	# handles, labels = ax1.get_legend_handles_labels()
	# ax1.legend(reversed(handles), reversed(labels),fontsize = 22, bbox_to_anchor=(1.01, 1))
	# plt.yticks(fontsize=20, fontweight='bold')
	# plt.ylabel('$/W', fontsize=24, fontweight='bold')

	module_relate_costs ={
		"Module Price":module_price,
		"Module Small Installer Supply Chain Costs":supply_chain_instal,
		"Module Large Installer Supply Chain Costs":supply_chain_integ,
		"Supply Chain Costs":supply_chain,
		"Module Costs Table": df_versus
	}

	return sales_tax, codb, module_relate_costs

def inverter_ship(df_inverter_ship):
	df_line = pd.DataFrame(columns=df_inverter_ship.columns)
	df_line.loc['Enphase ASP ($ per AC)'] = df_inverter_ship.loc['Enphase ASP ($ per AC)']
	df_line.loc['SolarEdge ASP ($ per AC)'] = df_inverter_ship.loc['SolarEdge Sales ($million)']/df_inverter_ship.loc['SolarEdge Shipments (MW AC)']
	
	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	df_line = df_line.transpose() 
	df_inverter_ship = df_inverter_ship.transpose()    
	df_inverter_ship.plot(y=['Enphase Shipments (MW AC)', 'SolarEdge Shipments (MW AC)'], kind='bar', stacked = True, figsize=[30,20], ax=ax2,legend='reverse')
	df_line.plot(kind='line', figsize=[30,20], ax=ax1)
	plt.xticks(rotation='horizontal', fontsize=20, fontweight='bold')
	ax1.legend(fontsize = 22, bbox_to_anchor=(1.01, 1))
	handles, labels = ax2.get_legend_handles_labels()
	ax2.legend(reversed(handles), reversed(labels),fontsize = 22, bbox_to_anchor=(1.01, 1))
	plt.yticks(fontsize=20, fontweight='bold')
	ax1.set_ylabel('$/W', fontsize=24, fontweight='bold')
	ax2.set_ylabel('Shipments MWac', fontsize=24, fontweight='bold')
	return df_line, fig, df_inverter_ship

def electrical_bos(inputs_dict, inverter_type, system_size_dict, dc_ac_ratio):
	
	df_wiring = inputs_dict['Wiring BoM']
	df_electrical_comp = inputs_dict['Electrical BoM']
	df_inputs = inputs_dict['Main Inputs']

	module_count = system_size_dict['Module Count']
	active_area = system_size_dict['Active Area']
	roofspace = system_size_dict['Roofspace']
	power = system_size_dict['System Size']

	df_electrical = df_electrical_comp.copy()
	string_size=df_inputs.loc['String Size','Value A']
	number_of_module_strings = np.ceil(module_count/string_size)

	# print(number_of_module_strings)

	if inverter_type == "String Inverter":
		df_wiring.loc[('String Inverter','Home Run Female MC Connectors'),'Quantity'] = number_of_module_strings
		df_wiring.loc[('String Inverter','Home Run Male MC Connectors'),'Quantity'] = number_of_module_strings
		df_wiring.loc[('String Inverter','Home Run Wiring (ft)'),'Quantity'] = (2*number_of_module_strings+1)*df_wiring.loc[('String Inverter','Home Run Conduit (ft)'),'Quantity']
		df_wiring.loc[('String Inverter','Rapid Shutdown Box and Controller'),'Quantity'] = 1
		module_width_ft = (df_inputs.loc['Module Spacing (in)','Value A']+df_inputs.loc['Module Width (m)', 'Value A']/0.0254)/12
		df_wiring.loc[('String Inverter','Row to Combiner Wiring (ft)'),'Quantity'] = number_of_module_strings*string_size*1.2*module_width_ft
		wiring_total = (df_wiring.loc['String Inverter','Cost']*df_wiring.loc['String Inverter','Quantity']).sum()
		electrical_bos = (df_electrical['Unit Price'].sum()+wiring_total)/power

		# print('String Size', string_size, '\n',
		# 	  'No. of. strings', number_of_module_strings, '\n',
		# 	  'Home Run Female MC Connectors', df_wiring.loc[('String Inverter','Home Run Female MC Connectors'),'Quantity'], '\n',
		# 	  'Home Run Male MC Connectors', df_wiring.loc[('String Inverter','Home Run Male MC Connectors'),'Quantity'],'\n',
		# 	  'Home Run Wiring (ft)', df_wiring.loc[('String Inverter','Home Run Wiring (ft)'),'Quantity'],'\n',
		# 	  'Rapid Shutdown Box and Controller', df_wiring.loc[('String Inverter','Rapid Shutdown Box and Controller'),'Quantity'],'\n',
		# 	  'Row to Combiner Wiring (ft)', df_wiring.loc[('String Inverter','Row to Combiner Wiring (ft)'),'Quantity'],'\n',
		# 	  )
		
	elif inverter_type == "Microinverter":
		df_wiring.loc[('Microinverter','Enphase AC Engage/Trunk Cabling - Portrait, 240VAC, 12 AWG'),'Quantity'] = module_count+(number_of_module_strings-1)
		df_wiring.loc[('Microinverter','Enphase Connector Clip'),'Quantity'] = (module_count+(number_of_module_strings-1))*3
		df_wiring.loc[('Microinverter','Enphase Frame Mount'),'Quantity'] = module_count
		wiring_total = (df_wiring.loc['Microinverter','Cost']*df_wiring.loc['Microinverter','Quantity']).sum()
		df_electrical.loc['AC Disconnect','Unit Price'] = 0
		df_electrical.loc['String Inverter System Monitor','Unit Price'] = 0
		electrical_bos = (df_electrical_comp['Unit Price'].sum()+wiring_total)/power
	else:
		# cellular_kit_and_rapid_shutdown_cable = (df_wiring.loc['DC Optimizer','Cost']*df_wiring.loc['DC Optimizer','Quantity']).sum()
		cellular_kit = df_wiring.loc[('DC Optimizer','SolarEdge Cellular Kit'),'Cost'] * df_wiring.loc[('DC Optimizer','SolarEdge Cellular Kit'),'Quantity']
		rapid_shutdown_cable = df_wiring.loc[('DC Optimizer','One Rapid Shutdown cable in each inverter'),'Cost'] * df_wiring.loc[('DC Optimizer','One Rapid Shutdown cable in each inverter'),'Quantity']
		df_wiring.loc[('DC Optimizer','SolarEdge DC Optimizer'),'Cost'] = 0.07/dc_ac_ratio
		df_wiring.loc[('DC Optimizer','SolarEdge DC Optimizer'),'Quantity'] = power
		
		df_wiring.loc[('String Inverter','Home Run Female MC Connectors'),'Quantity'] = number_of_module_strings
		df_wiring.loc[('String Inverter','Home Run Male MC Connectors'),'Quantity'] = number_of_module_strings
		df_wiring.loc[('String Inverter','Home Run Wiring (ft)'),'Quantity'] = 5*df_wiring.loc[('String Inverter','Home Run Conduit (ft)'),'Quantity']
		module_width_ft = (df_inputs.loc['Module Spacing (in)','Value A']+df_inputs.loc['Module Width (m)', 'Value A']/0.0254)/12
		df_wiring.loc[('String Inverter','Row to Combiner Wiring (ft)'),'Quantity'] = number_of_module_strings*string_size*module_width_ft*1.2
		df_wiring.loc[('String Inverter','Rapid Shutdown Box and Controller'),'Quantity'] = 0                    #
		wiring_total= (df_wiring.loc['String Inverter','Cost']*df_wiring.loc['String Inverter','Quantity']).sum()-np.nan_to_num(df_wiring.loc[('String Inverter','Rapid Shutdown Box and Controller'),'Cost'])+ (df_wiring.loc['DC Optimizer','Cost']*df_wiring.loc['DC Optimizer','Quantity']).sum() + cellular_kit + rapid_shutdown_cable
		
		df_electrical.loc['String Inverter System Monitor','Unit Price'] = 0                
		electrical_bos = (df_electrical['Unit Price'].sum()+wiring_total)/power

		# print(cellular_kit, rapid_shutdown_cable)

	#print(inverter_type, wiring_total)

	# print("strings #", number_of_module_strings)
	# print('DC Opt Qty', df_wiring.loc[('DC Optimizer','SolarEdge DC Optimizer'),'Quantity'])
	# print('DC Opt $/w', df_wiring.loc[('DC Optimizer','SolarEdge DC Optimizer'),'Cost'])


	inputs_dict['Wiring BoM'] = df_wiring

	return electrical_bos, inputs_dict

def supply_chain_costs(df_final_table, df_inputs, module_relate_costs):

	module_price = module_relate_costs['Module Price']
	supply_chain_instal = module_relate_costs['Module Small Installer Supply Chain Costs']
	supply_chain_integ = module_relate_costs['Module Large Installer Supply Chain Costs'] 
	supply_chain = module_relate_costs['Supply Chain Costs']

	# print(supply_chain_instal, supply_chain_integ)

	inverter_sc_installer = df_inputs.loc['Supply Chain Costs - Inverter','Value A']+supply_chain
	inverter_sc_integrator = df_inputs.loc['Supply Chain Costs - Inverter','Value B']+supply_chain

	string_installer = supply_chain_instal*module_price + df_final_table.loc['Inverter',('String Inverter Option','Small Installer')]*inverter_sc_installer+supply_chain*(df_final_table.loc['Structual BoS',('String Inverter Option','Small Installer')]+df_final_table.loc['Electrical BoS',('String Inverter Option','Small Installer')])
	string_integrator = supply_chain_integ*module_price + df_final_table.loc['Inverter',('String Inverter Option','Large Installer')]*inverter_sc_integrator+supply_chain*(df_final_table.loc['Structual BoS',('String Inverter Option','Large Installer')]+df_final_table.loc['Electrical BoS',('String Inverter Option','Large Installer')])
	
	dc_installer = supply_chain_instal*module_price + df_final_table.loc['Inverter',('Power Optimizer Option','Small Installer')]*inverter_sc_installer+supply_chain*(df_final_table.loc['Structual BoS',('Power Optimizer Option','Small Installer')]+df_final_table.loc['Electrical BoS',('Power Optimizer Option','Small Installer')])
	dc_integrator = supply_chain_integ*module_price + df_final_table.loc['Inverter',('Power Optimizer Option','Large Installer')]*inverter_sc_integrator+supply_chain*(df_final_table.loc['Structual BoS',('Power Optimizer Option','Large Installer')]+df_final_table.loc['Electrical BoS',('Power Optimizer Option','Large Installer')])
	
	micro_installer = supply_chain_instal*module_price + df_final_table.loc['Inverter',('Microinverter Option','Small Installer')]*inverter_sc_installer+supply_chain*(df_final_table.loc['Structual BoS',('Microinverter Option','Small Installer')]+df_final_table.loc['Electrical BoS',('Microinverter Option','Small Installer')])
	micro_integrator = supply_chain_integ*module_price + df_final_table.loc['Inverter',('Microinverter Option','Large Installer')]*inverter_sc_integrator+supply_chain*(df_final_table.loc['Structual BoS',('Microinverter Option','Large Installer')]+df_final_table.loc['Electrical BoS',('Microinverter Option','Large Installer')])

	print("Module SC",supply_chain_instal)
	print("Inverter SC",inverter_sc_installer)
	print("BOS SC",supply_chain)

	supply_chain_costs_dict = {
		'String Inverter Small Installer': string_installer,
		'String Inverter Large Installer':string_integrator,
		'DC Optimizer Small Installer':dc_installer,
		'DC Optimizer Large Installer':dc_integrator,
		'Microinverter Small Installer':micro_installer,
		'Microinverter Large Installer':micro_integrator
	}

	return supply_chain_costs_dict



def installation(inputs_dict, inverter_type, state, system_size_dict, labor_burden):

	df_electrical_hours = inputs_dict['Electrical Labor Hours'].copy()
	df_hardware_hours =inputs_dict['Hardware Labor Hours'].copy()
	df_wiring = inputs_dict['Wiring BoM']

	df_cpi = inputs_dict['Inflation']
	year = inputs_dict['Main Inputs'].loc['Year', 'Value A']

	labor_inflation = df_cpi.loc[year, 'cpi'] / df_cpi.loc[labor_data_year, 'cpi']

	df_labor_cost = labor_installation_data[["Electricians - 10", "Electricians - 50", "Electricians - 90",
											 "Construction Laborers - 10", "Construction Laborers - 50",
											 "Construction Laborers - 90",
											 "Operating Engineers and Other Construction Equipment Operators - 10",
											 "Operating Engineers and Other Construction Equipment Operators - 50",
											 "Operating Engineers and Other Construction Equipment Operators - 90"]] * labor_inflation

	# df_labor_cost = df_labor_cost.drop( ['Guam', 'Virgin Islands'], axis=0 )

	df_state = inputs_dict['State Data']
	df_inputs = inputs_dict['Main Inputs']
	module_count = system_size_dict['Module Count']
	power = system_size_dict['System Size']

	if inverter_type == "Microinverter":
		df_electrical_hours.loc['Moderate conduit run','Hours']=0
		df_electrical_hours.loc['Short-wiring','Hours']=0.02
		df_electrical_hours.loc['Long-wiring','Hours']=0.02
	
	elif inverter_type == "String Inverter":
		
		df_electrical_hours.loc['Short-wiring','Hours'] = df_electrical_hours.loc['Short-wiring','Hours']*(30+df_wiring.loc[('String Inverter','Home Run Wiring (ft)'),'Quantity'])
	
	else:
		df_electrical_hours.loc['Short-wiring','Hours'] = df_electrical_hours.loc['Short-wiring','Hours']*(df_wiring.loc[('String Inverter','Home Run Wiring (ft)'),'Quantity'])

	df_electrical_hours.loc['Long-wiring','Hours']= df_electrical_hours.loc['Long-wiring','Hours']*df_wiring.loc[('String Inverter','Row to Combiner Wiring (ft)'),'Quantity']
	df_hardware_hours.loc['Module install','Hours']=df_hardware_hours.loc['Module install','Hours']*module_count
	df_hardware_hours.loc['Racking install','Hours']=df_hardware_hours.loc['Racking install','Hours']*module_count

	df_cumulative_installs = df_state.join( residential_installation_data['Cumulative Install'] )

	electrical_labor_cost = inputs_dict['Labor Costs'].loc['United States', 'Electricians - 50']*labor_inflation*(1+labor_burden)
	hardware_labor_cost = inputs_dict['Labor Costs'].loc['United States', 'Construction Laborers - 50']*labor_inflation*(1+labor_burden)



	installation_cost = (electrical_labor_cost*df_electrical_hours['Hours'].sum()+hardware_labor_cost*df_hardware_hours['Hours'].sum())*df_inputs.loc['Labor Time Factor','Value A']/power
	print(inverter_type, "Electrical Hours",df_electrical_hours['Hours'].sum(), "Racking Hours",df_hardware_hours['Hours'].sum())
	
	return installation_cost

def permitting_inspection_interconnection(df_final_table, pre_loop_variables, codb, power):
	
	interconnection_non_labor_soft_cost_small=pre_loop_variables["interconnection_non_labor_soft_cost_small"]
	interconnection_non_labor_soft_cost_large=pre_loop_variables["interconnection_non_labor_soft_cost_large"]
	permitting_non_labor_soft_cost_small=pre_loop_variables["permitting_non_labor_soft_cost_small"]
	permitting_non_labor_soft_cost_large=pre_loop_variables["permitting_non_labor_soft_cost_large"]
	engineering_soft_cost_small=pre_loop_variables["engineering_soft_cost_small"]
	engineering_soft_cost_large=pre_loop_variables["engineering_soft_cost_large"]
	interconnection_labor_soft_cost_small=pre_loop_variables["interconnection_labor_soft_cost_small"]
	interconnection_labor_soft_cost_large=pre_loop_variables["interconnection_labor_soft_cost_large"]
	permitting_labor_soft_cost_small=pre_loop_variables["permitting_labor_soft_cost_small"]
	permitting_labor_soft_cost_large=pre_loop_variables["permitting_labor_soft_cost_large"]
	avg_size_soft_cost_small_installer = pre_loop_variables["avg_size_soft_cost_small_installer"]
	avg_size_soft_cost_large_installer = pre_loop_variables["avg_size_soft_cost_large_installer"]

	# print()
	
	
	market_share_small_installer=pre_loop_variables["market_share_small_installer"]
	market_share_large_installer=pre_loop_variables["market_share_large_installer"]

	df_final_table.loc['Permitting, Inspection, Interconnection',('String Inverter Option', 'Small Installer')] = (interconnection_non_labor_soft_cost_small+permitting_non_labor_soft_cost_small
		+(engineering_soft_cost_small+permitting_labor_soft_cost_small+interconnection_labor_soft_cost_small)*codb)/avg_size_soft_cost_small_installer
	df_final_table.loc['Permitting, Inspection, Interconnection',('Power Optimizer Option', 'Small Installer')] = (interconnection_non_labor_soft_cost_small+permitting_non_labor_soft_cost_small
		+(engineering_soft_cost_small+permitting_labor_soft_cost_small+interconnection_labor_soft_cost_small)*codb)/avg_size_soft_cost_small_installer
	df_final_table.loc['Permitting, Inspection, Interconnection',('Microinverter Option', 'Small Installer')] = (interconnection_non_labor_soft_cost_small+permitting_non_labor_soft_cost_small
		+(engineering_soft_cost_small+permitting_labor_soft_cost_small+interconnection_labor_soft_cost_small)*codb)/avg_size_soft_cost_small_installer
	df_final_table.loc['Permitting, Inspection, Interconnection',('String Inverter Option', 'Large Installer')] = (interconnection_non_labor_soft_cost_large+permitting_non_labor_soft_cost_large
		+(engineering_soft_cost_large+permitting_labor_soft_cost_large+interconnection_labor_soft_cost_large)*codb)/avg_size_soft_cost_large_installer
	df_final_table.loc['Permitting, Inspection, Interconnection',('Power Optimizer Option', 'Large Installer')] = (interconnection_non_labor_soft_cost_large+permitting_non_labor_soft_cost_large
		+(engineering_soft_cost_large+permitting_labor_soft_cost_large+interconnection_labor_soft_cost_large)*codb)/avg_size_soft_cost_large_installer
	df_final_table.loc['Permitting, Inspection, Interconnection',('Microinverter Option', 'Large Installer')] = (interconnection_non_labor_soft_cost_large+permitting_non_labor_soft_cost_large
		+(engineering_soft_cost_large+permitting_labor_soft_cost_large+interconnection_labor_soft_cost_large)*codb)/avg_size_soft_cost_large_installer


	return df_final_table

def customer_acquisition(df_final_table, pre_loop_variables, codb, power):

	customer_acq_labor_soft_cost_small=pre_loop_variables["customer_acq_labor_soft_cost_small"]
	customer_acq_labor_soft_cost_large=pre_loop_variables["customer_acq_labor_soft_cost_large"]
	customer_acq_non_labor_soft_cost_small=pre_loop_variables["customer_acq_non_labor_soft_cost_small"]
	customer_acq_non_labor_soft_cost_large=pre_loop_variables["customer_acq_non_labor_soft_cost_large"]
	avg_size_soft_cost_small_installer = pre_loop_variables["avg_size_soft_cost_small_installer"]
	avg_size_soft_cost_large_installer = pre_loop_variables["avg_size_soft_cost_large_installer"]

	df_final_table.loc['Sales & Marketing (Customer acquisition)',('String Inverter Option', 'Small Installer')] = (customer_acq_labor_soft_cost_small*codb + customer_acq_non_labor_soft_cost_small)/avg_size_soft_cost_small_installer
	df_final_table.loc['Sales & Marketing (Customer acquisition)',('Power Optimizer Option', 'Small Installer')] = (customer_acq_labor_soft_cost_small*codb + customer_acq_non_labor_soft_cost_small)/avg_size_soft_cost_small_installer
	df_final_table.loc['Sales & Marketing (Customer acquisition)',('Microinverter Option', 'Small Installer')] = (customer_acq_labor_soft_cost_small*codb + customer_acq_non_labor_soft_cost_small)/avg_size_soft_cost_small_installer
	df_final_table.loc['Sales & Marketing (Customer acquisition)',('String Inverter Option', 'Large Installer')] = (customer_acq_labor_soft_cost_large*codb + customer_acq_non_labor_soft_cost_large)/avg_size_soft_cost_large_installer
	df_final_table.loc['Sales & Marketing (Customer acquisition)',('Power Optimizer Option', 'Large Installer')] = (customer_acq_labor_soft_cost_large*codb +customer_acq_non_labor_soft_cost_large)/avg_size_soft_cost_large_installer
	df_final_table.loc['Sales & Marketing (Customer acquisition)',('Microinverter Option', 'Large Installer')] = (customer_acq_labor_soft_cost_large*codb + customer_acq_non_labor_soft_cost_large)/avg_size_soft_cost_large_installer

	#print(customer_acq_labor_soft_cost_small, customer_acq_non_labor_soft_cost_small)
	#print(customer_acq_labor_soft_cost_large, customer_acq_non_labor_soft_cost_large)
	return df_final_table

def overhead(df_final_table, pre_loop_variables, codb, power, df_soft):

	overhead_cost_rent_small=pre_loop_variables["overhead_cost_rent_small"]
	overhead_cost_rent_large=pre_loop_variables["overhead_cost_rent_large"]
	overhead_cost_labor_small=pre_loop_variables["overhead_cost_labor_small"]
	overhead_cost_labor_large=pre_loop_variables["overhead_cost_labor_large"]
	overhead_cost_other_small=pre_loop_variables["overhead_cost_other_small"]
	overhead_cost_other_large=pre_loop_variables["overhead_cost_other_large"]
	number_of_installs_small=pre_loop_variables["number_of_installs_small"]
	number_of_installs_large=pre_loop_variables["number_of_installs_large"]
	avg_size_soft_cost_small_installer = pre_loop_variables["avg_size_soft_cost_small_installer"]
	avg_size_soft_cost_large_installer = pre_loop_variables["avg_size_soft_cost_large_installer"]

	df_final_table.loc['Overhead (General & Admin.)',('String Inverter Option', 'Small Installer')] = ((overhead_cost_rent_small+overhead_cost_labor_small)*codb+overhead_cost_other_small)/number_of_installs_small/avg_size_soft_cost_small_installer
	df_final_table.loc['Overhead (General & Admin.)',('Power Optimizer Option', 'Small Installer')] = ((overhead_cost_rent_small+overhead_cost_labor_small)*codb+overhead_cost_other_small)/number_of_installs_small/avg_size_soft_cost_small_installer
	df_final_table.loc['Overhead (General & Admin.)',('Microinverter Option', 'Small Installer')] = ((overhead_cost_rent_small+overhead_cost_labor_small)*codb+overhead_cost_other_small)/number_of_installs_small/avg_size_soft_cost_small_installer
	df_final_table.loc['Overhead (General & Admin.)',('String Inverter Option', 'Large Installer')] = ((overhead_cost_rent_large+overhead_cost_labor_large)*codb+overhead_cost_other_large)/number_of_installs_large/avg_size_soft_cost_large_installer
	df_final_table.loc['Overhead (General & Admin.)',('Power Optimizer Option', 'Large Installer')] = ((overhead_cost_rent_large+overhead_cost_labor_large)*codb+overhead_cost_other_large)/number_of_installs_large/avg_size_soft_cost_large_installer
	df_final_table.loc['Overhead (General & Admin.)',('Microinverter Option', 'Large Installer')] = ((overhead_cost_rent_large+overhead_cost_labor_large)*codb+overhead_cost_other_large)/number_of_installs_large/avg_size_soft_cost_large_installer
	
	return df_final_table    
