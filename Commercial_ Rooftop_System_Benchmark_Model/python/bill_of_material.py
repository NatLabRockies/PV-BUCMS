import pandas as pd
import numpy as np
import statistics as stat
import math

def ballasted_systems(df_ballasted_systems, watts, project_size, df_inputs, max_wind):
    df_ballasted_systems['Extended Cost per 200kW'] = df_ballasted_systems['Cost Per Component']*df_ballasted_systems['QTY per 200kW']
    df_ballasted_systems['QTY per module'] = df_ballasted_systems['QTY per 200kW']/(200000/310)
    df_ballasted_systems['Cost per module'] = df_ballasted_systems['Extended Cost per 200kW']/(200000/310)

    ballast_bay_per_module = df_ballasted_systems.loc['Ballast Bay','QTY per module']
    distributor_discount = df_inputs.loc['Average Racking Distributor Cost Discount','Value A']
    wind_loading_factor = df_inputs.loc['Wind Loading Factor','Value A']
    ballast_cost_per_module = ((df_ballasted_systems.loc['Ballast Bay','Cost per module'] + df_ballasted_systems.loc['RM Module Clip','Cost per module'] + df_ballasted_systems.loc['RM Hex Bolt','Cost per module'])*(1-distributor_discount)+df_ballasted_systems.loc['Ballast Block','Cost per module'])*wind_loading_factor*max_wind/104.3

    return ballast_bay_per_module, ballast_cost_per_module

def design_criteria(importance_factor, length, width, weight, uncertainty_coeff, state, df_state):
    
    df_design = pd.DataFrame(columns = ['Value'])
    
    df_design.loc['Wind Speed (mph)', 'Value']=df_state.loc[state, ('ASCE 7-05 Design Criteria','Wind')]
    df_design.loc['Wind pressure on module (psf)', 'Value']=(df_design.loc['Wind Speed (mph)', 'Value']**2.0)*importance_factor*0.00256*0.85*1*0.85
    df_design.loc['qh*G (psf)', 'Value']=df_design.loc['Wind pressure on module (psf)', 'Value']*0.85
    df_design.loc['Wind pressure on tubing (lbs/ft)', 'Value']=df_design.loc['qh*G (psf)', 'Value']*length/12.0*uncertainty_coeff
    df_design.loc['Ground Snow (psf)', 'Value']=df_state.loc[state, ('ASCE 7-05 Design Criteria','Snow')]
    df_design.loc['Ground Snow on tubing (lbs/ft)', 'Value']=0.7*0.9*1.2*1*1*df_design.loc['Ground Snow (psf)', 'Value']*length/12.0
    # df_design.loc['Module dead load (psf)', 'Value']=weight/(length/12.0)/(width/12.0)
    # df_design.loc['Dead load on tubing (lbs/ft)', 'Value']=df_design.loc['Module dead load (psf)', 'Value']*length/12.0+df_torque_tube.loc['4"x4"x0.137" 70 KSI Tubing ','Weight (lb/ft)']

    return df_design

def loading_combo(df_design, df_loading_inputs):
    df_loading_inputs['SUM'] = df_loading_inputs['CNW']+ df_loading_inputs['CNL']
    df_loading_inputs['Wind']= df_loading_inputs['SUM']*df_design.loc['Wind pressure on tubing (lbs/ft)', 'Value']/2.0
    df_loading_inputs['Snow']=df_design.loc['Ground Snow on tubing (lbs/ft)', 'Value']*np.cos(df_loading_inputs['Angle']*math.pi/180)
    # df_loading_combo['Dead']=df_design.loc['Dead load on tubing (lbs/ft)', 'Value']*np.cos(df_loading_combo['Angle']*math.pi/180)
    # df_loading_combo['Wind-Control Case']=1.6*df_loading_combo['Wind']+0.5*df_loading_combo['Snow']+1.2*df_loading_combo['Dead']
    # df_loading_combo['Snow-Control Case']=0.8*df_loading_combo['Wind']+1.6*df_loading_combo['Snow']+1.2*df_loading_combo['Dead']
    df_loading_combo = df_loading_inputs
    return df_loading_combo