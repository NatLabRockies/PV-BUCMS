import pandas as pd
import numpy as np
import matplotlib as plt
import inverter as inv
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
def get_inverter_cost(df_inputs):
    x= df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', B]
    if df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', A]:
        inv_price_factor= x
    else:
        inv_price_factor = 1
    if df_inputs.loc['Tracker?', A]:
        inv_cost= df_inputs.loc['Inverter Price ($/Wac)', A]/df_inputs.loc['DC to AC Ratio', A]
    else:
        inv_cost= df_inputs.loc['Inverter Price ($/Wac)', A]/df_inputs.loc['DC to AC Ratio', B]
    
    return inv_cost

#Function to get final land acquisition cost
def get_land_acq_cost(df_inputs):
    land_acq_cost = df_inputs.loc['Land Acquisition ($/W)', A]
    return land_acq_cost


#Function to get final sales tax cost
def get_sales_tax_cost(material_cost, equipment_cost, sales_tax, project_size):
    total_tax = (material_cost+equipment_cost)*sales_tax
    tax_per_watt = total_tax/(project_size*1000000.0)
    
    return tax_per_watt

def get_structural_bos(df_utility,project_size, num_modules, df_inputs, df_state, state, hist_cost_index, df_module_db, year, df_torque_tube, df_pipe, df_rail_clamp, steel_inflation, df_inv_calc, df_loading_combo):
    
    df_bom = bom.bom_table_fixed(df_module_db, df_inputs, num_modules, year, df_state, state, project_size, df_torque_tube, df_pipe, df_rail_clamp, steel_inflation, df_loading_combo)
    
    df_fou_inv = lcf.foundation_inverter(df_utility, project_size, df_inputs, df_inv_calc, df_state, hist_cost_index, state)
    df_trenches = lcf.trenches(df_utility,project_size, num_modules, df_inputs, df_inv_calc, df_state, hist_cost_index, state)    
    df_found_vert_supp, size_factor = lcf.foundation_vertical_support(df_utility, df_inputs, df_bom, project_size, hist_cost_index, df_state, steel_inflation, df_pipe, state)
    df_hor_supp = lcf.horizontal_support(df_utility, df_inputs, df_bom, hist_cost_index, df_state, steel_inflation, df_torque_tube, state, size_factor)
    df_weld_bolt = lcf.welding_or_bolting(df_utility, df_inputs, df_bom, hist_cost_index, df_state, state)
    df_mod_mount = lcf.modules_mounting(df_utility, df_inputs, df_bom, hist_cost_index, df_state, num_modules, state, df_rail_clamp, steel_inflation, size_factor)
    df_t_conn = lcf.t_connection(df_utility, df_bom, hist_cost_index, df_state, state, size_factor)
    df_ujoint = lcf.ujoint_driveline(df_inputs,df_utility,df_state, num_modules, hist_cost_index, state, size_factor)
    df_slav_gear = lcf.slave_gearbox(df_utility, df_inputs,hist_cost_index, df_state, state, num_modules, size_factor)
    df_mc_equip = lcf.motor_controller_equip(df_utility, df_inputs,hist_cost_index, df_state, state, num_modules, size_factor)    
        
    df_list= [
        df_fou_inv,
        df_trenches,
        df_found_vert_supp,
        df_hor_supp,
        df_weld_bolt,
        df_mod_mount,
        df_t_conn,
        df_ujoint,
        df_slav_gear,
        df_mc_equip
    ]

    df_structural_bos = pd.concat(df_list, sort=False)    
    df_structural_bos['Material Cost'] = df_structural_bos['Material Cost Per Unit']*df_structural_bos['Job Quantity']
    df_structural_bos['Equipment Cost'] = df_structural_bos['Equipment Cost Per Unit']*df_structural_bos['Job Quantity']
    structural_bos = df_structural_bos['Material Cost'].sum()/(project_size*1000000)
    
    return structural_bos, df_structural_bos, df_bom, size_factor

