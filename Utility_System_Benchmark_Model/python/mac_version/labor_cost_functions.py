import pandas as pd
import numpy as np
import matplotlib as plt
import inverter as inv
import statistics as stat

#Create variables for column header strings
A = 'Value A'
B = 'Value B'
C = 'Value C'
D = 'Value D'

def material_bare_cost(description, df_state, df_utility, state):
    material_location_factor = float(df_state.loc[state, ('Location Factor', 'Material')])/100
    material_bare_no_location = df_utility.loc[description,'Material Bare Cost']
    material_bare_cost = material_location_factor*material_bare_no_location 
    return material_bare_cost

def equipment_bare_cost(description, df_state, df_utility, state):
    equip_location_factor = float(df_state.loc[state, ('Location Factor', 'Equipment')])/100
    equip_bare_no_location = df_utility.loc[description,'Equipment Bare Cost']
    equip_bare_cost = equip_location_factor*equip_bare_no_location 
    return equip_bare_cost

def preconstruction_surveys(df_utility, df_inputs, df_state, num_modules, project_size, state, inflation):
    df_pre_sur = pd.DataFrame(index=['Preconstruction Surveys'])
    if df_inputs.loc['Tracker?', A]:
        #NEED RAN INPUT ON NUMBERS
        average = 6.7*(num_modules/(3436*project_size))
    else:
        average = 5.8*(num_modules/(3436*project_size))
        
    if df_inputs.loc['Fixed Acreage ?', A]:
        pre_job = df_inputs.loc['Fixed Acreage ?', B]
    else:
        if df_inputs.loc['Thin Film?', A]:
            #NEED RAN INPUT ON THE NUMBERS
            pre_job = average*project_size*(295/81.25*0.72/1.94)
        else:
            pre_job = average*project_size
    
    if df_inputs.loc['Environment Saving?', A].lower()=='no':
        env = 1
    elif df_inputs.loc['Environment Saving?', A].lower()=='yes - low cast':
        env = 1-df_inputs.loc['Environment Land Acquisition', B]
    else:
        env = 1-df_inputs.loc['Environment Land Acquisition', C]
        
    df_pre_sur['Job Quantity'] = pre_job*env
    df_pre_sur['Labor Hours'] = df_utility.loc['Preconstruction Surveys','Labor Hours']
    df_pre_sur['Material Cost Per Unit'] = material_bare_cost('Preconstruction Surveys', df_state, df_utility, state)*inflation
    df_pre_sur['Equipment Cost Per Unit'] = equipment_bare_cost('Preconstruction Surveys', df_state, df_utility, state)*inflation
    return df_pre_sur

def access_roads_and_parking(df_utility, df_state, project_size, state, inflation, df_pre_sur):
    df_acc_roa = pd.DataFrame(index=['Access Roads and Parking'])
    if project_size<5:
        average = 0.05
    elif project_size>100:
        average = 0.01
    else:
        average = (100.0-project_size)*0.04/95+0.01
    
    preconstruct_job_quant = df_pre_sur.loc['Preconstruction Surveys','Job Quantity']
    
    #NEED RAN INPUT ON NUMBER
    df_acc_roa['Job Quantity'] = preconstruct_job_quant*average*4840.0
    df_acc_roa['Labor Hours'] = df_utility.loc['Access Roads and Parking','Labor Hours']
    df_acc_roa['Material Cost Per Unit'] = material_bare_cost('Access Roads and Parking', df_state, df_utility, state)*inflation
    df_acc_roa['Equipment Cost Per Unit'] = equipment_bare_cost('Access Roads and Parking', df_state, df_utility, state)*inflation
    
    return df_acc_roa

def security_fencing(df_utility, df_pre_sur, df_state, inflation, state):
    df_sec_fen = pd.DataFrame(index=['Security Fencing'])
    
    preconstruct_job_quant = df_pre_sur.loc['Preconstruction Surveys','Job Quantity']
    
    df_sec_fen['Job Quantity'] = (preconstruct_job_quant*43560.0)**(0.5)*4.0 #43560 is acre to sq ft conversion
    df_sec_fen['Labor Hours'] = df_utility.loc['Security Fencing','Labor Hours']
    df_sec_fen['Material Cost Per Unit'] = material_bare_cost('Security Fencing', df_state, df_utility, state)*inflation
    df_sec_fen['Equipment Cost Per Unit'] = equipment_bare_cost('Security Fencing', df_state, df_utility, state)*inflation
    return df_sec_fen

def temp_office(df_utility, df_state, inflation, state):
    df_tem_off = pd.DataFrame(index=['Temporary Office'])
    df_tem_off['Job Quantity'] = float(df_utility.loc['Temporary Office','Job Quantity'])
    df_tem_off['Labor Hours'] = float(df_utility.loc['Temporary Office','Labor Hours'])
    df_tem_off['Material Cost Per Unit'] = material_bare_cost('Temporary Office', df_state, df_utility, state)*inflation
    df_tem_off['Equipment Cost Per Unit'] = equipment_bare_cost('Temporary Office', df_state, df_utility, state)*inflation
    return df_tem_off

