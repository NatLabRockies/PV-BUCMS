import pandas as pd
import matplotlib as plt
import statistics as stat
import math

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

def preconstruction_surveys(df_utility, df_inputs, df_state, num_modules, project_size, state, hist_cost_index):
    df_pre_sur = pd.DataFrame(index=['Preconstruction Surveys'])
    average = 3.02*(num_modules/(3222*project_size))
        
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
    df_pre_sur['Material Cost Per Unit'] = material_bare_cost('Preconstruction Surveys', df_state, df_utility, state)*hist_cost_index
    df_pre_sur['Equipment Cost Per Unit'] = equipment_bare_cost('Preconstruction Surveys', df_state, df_utility, state)*hist_cost_index
    return df_pre_sur

def preconstruction_surveys_battery(df_utility, df_state, state, hist_cost_index, df_com_storage):
    df_pre_sur_bat = pd.DataFrame(index=['Preconstruction Surveys (for Battery)'])
    
    df_pre_sur_bat['Job Quantity'] = df_com_storage.loc['Length','Value']*df_com_storage.loc['Width','Value']*100/43560
    df_pre_sur_bat['Labor Hours'] = df_utility.loc['Preconstruction Surveys (for Battery)','Labor Hours']
    df_pre_sur_bat['Material Cost Per Unit'] = material_bare_cost('Preconstruction Surveys (for Battery)', df_state, df_utility, state)*hist_cost_index
    df_pre_sur_bat['Equipment Cost Per Unit'] = equipment_bare_cost('Preconstruction Surveys (for Battery)', df_state, df_utility, state)*hist_cost_index
    return df_pre_sur_bat

def security_fencing_battery(df_utility, df_state, state, hist_cost_index, df_com_storage):
    df_sec_fen_bat = pd.DataFrame(index=['Security Fencing (for Battery)'])
    
    df_sec_fen_bat['Job Quantity'] = (df_com_storage.loc['Length','Value']*2+df_com_storage.loc['Width','Value']*2)*2
    df_sec_fen_bat['Labor Hours'] = df_utility.loc['Security Fencing (for Battery)','Labor Hours']
    df_sec_fen_bat['Material Cost Per Unit'] = material_bare_cost('Security Fencing (for Battery)', df_state, df_utility, state)*hist_cost_index
    df_sec_fen_bat['Equipment Cost Per Unit'] = equipment_bare_cost('Security Fencing (for Battery)', df_state, df_utility, state)*hist_cost_index
    return df_sec_fen_bat

def site_prep_battery(df_utility, df_state, state, hist_cost_index, df_pre_sur_bat):
    df_site_prep = pd.DataFrame(index=['Site Preparation (Geotechnical Investigation)','Site Preparation (Soil Stripping and stockpiling)', 
                                           'Site Preparation (Grading)','Site Preparation (Compaction)'])
    
    df_site_prep.loc['Site Preparation (Geotechnical Investigation)','Job Quantity'] = df_utility.loc['Site Preparation (Geotechnical Investigation)','Job Quantity if Battery']
    df_site_prep.loc['Site Preparation (Soil Stripping and stockpiling)','Job Quantity'] = df_utility.loc['Site Preparation (Soil Stripping and stockpiling)','Average']*df_pre_sur_bat.loc['Preconstruction Surveys (for Battery)','Job Quantity']/2*4840
    df_site_prep.loc['Site Preparation (Grading)','Job Quantity'] = df_pre_sur_bat.loc['Preconstruction Surveys (for Battery)','Job Quantity']/2*4840
    df_site_prep.loc['Site Preparation (Compaction)','Job Quantity'] = df_utility.loc['Site Preparation (Compaction)','Average']*df_pre_sur_bat.loc['Preconstruction Surveys (for Battery)','Job Quantity']/2*4840
    
    df_site_prep['Labor Hours'] = df_site_prep.apply(lambda x:df_utility.loc[x.name,'Labor Hours'], axis=1)
    df_site_prep['Material Cost Per Unit'] = df_site_prep.apply(lambda x:material_bare_cost(x.name, df_state, df_utility, state)*hist_cost_index, axis=1)
    df_site_prep['Equipment Cost Per Unit'] = df_site_prep.apply(lambda x:equipment_bare_cost(x.name, df_state, df_utility, state)*hist_cost_index, axis=1)
    return df_site_prep

