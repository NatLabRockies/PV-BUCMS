import pandas as pd
import numpy as np
import matplotlib as plt

tuples = [('Power Dimension', 'AC active power, P_AC = S_AC × cosφ'),
         ('Power Dimension', 'DC input power of the inverter: P_DC = P_AC / η'),
         ('Power Dimension', 'PV array power: P_(DC-array) = P_DC / N'),
         ('Voltage Dimension', 'Max. open-circuit voltage: V_(OC,max)'),
         ('Voltage Dimension', 'Min. open-circuit voltage: V_(OC,min)'),
         ('Strings', 'Max. module # per string'),
         ('Strings', 'Min. module # per string'),
         ('Strings', '% change of module # per string, compared to 600V'),
         ('Strings', 'String #'),
         ('Strings', '% change of string #, compared to 600V'),
         ('Strings', '……...Reduce trenching, cables, conduit, wiring'),
         ("Combiner Box", 'Combiner box #'),
         ("Combiner Box", '% change of combiner box #, compared to 600V'),
         ('Inverter', 'Min. number of strings per inverter'),
         ('Inverter', 'Max. number of strings per inverter'),
         ('Inverter', '% change of string # per inverter'),
         ('Inverter', 'Inverter #'),
         ('Inverter', '% change of inverter #, compared to 600V'),
        ]

def inverter_calculations(num_modules, df_inverter, df_sys_cond):
    index = pd.MultiIndex.from_tuples(tuples, names = ['Category','Description'])
    inv_col = df_inverter.columns
    df_inv_calc = pd.DataFrame(index = index, columns=inv_col)
    df_inv_calc.loc['Power Dimension', 'AC active power, P_AC = S_AC × cosφ']= df_inverter.loc['Output AC','Apparent power (Sac), nominal AC power']*df_inverter.loc['Output AC','Power factor cos φ']
    df_inv_calc.loc['Power Dimension', 'DC input power of the inverter: P_DC = P_AC / η']= df_inv_calc.loc['Power Dimension', 'AC active power, P_AC = S_AC × cosφ']/df_inverter.loc['Output AC','CEC Efficiency (η)']
    df_inv_calc.loc['Power Dimension', 'PV array power: P_(DC-array) = P_DC / N']= df_inv_calc.loc['Power Dimension', 'DC input power of the inverter: P_DC = P_AC / η']/df_inverter.loc['Input DC','Nominal power ratio (N), assumed']

    df_inv_calc.loc['Voltage Dimension', 'Max. open-circuit voltage: V_(OC,max)']= (df_sys_cond.loc['Module','Open-circuit voltage (Voc)']*(1.0+df_sys_cond.loc['Module','Temperature coefficient of open-circuit current']*(df_sys_cond.loc['Site','Min. cell temperature of PV module']-25.0))).values
    df_inv_calc.loc['Voltage Dimension', 'Min. open-circuit voltage: V_(OC,min)']= (df_sys_cond.loc['Module','Voltage at max. power (Vmpp)']*(1.0+df_sys_cond.loc['Module','Temperature coefficient of open-circuit current']*(df_sys_cond.loc['Site','Max. cell temperature of PV module']-25.0))).values

    df_inv_calc.loc['Strings', 'Max. module # per string']=df_inverter.loc['Input DC','Max. input voltage']/df_inv_calc.loc['Voltage Dimension', 'Max. open-circuit voltage: V_(OC,max)']
    df_inv_calc.loc['Strings', 'Min. module # per string']=df_inverter.loc['Input DC','Min. input voltage']/df_inv_calc.loc['Voltage Dimension', 'Min. open-circuit voltage: V_(OC,min)']
    df_inv_calc.loc['Strings', 'String #']= num_modules/df_inv_calc.loc['Strings', 'Max. module # per string']
    
    df_inv_calc.loc['Combiner Box', 'Combiner box #']= df_inv_calc.loc['Strings', 'String #']/12
    
    df_inv_calc.loc['Inverter', 'Min. number of strings per inverter']=df_inv_calc.loc['Power Dimension', 'PV array power: P_(DC-array) = P_DC / N']*1000.0/(df_sys_cond.loc['Module','Max. Power'].values*df_inv_calc.loc['Strings', 'Max. module # per string'])
    df_inv_calc.loc['Inverter', 'Max. number of strings per inverter']=df_inverter.loc['Input DC','Max. input current per string']/df_sys_cond.loc['Module','Current at max. power (Impp)'].values
    df_inv_calc.loc['Inverter', 'Inverter #']=df_inv_calc.loc['Strings', 'String #']/df_inv_calc.loc['Inverter', 'Max. number of strings per inverter']
    
    return df_inv_calc