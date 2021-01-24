#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 16:29:34 2020

@author: lfiorentini
"""

import pandas as pd
from datetime import datetime
import argparse
import re

def transform_data(in_str): 
    """
    This functions modifies the time format.
    The data format the FBProphet deals with are
    YYYY-MM-DD for a date or YYYY-MM-DD HH:MM:SS
    using python datetime format those translate as
    %Y-%m-%d and %Y-%m-%d %H:%M:%S
    
    Parameters
    ----------
    in_str : str
        Current time description.

    Returns
    -------
    str
        Time with format %Y-%m-%d.

    """
    redict = {'janv.' : '01',
              'févr.' : '02',
              'mars' : '03',
              'avr.' : '04',
              'mai' : '05',
              'juin' : '06',
              'juil.' : '07',
              'août' : '08',
              'sept.' : '09',
              'oct.' : '10',
              'nov.' : '11',
              'déc.' : '12'}
    for k,v in redict.items():
        in_str = re.sub(k, v, in_str)

    return datetime.strptime(in_str, "%d %m %Y").strftime("%Y-%m-%d")

parser = argparse.ArgumentParser()
parser.add_argument("-i", help = "input file", default = "", type = str)
parser.add_argument("-o", help = "output file", default = "", type = str)
input_file = str(parser.parse_args().i)
output_file = str(parser.parse_args().o)

Data = pd.read_csv(input_file)
old_col = Data.columns
Data['ds'] = Data['Date'].apply(transform_data)
Data['y'] = Data['Comptes utilisateur actifs'].apply(lambda x: float(x))
Data.drop(old_col, inplace = True, axis = 1)
Data.to_csv(output_file, index = False)