def site_prep_roof(df_utility, df_state, state, hist_cost_index, df_pre_sur):
    df_site_prep_roof = pd.DataFrame(index=['Site Preparation (Roof Clean and Prep)'])
    
    df_site_prep_roof['Job Quantity'] = df_pre_sur.loc['Preconstruction Surveys','Job Quantity']
    df_site_prep_roof['Labor Hours'] = df_utility.loc['Site Preparation (Roof Clean and Prep)','Labor Hours']
    df_site_prep_roof['Material Cost Per Unit'] = material_bare_cost('Site Preparation (Roof Clean and Prep)', df_state, df_utility, state)*hist_cost_index
    df_site_prep_roof['Equipment Cost Per Unit'] = equipment_bare_cost('Site Preparation (Roof Clean and Prep)', df_state, df_utility, state)*hist_cost_index
    return df_site_prep_roof

def module_install(df_utility, df_state, state, hist_cost_index, num_modules):
    df_mod_install = pd.DataFrame(index=['Module Installation'])
    
    df_mod_install['Job Quantity'] = num_modules
    df_mod_install['Labor Hours'] = df_utility.loc['Module Installation','Labor Hours']
    df_mod_install['Material Cost Per Unit'] = material_bare_cost('Module Installation', df_state, df_utility, state)*hist_cost_index
    df_mod_install['Equipment Cost Per Unit'] = equipment_bare_cost('Module Installation', df_state, df_utility, state)*hist_cost_index
    return df_mod_install

def lift_crane(df_utility, df_state, state, hist_cost_index):
    df_lift_crane = pd.DataFrame(index=['Lifting & Hoisting by Crane'])
    
    df_lift_crane['Job Quantity'] = df_utility.loc['Lifting & Hoisting by Crane','Job Quantity']
    df_lift_crane['Labor Hours'] = df_utility.loc['Lifting & Hoisting by Crane','Labor Hours']
    df_lift_crane['Material Cost Per Unit'] = material_bare_cost('Lifting & Hoisting by Crane', df_state, df_utility, state)*hist_cost_index
    df_lift_crane['Equipment Cost Per Unit'] = equipment_bare_cost('Lifting & Hoisting by Crane', df_state, df_utility, state)*hist_cost_index
    return df_lift_crane

def lift_crane_battery(df_utility, df_state, state, hist_cost_index):
    df_lift_crane_bat = pd.DataFrame(index=['Lifting & Hoisting by Crane on site (for Battery)'])
    
    df_lift_crane_bat['Job Quantity'] = df_utility.loc['Lifting & Hoisting by Crane on site (for Battery)','Job Quantity if Battery']
    df_lift_crane_bat['Labor Hours'] = df_utility.loc['Lifting & Hoisting by Crane on site (for Battery)','Labor Hours']
    df_lift_crane_bat['Material Cost Per Unit'] = material_bare_cost('Lifting & Hoisting by Crane on site (for Battery)', df_state, df_utility, state)*hist_cost_index
    df_lift_crane_bat['Equipment Cost Per Unit'] = equipment_bare_cost('Lifting & Hoisting by Crane on site (for Battery)', df_state, df_utility, state)*hist_cost_index
    return df_lift_crane_bat

def racking_install(df_inputs,ballast_bay_per_module, num_modules, ballast_cost_per_module, df_utility, df_state, state, hist_cost_index):
    df_racking_install = pd.DataFrame(index=['Racking Installation'])
    
    uncertainty_coefficient = df_inputs.loc['Coefficiency Uncertainty', A]
    df_racking_install['Job Quantity'] = num_modules*ballast_bay_per_module*uncertainty_coefficient
    
    df_racking_install['Labor Hours'] = df_utility.loc['Racking Installation','Labor Hours']
    
    material_location_factor = float(df_state.loc[state, ('Location Factor', 'Material')])/100
    df_racking_install['Material Cost Per Unit'] = ballast_cost_per_module*material_location_factor
    
    df_racking_install['Equipment Cost Per Unit'] = equipment_bare_cost('Racking Installation', df_state, df_utility, state)*hist_cost_index
    return df_racking_install

# def loading_drive()



def loading_drive_battery(df_utility, df_state, state, hist_cost_index):
    df_loading_drive_bat = pd.DataFrame(index=['Loading & Drive from OEM (for Battery)'])
    
    df_loading_drive_bat['Job Quantity'] = df_utility.loc['Loading & Drive from OEM (for Battery)','Job Quantity if Battery']
    df_loading_drive_bat['Labor Hours'] = df_utility.loc['Loading & Drive from OEM (for Battery)','Labor Hours']
    df_loading_drive_bat['Material Cost Per Unit'] = material_bare_cost('Loading & Drive from OEM (for Battery)', df_state, df_utility, state)*hist_cost_index
    df_loading_drive_bat['Equipment Cost Per Unit'] = equipment_bare_cost('Loading & Drive from OEM (for Battery)', df_state, df_utility, state)*hist_cost_index
    return df_loading_drive_bat

