from random import sample
from datetime import datetime, timedelta

def intersection(ls1, ls2): 
    '''Finding the intersection of two lists. It preserves the order of as those in ls1.'''
    ls3 = [(i, value) for i, value in enumerate(ls1) if value in ls2] 
    return ls3

def overlapping_lists(ls1, ls2):
    return bool(set(ls1) & set(ls2))
    
def remove_empty_lists(d1):
    d2 = {key: value for key ,value in d1.items() if len(value) > 0}
    return d2
             
def get_duration(fmt, start, end):
    '''Obtains the duration of time between the timestamps start and end.'''
    tdelta = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
    return tdelta

def clean_dict(d1):
    '''Cleans a dictionary from empty lists and duplicated entries, returning
    a copy of a cleaned copy and a duplicated copy'.'''
    d2 = {}
    for i, j in d1.items():
        if len(j) > 0:
            d2[i] = list(set(j))
    return d2

def count_dict_values(d1):
    '''Counting all the number of different values in a dictionary.'''
    count = 0
    for i, j in d1.items():
        count += len(d1[i])
    return count

def get_token(d1, target):
    '''Returning the token key for a given value in a dictionary.''' 
    for key, value in d1.items(): 
         if value == target: 
             return key 

def shuffle_with_fix(ls1, indices):
    shuffle_indices, shuffle_elements = zip(*[(i, j) for i, j in enumerate(ls1) if i not in indices])
    shuffle_indices = list(shuffle_indices)
    ls2 = sample(shuffle_indices, len(shuffle_indices))
    for i, j in zip(ls2, shuffle_elements):
        ls1[i] = j
    return ls1

def tokenization(ls):
    '''Creates tokens using the positional index of each item in the list. Returns
    a dictionary.''' 
    tokens = {}
    for i, j in enumerate(ls):
        tokens[i] = j
    return tokens