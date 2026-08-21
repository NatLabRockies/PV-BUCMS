import pandas as pd
import numpy as np
import matplotlib as plt
import labor_cost_functions as lcf
import bill_of_material as bom
import statistics as stat
import labor_database as ld


#Create variables for column header strings
A = 'Value A'
B = 'Value B'
C = 'Value C'
D = 'Value D'

#Function to get final module cost
def get_module_cost(df_inputs):
    
    mod_supply_chain = 0.2691
    mod_cost = df_inputs.loc['Module Price ($/W)', A] + (df_inputs.loc['Module Price ($/W)', A])*mod_supply_chain
    
    return mod_cost

#Function to get final inverter cost
def get_inverter_cost(state,nec_list, df_inputs):
  if state in nec_list:
    inv_cost= df_inputs.loc['DC Optimizer Inverter Price ($/Wac)', A]/df_inputs.loc['DC Optimizer DC to AC Ratio', A]
  else:
    inv_cost= df_inputs.loc['Three Phase Inverter Price ($/Wac)', A]/df_inputs.loc['Three Phase DC to AC Ratio', A]

  return inv_cost

# def get_inverter_cost(state,nec_list, df_inputs):
#
#     inv_cost= df_inputs.loc['Inverter Price ($/Wac)', A]/df_inputs.loc['DC to AC Ratio', A]
#     return inv_cost

#Function to get final land acquisition cost
def get_land_acq_cost(df_inputs):
    land_acq_cost = df_inputs.loc['Land Acquisition ($/W)', A]
    return land_acq_cost

#Function to get final sales tax cost
def get_sales_tax_cost(df_install, sales_tax, project_size, module_cost, inverter_cost):
    material_cost = df_install['Material Cost'].sum()
    equipment_cost = df_install['Equipment Cost'].sum()
    
    tax_per_watt = ((material_cost+equipment_cost)/(project_size)+module_cost+inverter_cost)*sales_tax
    
    return tax_per_watt, material_cost, equipment_cost

def get_structural_bos(df_module_db, df_ballasted_systems, df_utility,project_size, num_modules, df_inputs, df_state, state, hist_cost_index, year, watts, df_loading_inputs):
    importance_factor = df_inputs.loc['Importance Factor, I','Value A']
    uncertainty_coeff = df_inputs.loc['Coefficiency Uncertainty','Value A']
    module = df_inputs.loc['Module Name','Value A']
    width = df_module_db.loc[module, 'Width (in)']
    length = df_module_db.loc[module, 'Length (in)']
    weight = df_module_db.loc[module, 'Weight (lb)']
    df_design = bom.design_criteria(importance_factor, length, width, weight, uncertainty_coeff, state, df_state)
    df_loading_combo = bom.loading_combo(df_design, df_loading_inputs)
    max_wind = np.amax(df_loading_combo['Wind'])
    ballast_bay_per_module, ballast_cost_per_module = bom.ballasted_systems(df_ballasted_systems, watts, project_size, df_inputs, max_wind) 
    df_structural_bos=lcf.racking_install(df_inputs,ballast_bay_per_module, num_modules, ballast_cost_per_module, df_utility, df_state, state, hist_cost_index)
     
    df_structural_bos['Material Cost'] = df_structural_bos['Material Cost Per Unit']*df_structural_bos['Job Quantity']
    structural_bos = df_structural_bos['Material Cost'].sum()/project_size

    # print("Total Moulde Area", width*length*0.000645*num_modules)
    
    return structural_bos, df_structural_bos

