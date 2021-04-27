import datetime
import re #Regex library
from os import walk
import yaml
import pandas as pd 
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import numpy as np # name, patientid, date of death, lat, lon
#Float Generator

#-column: blood sugar
#   type: float
#   distribution: {name: 'normal', mean: '5.5', std: '1.5'}
#   constraints: {upper:8 , lower:2}


# name - string field name
# distribution - dictionary 
# constraints - dictionary
# size - num rows
def check_parameters(parameters):
    for p in parameters:
        if type(p) not in [int, float]:
            raise SyntaxError("parameters must to integers or floats")

def float_generator(distribution, constraints, size):
    # Extract parameters from distribution
    # Use the correct function from np and pass in proper parameters + size
    # Clip the distribution based off of lower and upper constraints
    # Insert the values into a Series
   
   #checks if the 'size' input is an integer
    if type(size) != int:
        raise SyntaxError("size must be an integer")
    
    name = distribution['name']
    
    #generates data with numpy random distributions 
    if name == 'normal':
        mean, std = distribution['mean'], distribution['std']
        check_parameters([mean, std])
        data = np.random.normal(mean, std, size)
    

    elif name == 'lognormal':
        mean, std = distribution['mean'], distribution['std']
        check_parameters([mean, std])
        data = np.random.lognormal(mean, std, size)
    
    elif name == 'uniform':
        a, b = distribution['a'], distribution['b']
        check_parameters([a, b])
        if a > b:
            raise SyntaxError("a must be less than b")
        data = np.random.uniform(a, b, size)

    elif name == 'binomial':
        n, p = distribution['n'], distribution['prob']
        check_parameters([n, p])
        data = np.random.binomial(n, p, size)
    
    elif name == 'poisson':
        lam = distribution['lam']
        check_parameters([lam])
        data = np.random.poisson(lam, size)
    
    elif name == 'beta':
        alpha, beta = distribution['alpha'], distribution['beta']
        check_parameters([alpha, beta])
        data = np.random.beta(alpha, beta, size)
    
    elif name == 'gamma':
        shape, scale = distribution['shape'], distribution['scale']
        check_parameters([shape, scale])
        data = np.random.gamma(shape, scale, size)
    
    elif name == 'exponential':
        lam = distribution['lam']
        check_parameters([lam])
        data = np.random.exponential(lam, size)

    #checks if 'name' input is supported by generator 
    else:
        raise SyntaxError(name +" not recognized")

    #checks for constraints 
    if constraints == None:
        return data.tolist()

    #clip outliers based on constraint conditions
    elif 'max' not in constraints:
        data = np.clip(data, a_min = constraints['min'], a_max = None)
        return data.tolist()
    elif 'min' not in constraints:
        data = np.clip(data, a_min = None, a_max = constraints['max'])
        return data.tolist()
    elif 'min' in constraints and 'max' in constraints: 
        data = np.clip(data, a_min = constraints['min'], a_max = constraints['max'])
        return data.tolist()
    #raises error if 'constraints' inputs are invalid
    else:
        raise SyntaxError("min and max not recognized")

def int_generator(distribution, constraints, size):
    # Extract parameters from distribution
    # Use the correct function from np and pass in proper parameters + size
    # Clip the distribution based off of lower and upper constraints
    # Convert values to int type 
    # Insert the values into a Series

    #generate data with np random distributions 
    #checks if user inputs a bernoulli distribution and uses a binomial to generate it
    if type(size) != int:
        raise SyntaxError("size must be an integer")
    
    if distribution['name'] == 'bernoulli':
        data = np.random.binomial(1, distribution['p'], size)
        data = data.tolist()
    
    else:
        data = float_generator(distribution, constraints, size)
    
    #rounds values and convert to ints
    return np.round(data).astype(int).tolist() 

