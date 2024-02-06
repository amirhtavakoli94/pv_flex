# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 17:20:36 2024

@author: amirhossein.tavakoli
"""

 
import pandas as pd

import linear_model

import ILP_model_B
import ILP_model_C_packs

class Instance_Schedule:
    def __init__(self, dataframe):
        for column_name in dataframe:
            attr_name = column_name.lower().replace(' ', '_').replace(',', '').replace('/','_')
            setattr(self, attr_name, dataframe[column_name].values)
            




input_data = pd.read_excel("technical_task_test_data.xlsx")
instance_schedule = Instance_Schedule(input_data)

optimal_model_A = linear_model.build_common_model(instance_schedule)
optimal_model_A.optimize()



optimal_model_B = ILP_model_B.build_common_model(instance_schedule)
optimal_model_B.optimize()




optimal_model_C = ILP_model_C_packs.build_common_model(instance_schedule)
optimal_model_C.optimize()