def get_electrical_bos_battery(df_utility,project_size, num_modules, df_inputs, df_state, state, hist_cost_index, year, df_module_db, df_bos_cost, df_com_storage):
    df_pre_sur = lcf.preconstruction_surveys(df_utility, df_inputs, df_state, num_modules, project_size, state, hist_cost_index)
    df_pre_sur_bat = lcf.preconstruction_surveys_battery(df_utility, df_state, state, hist_cost_index, df_com_storage)
    df_sec_fen_bat = lcf.security_fencing_battery(df_utility, df_state, state, hist_cost_index, df_com_storage)
    
    df_pv_source_conductor, pv_source_conductor_job_qty, strings, array_length = lcf.pv_source_conductor(df_inputs, df_module_db, num_modules, df_utility, df_state, state, hist_cost_index)
    df_pv_output_conductor = lcf.pv_output_conductor(strings, df_inputs, df_utility, df_state, state, hist_cost_index)
    df_conduit_trans_to_inv, strings_per_trans = lcf.conduit_trans_to_inv(strings, df_inputs, df_utility, df_state, state, hist_cost_index)
    df_trans_boxes = lcf.trans_boxes(strings,strings_per_trans, df_utility, df_state, state, hist_cost_index)
    df_ground_bonding = lcf.ground_bonding(pv_source_conductor_job_qty,df_utility, df_state, state, hist_cost_index)
    df_grounding_cable_bat = lcf.grounding_cable_battery(df_utility, df_state, state, hist_cost_index)
    df_inverter, inverter_count = lcf.inverter(array_length, project_size, num_modules, df_inputs, df_utility, df_state, state, hist_cost_index)
    df_cond_inv = lcf.conductor_inverter_to_ac(inverter_count, df_inputs, df_utility, df_state, state, hist_cost_index)
    df_conduit_inv = lcf.conduit_inverter_to_ac(inverter_count, df_inputs, df_utility, df_state, state, hist_cost_index)
    df_ac_subpanel = lcf.ac_subpanel(df_utility, df_state, state, hist_cost_index)
    df_ac_disco = lcf.big_ac_disco(df_utility, df_state, state, hist_cost_index, project_size)
    df_cond_ac, ac_run = lcf.conductor_ac_to_interconnect(df_inputs, df_utility, df_state, state, hist_cost_index)
    df_conduit_ac = lcf.conduit_ac_to_interconnect(ac_run, df_utility, df_state, state, hist_cost_index)
    df_conduit_wiring = lcf.conduit_wiring(df_utility, df_state, state, hist_cost_index)
    df_revenue_meter = lcf.revenue_grade_meter(df_utility, df_state, state, hist_cost_index, project_size, df_bos_cost)
    df_system_monitor = lcf.system_monitor(df_utility, df_state, state, hist_cost_index, project_size, df_bos_cost)
      
    df_list = [df_pre_sur,
              df_pre_sur_bat,
              df_sec_fen_bat,
              df_pv_source_conductor,
              df_pv_output_conductor,
              df_conduit_trans_to_inv,
              df_trans_boxes,
              df_ground_bonding,
              df_grounding_cable_bat,
              df_inverter,
              df_cond_inv,
              df_conduit_inv,
              df_ac_subpanel,
              df_ac_disco,
              df_cond_ac,
              df_conduit_ac,
              df_conduit_wiring,
              df_revenue_meter,
              df_system_monitor 
              ]
    
    
    
    df_electrical_bos = pd.concat(df_list, sort=False)
    df_electrical_bos['Material Cost'] = df_electrical_bos['Material Cost Per Unit']*df_electrical_bos['Job Quantity']
    electrical_bos = df_electrical_bos['Material Cost'].sum()/project_size
    
    return electrical_bos, df_electrical_bos, pv_source_conductor_job_qty, df_pre_sur, df_pre_sur_bat

