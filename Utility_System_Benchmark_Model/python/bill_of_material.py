import pandas as pd
import numpy as np
import statistics as stat
import math

#DataFrames specific to this script
tuples = [('Tubing', 'Est. Tubing Length (ft)'),
          ('Tubing', 'Est. Tubing Cost per foot ($)'),
         ('Tubing', 'Est. Tubing Total Cost ($)'),
          ('Tubing', 'Percent of Total System '),
         ('Column', 'Est. Number of Columns'),
         ('Column', 'Est. Column Length (ft)'),
         ('Column', 'Est. Column Cost per foot ($)'),
         ('Column', 'Est. Column Total Cost ($)'),
         ('Column', 'Percent of Total System '),
         ('T - Connection', 'Est. Number of T-Connections'),
         ('T - Connection', 'Est. Connection Total Cost ($)'),
         ('T - Connection', 'Est. Hardware (e.g. bolts/washers)'),
         ("T - Connection", 'Percent of Total System '),
         ("Racking Hardware", 'Est. Number of Clamp/Clip'),
         ('Racking Hardware', 'Est. Clamp/Clip (ft)'),
         ('Racking Hardware', 'Est. Clamp/Clip Cost per foot ($)'),
         ('Racking Hardware', 'Est. Clamp/Clip Cost ($)'),
         ('Racking Hardware', 'Est. Hardware (e.g. bolts/washers)'),
         ('Racking Hardware', 'Percent of Total System '),
         ('Center Gear Drive', 'Est. Center Gear Cost ($)'),
         ('Center Gear Drive', 'Est. Hardware (e.g. bolts/washers)'),
         ('Center Gear Drive', 'Percent of Total System '),
         ('Total', 'Est. Total Material Cost ($)'),
         ('Total', 'Est. Dollar per W'),
        ]



def design_criteria(importance_factor, length, width, weight, uncertainty_coeff, state, df_state, df_torque_tube):
    
    df_design = pd.DataFrame(columns = ['Value'])
    
    df_design.loc['Wind Speed (mph)', 'Value']=df_state.loc[state, ('ASCE 7-05 Design Criteria','Wind')]
    df_design.loc['Wind pressure on module (psf)', 'Value']=(df_design.loc['Wind Speed (mph)', 'Value']**2.0)*importance_factor*0.00256*0.85*1*0.85
    df_design.loc['qh*G (psf)', 'Value']=df_design.loc['Wind pressure on module (psf)', 'Value']*0.85
    df_design.loc['Wind pressure on tubing (lbs/ft)', 'Value']=df_design.loc['qh*G (psf)', 'Value']*length/12.0*uncertainty_coeff
    df_design.loc['Ground Snow (psf)', 'Value']=df_state.loc[state, ('ASCE 7-05 Design Criteria','Snow')]
    df_design.loc['Ground Snow on tubing (lbs/ft)', 'Value']=0.7*0.9*1.2*1*1*df_design.loc['Ground Snow (psf)', 'Value']*length/12.0
    df_design.loc['Module dead load (psf)', 'Value']=weight/(length/12.0)/(width/12.0)
    df_design.loc['Dead load on tubing (lbs/ft)', 'Value']=df_design.loc['Module dead load (psf)', 'Value']*length/12.0+df_torque_tube.loc['4"x4"x0.137" 70 KSI Tubing ','Weight (lb/ft)']

    return df_design

def loading_combo(df_design, df_loading_combo):
    df_loading_combo['SUM'] = df_loading_combo['CNW']+ df_loading_combo['CNL']
    df_loading_combo['Wind']= df_loading_combo['SUM']*df_design.loc['Wind pressure on tubing (lbs/ft)', 'Value']/2.0
    df_loading_combo['Snow']=df_design.loc['Ground Snow on tubing (lbs/ft)', 'Value']*np.cos(df_loading_combo['Angle']*math.pi/180)
    df_loading_combo['Dead']=df_design.loc['Dead load on tubing (lbs/ft)', 'Value']*np.cos(df_loading_combo['Angle']*math.pi/180)
    df_loading_combo['Wind-Control Case']=1.6*df_loading_combo['Wind']+0.5*df_loading_combo['Snow']+1.2*df_loading_combo['Dead']
    df_loading_combo['Snow-Control Case']=0.8*df_loading_combo['Wind']+1.6*df_loading_combo['Snow']+1.2*df_loading_combo['Dead']
        
    return df_loading_combo