def get_electrical_bos(df_structural_bos, df_utility, hist_cost_index, df_state, state, df_bom, size_factor, num_modules, df_inv_calc, df_inputs, project_size):  
    df_pre_sur = lcf.preconstruction_surveys(df_utility, df_inputs, df_state, num_modules, project_size, state, hist_cost_index)
    df_acc_roa = lcf.access_roads_and_parking(df_utility, df_state, project_size, state, hist_cost_index, df_pre_sur)
    df_sec_fen = lcf.security_fencing(df_utility, df_pre_sur, df_state, hist_cost_index, state)
    df_tem_off = lcf.temp_office(df_utility, df_state, hist_cost_index, state, project_size)
    df_sto_box = lcf.storage_box(df_utility, df_state, num_modules, hist_cost_index, state, project_size)
    df_om_build = lcf.om_building(df_utility, df_state, hist_cost_index, state, project_size)
    df_site_prep = lcf.site_prep(df_inputs, df_utility, df_state, df_inv_calc, hist_cost_index, state, df_pre_sur)
    df_cond_wire = lcf.conduit_wiring(df_structural_bos, df_utility, hist_cost_index, df_state, state, size_factor)
    df_ground = lcf.grounding_cable(df_structural_bos, df_bom, df_utility, hist_cost_index, df_state, state, size_factor)
    df_junc = lcf.junction_box(df_inv_calc, df_inputs, df_utility, df_state, state, hist_cost_index, size_factor, num_modules)
    df_inv_house = lcf.inverter_house(df_inv_calc, df_inputs, df_utility, df_state, state, hist_cost_index, project_size)
    df_onsite_trans = lcf.onsite_transmission(df_inv_house, df_utility, df_state, state, hist_cost_index)
    df_pvcs = lcf.pv_combining_switchgear(df_inputs, df_utility, df_state, state, hist_cost_index)
    df_onsite_subs = lcf.onsite_transformer_substation(df_inputs, df_utility, df_state, state, hist_cost_index, df_inv_calc, project_size, size_factor)
    
    df_list = [
            df_pre_sur,
            df_acc_roa, 
            df_sec_fen,
            df_tem_off,
            df_sto_box,
            df_om_build,  
            df_site_prep,  
            df_cond_wire,
            df_ground,
            df_junc,
            df_inv_house,
            df_onsite_trans,
            df_pvcs,
            df_onsite_subs
              ]
    
    df_electrical_bos = pd.concat(df_list, sort=False) 
    df_electrical_bos['Material Cost'] = df_electrical_bos['Material Cost Per Unit']*df_electrical_bos['Job Quantity']
    df_electrical_bos['Equipment Cost'] = df_electrical_bos['Equipment Cost Per Unit']*df_electrical_bos['Job Quantity']
    electrical_bos = df_electrical_bos['Material Cost'].sum()/(project_size*1000000)

    # print(df_electrical_bos['Job Quantity']) #testing
    # print("Project Size", project_size, "\n", "Electrical Cost", df_electrical_bos['Material Cost'])
    
    return electrical_bos, df_electrical_bos

def get_install_cost(df_electrical_bos, df_structural_bos, df_utility, df_labor, df_labor_weight, df_state, state, project_size, df_inputs, df_labor_table):
    
    df_wage = ld.average_wage_by_state(df_inputs, state, df_labor_table, df_labor, project_size, df_state)
    df_install = pd.concat([df_electrical_bos, df_structural_bos], axis=0, sort=False)
    
    df_install['ID'] = df_install.apply(lambda x:df_utility.loc[x.name,'ID'], axis=1)
    df_install['Labor Cost per Unit per Hour'] = df_install['ID'].apply(lambda x:(df_labor_weight.loc['Common Laborers', x]*df_wage.loc['Common Laborers','Base Hourly'] +\
        df_labor_weight.loc['Electricians', x]*df_wage.loc['Electricians','Base Hourly']+ \
        df_labor_weight.loc['Equipment Operators', x]*df_wage.loc['Equipment Operators','Base Hourly'])/df_labor_weight[x].sum())
    # print(df_install['Labor Cost per Unit per Hour'])
    df_install['Labor Cost per Unit'] = df_install['Labor Cost per Unit per Hour']*df_install['Labor Hours']
    df_install['Labor Cost'] = df_install['Labor Cost per Unit']*df_install['Job Quantity']    
    
    install_cost= (df_install['Labor Cost'].sum() + df_install['Equipment Cost'].sum())/(project_size*1000000)

    # print("Install", df_install)
    # print("Project Size", project_size, "Total Labor Hours", (df_install['Labor Hours']*df_install['Job Quantity']).sum())
    print("Equipment Cost", df_install['Equipment Cost'].sum(), "Labor Cost", df_install['Labor Cost'].sum())

    return install_cost, df_install, df_wage