def pv_source_conductor(df_inputs, df_module_db, num_modules, df_utility, df_state, state, hist_cost_index):
    df_pv_source_conductor = pd.DataFrame(index=['PV source conductor - array to transition box'])
    
    module=df_inputs.loc['Module Name', A]
    mod_orientation = df_inputs.loc['Module Orientation', A]
    array_length = math.ceil(math.sqrt(math.ceil(num_modules)))
    total_modules = array_length**2
    system_vdc = df_inputs.loc['System VDC', A]
    mod_length = df_module_db.loc[module,'Length (in)']/12
    mod_width = df_module_db.loc[module,'Width (in)']/12
    mod_voc = df_module_db.loc[module,'Voc (A)']
    max_volt = mod_voc+(25-df_inputs.loc['Record Low, C', A])*-1*mod_voc*df_module_db.loc[module,'Temp Coeff Voc (%/deg C)']
    mod_per_string = math.floor(system_vdc/max_volt)
    strings = math.ceil(total_modules/mod_per_string)
    
    if mod_orientation == 'Landscape':
        df_pv_source_conductor['Job Quantity'] = strings*math.ceil(2*mod_per_string)*mod_length/100
    else:
        df_pv_source_conductor['Job Quantity'] = strings*math.ceil(2*mod_per_string)*mod_width/100
    df_pv_source_conductor['Labor Hours'] = df_utility.loc['PV source conductor - array to transition box','Labor Hours']
    df_pv_source_conductor['Material Cost Per Unit'] = material_bare_cost('PV source conductor - array to transition box', df_state, df_utility, state)*hist_cost_index
    df_pv_source_conductor['Equipment Cost Per Unit'] = equipment_bare_cost('PV source conductor - array to transition box', df_state, df_utility, state)*hist_cost_index
    return df_pv_source_conductor, df_pv_source_conductor.loc['PV source conductor - array to transition box','Job Quantity'], strings, array_length

def loading_drive(pv_source_conductor_job_qty, df_utility, df_state, state, hist_cost_index):
    df_loading_drive = pd.DataFrame(index=['Loading, Drive, and Unloading'])
    
    if pv_source_conductor_job_qty<500:
        df_loading_drive['Job Quantity'] = df_utility.loc['Loading, Drive, and Unloading','Job Quantity']
    elif pv_source_conductor_job_qty<1000:
        df_loading_drive['Job Quantity'] = 2
    else:
        df_loading_drive['Job Quantity'] = 3
    
    df_loading_drive['Labor Hours'] = df_utility.loc['Loading, Drive, and Unloading','Labor Hours']
    df_loading_drive['Material Cost Per Unit'] = material_bare_cost('Loading, Drive, and Unloading', df_state, df_utility, state)*hist_cost_index
    df_loading_drive['Equipment Cost Per Unit'] = equipment_bare_cost('Loading, Drive, and Unloading', df_state, df_utility, state)*hist_cost_index
    
    return df_loading_drive

def pv_output_conductor(strings, df_inputs, df_utility, df_state, state, hist_cost_index):
    df_pv_output_conductor = pd.DataFrame(index=['PV output conductor - transition box to inverter'])
    
    df_pv_output_conductor['Job Quantity'] = 3*strings*df_inputs.loc['Average output conductor run, LF',A]/100
    
    df_pv_output_conductor['Labor Hours'] = df_utility.loc['PV output conductor - transition box to inverter','Labor Hours']
    df_pv_output_conductor['Material Cost Per Unit'] = material_bare_cost('PV output conductor - transition box to inverter', df_state, df_utility, state)*hist_cost_index
    df_pv_output_conductor['Equipment Cost Per Unit'] = equipment_bare_cost('PV output conductor - transition box to inverter', df_state, df_utility, state)*hist_cost_index
   
    return df_pv_output_conductor