def storage_box(df_utility, df_state, num_modules, inflation, state, project_size):
    df_sto_box = pd.DataFrame(index=['Storage Box'])
    if project_size<5:
        average = 3.0
    elif project_size>100:
        average = 1.0
    else:
        average = (100.0-project_size)*2.0/95.0+1.0
        
    #NEED RAN INPUT ON NUMBERS    
    df_sto_box['Job Quantity'] = (num_modules/3436.43)*average
    df_sto_box['Labor Hours'] = df_utility.loc['Storage Box','Labor Hours']
    df_sto_box['Material Cost Per Unit'] = material_bare_cost('Storage Box', df_state, df_utility, state)*inflation
    df_sto_box['Equipment Cost Per Unit'] = equipment_bare_cost('Storage Box', df_state, df_utility, state)*inflation
    return df_sto_box

def om_building(df_utility, df_state, inflation, state):
    df_om_build = pd.DataFrame(index=['O & M Building'])
    df_om_build['Job Quantity'] = float(df_utility.loc['O & M Building','Job Quantity'])
    df_om_build['Labor Hours'] = float(df_utility.loc['O & M Building','Labor Hours'])
    df_om_build['Material Cost Per Unit'] = material_bare_cost('O & M Building', df_state, df_utility, state)*inflation
    df_om_build['Equipment Cost Per Unit'] = equipment_bare_cost('O & M Building', df_state, df_utility, state)*inflation
    return df_om_build