def bom_table_fixed(df_module_db, df_inputs, num_modules, year, df_state, state, project_size, df_torque_tube, df_pipe, df_rail_clamp, steel_inflation, df_loading_combo):
    index = pd.MultiIndex.from_tuples(tuples, names = ['Category','Description'])
    df_bom = pd.DataFrame(index = index, columns=['Fixed-Tilt',  'Tracker'])
    a = 'Fixed-Tilt'
    module = df_inputs.loc['Module Name','Value A']
    width = df_module_db.loc[module, 'Width (in)']
    length = df_module_db.loc[module, 'Length (in)']
    weight = df_module_db.loc[module, 'Weight (lb)']
    uncertainty_coeff = df_inputs.loc['Coefficiency Uncertainty','Value A']
    #ERROR IN SPREADSHEET FOR HOW UNCERTAINTIES ARE CALCULATED
    # design_con_mean = stat.mean([float(df_inputs.loc['Design Conservatism Factor', 'Value A']), float(df_inputs.loc['Design Conservatism Factor', 'Value B']), float(df_inputs.loc['Design Conservatism Factor', 'Value C'])])
    design_con_mean = df_inputs.loc['Design Conservatism Factor', 'Value D']
    importance_factor = df_inputs.loc['Importance Factor, I', 'Value A']
    
    
    
    df_design = design_criteria(importance_factor, length, width, weight, uncertainty_coeff, state, df_state, df_torque_tube)
    df_loading_combo = loading_combo(df_design,df_loading_combo)
    
    df_bom.loc[('Tubing', 'Est. Tubing Length (ft)'), a]= num_modules*width/12.0*design_con_mean*uncertainty_coeff/0.75
    df_bom.loc[('Tubing', 'Est. Tubing Cost per foot ($)'), a]=df_torque_tube.loc[df_inputs.loc['Tubing','Value A'],'2012 Price ($/ft)']*steel_inflation
    df_bom.loc[('Tubing', 'Est. Tubing Total Cost ($)'), a]= df_bom.loc[('Tubing', 'Est. Tubing Length (ft)'), a]*df_bom.loc[('Tubing', 'Est. Tubing Cost per foot ($)'), a]
    
    worst_case = np.amax([np.amax(df_loading_combo['Wind-Control Case']),np.amax(df_loading_combo['Snow-Control Case'])])
    l_max_span = math.sqrt((df_torque_tube.loc[df_inputs.loc['Tubing','Value A'],'phiMn (k-")']/12.0)*1000.0/0.106/worst_case)
    #WHY WE ADDING 1 DOWN IN THE NEXT LINE?
    df_bom.loc[('Column', 'Est. Number of Columns'), a]= (df_bom.loc[('Tubing', 'Est. Tubing Length (ft)'), a]/l_max_span)+1.0
    df_bom.loc[('Column', 'Est. Column Length (ft)'), a]= df_bom.loc[('Column', 'Est. Number of Columns'), a]*15*design_con_mean*uncertainty_coeff/0.75
    df_bom.loc[('Column', 'Est. Column Cost per foot ($)'), a]=df_pipe.loc[df_inputs.loc['Column','Value A'],'2012 Price ($/ft)']*steel_inflation
    df_bom.loc[('Column', 'Est. Column Total Cost ($)'), a]= df_bom.loc[('Column', 'Est. Column Cost per foot ($)'), a]*df_bom.loc[('Column', 'Est. Column Length (ft)'), a]
    
    df_bom.loc[('T - Connection', 'Est. Number of T-Connections'), a]=df_bom.loc[('Column', 'Est. Number of Columns'), a]
    df_bom.loc[('T - Connection', 'Est. Connection Total Cost ($)'), a]=df_bom.loc[('Column', 'Est. Column Total Cost ($)'), a]*0.5
    df_bom.loc[('T - Connection', 'Est. Hardware (e.g. bolts/washers)'), a]=df_bom.loc[('T - Connection', 'Est. Connection Total Cost ($)'), a]*0.2
    
    df_bom.loc[('Racking Hardware', 'Est. Number of Clamp/Clip'), a]=num_modules
    df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip (ft)'), a]=df_bom.loc[('Racking Hardware', 'Est. Number of Clamp/Clip'), a]*3*design_con_mean*uncertainty_coeff/0.75
    df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip Cost per foot ($)'), a]=df_rail_clamp.loc[df_inputs.loc['Clamp','Value A'],'2012 Price ($/ft)']*steel_inflation
    df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip Cost ($)'), a]=df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip Cost per foot ($)'), a]*df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip (ft)'), a]
    df_bom.loc[('Racking Hardware', 'Est. Hardware (e.g. bolts/washers)'), a]=df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip Cost ($)'), a]*0.5
    
    df_bom.loc[('Center Gear Drive', 'Est. Center Gear Cost ($)'), a]=0
    df_bom.loc[('Center Gear Drive', 'Est. Hardware (e.g. bolts/washers)'), a]=0
    
    df_bom.loc[('Total', 'Est. Total Material Cost ($)'), a]= df_bom.loc[('Tubing', 'Est. Tubing Total Cost ($)'), a] \
                                                            +df_bom.loc[('Column', 'Est. Column Total Cost ($)'), a] \
                                                            +df_bom.loc[('T - Connection', 'Est. Connection Total Cost ($)'), a] \
                                                            +df_bom.loc[('T - Connection', 'Est. Hardware (e.g. bolts/washers)'), a] \
                                                            +df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip Cost ($)'), a] \
                                                            +df_bom.loc[('Racking Hardware', 'Est. Hardware (e.g. bolts/washers)'), a] \
                                                            +df_bom.loc[('Center Gear Drive', 'Est. Center Gear Cost ($)'), a] \
                                                            +df_bom.loc[('Center Gear Drive', 'Est. Hardware (e.g. bolts/washers)'), a]
    
    df_bom.loc[('Total', 'Est. Dollar per W'), a]=df_bom.loc[('Total', 'Est. Total Material Cost ($)'), a]/(project_size*1000000)
    return df_bom