def conduit_trans_to_inv(strings, df_inputs, df_utility, df_state, state, hist_cost_index):
    df_conduit_trans_to_inv = pd.DataFrame(index=["Conduit - transition box to inverter"])
    strings_per_trans = df_inputs.loc['Strings per Transition Box',A]
    df_conduit_trans_to_inv['Job Quantity'] = df_inputs.loc['Average output conductor run, LF',A]*math.ceil(strings/strings_per_trans)
    
    df_conduit_trans_to_inv['Labor Hours'] = df_utility.loc['Conduit - transition box to inverter','Labor Hours']
    df_conduit_trans_to_inv['Material Cost Per Unit'] = df_utility.loc['Conduit - transition box to inverter','Material Bare Cost']
    df_conduit_trans_to_inv['Equipment Cost Per Unit'] = equipment_bare_cost('Conduit - transition box to inverter', df_state, df_utility, state)*hist_cost_index
   
    return df_conduit_trans_to_inv, strings_per_trans

def trans_boxes(strings,strings_per_trans, df_utility, df_state, state, hist_cost_index):
    df_trans_boxes = pd.DataFrame(index=["Transition Boxes"])
    
    df_trans_boxes['Job Quantity'] = math.ceil(strings/strings_per_trans)
    df_trans_boxes['Labor Hours'] = df_utility.loc["Transition Boxes",'Labor Hours']
    df_trans_boxes['Material Cost Per Unit'] = material_bare_cost('Transition Boxes', df_state, df_utility, state)*hist_cost_index
    df_trans_boxes['Equipment Cost Per Unit'] = equipment_bare_cost("Transition Boxes", df_state, df_utility, state)*hist_cost_index
   
    return df_trans_boxes

def ground_bonding(pv_source_conductor_job_qty,df_utility, df_state, state, hist_cost_index):
    df_ground_bonding = pd.DataFrame(index=["Grounding and bonding for array"])
    
    df_ground_bonding['Job Quantity'] = pv_source_conductor_job_qty
    df_ground_bonding['Labor Hours'] = df_utility.loc["Grounding and bonding for array",'Labor Hours']
    df_ground_bonding['Material Cost Per Unit'] = material_bare_cost('Grounding and bonding for array', df_state, df_utility, state)*hist_cost_index
    df_ground_bonding['Equipment Cost Per Unit'] = equipment_bare_cost("Grounding and bonding for array", df_state, df_utility, state)*hist_cost_index
   
    return df_ground_bonding

def grounding_cable_battery(df_utility, df_state, state, hist_cost_index):
    df_grounding_cable_bat = pd.DataFrame(index=['Grounding, DC Cable'])
    
    df_grounding_cable_bat['Job Quantity'] = df_utility.loc['Grounding, DC Cable','Job Quantity if Battery']
    df_grounding_cable_bat['Labor Hours'] = df_utility.loc['Grounding, DC Cable','Labor Hours']
    df_grounding_cable_bat['Material Cost Per Unit'] = material_bare_cost('Grounding, DC Cable', df_state, df_utility, state)*hist_cost_index
    df_grounding_cable_bat['Equipment Cost Per Unit'] = equipment_bare_cost('Grounding, DC Cable', df_state, df_utility, state)*hist_cost_index
    return df_grounding_cable_bat

def inverter(array_length, project_size, num_modules, df_inputs, df_utility, df_state, state, hist_cost_index,dc_ac_ratio):
    df_inverter=pd.DataFrame(index=['Inverter'])

    df_inverter['Job Quantity'] = math.ceil(array_length**2*(project_size/num_modules/1000)/df_inputs.loc['Inverter Size (kW)', A]/dc_ac_ratio)
    df_inverter['Labor Hours'] = df_utility.loc['Inverter','Labor Hours']
    df_inverter['Material Cost Per Unit'] = material_bare_cost('Inverter', df_state, df_utility, state)*hist_cost_index
    df_inverter['Equipment Cost Per Unit'] = equipment_bare_cost('Inverter', df_state, df_utility, state)*hist_cost_index
    return df_inverter, df_inverter.loc['Inverter','Job Quantity']

def conductor_inverter_to_ac(inverter_count, df_inputs, df_utility, df_state, state, hist_cost_index):
    df_cond_inv=pd.DataFrame(index=['Conductor - inverter to AC panel'])
    df_cond_inv['Job Quantity']= inverter_count*df_inputs.loc['Average inverter AC conductor run, LF',A]*4/100
    df_cond_inv['Labor Hours'] = df_utility.loc['Conductor - inverter to AC panel','Labor Hours']
    df_cond_inv['Material Cost Per Unit'] = material_bare_cost('Conductor - inverter to AC panel', df_state, df_utility, state)*hist_cost_index
    df_cond_inv['Equipment Cost Per Unit'] = equipment_bare_cost('Conductor - inverter to AC panel', df_state, df_utility, state)*hist_cost_index
    return df_cond_inv

