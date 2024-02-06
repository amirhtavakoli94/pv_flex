# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 21:42:57 2024

@author: amirhossein.tavakoli
"""

import gurobipy as gp
from gurobipy import GRB





def build_common_model(inst):
    """Building linear model"""

    lp = gp.Model('energy_linear_model')
    lp.update()

    qvar_SB = {}  # flow_solar_battery
    hvar_B = {}   # storage_battery
    qvar_GB = {}  # flow_grid_battery
    qvar_BG = {}  # flow_battery_grid
    qvar_SD = {}  # flow_solar_demand
    qvar_GD = {}  # flow_grid_demand
    qvar_SG = {}  # flow_solar_grid
    qvar_BD = {}  # flow_battery_demand
    qexpr_B = {}  # flow_battery_charge(positive)_discharge(negative)_total
    
    horizon = range(len(inst.datetime))
    
    
    for t in horizon:
        qvar_BD[t] = lp.addVar(lb= 0, ub= 10000)
        qvar_BG[t] = lp.addVar(lb= 0, ub= 10000)
        qvar_GB[t] = lp.addVar(lb= 0, ub= 10000)
        qvar_GD[t] = lp.addVar(lb= 0, ub= 10000)
        qvar_SB[t] = lp.addVar(lb= 0, ub= inst.pv_production_kwh[t])
        qvar_SG[t] = lp.addVar(lb= 0, ub= inst.pv_production_kwh[t])
        qvar_SD[t] = lp.addVar(lb= 0, ub= inst.pv_production_kwh[t])
        
        qexpr_B[t] = lp.addVar(lb= -100, ub= 100)
        
    for t in horizon:
        if t == 0:
            hvar_B[t] = lp.addVar(lb=0, ub=0)
        else:
            hvar_B[t] = lp.addVar(lb=0, ub= 160)
    
    hvar_B[len(inst.datetime)] = lp.addVar(lb=0, ub= 160)
    
    for t in horizon:
        lp.addConstr(hvar_B[t] <= 160)
        lp.addConstr(hvar_B[t] >= 0)
    
    #flow conservation cnstrs
    for t in horizon:
        lp.addConstr(0.92*qvar_SB[t] + 0.92*qvar_GB[t] - qvar_BG[t] - qvar_BD[t] == qexpr_B[t])
        lp.addConstr(qvar_SD[t]+qvar_BD[t]+qvar_GD[t] == inst.electrical_consumption_kwh[t])
        lp.addConstr(qvar_SD[t]+qvar_SB[t]+qvar_SG[t] == inst.pv_production_kwh[t])
        
    for t in horizon:
        lp.addConstr(hvar_B[t+1] == hvar_B[t] + qexpr_B[t])
    
    
    #objective function
    obj = gp.quicksum(-qvar_SG[t]*inst.electricity_selling_price_c_kwh[t]- qvar_BG[t]*inst.electricity_selling_price_c_kwh[t] + hvar_B[t]* 9.3 + qvar_GB[t]*inst.electricity_buying_price_c_kwh[t]+ qvar_GD[t]*inst.electricity_buying_price_c_kwh[t]  for t in horizon)
    lp.setObjective(obj, GRB.MINIMIZE)
    
    lp.update()
    
    return lp