def site_prep(df_inputs, df_utility, df_state, df_inv_calc, inflation, state, df_pre_sur):
    #### STILL NEEDS WORK WITH THE 600,1500 V thing
    df_site_prep = pd.DataFrame(index=['Site Preparation (Geotechnical Investigation)','Site Preparation (Clearing and Grubbing)',
                                      'Site Preparation (Soil Stripping and stockpiling)', 'Site Preparation (Grading)','Site Preparation (Compaction)'])
    acre = df_pre_sur.loc['Preconstruction Surveys','Job Quantity']
    avg = 1.0
    if df_inputs.loc['Environment Saving?', A].lower()=='no':
        env = acre*avg
    elif df_inputs.loc['Environment Saving?', A].lower()=='yes - low cast':
        env = acre*avg*(1.0-df_inputs.loc['Environment Land Acquisition', B])
    else:
        env = acre*avg*(1.0-df_inpus.loc['Environment Land Acquisition', C])
        
    combiner_box = df_inv_calc.loc[('Combiner Box', 'Combiner box #'),'SC 2500']/df_inv_calc.loc[('Combiner Box', 'Combiner box #'),'720CP-US']-1


    if df_inputs.loc['Medium Voltage DC Plant (MWDC) ?',A]=="TRUE":
        df_site_prep.loc['Site Preparation (Geotechnical Investigation)','Job Quantity'] = env*(df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', B])
        df_site_prep.loc['Site Preparation (Clearing and Grubbing)','Job Quantity'] = env*(df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', B])
        if df_inputs.loc['System VDC',A] == 1000.0:
            df_site_prep.loc['Site Preparation (Soil Stripping and stockpiling)','Job Quantity'] = env*0.2*4840.0*1
            df_site_prep.loc['Site Preparation (Grading)','Job Quantity'] = env*4840
            df_site_prep.loc['Site Preparation (Compaction)','Job Quantity'] = env*0.23*4840
        else:
            df_site_prep.loc['Site Preparation (Soil Stripping and stockpiling)','Job Quantity'] = env*0.2*4840.0*(df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', B])
            df_site_prep.loc['Site Preparation (Grading)','Job Quantity'] = env*4840.0*(df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', B])
            df_site_prep.loc['Site Preparation (Compaction)','Job Quantity'] = env*0.23*4840.0*(df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', B])
    else:
        df_site_prep.loc['Site Preparation (Geotechnical Investigation)','Job Quantity'] = env
        df_site_prep.loc['Site Preparation (Clearing and Grubbing)','Job Quantity'] = env
        if df_inputs.loc['System VDC',A] == 1000.0:
            df_site_prep.loc['Site Preparation (Soil Stripping and stockpiling)','Job Quantity'] = env*0.2*4840.0
            df_site_prep.loc['Site Preparation (Grading)','Job Quantity'] = env*4840.0
            df_site_prep.loc['Site Preparation (Compaction)','Job Quantity'] = env*0.23*4840
        else:
            df_site_prep.loc['Site Preparation (Soil Stripping and stockpiling)','Job Quantity'] = env*0.2*4840.0*(1+combiner_box)
            df_site_prep.loc['Site Preparation (Grading)','Job Quantity'] = env*4840.0*(1+combiner_box)
            df_site_prep.loc['Site Preparation (Compaction)','Job Quantity'] = env*0.23*4840.0*(1+combiner_box)
    
    df_site_prep['Labor Hours'] = df_site_prep.apply(lambda x:df_utility.loc[x.name,'Labor Hours'], axis=1)
    df_site_prep['Material Cost Per Unit'] = df_site_prep.apply(lambda x:material_bare_cost(x.name, df_state, df_utility, state)*inflation, axis=1)
    df_site_prep['Equipment Cost Per Unit'] = df_site_prep.apply(lambda x:equipment_bare_cost(x.name, df_state, df_utility, state)*inflation, axis=1)
    
    return df_site_prep

def foundation_inverter(df_utility, project_size, df_inputs, df_inv_calc, df_state, inflation, state):
    inverter_1000 = df_inv_calc.loc[('Inverter', 'Inverter #'),'720CP-US']/df_inv_calc.loc[('Inverter', 'Inverter #'),'500CP-US 600V']-1
    inverter_1500 = df_inv_calc.loc[('Inverter', 'Inverter #'),'SC 2500']/df_inv_calc.loc[('Inverter', 'Inverter #'),'500CP-US 600V']-1

    df_fou_inv = pd.DataFrame(index=['Foundation for inverter/transformer/PVCS/Substation'])
    if df_inputs.loc['System VDC',A] == 600.0:
        df_fou_inv['Job Quantity'] = project_size/1.2*100+1000
    elif df_inputs.loc['System VDC',A] == 1000.0:
        df_fou_inv['Job Quantity'] = project_size/1.2*100*(1.0+inverter_1000)+1000.0
    else:
        df_fou_inv['Job Quantity'] = project_size/1.2*100*(1.0+inverter_1500)+1000.0
            
    df_fou_inv['Labor Hours'] = df_utility.loc['Foundation for inverter/transformer/PVCS/Substation','Labor Hours']
    df_fou_inv['Material Cost Per Unit'] = material_bare_cost('Foundation for inverter/transformer/PVCS/Substation', df_state, df_utility, state)*inflation
    df_fou_inv['Equipment Cost Per Unit'] = equipment_bare_cost('Foundation for inverter/transformer/PVCS/Substation', df_state, df_utility, state)*inflation
    
    return df_fou_inv

def trenches(df_utility,project_size, num_modules, df_inputs, df_inv_calc, df_state, inflation, state):
    string_1000 = df_inv_calc.loc[('Strings', 'String #'),'720CP-US']/df_inv_calc.loc[('Strings', 'String #'),'500CP-US 600V']-1
    string_1500 = df_inv_calc.loc[('Strings', 'String #'),'SC 2500']/df_inv_calc.loc[('Strings', 'String #'),'500CP-US 600V']-1
    df_trenches = pd.DataFrame(index=['Trenches'])
    
    if project_size<5:
        average = 5000.0
    elif project_size>100:
        average = 2000.0
    else:
        average = (100.0-project_size)*3000.0/95.0+2000.0
    
    if df_inputs.loc['Medium Voltage DC Plant (MWDC) ?',A]:        
        if df_inputs.loc['System VDC',A] == 600.0:
            df_trenches['Job Quantity'] = average*num_modules/3426.43*(0.25/0.67)
        elif df_inputs.loc['System VDC',A] == 1000.0:
            df_trenches['Job Quantity'] = average*num_modules/3426.43*(0.25/0.67)*(1+string_1000)
        else:
            df_trenches['Job Quantity'] = average*num_modules/3426.43*(0.25/0.67)*(1+string_1500)
    else:
        if df_inputs.loc['System VDC',A] == 600.0:
            df_trenches['Job Quantity'] = average*num_modules/3426.43
        elif df_inputs.loc['System VDC',A] == 1000.0:
            df_trenches['Job Quantity'] = average*num_modules/3426.43*(1+string_1000)
        else:
            df_trenches['Job Quantity'] = average*num_modules/3426.43*(1+string_1500)
    
    df_trenches['Labor Hours'] = df_utility.loc['Trenches','Labor Hours']
    df_trenches['Material Cost Per Unit'] = material_bare_cost('Trenches', df_state, df_utility, state)*inflation
    df_trenches['Equipment Cost Per Unit'] = equipment_bare_cost('Trenches', df_state, df_utility, state)*inflation
    
    return df_trenches

def foundation_vertical_support(df_utility, df_inputs, df_bom, project_size, inflation, df_state, steel_inflation, df_pipe, state):
    df_found_vert_supp = pd.DataFrame(index=['Foundation for Vertical Support'])
    if df_inputs.loc['System VDC',A] == 1000.0:
        df_found_vert_supp['Job Quantity'] = df_bom.loc[('Column', 'Est. Column Length (ft)'), 'Fixed-Tilt']       
    elif df_inputs.loc['Medium Voltage DC Plant (MWDC) ?',A]:
        #NEED RAN INPUT ON NUMBER
        df_found_vert_supp['Job Quantity'] = df_bom.loc[('Column', 'Est. Column Length (ft)'), 'Fixed-Tilt']*0.7 
    else:
        #NEED RAN INPUT ON NUMBER
        df_found_vert_supp['Job Quantity'] = df_bom.loc[('Column', 'Est. Column Length (ft)'), 'Fixed-Tilt']*0.8
    
    df_found_vert_supp['Labor Hours'] = df_utility.loc['Foundation for Vertical Support','Labor Hours']
    
    if project_size<5:
        size_factor = 1.0
    elif project_size>100:
        size_factor = 0.8
    else:
        size_factor = (100.0-project_size)*.2/95.0+0.8
    
    df_found_vert_supp['Material Cost Per Unit']= size_factor*df_pipe.loc[df_inputs.loc['Column',A],'2012 Price ($/ft)']*steel_inflation*float(df_state.loc[state, ('Location Factor', 'Material')])/100
    df_found_vert_supp['Equipment Cost Per Unit'] = equipment_bare_cost('Foundation for Vertical Support', df_state, df_utility, state)*inflation
    
    return df_found_vert_supp, size_factor

def horizontal_support(df_utility, df_inputs, df_bom, inflation, df_state, steel_inflation, df_torque_tube, state, size_factor):
    df_hor_supp = pd.DataFrame(index=['Horizontal Support Structures'])
    df_hor_supp['Job Quantity'] = df_bom.loc[('Tubing', 'Est. Tubing Length (ft)'), 'Fixed-Tilt']/12
    df_hor_supp['Labor Hours'] = df_utility.loc['Horizontal Support Structures','Labor Hours']       
    df_hor_supp['Material Cost Per Unit']= size_factor*df_torque_tube.loc[df_inputs.loc['Tubing',A],'2012 Price ($/ft)']*steel_inflation*12*float(df_state.loc[state, ('Location Factor', 'Material')])/100
    df_hor_supp['Equipment Cost Per Unit'] = equipment_bare_cost('Horizontal Support Structures', df_state, df_utility, state)*inflation

    return df_hor_supp

def welding_or_bolting(df_utility, df_inputs, df_bom, inflation, df_state, state):
    df_weld_bolt = pd.DataFrame(index=['Welding or Bolting'])
    df_weld_bolt['Job Quantity'] = (1*df_bom.loc[('Column', 'Est. Number of Columns'), 'Fixed-Tilt'])+(0.5*df_bom.loc[('Tubing', 'Est. Tubing Length (ft)'), 'Fixed-Tilt']/20)
    df_weld_bolt['Labor Hours'] = df_utility.loc['Welding or Bolting','Labor Hours']
    df_weld_bolt['Material Cost Per Unit'] = material_bare_cost('Welding or Bolting', df_state, df_utility, state)*inflation
    df_weld_bolt['Equipment Cost Per Unit'] = equipment_bare_cost('Welding or Bolting', df_state, df_utility, state)*inflation
    
    return df_weld_bolt

def modules_mounting(df_utility, df_inputs, df_bom, inflation, df_state, num_modules, state, df_rail_clamp, steel_inflation, size_factor):
    df_mod_mount = pd.DataFrame(index=['Modules Mounting'])
    uncertainty_coeff = df_inputs.loc['Coefficiency Uncertainty', A]
    #ERROR IN SPREADSHEET FOR HOW UNCERTAINTIES ARE CALCULATED
    # design_con_mean = stat.mean([float(df_inputs.loc['Design Conservatism Factor', A]), float(df_inputs.loc['Design Conservatism Factor', B]), float(df_inputs.loc['Design Conservatism Factor', C])])
    design_con_mean = df_inputs.loc['Design Conservatism Factor', D]
    df_mod_mount['Job Quantity'] = num_modules
       
    if df_inputs.loc['Glue for large module ?', A]:
        df_mod_mount['Labor Hours'] = df_utility.loc['Modules Mounting (Large)','Labor Hours']
        df_mod_mount['Material Cost Per Unit'] = 4*0.1+4*0.12*size_factor
    else:
        df_mod_mount['Labor Hours'] = df_utility.loc['Modules Mounting','Labor Hours']
        df_mod_mount['Material Cost Per Unit'] = df_rail_clamp.loc[df_inputs.loc['Clamp',A],'2012 Price ($/ft)']*steel_inflation*float(df_state.loc[state, ('Location Factor', 'Material')])/100*1.5*3*design_con_mean*uncertainty_coeff/0.75*size_factor
    
    df_mod_mount['Equipment Cost Per Unit'] = equipment_bare_cost('Modules Mounting', df_state, df_utility, state)*inflation
    
    return df_mod_mount

def t_connection(df_utility, df_bom, inflation, df_state, state, size_factor):
    df_t_conn = pd.DataFrame(index=['T- Connection'])
    df_t_conn['Job Quantity'] = df_bom.loc[('T - Connection', 'Est. Number of T-Connections'), 'Fixed-Tilt']
    df_t_conn['Labor Hours'] = df_utility.loc['T- Connection','Labor Hours']
        
    df_t_conn['Material Cost Per Unit'] = df_bom.loc[('T - Connection', 'Est. Connection Total Cost ($)'), 'Fixed-Tilt']/df_bom.loc[('T - Connection', 'Est. Number of T-Connections'), 'Fixed-Tilt']* \
                                            float(df_state.loc[state, ('Location Factor', 'Material')])/100*1.2*size_factor
    df_t_conn['Equipment Cost Per Unit'] = equipment_bare_cost('T- Connection', df_state, df_utility, state)*inflation
    
    return df_t_conn

def ujoint_driveline(df_inputs,df_utility,df_state, num_modules, inflation, state, size_factor):
    df_ujoint = pd.DataFrame(index=['U-Joint & Driveline'])
    if df_inputs.loc['Tracker?', A]:
        #NEED RAN INPUT ON NUMER
        df_ujoint['Job Quantity'] = num_modules/54
    else:
        df_ujoint['Job Quantity'] = 0
        
    df_ujoint['Labor Hours'] = df_utility.loc['U-Joint & Driveline','Labor Hours']
    
    df_ujoint['Material Cost Per Unit'] = material_bare_cost('U-Joint & Driveline', df_state, df_utility, state)*inflation*size_factor
    df_ujoint['Equipment Cost Per Unit'] = equipment_bare_cost('U-Joint & Driveline', df_state, df_utility, state)*inflation
    return df_ujoint

def slave_gearbox(df_utility, df_inputs,inflation, df_state, state, num_modules, size_factor):
    df_slav_gear = pd.DataFrame(index=['Slave Gearbox'])
    if df_inputs.loc['Tracker?', A]:
        #NEED RAN INPUT ON NUMER
        df_slav_gear['Job Quantity'] = num_modules/54
    else:
        df_slav_gear['Job Quantity'] = 0
        
    df_slav_gear['Labor Hours'] = df_utility.loc['Slave Gearbox','Labor Hours']
       
    df_slav_gear['Material Cost Per Unit'] = df_utility.loc['Slave Gearbox','Material Bare Cost']*inflation*size_factor
    df_slav_gear['Equipment Cost Per Unit'] = equipment_bare_cost('Slave Gearbox', df_state, df_utility, state)*inflation
    return df_slav_gear

def motor_controller_equip(df_utility, df_inputs,inflation, df_state, state, num_modules, size_factor):
    df_mc_equip = pd.DataFrame(index=['Motor & Controller Equipment'])
    if df_inputs.loc['Tracker?', A]:
        #NEED RAN INPUT ON NUMER
        df_mc_equip['Job Quantity'] = num_modules/54/20
    else:
        df_mc_equip['Job Quantity'] = 0
        
    df_mc_equip['Labor Hours'] = df_utility.loc['Motor & Controller Equipment','Labor Hours']
      
    df_mc_equip['Material Cost Per Unit'] = df_utility.loc['Motor & Controller Equipment','Material Bare Cost']*inflation*size_factor
    df_mc_equip['Equipment Cost Per Unit'] = equipment_bare_cost('Motor & Controller Equipment', df_state, df_utility, state)*inflation
    return df_mc_equip


############ ELECTRICAL ############

def conduit_wiring(df_structural_bos, df_utility, inflation, df_state, state, size_factor):
    df_cond_wire = pd.DataFrame(index=['Conduit, Wiring'])
    df_cond_wire['Job Quantity'] = df_structural_bos.loc['Trenches','Job Quantity']
    df_cond_wire['Labor Hours'] = df_utility.loc['Conduit, Wiring', 'Labor Hours']
    df_cond_wire['Material Cost Per Unit'] = material_bare_cost('Conduit, Wiring', df_state, df_utility, state)*inflation*size_factor
    df_cond_wire['Equipment Cost Per Unit'] = equipment_bare_cost('Conduit, Wiring', df_state, df_utility, state)*inflation
    
    return df_cond_wire

def grounding_cable(df_structural_bos, df_bom, df_utility, inflation, df_state, state, size_factor):
    df_ground = pd.DataFrame(index=['Grounding, DC Cable'])
    df_ground['Job Quantity'] = df_structural_bos.loc['Trenches','Job Quantity']/100+df_bom.loc[('Tubing','Est. Tubing Length (ft)'),'Fixed-Tilt']/100
    df_ground['Labor Hours'] = df_utility.loc['Grounding, DC Cable', 'Labor Hours']
    df_ground['Material Cost Per Unit'] = material_bare_cost('Grounding, DC Cable', df_state, df_utility, state)*inflation*size_factor
    df_ground['Equipment Cost Per Unit'] = equipment_bare_cost('Grounding, DC Cable', df_state, df_utility, state)*inflation
    
    return df_ground

def junction_box(df_inv_calc, df_inputs, df_utility, df_state, state, inflation, size_factor, num_modules):
    df_junc = pd.DataFrame(index=['Junction/Combiner Boxes'])

    inverter_1000 = df_inv_calc.loc[('Combiner Box','Combiner box #'),'720CP-US']/df_inv_calc.loc[('Combiner Box','Combiner box #'),'500CP-US 600V']-1
    inverter_1500 = df_inv_calc.loc[('Combiner Box','Combiner box #'),'SC 2500']/df_inv_calc.loc[('Combiner Box','Combiner box #'),'500CP-US 600V']-1
    if df_inputs.loc['System VDC',A] == 600.0:
        inverter_factor = 1
    elif df_inputs.loc['System VDC',A] == 1000.0:
        inverter_factor = 1+inverter_1000
    else:
        inverter_factor = 1+inverter_1500
    
    df_junc['Job Quantity'] = num_modules/12/12*inverter_factor
    df_junc['Labor Hours'] = df_utility.loc['Junction/Combiner Boxes', 'Labor Hours']
    df_junc['Material Cost Per Unit'] = material_bare_cost('Junction/Combiner Boxes', df_state, df_utility, state)*inflation*size_factor
    df_junc['Equipment Cost Per Unit'] = equipment_bare_cost('Junction/Combiner Boxes', df_state, df_utility, state)*inflation
    
    return df_junc

def inverter_house(df_inv_calc, df_inputs, df_utility, df_state, state, inflation, project_size):
    df_inv_house = pd.DataFrame(index=['Inverter House'])
    inverter_1000 = df_inv_calc.loc[('Inverter','Inverter #'),'720CP-US']/df_inv_calc.loc[('Inverter','Inverter #'),'500CP-US 600V']-1
    inverter_1500 = df_inv_calc.loc[('Inverter','Inverter #'),'SC 2500']/df_inv_calc.loc[('Inverter','Inverter #'),'500CP-US 600V']-1
    if df_inputs.loc['System VDC',A] == 600.0:
        inverter_factor = 1
    elif df_inputs.loc['System VDC',A] == 1000.0:
        inverter_factor = 1+inverter_1000
    else:
        inverter_factor = 1+inverter_1500
    
    if df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', A]:
        df_inv_house['Job Quantity'] = 1
    else:
        #NEED RAN INPUT ON NUMBER
        df_inv_house['Job Quantity'] = project_size/1.1*inverter_factor
    
    df_inv_house['Labor Hours'] = df_utility.loc['Inverter House', 'Labor Hours']
    df_inv_house['Material Cost Per Unit'] = material_bare_cost('Inverter House', df_state, df_utility, state)*inflation
    df_inv_house['Equipment Cost Per Unit'] = equipment_bare_cost('Inverter House', df_state, df_utility, state)*inflation
    
    return df_inv_house

def onsite_transmission(df_inv_house, df_utility, df_state, state, inflation):
    df_onsite_trans = pd.DataFrame(index=['On-site Transmission'])
    df_onsite_trans['Job Quantity'] = df_inv_house.loc[df_inv_house.index[0],'Job Quantity']
    df_onsite_trans['Labor Hours'] = df_utility.loc['On-site Transmission', 'Labor Hours']
    df_onsite_trans['Material Cost Per Unit'] = material_bare_cost('On-site Transmission', df_state, df_utility, state)*inflation
    df_onsite_trans['Equipment Cost Per Unit'] = equipment_bare_cost('On-site Transmission', df_state, df_utility, state)*inflation
    
    return df_onsite_trans

def pv_combining_switchgear(df_inputs, df_utility, df_state, state, inflation):
    df_pvcs=pd.DataFrame(index=['PV Combining Switchgear (PVCS)'])
    
    if df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', A]:
        df_pvcs['Job Quantity'] = 0
    else:
        #NEED RAN INPUT ON NUMBER
        df_pvcs['Job Quantity'] = 1
    
    df_pvcs['Labor Hours'] = df_utility.loc['PV Combining Switchgear (PVCS)', 'Labor Hours']
    df_pvcs['Material Cost Per Unit'] = material_bare_cost('PV Combining Switchgear (PVCS)', df_state, df_utility, state)*inflation
    df_pvcs['Equipment Cost Per Unit'] = equipment_bare_cost('PV Combining Switchgear (PVCS)', df_state, df_utility, state)*inflation
    
    return df_pvcs

def onsite_transformer_substation(df_inputs, df_utility, df_state, state, inflation, df_inv_calc, project_size, size_factor):
    df_onsite_subs =pd.DataFrame(index=['On-site transformer & Substation'])
    #NEED RAN INPUT ON NUMBER
    if df_inputs.loc['System VDC', A]==1500:
        if df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', A]:
            df_onsite_subs['Job Quantity'] = 0.3*0 + 0.7*0.75
        else:
            df_onsite_subs['Job Quantity'] = 0.3*(df_inv_calc.loc[('Inverter','Inverter #'),'SC 2500']/df_inv_calc.loc[('Inverter','Inverter #'),'720CP-US']) + 0.7*1
    else:
        if df_inputs.loc['Medium Voltage DC Plant (MWDC) ?', A]:
            df_onsite_subs['Job Quantity'] = 0.3*1 + 0.7*0.75
        else:
            df_onsite_subs['Job Quantity'] = 0.3*1 + 0.7*1
            
    df_onsite_subs['Labor Hours'] = df_utility.loc['On-site transformer & Substation', 'Labor Hours']
    #NEED RAN INPUT ON NUMBER
#     substation_cost_factor = stat.mean([df_inputs.loc['Substation Cost', A], df_inputs.loc['Substation Cost', B], df_inputs.loc['Substation Cost', C]])
    substation_cost_factor = df_inputs.loc['Substation Cost', D]
    
    df_onsite_subs['Material Cost Per Unit'] = ((1240674.0-247620.0)/19.0+2540000.0/27.0)/2.0*project_size*size_factor*inflation* \
                                        substation_cost_factor* \
                                        float(df_state.loc[state, ('Location Factor', 'Material')])/100
    
    df_onsite_subs['Equipment Cost Per Unit'] = equipment_bare_cost('On-site transformer & Substation', df_state, df_utility, state)*inflation
    
    return df_onsite_subs

def site_prep_transmission(df_inputs, df_utility, df_state, state, inflation, project_size, path):
    df_site_prep_trans =pd.DataFrame(index=['Site Preparation (Clearing and Grubbing) Transmission'])
    df_trans = pd.read_excel(path + '/input_data/Overhead.xlsx', sheetname='Transmission Line', index_col=0)
    trans_min = df_trans.index[0]
    trans_max = df_trans.index[1]
    if project_size<trans_min:
        transmission_len = df_trans.loc[trans_min,'Mile']
    elif project_size>trans_max:
        transmission_len = df_trans.loc[trans_max,'Mile']
    else:
        transmission_len = (project_size-trans_min)*(df_trans.loc[trans_max,'Mile']-df_trans.loc[trans_min,'Mile'])/(trans_max-trans_min)+df_trans.loc[trans_min,'Mile']
    
#     transmission_line_factor = stat.mean([df_inputs.loc['Transmission line distance (mode=0.5 mile)', A], df_inputs.loc['Transmission line distance (mode=0.5 mile)', B], df_inputs.loc['Transmission line distance (mode=0.5 mile)', C]])
    transmission_line_factor = df_inputs.loc['Transmission line distance (mode=0.5 mile)', D]
    
    if df_inputs.loc['Transmission?', A]:
        #NEED RAN INPUT ON NUMBERS AND MEAN OF UNCERTAINTY ANALYSIS
        df_site_prep_trans['Job Quantity']=68.33*4/5*transmission_len/5*transmission_line_factor                                        
    else:
        df_site_prep_trans['Job Quantity']=0*transmission_len/5
        
    df_site_prep_trans['Labor Hours'] = df_utility.loc['Site Preparation (Clearing and Grubbing) Transmission', 'Labor Hours']
    df_site_prep_trans['Material Cost Per Unit'] = material_bare_cost('Site Preparation (Clearing and Grubbing) Transmission', df_state, df_utility, state)*inflation
    df_site_prep_trans['Equipment Cost Per Unit'] = equipment_bare_cost('Site Preparation (Clearing and Grubbing) Transmission', df_state, df_utility, state)*inflation
    
    return df_site_prep_trans, transmission_len, transmission_line_factor

def tower_foundation_installation(transmission_len, df_inputs, transmission_line_factor):
    df_tower_found =pd.DataFrame(index=['Tower: Foundation Installation'])
    
    if df_inputs.loc['Transmission?', A]:
        #NEED RAN INPUT ON NUMBERS AND MEAN OF UNCERTAINTY ANALYSIS
        df_tower_found['Job Quantity']=60*8*transmission_len/5*transmission_line_factor
    else:
        df_tower_found['Job Quantity']=0*transmission_len/5
    
    df_tower_found['Labor Hours'] = float('nan')
    df_tower_found['Material Cost Per Unit'] = float('nan')
    df_tower_found['Equipment Cost Per Unit'] = float('nan')
    
    return df_tower_found

def tower_structure_costs(transmission_len, df_inputs, df_utility, transmission_line_factor):
    df_tower_struct =pd.DataFrame(index=['Tower: Structure Costs'])
    
    if df_inputs.loc['Transmission?', A]:
        #NEED RAN INPUT ON NUMBERS AND MEAN OF UNCERTAINTY ANALYSIS
        df_tower_struct['Job Quantity']=4*10*transmission_len/5*transmission_line_factor
    else:
        df_tower_struct['Job Quantity']=0*transmission_len/5
    
    df_tower_struct['Labor Hours'] = df_utility.loc['Tower: Structure Costs', 'Labor Hours']
    df_tower_struct['Material Cost Per Unit'] = float('nan')
    df_tower_struct['Equipment Cost Per Unit'] = float('nan')
    
    return df_tower_struct

def tower_top_assembly(transmission_len, df_inputs, df_utility, transmission_line_factor):
    df_tower_top =pd.DataFrame(index=['Tower: Top Assembly'])
      
    if df_inputs.loc['Transmission?', A]:
        #NEED RAN INPUT ON NUMBERS AND MEAN OF UNCERTAINTY ANALYSIS
        df_tower_top['Job Quantity']=200*8*transmission_len/5*transmission_line_factor
    else:
        df_tower_top['Job Quantity']=0*transmission_len/5
    
    df_tower_top['Labor Hours'] = df_utility.loc['Tower: Top Assembly', 'Labor Hours']
    df_tower_top['Material Cost Per Unit'] = float('nan')
    df_tower_top['Equipment Cost Per Unit'] = float('nan')
    
    return df_tower_top

def conductor_cable_transmission(transmission_len, df_inputs, df_utility, transmission_line_factor, df_state, state, inflation):
    df_cond_trans =pd.DataFrame(index=['Conductor and Cable Transmission'])
  
    if df_inputs.loc['Transmission?', A]:
        #NEED RAN INPUT ON NUMBERS AND MEAN OF UNCERTAINTY ANALYSIS
        df_cond_trans['Job Quantity']=4*5280*transmission_len/5*0.5*transmission_line_factor
    else:
        df_cond_trans['Job Quantity']=0*transmission_len/5
    
    df_cond_trans['Labor Hours'] = df_utility.loc['Conductor and Cable Transmission', 'Labor Hours']
    df_cond_trans['Material Cost Per Unit'] = material_bare_cost('Conductor and Cable Transmission', df_state, df_utility, state)*inflation
    df_cond_trans['Equipment Cost Per Unit'] = equipment_bare_cost('Conductor and Cable Transmission', df_state, df_utility, state)*inflation
    
    return df_cond_trans

def misc_assembly_transmission(df_utility):
    df_misc_trans =pd.DataFrame(index=['Misc. Assembly Units Transmission'])
    
    df_misc_trans['Job Quantity']=float(df_utility.loc['Misc. Assembly Units Transmission', 'Job Quantity'].strip('%'))/100
    df_misc_trans['Labor Hours'] = float('nan')
    df_misc_trans['Material Cost Per Unit'] = float('nan')
    df_misc_trans['Equipment Cost Per Unit'] = float('nan')
    
    return df_misc_trans

def site_prep_distribution(transmission_len, df_inputs, df_utility, transmission_line_factor, df_state, state, inflation):
    df_site_prep_dist =pd.DataFrame(index=['Site Preparation (Clearing and Grubbing) Distribution'])

    if df_inputs.loc['Transmission?', A]:
        #NEED RAN INPUT ON NUMBERS AND MEAN OF UNCERTAINTY ANALYSIS
        df_site_prep_dist['Job Quantity']=68.33*1/5*transmission_len/5*transmission_line_factor
    else:
        df_site_prep_dist['Job Quantity']=0*transmission_len/5
    
    df_site_prep_dist['Labor Hours'] = df_utility.loc['Site Preparation (Clearing and Grubbing) Distribution', 'Labor Hours']
    df_site_prep_dist['Material Cost Per Unit'] = material_bare_cost('Site Preparation (Clearing and Grubbing) Distribution', df_state, df_utility, state)*inflation
    df_site_prep_dist['Equipment Cost Per Unit'] = equipment_bare_cost('Site Preparation (Clearing and Grubbing) Distribution', df_state, df_utility, state)*inflation
    
    return df_site_prep_dist

def wood_pole_foundation_installation(df_tower_found, transmission_len):
    df_wood_found =pd.DataFrame(index=['Wood Pole: Foundation Installation'])
    
    df_wood_found['Job Quantity']=df_tower_found.loc[df_tower_found.index[0], 'Job Quantity']*(1/5)*transmission_len/5
    df_wood_found['Labor Hours'] = float('nan')
    df_wood_found['Material Cost Per Unit'] = float('nan')
    df_wood_found['Equipment Cost Per Unit'] = float('nan')
    
    return df_wood_found

def wood_pole_structure_costs(transmission_len, df_inputs, df_utility, transmission_line_factor):
    df_wood_struct =pd.DataFrame(index=['Wood Pole: Structure Costs'])

    if df_inputs.loc['Transmission?', A]:
        #NEED RAN INPUT ON NUMBERS AND MEAN OF UNCERTAINTY ANALYSIS
        df_wood_struct['Job Quantity']=1*10*transmission_len/5*transmission_line_factor
    else:
        df_wood_struct['Job Quantity']=0*transmission_len/5
    
    df_wood_struct['Labor Hours'] = df_utility.loc['Wood Pole: Structure Costs', 'Labor Hours']
    df_wood_struct['Material Cost Per Unit'] = float('nan')
    df_wood_struct['Equipment Cost Per Unit'] = float('nan')
    
    return df_wood_struct

def wood_pole_top_assembly(transmission_len, df_inputs, df_utility, transmission_line_factor):
    df_wood_top =pd.DataFrame(index=['Wood Pole: Top Assembly'])
  
    if df_inputs.loc['Transmission?', A]:
        #NEED RAN INPUT ON NUMBERS AND MEAN OF UNCERTAINTY ANALYSIS
        df_wood_top['Job Quantity']=8*100*transmission_len/5*transmission_line_factor
    else:
        df_wood_top['Job Quantity']=0*transmission_len/5
    
    df_wood_top['Labor Hours'] = df_utility.loc['Wood Pole: Top Assembly', 'Labor Hours']
    df_wood_top['Material Cost Per Unit'] = float('nan')
    df_wood_top['Equipment Cost Per Unit'] = float('nan')
    
    return df_wood_top

def conductor_cable_distribution(transmission_len, df_inputs, df_utility, transmission_line_factor, df_state, state, inflation):
    df_cond_dist =pd.DataFrame(index=['Conductor and Cable Distribution'])
  
    if df_inputs.loc['Transmission?', A]:
        #NEED RAN INPUT ON NUMBERS AND MEAN OF UNCERTAINTY ANALYSIS
        df_cond_dist['Job Quantity']=1*5280*transmission_len/5*transmission_line_factor
    else:
        df_cond_dist['Job Quantity']=0*transmission_len/5
    
    df_cond_dist['Labor Hours'] = df_utility.loc['Conductor and Cable Distribution', 'Labor Hours']
    df_cond_dist['Material Cost Per Unit'] = material_bare_cost('Conductor and Cable Distribution', df_state, df_utility, state)*inflation
    df_cond_dist['Equipment Cost Per Unit'] = equipment_bare_cost('Conductor and Cable Distribution', df_state, df_utility, state)*inflation
    
    return df_cond_dist

def misc_assembly_dist(df_utility):
    df_misc_dist =pd.DataFrame(index=['Misc. Assembly Units Distribution'])
    
    df_misc_dist['Job Quantity']=float(df_utility.loc['Misc. Assembly Units Distribution', 'Job Quantity'].strip('%'))/100
    df_misc_dist['Labor Hours'] = float('nan')
    df_misc_dist['Material Cost Per Unit'] = float('nan')
    df_misc_dist['Equipment Cost Per Unit'] = float('nan')
    
    return df_misc_dist

def interconnection_fee(df_inputs, df_utility, df_state, state, inflation, project_size):
    df_intercon_fee = pd.DataFrame(index=['Interconnection Fee Per MW'])
    df_intercon_fee['Job Quantity'] = float(df_utility.loc['Interconnection Fee Per MW','Job Quantity'])
    df_intercon_fee['Labor Hours'] = float(df_utility.loc['Interconnection Fee Per MW','Labor Hours'])
    
    # intercon_cost_factor = stat.mean([df_inputs.loc['Interconnection Fee Factor', A], df_inputs.loc['Interconnection Fee Factor', B], df_inputs.loc['Interconnection Fee Factor', C]])
    intercon_cost_factor = df_inputs.loc['Interconnection Fee Factor', D]
    
    df_intercon_fee['Material Cost Per Unit'] = material_bare_cost('Interconnection Fee Per MW', df_state, df_utility, state)*inflation*project_size*df_inputs.loc['Interconnection Fee Factor', D] \
                                            #*stat.mean([float(df_inputs.loc['Interconnection Fee Factor', A]), float(df_inputs.loc['Interconnection Fee Factor', B]), float(df_inputs.loc['Interconnection Fee Factor', C])])
    
    df_intercon_fee['Equipment Cost Per Unit'] = equipment_bare_cost('Interconnection Fee Per MW', df_state, df_utility, state)*inflation
    return df_intercon_fee