def conduit_inverter_to_ac(inverter_count, df_inputs, df_utility, df_state, state, hist_cost_index):
    df_conduit_inv=pd.DataFrame(index=['Conduit - inverter to AC panel'])
    
    df_conduit_inv['Job Quantity']= inverter_count*df_inputs.loc['Average inverter AC conductor run, LF',A]
    df_conduit_inv['Labor Hours'] = df_utility.loc['Conduit - inverter to AC panel','Labor Hours']
    df_conduit_inv['Material Cost Per Unit'] = material_bare_cost('Conduit - inverter to AC panel', df_state, df_utility, state)*hist_cost_index
    df_conduit_inv['Equipment Cost Per Unit'] = equipment_bare_cost('Conduit - inverter to AC panel', df_state, df_utility, state)*hist_cost_index
    return df_conduit_inv

def ac_subpanel(df_utility, df_state, state, hist_cost_index):
    df_ac_subpanel = pd.DataFrame(index=['AC Subpanel'])
    
    df_ac_subpanel['Job Quantity'] = df_utility.loc['AC Subpanel','Job Quantity']
    df_ac_subpanel['Labor Hours'] = df_utility.loc['AC Subpanel','Labor Hours']
    df_ac_subpanel['Material Cost Per Unit'] = material_bare_cost('AC Subpanel', df_state, df_utility, state)*hist_cost_index
    df_ac_subpanel['Equipment Cost Per Unit'] = equipment_bare_cost('AC Subpanel', df_state, df_utility, state)*hist_cost_index
    return df_ac_subpanel

def big_ac_disco(df_utility, df_state, state, hist_cost_index, project_size):
    df_ac_disco = pd.DataFrame(index=['Big AC Disco'])
    
    df_ac_disco['Job Quantity'] = df_utility.loc['Big AC Disco','Job Quantity']
    df_ac_disco['Labor Hours'] = df_utility.loc['Big AC Disco','Labor Hours']
    df_ac_disco['Material Cost Per Unit'] = float(df_state.loc[state, ('Location Factor', 'Material')])/100*(project_size)*0.014*hist_cost_index
    df_ac_disco['Equipment Cost Per Unit'] = equipment_bare_cost('Big AC Disco', df_state, df_utility, state)*hist_cost_index
    return df_ac_disco

def conductor_ac_to_interconnect(df_inputs, df_utility, df_state, state, hist_cost_index):
    df_cond_ac = pd.DataFrame(index=['Conductor - AC disco to point of interconnection'])
    ac_run = df_inputs.loc['Average AC interconnection conductor run, LF',A]
    df_cond_ac['Job Quantity'] = ac_run*df_inputs.loc['Conductors per conduit',A]/100
    df_cond_ac['Labor Hours'] = df_utility.loc['Conductor - AC disco to point of interconnection','Labor Hours']
    df_cond_ac['Material Cost Per Unit'] = material_bare_cost('Conductor - AC disco to point of interconnection', df_state, df_utility, state)*hist_cost_index
    df_cond_ac['Equipment Cost Per Unit'] = equipment_bare_cost('Conductor - AC disco to point of interconnection', df_state, df_utility, state)*hist_cost_index
    return df_cond_ac, ac_run

def conduit_ac_to_interconnect(ac_run, df_utility, df_state, state, hist_cost_index):
    df_conduit_ac = pd.DataFrame(index=['Conduit - AC disco to point of interconnection'])
    
    df_conduit_ac['Job Quantity'] = ac_run
    df_conduit_ac['Labor Hours'] = df_utility.loc['Conduit - AC disco to point of interconnection','Labor Hours']
    df_conduit_ac['Material Cost Per Unit'] = material_bare_cost('Conduit - AC disco to point of interconnection', df_state, df_utility, state)*hist_cost_index
    df_conduit_ac['Equipment Cost Per Unit'] = equipment_bare_cost('Conduit - AC disco to point of interconnection', df_state, df_utility, state)*hist_cost_index
    return df_conduit_ac