def string_generator(dist, choices, i, data_list, number_of_points):
    for j in range(number_of_points):
        if dist['name'] == 'normal':
            assert 'mean' in dist and 'std' in dist, "must provide mean and std for normal dist"
            a = int(np.random.normal(loc=dist['mean'], scale=dist['std']))
        
        elif dist['name'] == 'lognormal':
            assert 'mean' in dist and 'std' in dist, "must provide mean and std for lognormal dist"
            a = int(np.random.lognormal(loc=dist['mean'], scale=dist['std']))

        elif dist['name'] in ['binomial', 'bernoulli']:
            assert 'n' in dist and 'prob' in dist, "must provide n and prob for binomial or bernoulli"
            a = int(np.random.binomial(n=dist['n'], p=dist['prob']))
        
        elif dist['name'] == 'poisson':
            assert 'lam' in dist, "must provide lam for poission"
            a = int(np.random.poisson(dist['lam']))
        
        elif dist['name'] == 'beta':
            assert 'alpha' in dist and 'beta' in dist, "must provide alpha and beta for beta dist"
            a = int(np.random.beta(dist['alpha'], dist['beta']))
        
        elif dist['name'] == 'gamma':
            assert 'shape' in dist and 'scale' in dist, 'must provide shape and scale for gamma dist'
            a = int(np.random.gamma(dist['shape'], dist['scale']))
        
        elif dist['name'] == 'exponential':
            assert 'lam' in dist, 'must provide lam for exponential'
            a = int(np.random.exponential(dist['lam']))
        
        elif dist['name'] == 'uniform':
            assert 'min' in dist and 'max' in dist, 'must provide min and max for uniform dist (separate from constraints)'
            a = int(np.random.randint(dist['min'], dist['max']))
        
        else:
            raise SyntaxError("Bad String dist type")
        data_list[i].append(choices[a])


def generateDate(size, minYear, maxYear):
    if type(size) != int or type(minYear) != int or type(maxYear) != int:
        raise SyntaxError("size must be an integer")
    if len(str(minYear)) != 4 or len(str(maxYear)) != 4:
        raise SyntaxError("year must be 4 digits")
    i=0
    dates_lst = []
    while i < size:
        i+=1
        dateVal = datetime.date(np.random.randint(minYear, maxYear), np.random.randint(1, 12), np.random.randint(1, 28))
        dates_lst.append(str(dateVal))
    
    return dates_lst

def datagen(direc, filename):
    assert type(direc) == str and type(filename) == str, "datagen accepts a file directory and filename in string format as its arguments."
    data_list = {}
    try:
        a = open(direc + filename)
    except FileNotFoundError:
        raise TypeError("File " + direc + filename + " does not exist at the specified directory.")
    except:
        raise Exception("Another error occurred.")
    try:
        loaded = yaml.load(a, Loader=yaml.FullLoader)
    except:
        raise SyntaxError("Improperly formatted yaml file: " + direc + filename)
    assert 'rows' in loaded, "number of rows not specified in " + direc + filename + "."
    rows = loaded['rows']
    assert type(rows) in [int, float] and rows >= 1, "number of rows improperly specified in " + direc + filename + "."

    for i in list(loaded)[1:]:
        assert 'type' in loaded[i], "no type for column " + i
        the_type = loaded[i]['type']
        assert 'distribution' in loaded[i], "no distribution specified for column " + i
        the_dist = loaded[i]['distribution']

        the_consts = loaded[i]['constraints']

        if the_type == 'int':
            data_list[i] = int_generator(the_dist, the_consts, rows)
        
        elif the_type == 'float':
            data_list[i] = float_generator(the_dist, the_consts, rows)
        
        elif the_type == 'string': 
            assert 'strings' in loaded[i] and type(loaded[i]['strings'] == str), 'improperly specified string path for ' + i
            try:
                choices = open(direc + loaded[i]['strings'],'r').read().split(", ")
            except:
                raise FileNotFoundError("Bad file directory for " + i + ":" + direc + loaded[i]['strings'])
            data_list[i] = []
            string_generator(the_dist, choices, i, data_list, rows)
        
        elif loaded[i]['type'] == 'date':
            data_list[i] = generateDate(rows, the_consts['min'], the_consts['max'])
            # OLD CODE BELOW
            #if loaded[i]['pair_of_dates'] == 1:
            #    generated = generate_birthDate(rows, the_consts['min'], the_consts['max'])
            #    data_list[i + "_start"] = generated[0]
            #    data_list[i + "_end"] = generated[1]
            #elif loaded[i]['pair_of_dates'] == 0:
            #    generated = generate_birthDate(rows, the_consts['min'], the_consts['max'])
            #    data_list[i] = generated[0]
        else:
            raise SyntaxError("Type for " + i + " not 'int', 'float', 'string', or 'date': " + loaded[i]['type'])
        df = pd.DataFrame(data_list)
    return df.to_csv("../synthetic-data/" + filename[:-5] + ".csv") #(CSV for each yaml file -> synthetic-data directory)

def to_integer(dt_time):
    return 1*dt_time.year
    
def generate_all_yamls(yaml_directory):
    returned = []

    for root, dirs, files in walk(yaml_directory):
        for filename in files:
            print(filename)
            if ".yaml" in filename:
                try:
                    returned.append(datagen(yaml_directory, filename))
                except:
                    returned.append({filename: "generation failed"})
    return returned

def main():
    generate_all_yamls("../yaml-files/")