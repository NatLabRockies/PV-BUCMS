import time as clock
start_time=clock.time()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import ntpath
import intermediate_functions as ifunc

path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-1])
path.replace(os.sep,ntpath.sep)

benchmark_states = ['United States']
# benchmark_states = ['United States','Massachusetts','New Jersey','California','Connecticut','New York','Maryland','Nevada','Arizona','Texas','Colorado','Florida','Hawaii']


#Pull in input data
if os.name=="nt":
	path = '//'.join(os.path.dirname(os.path.abspath(__file__)).split('//')[0:-1])
	path.replace(os.sep,ntpath.sep)
	inputs_dict = ifunc.read_in_input_data_windows(path)
	pre_loop_variables = ifunc.variable_prep_for_main(inputs_dict, benchmark_states)
	export_path = '//'.join(os.path.dirname(os.path.abspath(__file__)).split('//')[0:-1]) + "//results//"+pre_loop_variables['Fiscal Year']+" Residential Benchmark Table for Chart.xlsx"

else:
	path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-1])
	path.replace(os.sep,ntpath.sep)
	inputs_dict = ifunc.read_in_input_data_mac(path)
	pre_loop_variables = ifunc.variable_prep_for_main(inputs_dict, benchmark_states)
	export_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-1]) + "/results/"+pre_loop_variables['Fiscal Year']+" Residential Benchmark Table for Chart.xlsx"
	