def conduit_wiring(df_utility, df_state, state, hist_cost_index):
    df_conduit_wiring = pd.DataFrame(index=['Conduit, Wiring'])
    
    df_conduit_wiring['Job Quantity'] = df_utility.loc['Conduit, Wiring','Job Quantity if Battery']
    df_conduit_wiring['Labor Hours'] = df_utility.loc['Conduit, Wiring','Labor Hours']
    df_conduit_wiring['Material Cost Per Unit'] = material_bare_cost('Conduit, Wiring', df_state, df_utility, state)*hist_cost_index
    df_conduit_wiring['Equipment Cost Per Unit'] = equipment_bare_cost('Conduit, Wiring', df_state, df_utility, state)*hist_cost_index
    return df_conduit_wiring

def revenue_grade_meter(df_utility, df_state, state, hist_cost_index, project_size, df_bos_cost):
    df_revenue_meter = pd.DataFrame(index=['Revenue Grade Meter'])
    
    df_revenue_meter['Job Quantity'] = df_utility.loc['Revenue Grade Meter','Job Quantity']
    df_revenue_meter['Labor Hours'] = df_utility.loc['Revenue Grade Meter','Labor Hours']
    df_revenue_meter['Material Cost Per Unit'] = df_bos_cost.loc['Meter','Cost']*float(df_state.loc[state, ('Location Factor', 'Material')])/100*(project_size)*hist_cost_index
    df_revenue_meter['Equipment Cost Per Unit'] = equipment_bare_cost('Revenue Grade Meter', df_state, df_utility, state)*hist_cost_index
    return df_revenue_meter

def system_monitor(df_utility, df_state, state, hist_cost_index, project_size, df_bos_cost):
    df_system_monitor = pd.DataFrame(index=['System Monitor'])
    
    df_system_monitor['Job Quantity'] = df_utility.loc['System Monitor','Job Quantity']
    df_system_monitor['Labor Hours'] = df_utility.loc['System Monitor','Labor Hours']
    df_system_monitor['Material Cost Per Unit'] = df_bos_cost.loc['System monitor','Cost']*float(df_state.loc[state, ('Location Factor', 'Material')])/100*(project_size)*hist_cost_index
    df_system_monitor['Equipment Cost Per Unit'] = equipment_bare_cost('System Monitor', df_state, df_utility, state)*hist_cost_index
    return df_system_monitor

def pe_stamped_calcs(df_utility, df_state, state, hist_cost_index):
    df_stamped_calcs = pd.DataFrame(index=['PE stamped calcs & drawings'])
    
    df_stamped_calcs['Job Quantity'] = df_utility.loc['PE stamped calcs & drawings','Job Quantity if Battery']
    df_stamped_calcs['Labor Hours'] = df_utility.loc['PE stamped calcs & drawings','Labor Hours']
    df_stamped_calcs['Material Cost Per Unit'] = material_bare_cost('PE stamped calcs & drawings', df_state, df_utility, state)*hist_cost_index
    df_stamped_calcs['Equipment Cost Per Unit'] = equipment_bare_cost('PE stamped calcs & drawings', df_state, df_utility, state)*hist_cost_index
    return df_stamped_calcs

def oem_testing_battery(df_utility, df_state, state, hist_cost_index):
    df_oem_testing = pd.DataFrame(index=['OEM testing and commissioning (Battery)'])
    
    df_oem_testing['Job Quantity'] = df_utility.loc['OEM testing and commissioning (Battery)','Job Quantity if Battery']
    df_oem_testing['Labor Hours'] = df_utility.loc['OEM testing and commissioning (Battery)','Labor Hours']
    df_oem_testing['Material Cost Per Unit'] = material_bare_cost('OEM testing and commissioning (Battery)', df_state, df_utility, state)*hist_cost_index
    df_oem_testing['Equipment Cost Per Unit'] = equipment_bare_cost('OEM testing and commissioning (Battery)', df_state, df_utility, state)*hist_cost_index
    return df_oem_testing

def interconnection(df_utility, df_state, state, other_inflation):
    df_intercon = pd.DataFrame(index=['Interconnection, testing and commissioning'])
    
    df_intercon['Job Quantity'] = df_utility.loc['Interconnection, testing and commissioning','Job Quantity']
    df_intercon['Labor Hours'] = df_utility.loc['Interconnection, testing and commissioning','Labor Hours']
    df_intercon['Material Cost Per Unit'] = material_bare_cost('Interconnection, testing and commissioning', df_state, df_utility, state)*other_inflation
    df_intercon['Equipment Cost Per Unit'] = equipment_bare_cost('Interconnection, testing and commissioning', df_state, df_utility, state)*other_inflation


    return df_intercon