# def bom_table_tracker(df_module_db, df_inputs, num_modules, year, df_state, state, project_size):
#     df_bom = bom_table_fixed(df_module_db, df_inputs, num_modules, year, df_state, state, project_size)
#     a = 'Fixed-Tilt'
#     b = 'Tracker'
#     df_bom.loc[('Tubing', 'Est. Tubing Length (ft)'), b]=df_bom.loc[('Tubing', 'Est. Tubing Length (ft)'), a]*1.05
#     df_bom.loc[('Tubing', 'Est. Tubing Cost per foot ($)'), b]=df_bom.loc[('Tubing', 'Est. Tubing Cost per foot ($)'), a]
#     df_bom.loc[('Tubing', 'Est. Tubing Total Cost ($)'), b]=df_bom.loc[('Tubing', 'Est. Tubing Cost per foot ($)'), b]*df_bom.loc[('Tubing', 'Est. Tubing Length (ft)'), b]
    
#     df_bom.loc[('Column', 'Est. Number of Columns'), b]=(df_bom.loc[('Column', 'Est. Number of Columns'), a]-1.0)*1.05+1
#     df_bom.loc[('Column', 'Est. Column Length (ft)'), b]= df_bom.loc[('Column', 'Est. Number of Columns'), b]/df_bom.loc[('Column', 'Est. Number of Columns'), a]*df_bom.loc[('Column', 'Est. Column Length (ft)'), a]
#     df_bom.loc[('Column', 'Est. Column Cost per foot ($)'), b]=df_bom.loc[('Column', 'Est. Column Cost per foot ($)'), a]
#     df_bom.loc[('Column', 'Est. Column Total Cost ($)'), b]= df_bom.loc[('Column', 'Est. Column Cost per foot ($)'), b]*df_bom.loc[('Column', 'Est. Column Length (ft)'), b]
    
#     df_bom.loc[('T - Connection', 'Est. Number of T-Connections'), b]=df_bom.loc[('Column', 'Est. Number of Columns'), b]
#     df_bom.loc[('T - Connection', 'Est. Connection Total Cost ($)'), b]=df_bom.loc[('Column', 'Est. Column Total Cost ($)'), b]*0.5
#     df_bom.loc[('T - Connection', 'Est. Hardware (e.g. bolts/washers)'), b]=df_bom.loc[('T - Connection', 'Est. Connection Total Cost ($)'), b]*0.2
    
#     df_bom.loc[('Racking Hardware', 'Est. Number of Clamp/Clip'), b]=num_modules
#     df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip (ft)'), b]=df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip (ft)'), a]
#     df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip Cost per foot ($)'), b]=df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip Cost per foot ($)'), a]
#     df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip Cost ($)'), b]=df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip Cost ($)'), a]
#     df_bom.loc[('Racking Hardware', 'Est. Hardware (e.g. bolts/washers)'), b]=df_bom.loc[('Racking Hardware', 'Est. Hardware (e.g. bolts/washers)'), a]
    
#     df_bom.loc[('Center Gear Drive', 'Est. Center Gear Cost ($)'), b]=df_bom.loc[('Column', 'Est. Number of Columns'), b]/13*700
#     df_bom.loc[('Center Gear Drive', 'Est. Hardware (e.g. bolts/washers)'), b]=df_bom.loc[('Center Gear Drive', 'Est. Center Gear Cost ($)'), b]*0.1
    
#     df_bom.loc[('Total', 'Est. Total Material Cost ($)'), b]= df_bom.loc[('Tubing', 'Est. Tubing Total Cost ($)'), b] \
#                                                             +df_bom.loc[('Column', 'Est. Column Total Cost ($)'), b] \
#                                                             +df_bom.loc[('T - Connection', 'Est. Connection Total Cost ($)'), b] \
#                                                             +df_bom.loc[('T - Connection', 'Est. Hardware (e.g. bolts/washers)'), b] \
#                                                             +df_bom.loc[('Racking Hardware', 'Est. Clamp/Clip Cost ($)'), b] \
#                                                             +df_bom.loc[('Racking Hardware', 'Est. Hardware (e.g. bolts/washers)'), b] \
#                                                             +df_bom.loc[('Center Gear Drive', 'Est. Center Gear Cost ($)'), b] \
#                                                             +df_bom.loc[('Center Gear Drive', 'Est. Hardware (e.g. bolts/washers)'), b]
    
#     df_bom.loc[('Total', 'Est. Dollar per W'), b]=df_bom.loc[('Total', 'Est. Total Material Cost ($)'), b]/(project_size*1000000)
    
#     return df_bom