def get_electrical_bos(df_utility,project_size, num_modules, df_inputs, df_state, state, hist_cost_index, year, df_module_db, df_bos_cost,dc_ac_ratio):
    df_pre_sur = lcf.preconstruction_surveys(df_utility, df_inputs, df_state, num_modules, project_size, state, hist_cost_index)
    df_pv_source_conductor, pv_source_conductor_job_qty, strings, array_length = lcf.pv_source_conductor(df_inputs, df_module_db, num_modules, df_utility, df_state, state, hist_cost_index)
    df_pv_output_conductor = lcf.pv_output_conductor(strings, df_inputs, df_utility, df_state, state, hist_cost_index)
    df_conduit_trans_to_inv, strings_per_trans = lcf.conduit_trans_to_inv(strings, df_inputs, df_utility, df_state, state, hist_cost_index)
    df_trans_boxes = lcf.trans_boxes(strings,strings_per_trans, df_utility, df_state, state, hist_cost_index)
    df_ground_bonding = lcf.ground_bonding(pv_source_conductor_job_qty,df_utility, df_state, state, hist_cost_index)
    df_inverter, inverter_count = lcf.inverter(array_length, project_size, num_modules, df_inputs, df_utility, df_state, state, hist_cost_index,dc_ac_ratio)
    df_cond_inv = lcf.conductor_inverter_to_ac(inverter_count, df_inputs, df_utility, df_state, state, hist_cost_index)
    df_conduit_inv = lcf.conduit_inverter_to_ac(inverter_count, df_inputs, df_utility, df_state, state, hist_cost_index)
    df_ac_subpanel = lcf.ac_subpanel(df_utility, df_state, state, hist_cost_index)
    df_ac_disco = lcf.big_ac_disco(df_utility, df_state, state, hist_cost_index, project_size)
    df_cond_ac, ac_run = lcf.conductor_ac_to_interconnect(df_inputs, df_utility, df_state, state, hist_cost_index)
    df_conduit_ac = lcf.conduit_ac_to_interconnect(ac_run, df_utility, df_state, state, hist_cost_index)
    df_revenue_meter = lcf.revenue_grade_meter(df_utility, df_state, state, hist_cost_index, project_size, df_bos_cost)
    df_system_monitor = lcf.system_monitor(df_utility, df_state, state, hist_cost_index, project_size, df_bos_cost)
      
    df_list = [df_pre_sur,
              df_pv_source_conductor,
              df_pv_output_conductor,
              df_conduit_trans_to_inv,
              df_trans_boxes,
              df_ground_bonding,
              df_inverter,
              df_cond_inv,
              df_conduit_inv,
              df_ac_subpanel,
              df_ac_disco,
              df_cond_ac,
              df_conduit_ac,
              df_revenue_meter,
              df_system_monitor 
              ]
    
    
    
    df_electrical_bos = pd.concat(df_list, sort=False)
    df_electrical_bos['Material Cost'] = df_electrical_bos['Material Cost Per Unit']*df_electrical_bos['Job Quantity']
    electrical_bos = df_electrical_bos['Material Cost'].sum()/project_size
    # print("electrical BOS \n", df_electrical_bos['Material Cost'])

    return electrical_bos, df_electrical_bos, pv_source_conductor_job_qty, df_pre_sur

def get_install_cost(df_electrical_bos, df_structural_bos, df_utility, df_labor, df_labor_weight, df_state, state, inflation, project_size, df_inputs, df_labor_table, num_modules, pv_source_conductor_job_qty, df_pre_sur, watts):
    df_site_prep_roof = lcf.site_prep_roof(df_utility, df_state, state, inflation, df_pre_sur)
    df_mod_install = lcf.module_install(df_utility, df_state, state, inflation, num_modules)
    df_lift_crane = lcf.lift_crane(df_utility, df_state, state, inflation)
    df_loading_drive = lcf.loading_drive(pv_source_conductor_job_qty, df_utility, df_state, state, inflation)
    
    df_structural_bos = pd.concat([df_site_prep_roof,
                                  df_mod_install,
                                  df_lift_crane,
                                   df_loading_drive,
                                   df_structural_bos
                                  ], sort=False)
    
    df_wage = ld.average_wage_by_state(df_inputs, state, df_labor_table, df_labor, project_size, df_state)
    df_install = pd.concat([df_electrical_bos, df_structural_bos], axis=0, sort=False)
    df_install['Equipment Cost'] = df_install['Equipment Cost Per Unit']*df_install['Job Quantity']
    df_install['ID'] = df_install.apply(lambda x:df_utility.loc[x.name,'ID'], axis=1)
    df_install['Labor Cost per Unit per Hour'] = df_install['ID'].apply(lambda x:(df_labor_weight.loc['Common Laborers', x]*df_wage.loc['Common Laborers','Base Hourly'] +\
        df_labor_weight.loc['Electricians', x]*df_wage.loc['Electricians','Base Hourly']+ \
        df_labor_weight.loc['Equipment Operators', x]*df_wage.loc['Equipment Operators','Base Hourly'])/df_labor_weight[x].sum())  
        
    df_install['Labor Cost per Unit'] = df_install['Labor Cost per Unit per Hour']*df_install['Labor Hours']
    df_install['Labor Cost'] = df_install['Labor Cost per Unit']*df_install['Job Quantity']    
    
    install_cost= (df_install['Labor Cost'].sum() + df_install['Equipment Cost'].sum())/(project_size)
    # # print( df_install['Labor Cost'].sum(), df_install['Equipment Cost'].sum() )
    # print("Project Size", project_size)
    print("Equipment Cost", df_install['Equipment Cost'].sum(), "Labor Cost", df_install['Labor Cost'].sum())
    return install_cost, df_install, df_wage
    