def main(inputs_dict, pre_loop_variables, states=benchmark_states, power=ifunc.power, export_path=export_path):
	df_states = pre_loop_variables['State Results Table']
	 
	df_final_tables = {}
	
	system_size_dict = ifunc.power(inputs_dict['Main Inputs'])

	electrical_bos_micro, inputs_dict=ifunc.electrical_bos(inputs_dict, "Microinverter", system_size_dict, pre_loop_variables['Microinverter DC AC Ratio'])
	electrical_bos_optimizer, inputs_dict=ifunc.electrical_bos(inputs_dict, "DC Optimizer", system_size_dict, pre_loop_variables['DC Optimizer DC AC Ratio'])
	electrical_bos_string, inputs_dict=ifunc.electrical_bos(inputs_dict, "String Inverter", system_size_dict, pre_loop_variables['String DC AC Ratio'])
	#print( electrical_bos_string, electrical_bos_micro, electrical_bos_optimizer )
	#Kelsey's method
	
	avg_system_area =inputs_dict['Soft Costs'].loc['Average system size: original (kW)']*1000/172
	aconst_system_size=avg_system_area*system_size_dict['Module Efficiency']
	inputs_dict['Soft Costs'].loc['New Portfolio'] = (aconst_system_size*inputs_dict['Soft Costs'].loc["Assumed fraction of area-constrained systems in the company's portfolio"]*inputs_dict['Soft Costs'].loc['Assumed number of annual installs']
		+inputs_dict['Soft Costs'].loc['Average system size: original (kW)']*(1-inputs_dict['Soft Costs'].loc["Assumed fraction of area-constrained systems in the company's portfolio"])*inputs_dict['Soft Costs'].loc['Assumed number of annual installs'])*1000

	# print('new porfolio size with Kelsey method is:',inputs_dict['Soft Costs'].loc['New Portfolio'])
	# David's method
	david_new_portfolio = inputs_dict['Soft Costs'].loc['Assumed number of annual installs']*system_size_dict['System Size']
	# print('new porfolio size with David method is:',david_new_portfolio)

	for state in states:
		midx = pd.MultiIndex(levels=[['String Inverter Option','Power Optimizer Option','Microinverter Option'],['Small Installer','Large Installer','Weighted Average']], codes=[[0,0,0,1,1,1,2,2,2],[0,1,2,0,1,2,0,1,2]])
		df_final_table = pd.DataFrame(columns=midx)

		sales_tax, codb, module_relate_costs = ifunc.installer_vs_integrator(inputs_dict, state)

		if state=="United States":
			df_us_module_costs = module_relate_costs["Module Costs Table"]
		#
		# ##Kelsey's Method
		# df_final_table.loc['Inverter','String Inverter Option'] = ifunc.single_inverter(system_size_dict['System Size'], inputs_dict['String Inverter Calculation'])
		# #print('cost for string inverter with kelsey method is:', kstring)
		# df_final_table.loc['Inverter','Microinverter Option']= ifunc.microinverter(system_size_dict, inputs_dict['Microinverter Calculation'],pre_loop_variables["Microinverter DC AC Ratio"])
		# #print('cost for micro inverter with kelsey method is:',kmicro)
		# df_final_table.loc['Inverter','Power Optimizer Option'] = ifunc.dc_optimizer(system_size_dict['System Size'], inputs_dict['DC Optimizer Calculation'], pre_loop_variables["DC Optimizer DC AC Ratio"])
		# #print('cost for dc-dc optimizer with kelsey method is:',kdcdc)

		#David's Method
		df_final_table.loc['Inverter','String Inverter Option'] = pre_loop_variables["String Inverter $/Wac"]/pre_loop_variables["String DC AC Ratio"]
		# print('cost for string inverter with david method is:',df_final_table.loc['Inverter','String Inverter Option'])
		df_final_table.loc['Inverter','Microinverter Option'] = pre_loop_variables["Microinverter $/Wac"]/pre_loop_variables["Microinverter DC AC Ratio"]
		# print('cost for micro inverter with david method is:',df_final_table.loc['Inverter','Microinverter Option'])
		df_final_table.loc['Inverter','Power Optimizer Option'] = pre_loop_variables["DC Optimizer $/Wac"]/pre_loop_variables["DC Optimizer DC AC Ratio"]
		# print('cost for dc-dc optimizer with david method is:',df_final_table.loc['Inverter','Power Optimizer Option'])

		
		df_final_table.loc['Module'] = module_relate_costs['Module Price']

		df_final_table.loc['Structual BoS']=(pre_loop_variables['Racking Cost Table']['Total Price'].sum())/system_size_dict['System Size']
		
		df_final_table.loc['Electrical BoS','Microinverter Option'] = electrical_bos_micro
		df_final_table.loc['Electrical BoS','Power Optimizer Option'] = electrical_bos_optimizer
		df_final_table.loc['Electrical BoS','String Inverter Option'] = electrical_bos_string

		supply_chain_costs_dict = ifunc.supply_chain_costs(df_final_table, inputs_dict['Main Inputs'], module_relate_costs)
		df_final_table.loc['Supply Chain Costs',('String Inverter Option', 'Small Installer')]=supply_chain_costs_dict['String Inverter Small Installer']
		df_final_table.loc['Supply Chain Costs',('String Inverter Option', 'Large Installer')]=supply_chain_costs_dict['String Inverter Large Installer']
		df_final_table.loc['Supply Chain Costs',('Power Optimizer Option', 'Small Installer')]= supply_chain_costs_dict['DC Optimizer Small Installer']
		df_final_table.loc['Supply Chain Costs',('Power Optimizer Option', 'Large Installer')]= supply_chain_costs_dict['DC Optimizer Large Installer']
		df_final_table.loc['Supply Chain Costs',('Microinverter Option', 'Small Installer')]= supply_chain_costs_dict['Microinverter Small Installer']
		df_final_table.loc['Supply Chain Costs',('Microinverter Option', 'Large Installer')]= supply_chain_costs_dict['Microinverter Large Installer']

		df_final_table.loc['Sales Tax',('String Inverter Option', 'Small Installer')]= df_final_table[('String Inverter Option', 'Small Installer')].sum()*sales_tax
		df_final_table.loc['Sales Tax',('String Inverter Option', 'Large Installer')]=df_final_table[('String Inverter Option', 'Large Installer')].sum()*sales_tax
		df_final_table.loc['Sales Tax',('Power Optimizer Option', 'Small Installer')]= df_final_table[('Power Optimizer Option', 'Small Installer')].sum()*sales_tax
		df_final_table.loc['Sales Tax',('Power Optimizer Option', 'Large Installer')]=df_final_table[('Power Optimizer Option', 'Large Installer')].sum()*sales_tax
		df_final_table.loc['Sales Tax',('Microinverter Option', 'Small Installer')]= df_final_table[('Microinverter Option', 'Small Installer')].sum()*sales_tax
		df_final_table.loc['Sales Tax',('Microinverter Option', 'Large Installer')]= df_final_table[('Microinverter Option', 'Large Installer')].sum()*sales_tax

		df_final_table.loc['Install Labor','Microinverter Option']=ifunc.installation(inputs_dict, "Microinverter", state, system_size_dict, pre_loop_variables['Labor Burden'])
		df_final_table.loc['Install Labor','Power Optimizer Option']=ifunc.installation(inputs_dict, "DC Optimizer", state, system_size_dict, pre_loop_variables['Labor Burden'])
		df_final_table.loc['Install Labor','String Inverter Option']=ifunc.installation(inputs_dict, "String Inverter", state, system_size_dict, pre_loop_variables['Labor Burden'])
		
		df_final_table = ifunc.permitting_inspection_interconnection(df_final_table, pre_loop_variables, codb, system_size_dict['System Size'])

		df_sum = (df_final_table.sum(axis=0))
		df_final_table.loc['Net Profit'] = inputs_dict['Main Inputs'].loc['Gross Margin','Value B']*df_sum

		df_final_table = ifunc.customer_acquisition(df_final_table, pre_loop_variables, codb, system_size_dict['System Size'])

		df_final_table = ifunc.overhead(df_final_table, pre_loop_variables, codb, system_size_dict['System Size'], inputs_dict['Soft Costs'])
		
		df_final_table.loc['Total Price'] = (df_final_table.sum(axis=0))

		df_final_table[('String Inverter Option', 'Weighted Average')] = (df_final_table[('String Inverter Option', 'Small Installer')]*pre_loop_variables["market_share_small_installer"]
			+df_final_table[('String Inverter Option', 'Large Installer')]*pre_loop_variables["market_share_large_installer"])
		df_final_table[('Power Optimizer Option', 'Weighted Average')] = (df_final_table[('Power Optimizer Option', 'Small Installer')]*pre_loop_variables["market_share_small_installer"]
			+df_final_table[('Power Optimizer Option', 'Large Installer')]*pre_loop_variables["market_share_large_installer"])
		df_final_table[('Microinverter Option', 'Weighted Average')] = (df_final_table[('Microinverter Option', 'Small Installer')]*pre_loop_variables["market_share_small_installer"]
			+df_final_table[('Microinverter Option', 'Large Installer')]*pre_loop_variables["market_share_large_installer"])

		df_final_table[('Mixed','Weighted Average')] = (inputs_dict['Main Inputs'].loc['String Inverter','Value A']*df_final_table[('String Inverter Option', 'Weighted Average')]
														+inputs_dict['Main Inputs'].loc['DC Optimizer','Value A']*df_final_table[('Power Optimizer Option', 'Weighted Average')]
														+inputs_dict['Main Inputs'].loc['Microinverter','Value A']*df_final_table[('Microinverter Option', 'Weighted Average')])
		
		df_final_tables[state]=df_final_table
		df_states[state] = df_final_table[('Microinverter Option','Small Installer')]

	writer = pd.ExcelWriter(export_path, engine = 'xlsxwriter')

	df_final_tables['United States'].to_excel(writer, sheet_name = 'USA Full Results')
	df_states.to_excel(writer, sheet_name = 'State Weighted Average Results')
	inputs_dict['Integrator Market Share'].to_excel(writer, sheet_name = 'Integrator Market Share')
	# df_us_module_costs.to_excel(writer, sheet_name = 'Module Related Costs')
	total_cost = df_final_table.loc['Total Price', ('Mixed', 'Weighted Average')]
	print(system_size_dict['System Size'])
	print( "Total Cost ", total_cost )
	# print( df_final_table )
	writer.save()
	writer.close()

main(inputs_dict,pre_loop_variables)



print('done')
print("--- %s seconds ---" % (clock.time() - start_time))