def get_oh_p_cost(df_inputs, df_install, df_utility, df_state, state, inflation, hist_cost_index, project_size, poi, df_labor_weight, df_wage, df_epc, df_trans):

    epc_min = df_epc.index[0]
    epc_max = df_epc.index[1]
    overhead_profit_markup = (project_size-epc_min)*(df_epc.loc[epc_max,'Percent']-df_epc.loc[epc_min,'Percent'])/(epc_max-epc_min)+df_epc.loc[epc_min,'Percent']
    
    df_site_prep_trans, transmission_len, transmission_line_factor = lcf.site_prep_transmission(df_inputs, df_utility, df_state, state, hist_cost_index, project_size, poi, df_trans)
    df_site_prep_trans['Material Cost'] = df_site_prep_trans['Material Cost Per Unit']*df_site_prep_trans['Job Quantity']
    df_site_prep_trans['Equipment Cost'] = df_site_prep_trans['Equipment Cost Per Unit']*df_site_prep_trans['Job Quantity']
    df_tower_found = lcf.tower_foundation_installation(transmission_len, df_inputs, transmission_line_factor)
    df_tower_struct = lcf.tower_structure_costs(transmission_len, df_inputs, df_utility, transmission_line_factor)
    df_tower_top = lcf.tower_top_assembly(transmission_len, df_inputs, df_utility, transmission_line_factor)
    df_cond_trans = lcf.conductor_cable_transmission(transmission_len, df_inputs, df_utility, transmission_line_factor, df_state, state, hist_cost_index)
    df_misc_trans = lcf.misc_assembly_transmission(df_utility)
    df_site_prep_dist = lcf.site_prep_distribution(transmission_len, df_inputs, df_utility, transmission_line_factor, df_state, state, hist_cost_index)
    df_wood_found = lcf.wood_pole_foundation_installation(df_tower_found, transmission_len)
    df_wood_struct = lcf.wood_pole_structure_costs(transmission_len, df_inputs, df_utility, transmission_line_factor)
    df_wood_top = lcf.wood_pole_top_assembly(transmission_len, df_inputs, df_utility, transmission_line_factor)
    df_cond_dist = lcf.conductor_cable_distribution(transmission_len, df_inputs, df_utility, transmission_line_factor, df_state, state, hist_cost_index)
    df_misc_dist = lcf.misc_assembly_dist(df_utility)
    df_intercon_fee = lcf.interconnection_fee(df_inputs,df_utility, df_state, state, inflation, project_size, poi)
    
    df_list = [
        df_site_prep_trans,
        df_tower_found, 
        df_tower_struct, 
        df_tower_top, 
        df_cond_trans, 
        df_misc_trans, 
        df_site_prep_dist, 
        df_wood_found, 
        df_wood_struct,
        df_wood_top,
        df_cond_dist,
        df_misc_dist,
        df_intercon_fee
    ]
    
    df_temp = pd.concat(df_list, sort=False)

    df_temp['ID'] = df_temp.apply(lambda x:df_utility.loc[x.name,'ID'], axis=1)
    df_temp['Labor Cost per Unit per Hour'] = df_temp['ID'].apply(lambda x:(df_labor_weight.loc['Common Laborers', x]*df_wage.loc['Common Laborers','Base Hourly'] +\
        df_labor_weight.loc['Electricians', x]*df_wage.loc['Electricians','Base Hourly']+ \
        df_labor_weight.loc['Equipment Operators', x]*df_wage.loc['Equipment Operators','Base Hourly'])/df_labor_weight[x].sum())  
    
    df_temp.loc['Site Preparation (Clearing and Grubbing) Transmission', 'Labor Cost']= df_temp.loc['Site Preparation (Clearing and Grubbing) Transmission','Labor Cost per Unit per Hour']*df_temp.loc['Site Preparation (Clearing and Grubbing) Transmission','Job Quantity']*df_temp.loc['Site Preparation (Clearing and Grubbing) Transmission','Labor Hours']
    df_temp.loc['Tower: Foundation Installation', 'Labor Cost'] = 2*df_temp.loc['Tower: Foundation Installation','Labor Cost per Unit per Hour']*df_temp.loc['Tower: Foundation Installation','Job Quantity']
    df_temp.loc['Tower: Top Assembly', 'Labor Cost'] = df_temp.loc['Tower: Top Assembly','Labor Cost per Unit per Hour']*df_temp.loc['Tower: Top Assembly','Job Quantity']
    df_temp.loc['Conductor and Cable Transmission', 'Labor Cost'] = df_temp.loc['Conductor and Cable Transmission','Labor Cost per Unit per Hour']*df_temp.loc['Conductor and Cable Transmission','Job Quantity']*df_temp.loc['Conductor and Cable Transmission','Labor Hours']                                                                 
    df_temp.loc['Misc. Assembly Units Transmission', 'Labor Cost'] = df_temp.loc['Misc. Assembly Units Transmission','Job Quantity']*\
                                                                    (df_temp.loc['Conductor and Cable Transmission', 'Labor Cost']\
                                                                     +df_temp.loc['Tower: Top Assembly', 'Labor Cost']\
                                                                     +df_temp.loc['Tower: Foundation Installation', 'Labor Cost']\
                                                                     +df_temp.loc['Site Preparation (Clearing and Grubbing) Transmission', 'Labor Cost'])                                                                  
    df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Labor Cost']= df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution','Labor Cost per Unit per Hour']*df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution','Job Quantity']*df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution','Labor Hours']
    df_temp.loc['Wood Pole: Foundation Installation', 'Labor Cost'] = 2*df_temp.loc['Wood Pole: Foundation Installation','Labor Cost per Unit per Hour']*df_temp.loc['Wood Pole: Foundation Installation','Job Quantity']
    df_temp.loc['Wood Pole: Top Assembly', 'Labor Cost'] = df_temp.loc['Wood Pole: Top Assembly','Labor Cost per Unit per Hour']*df_temp.loc['Wood Pole: Top Assembly','Job Quantity']
    df_temp.loc['Conductor and Cable Distribution', 'Labor Cost'] = df_temp.loc['Conductor and Cable Distribution','Labor Cost per Unit per Hour']*df_temp.loc['Conductor and Cable Distribution','Job Quantity']*df_temp.loc['Conductor and Cable Distribution','Labor Hours']                                                                 
    df_temp.loc['Misc. Assembly Units Distribution', 'Labor Cost'] = df_temp.loc['Misc. Assembly Units Distribution','Job Quantity']*\
                                                                    (df_temp.loc['Conductor and Cable Distribution', 'Labor Cost']\
                                                                     +df_temp.loc['Wood Pole: Top Assembly', 'Labor Cost']\
                                                                     +df_temp.loc['Wood Pole: Foundation Installation', 'Labor Cost']\
                                                                     +df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Labor Cost'])                                                                  
    
    
    
    df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Material Cost'] = df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Material Cost Per Unit']*df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Job Quantity']
    df_temp.loc['Tower: Structure Costs', 'Material Cost']= df_temp.loc['Tower: Structure Costs', 'Job Quantity']*20000
    df_temp.loc['Tower: Foundation Installation', 'Material Cost'] = df_temp.loc['Tower: Foundation Installation', 'Labor Cost']*(0.5/0.11)
    df_temp.loc['Tower: Top Assembly', 'Material Cost'] = df_temp.loc['Tower: Top Assembly', 'Labor Cost']*(0.5/0.11)
    df_temp.loc['Conductor and Cable Transmission', 'Material Cost'] = df_temp.loc['Conductor and Cable Transmission', 'Material Cost Per Unit']*df_temp.loc['Conductor and Cable Transmission', 'Job Quantity']
    df_temp.loc['Misc. Assembly Units Transmission', 'Material Cost'] = df_temp.loc['Misc. Assembly Units Transmission','Job Quantity']*\
                                                                    (df_temp.loc['Conductor and Cable Transmission', 'Material Cost']\
                                                                     +df_temp.loc['Tower: Top Assembly', 'Material Cost']\
                                                                     +df_temp.loc['Tower: Structure Costs', 'Material Cost']\
                                                                     +df_temp.loc['Tower: Foundation Installation', 'Material Cost']\
                                                                     +df_temp.loc['Site Preparation (Clearing and Grubbing) Transmission', 'Material Cost'])                                                                  
    
    df_temp.loc['Wood Pole: Structure Costs', 'Material Cost']= df_temp.loc['Wood Pole: Structure Costs', 'Job Quantity']*20000 
    df_temp.loc['Wood Pole: Foundation Installation', 'Material Cost'] = df_temp.loc['Wood Pole: Foundation Installation', 'Labor Cost']*(0.5/0.11)
    df_temp.loc['Wood Pole: Top Assembly', 'Material Cost'] = df_temp.loc['Wood Pole: Top Assembly', 'Labor Cost']*(0.5/0.11)
    df_temp.loc['Conductor and Cable Distribution', 'Material Cost'] =  df_temp.loc['Conductor and Cable Distribution', 'Material Cost Per Unit']*df_temp.loc['Conductor and Cable Distribution', 'Job Quantity']
    df_temp.loc['Misc. Assembly Units Distribution', 'Material Cost'] = df_temp.loc['Misc. Assembly Units Distribution','Job Quantity']*\
                                                                    (df_temp.loc['Conductor and Cable Distribution', 'Material Cost']\
                                                                     +df_temp.loc['Wood Pole: Top Assembly', 'Material Cost']\
                                                                     +df_temp.loc['Wood Pole: Structure Costs', 'Material Cost']\
                                                                     +df_temp.loc['Wood Pole: Foundation Installation', 'Material Cost']\
                                                                     +df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Material Cost'])                                                                  
    
    df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Equipment Cost'] = df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Equipment Cost Per Unit']*df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Job Quantity']
    df_temp.loc['Tower: Foundation Installation', 'Equipment Cost'] = df_temp.loc['Tower: Foundation Installation', 'Labor Cost']*(0.28/0.11)
    df_temp.loc['Tower: Top Assembly', 'Equipment Cost'] = df_temp.loc['Tower: Top Assembly', 'Labor Cost']*(0.28/0.11)
    df_temp.loc['Conductor and Cable Transmission', 'Equipment Cost'] = df_temp.loc['Conductor and Cable Transmission', 'Equipment Cost Per Unit']*df_temp.loc['Conductor and Cable Transmission', 'Job Quantity']
    df_temp.loc['Misc. Assembly Units Transmission', 'Equipment Cost'] = df_temp.loc['Misc. Assembly Units Transmission','Job Quantity']*\
                                                                    (df_temp.loc['Conductor and Cable Transmission', 'Equipment Cost']\
                                                                     +df_temp.loc['Tower: Top Assembly', 'Equipment Cost']\
                                                                     +df_temp.loc['Tower: Foundation Installation', 'Equipment Cost']\
                                                                     +df_temp.loc['Site Preparation (Clearing and Grubbing) Transmission', 'Equipment Cost'])                                                                  
    
    df_temp.loc['Wood Pole: Foundation Installation', 'Equipment Cost'] = df_temp.loc['Wood Pole: Foundation Installation', 'Labor Cost']*(0.28/0.11)
    df_temp.loc['Wood Pole: Top Assembly', 'Equipment Cost'] = df_temp.loc['Wood Pole: Top Assembly', 'Labor Cost']*(0.28/0.11)
    df_temp.loc['Conductor and Cable Distribution', 'Equipment Cost'] =  df_temp.loc['Conductor and Cable Distribution', 'Equipment Cost Per Unit']*df_temp.loc['Conductor and Cable Distribution', 'Job Quantity']
    df_temp.loc['Misc. Assembly Units Distribution', 'Equipment Cost'] = df_temp.loc['Misc. Assembly Units Distribution','Job Quantity']*\
                                                                    (df_temp.loc['Conductor and Cable Distribution', 'Equipment Cost']\
                                                                     +df_temp.loc['Wood Pole: Top Assembly', 'Equipment Cost']\
                                                                     +df_temp.loc['Wood Pole: Foundation Installation', 'Equipment Cost']\
                                                                     +df_temp.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Equipment Cost'])                                                                     
    df_temp['Material Cost Incl OH&P'] = df_temp['Material Cost']
    df_temp['Equipment Cost Incl OH&P'] = df_temp['Equipment Cost']
    
    df_temp.loc['Interconnection Fee Per MW', 'Material Cost'] = df_temp.loc['Interconnection Fee Per MW', 'Material Cost Per Unit']*df_temp.loc['Interconnection Fee Per MW', 'Job Quantity']
    df_temp.loc['Interconnection Fee Per MW', 'Material Cost Incl OH&P'] = (1+overhead_profit_markup)*df_temp.loc['Interconnection Fee Per MW', 'Material Cost']
    
    df_install['Material Cost Incl OH&P'] = (1+overhead_profit_markup)*df_install['Material Cost']
    df_install['Equipment Cost Incl OH&P'] = (1+overhead_profit_markup)*df_install['Equipment Cost']
    df_total_installed_cost=pd.concat([df_temp, df_install], axis=0, sort = False)
    
    df_total_installed_cost['Labor Cost Incl OH&P'] = df_total_installed_cost['ID'].apply(lambda x:(df_labor_weight.loc['Common Laborers', x]*df_wage.loc['Common Laborers','Total Hourly'] +\
        df_labor_weight.loc['Electricians', x]*df_wage.loc['Electricians','Total Hourly']+ \
        df_labor_weight.loc['Equipment Operators', x]*df_wage.loc['Equipment Operators','Total Hourly'])/df_labor_weight[x].sum())  

    df_total_installed_cost=df_total_installed_cost.fillna(0)
    df_total_installed_cost['Labor Cost Incl OH&P'] = df_total_installed_cost['Labor Cost Incl OH&P']*df_total_installed_cost['Job Quantity']*df_total_installed_cost['Labor Hours']
    
    df_total_installed_cost.loc['Tower: Structure Costs','Labor Cost Incl OH&P'] = (1+.33)*df_total_installed_cost.loc['Tower: Structure Costs','Labor Cost']
    df_total_installed_cost.loc['Tower: Foundation Installation','Labor Cost Incl OH&P'] =(1+.33)*df_total_installed_cost.loc['Tower: Foundation Installation','Labor Cost']
    df_total_installed_cost.loc['Tower: Top Assembly','Labor Cost Incl OH&P'] =(1+.33)*df_total_installed_cost.loc['Tower: Top Assembly','Labor Cost']
    df_total_installed_cost.loc['Wood Pole: Structure Costs','Labor Cost Incl OH&P'] =(1+.33)*df_total_installed_cost.loc['Wood Pole: Structure Costs','Labor Cost']
    df_total_installed_cost.loc['Wood Pole: Foundation Installation','Labor Cost Incl OH&P'] =(1+.33)*df_total_installed_cost.loc['Wood Pole: Foundation Installation','Labor Cost']
    df_total_installed_cost.loc['Wood Pole: Top Assembly','Labor Cost Incl OH&P'] = (1+.33)*df_total_installed_cost.loc['Wood Pole: Top Assembly','Labor Cost']
    df_total_installed_cost.loc['Misc. Assembly Units Transmission', 'Labor Cost Incl OH&P'] = df_total_installed_cost.loc['Misc. Assembly Units Transmission','Job Quantity']*\
                                                                    (df_total_installed_cost.loc['Conductor and Cable Transmission', 'Labor Cost Incl OH&P']\
                                                                     +df_total_installed_cost.loc['Tower: Top Assembly', 'Labor Cost Incl OH&P']\
                                                                     +df_total_installed_cost.loc['Tower: Foundation Installation', 'Labor Cost Incl OH&P']\
                                                                     +df_total_installed_cost.loc['Site Preparation (Clearing and Grubbing) Transmission', 'Labor Cost Incl OH&P'])                                                                  
    df_total_installed_cost.loc['Misc. Assembly Units Distribution', 'Labor Cost Incl OH&P'] = df_total_installed_cost.loc['Misc. Assembly Units Distribution','Job Quantity']*\
                                                                    (df_total_installed_cost.loc['Conductor and Cable Distribution', 'Labor Cost Incl OH&P']\
                                                                     +df_total_installed_cost.loc['Wood Pole: Top Assembly', 'Labor Cost Incl OH&P']\
                                                                     +df_total_installed_cost.loc['Wood Pole: Foundation Installation', 'Labor Cost Incl OH&P']\
                                                                     +df_total_installed_cost.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Labor Cost Incl OH&P'])                                                                  
    df_bare_cost = pd.concat([df_total_installed_cost['Material Cost'],df_total_installed_cost['Equipment Cost'],df_total_installed_cost['Labor Cost']],axis=1, sort = False)
    
    trans_dist_list = ['Site Preparation (Clearing and Grubbing) Transmission',
                       'Tower: Foundation Installation',
                       'Tower: Structure Costs',
                       'Tower: Top Assembly',
                       'Conductor and Cable Transmission',
                       'Misc. Assembly Units Transmission',
                       'Site Preparation (Clearing and Grubbing) Distribution',
                       'Wood Pole: Foundation Installation',
                       'Wood Pole: Structure Costs',
                       'Wood Pole: Top Assembly',
                       'Conductor and Cable Distribution',
                       'Misc. Assembly Units Distribution'
                      ]
    
    df_total_installed_cost.loc['Others: engineering and commissioning', 'Labor Cost'] = sum([df_bare_cost.loc[x].sum() for x in trans_dist_list])*(.1/.9)
      
    df_total_installed_cost.loc['Others: engineering and commissioning', 'Labor Cost Incl OH&P'] = (1+0.33)*df_total_installed_cost.loc['Others: engineering and commissioning', 'Labor Cost']
    epc_overhead = ((df_total_installed_cost['Equipment Cost Incl OH&P'].sum()+df_total_installed_cost['Labor Cost Incl OH&P'].sum()+df_total_installed_cost['Material Cost Incl OH&P'].sum())-\
                (df_total_installed_cost['Equipment Cost'].sum()+df_total_installed_cost['Labor Cost'].sum()+df_total_installed_cost['Material Cost'].sum()))/(project_size*1000000)
    
    return epc_overhead, df_total_installed_cost, df_bare_cost, trans_dist_list


def get_permitting_cost(state, df_state, df_inputs, project_size, other_inflation):
    interconnection = df_state.loc[state, ('Building & Electrical PE/Interconnection ($)', 'Utility')]
    
    if df_inputs.loc['Environment Saving?', A].lower()=="no":
        blm_cost = df_state.loc[state, ('BLM Cost', 'Utility')]
    elif df_inputs.loc['Environment Saving?', A].lower()=="yes - low cast":
        blm_cost = df_state.loc[state, ('BLM Cost', 'Utility')]*(1-df_inputs.loc['Environment Permit Reduction', B])
    else:
        blm_cost = df_state.loc[state, ('BLM Cost', 'Utility')]*(1-df_inputs.loc['Environment Permit Reduction', C])
    # print(interconnection, blm_cost)
    #uncertainty_coeff = stat.mean(df_inputs.loc['Permitting Cost', A], df_inputs.loc['Permitting Cost', B], df_inputs.loc['Permitting Cost', C])
    #NEED RAN INPUT ON UNCERTAINTY TAB
    uncertainty_coeff = df_inputs.loc['Permitting Cost', D]
    permitting_cost = ((interconnection + blm_cost)*uncertainty_coeff)/(project_size*1000000)*other_inflation
    # print(project_size, '%.4f' % permitting_cost)
    permitting_cost = np.nan_to_num(permitting_cost)

    return permitting_cost


def get_interconnection_cost(df_utility, df_state, state, other_inflation, project_size, poi, df_inputs):
    df_intercon_fee = lcf.interconnection_fee(df_inputs, df_utility, df_state, state, other_inflation, project_size, poi)
    interconn_cost = float(df_intercon_fee.loc[df_intercon_fee.index[0], 'Job Quantity'])*df_intercon_fee.loc[df_intercon_fee.index[0], 'Material Cost Per Unit']/(project_size*1000000.0)

    return interconn_cost


def get_transmission_cost(df_bare_cost, trans_dist_list, project_size, poi):
    df_bare_cost['Total'] = df_bare_cost['Material Cost']+df_bare_cost['Equipment Cost']+df_bare_cost['Labor Cost']
    transmission_cost = 0
    other_eng = 0
    
    transmission_cost = (sum([df_bare_cost.loc[x,'Total'] for x in trans_dist_list])*(1+(.1/.9)))/(project_size*1000000)
    other_eng = sum([df_bare_cost.loc[x,'Total'] for x in trans_dist_list])*(0.1/0.9)
    
    return transmission_cost, other_eng


def get_contigency_cost(df_inputs, df_bare_cost, other_eng, module_cost, inverter_cost, land_acq_cost, project_size, sales_tax, epc_overhead, permitting_cost):
    if df_inputs.loc['Improved Logistics', A]:
        contigency_percent = 0.015
    else:
        contigency_percent = 0.04
    
    material_cost = df_bare_cost['Material Cost'].sum()+(module_cost + inverter_cost + land_acq_cost)*project_size*1000000
    equipment_cost = df_bare_cost['Equipment Cost'].sum()+other_eng
    labor_cost = df_bare_cost['Labor Cost'].sum()+other_eng
    
    pre_tax_total = material_cost+equipment_cost+labor_cost
    
    total_tax = (material_cost+equipment_cost)*sales_tax 
    total_epc_overhead = epc_overhead*project_size*1000000
    permitting_total = (permitting_cost*project_size*1000000)
    pre_contigency_developer_oh_total = pre_tax_total + total_tax + total_epc_overhead + permitting_total
    
    contigency_cost = pre_contigency_developer_oh_total*contigency_percent/(project_size*1000000)
    
    return contigency_cost, material_cost, equipment_cost, pre_contigency_developer_oh_total


def get_developer_overhead_cost(pre_contigency_developer_oh_total, project_size):
    #NEED RAN INPUT ON NUMBERS
    developer_overhead = 0.3
    developer_overhead_cost = developer_overhead*pre_contigency_developer_oh_total/(project_size*1000000)
    # print(project_size, developer_overhead_cost)
    return developer_overhead_cost


def get_net_profit(df_final,state,project_size, df_profit):
    
    if project_size<5:
        profit_margin = df_profit.loc[5,'Percent']
    elif project_size>100:
        profit_margin = df_profit.loc[100,'Percent']
    else:
        profit_margin = (project_size-5)*(df_profit.loc[100,'Percent']-df_profit.loc[5,'Percent'])/(100-5)+df_profit.loc[5,'Percent']
    
    net_profit = df_final[state].sum()*profit_margin

    return net_profit


def get_total_cost(df_final, state):
    total_cost = df_final[state].sum()
    
    return total_cost