def get_install_cost_battery(df_electrical_bos, df_structural_bos, df_utility, df_labor, df_labor_weight, df_state, state, inflation, project_size, df_inputs, df_labor_table, num_modules, pv_source_conductor_job_qty, df_pre_sur, watts, df_pre_sur_bat):
    df_site_prep = lcf.site_prep_battery(df_utility, df_state, state, inflation, df_pre_sur_bat)
    df_site_prep_roof = lcf.site_prep_roof(df_utility, df_state, state, inflation, df_pre_sur)
    df_mod_install = lcf.module_install(df_utility, df_state, state, inflation, num_modules)
    df_lift_crane = lcf.lift_crane(df_utility, df_state, state, inflation)
    df_lift_crane_bat = lcf.lift_crane_battery(df_utility, df_state, state, inflation)
    df_loading_drive = lcf.loading_drive(pv_source_conductor_job_qty, df_utility, df_state, state, inflation)
    df_loading_drive_bat = lcf.loading_drive_battery(df_utility, df_state, state, inflation)
    
    df_structural_bos = pd.concat([df_site_prep,
                                   df_site_prep_roof,
                                  df_mod_install,
                                  df_lift_crane,
                                    df_lift_crane_bat,
                                   df_loading_drive,
                                   df_loading_drive_bat,
                                   df_structural_bos
                                  ], sort=False)
    
    
    
    df_wage = ld.average_wage_by_state(df_inputs, state, df_labor_table, df_labor, project_size, df_state)
    df_install = pd.concat([df_electrical_bos, df_structural_bos], axis=0, sort=False)
    df_install['Equipment Cost'] = df_install['Equipment Cost Per Unit']*df_install['Job Quantity']
    df_install['ID'] = df_install.apply(lambda x:df_utility.loc[x.name,'ID'], axis=1)
    df_install['Labor Cost per Unit per Hour'] = df_install['ID'].apply(lambda x:(df_labor_weight.loc['Common Laborers', x]*df_wage.loc['Common Laborers','Base Hourly'] +\
        df_labor_weight.loc['Electricians', x]*df_wage.loc['Electricians','Base Hourly']+ \
        df_labor_weight.loc['Equipment Operators', x]*df_wage.loc['Equipment Operators','Base Hourly'])/df_labor_weight[x].sum())  
        
    df_install['Labor Cost per Unit'] = df_install['Labor Cost per Unit per Hour']*df_install['Labor Hours']
    df_install['Labor Cost'] = df_install['Labor Cost per Unit']*df_install['Job Quantity']    
    
    install_cost= (df_install['Labor Cost'].sum() + df_install['Equipment Cost'].sum())/(project_size)
    return install_cost, df_install, df_wage



def get_permitting_cost(state, df_state, df_inputs, project_size, poi, df_wage, df_labor_weight, df_utility, other_inflation):
    
    permitting_cost = df_state.loc[state, ('Building & Electrical PE/Interconnection ($)', 'Commercial')]*other_inflation
    df_interconnect = lcf.interconnection(df_utility, df_state, state, other_inflation) 
    df_interconnect['ID'] = df_interconnect.apply(lambda x:df_utility.loc[x.name,'ID'], axis=1)
    df_interconnect['Labor Cost per Unit per Hour'] = df_interconnect['ID'].apply(lambda x:(df_labor_weight.loc['Common Laborers', x]*df_wage.loc['Common Laborers','Total Hourly'] +\
        df_labor_weight.loc['Electricians', x]*df_wage.loc['Electricians','Total Hourly']+ \
        df_labor_weight.loc['Equipment Operators', x]*df_wage.loc['Equipment Operators','Total Hourly'])/df_labor_weight[x].sum())  
        
    df_interconnect['Labor Cost per Unit'] = df_interconnect['Labor Cost per Unit per Hour']*df_interconnect['Labor Hours']
    df_interconnect['Labor Cost'] = df_interconnect['Labor Cost per Unit']*df_interconnect['Job Quantity'] * (poi/0.2/1000000) #testing

    #uncertainty_coeff = stat.mean(df_inputs.loc['Permitting Cost', A], df_inputs.loc['Permitting Cost', B], df_inputs.loc['Permitting Cost', C])
    #NEED RAN INPUT ON UNCERTAINTY TAB
    uncertainty_coeff = df_inputs.loc['Permitting Cost', D]
    total_permitting_cost = (df_interconnect.loc['Interconnection, testing and commissioning','Labor Cost'] + permitting_cost)/(project_size) + 0.06
    
    # print("Intercon", df_labor_weight.loc['Electricians'])
    # print("total permitting", total_permitting_cost)
    return total_permitting_cost, permitting_cost

def get_oh_p_cost(df_install, project_size, df_labor_weight, df_wage):
    df_install['Labor Cost Incl OH & P'] = df_install['ID'].apply(lambda x:(df_labor_weight.loc['Common Laborers', x]*df_wage.loc['Common Laborers','Total Hourly'] +\
        df_labor_weight.loc['Electricians', x]*df_wage.loc['Electricians','Total Hourly']+ \
        df_labor_weight.loc['Equipment Operators', x]*df_wage.loc['Equipment Operators','Total Hourly'])/df_labor_weight[x].sum())*df_install['Labor Hours']*df_install['Job Quantity']
    oh_p_cost = df_install['Labor Cost Incl OH & P'].sum()-df_install['Labor Cost'].sum()+df_install['Material Cost'].sum()*0.13+df_install['Equipment Cost'].sum()*0.13   
    epc_overhead = oh_p_cost/project_size + (2*60*100)/(200000)
    return epc_overhead, oh_p_cost, df_install
     
def get_contigency_cost(df_inputs, material_cost, equipment_cost, df_install, module_cost, inverter_cost, permitting_cost, project_size, sales_tax, oh_p_cost):
    subtotal = (material_cost + equipment_cost + df_install['Labor Cost'].sum() + oh_p_cost + permitting_cost)/project_size + module_cost + inverter_cost + sales_tax
    contingency_cost = subtotal*df_inputs.loc['Contigency & Logistics Percent','Value A']
    
    return contingency_cost, subtotal*project_size

# def get_developer_overhead_cost(df_dev_costs, df_dev_business_model, df_ancillary_exp, state, df_state, project_size, inflation, inflation_2015):
#     total_mw_per_year = df_dev_business_model.loc['Leads Generated/Assessed','Value']*df_dev_business_model.loc['Win Rate','Value']*df_dev_business_model.loc['Avg kW/project','Value']*1000
#     state_dev_cost_of_doing_business = df_state.loc[state,("Moody's cost of doing business","Labor (dev team)")]/100
#     inflation_2018_2015= inflation/inflation_2015
#     df_dev_costs['Wage'] = df_dev_costs['Annual Salary ($)']*state_dev_cost_of_doing_business*inflation_2018_2015
#     df_dev_costs['Total Wage per W']= df_dev_costs['FTE']*df_dev_costs['Wage']*(1+df_dev_costs['Burden (%)'])/total_mw_per_year
#
#     travel = (df_ancillary_exp.loc['Sales Travel Frequency','Value']*df_dev_costs.loc['BizDev','FTE']+
#               df_ancillary_exp.loc['Others Travel Frequency','Value']*(df_dev_costs.loc['CEO','FTE']+
#                                                                        df_dev_costs.loc['CFO','FTE']+
#                                                                        df_dev_costs.loc['COO','FTE']+
#                                                                       df_dev_costs.loc['Marketing','FTE']+
#                                                                       df_dev_costs.loc['Project Mgr','FTE']))*df_ancillary_exp.loc['Travel Per Diem (Including Flight) ($)','Value']*52
#
#     ancillary_exp_per_watt=((df_ancillary_exp.loc['Billing system ($)','Value']+
#         df_ancillary_exp.loc['Dues and memberships ($)','Value']+
#         df_ancillary_exp.loc['Insurance ($)','Value']+
#         df_ancillary_exp.loc['Other ($)','Value']+
#         (df_ancillary_exp.loc['Office space ($/person)','Value']+df_ancillary_exp.loc['Office expenses ($/person)','Value'])*df_dev_costs['FTE'].sum()+
#         travel)/total_mw_per_year+
#         df_ancillary_exp.loc['External corporate services ($/W)','Value'])*state_dev_cost_of_doing_business
#     developer_overhead_cost = df_dev_costs['Total Wage per W'].sum()+ancillary_exp_per_watt
#
#     return developer_overhead_cost

def get_developer_overhead_cost(pre_contigency_developer_oh_total, project_size):
    #NEED RAN INPUT ON NUMBERS
    developer_overhead = 0.3
    developer_overhead_cost = developer_overhead*pre_contigency_developer_oh_total/(project_size)
    #print(project_size, developer_overhead_cost)
    return developer_overhead_cost

def get_net_profit(df_final, state, df_profit):
    profit_margin = df_profit.loc['Developer Net Profit Percentage','Value']
    net_profit = df_final[state].sum()*profit_margin

    return net_profit

def get_total_cost(df_final, state):
    total_cost = df_final[state].sum()
    
    return total_cost