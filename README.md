# Medic Synthetic Data Generator
# Setup 
1. `pip install virtualenv`
2. `python -m venv myvenv/`
3. `source myvenv/bin/activate`
OR `source myvenv/Scripts/activate`
4. `pip install -r requirements.txt` 

# Instructions 
1. Upload .xml files into the *xml-files* directory 
2. Within the scripts directory, run: `python3 xml-parse.py`
  1. This function will parse every .xml file in the directory for their field names and produce empty .yaml files in the *yaml-files* directory
3. In the *yaml-files* directory, fill in each yaml file following guidelines written in the **DATATYPE KEYS** section of this document
  1. For each string field, create a new `.txt` file in the folder *yaml-files/default-text* which contains a list of strings to be sampled from
4. Within the *scripts* directory, run: `python3 data_generator.py`
  1. For detailed debugging, input `python3 data_generator.py --verbose`
5. Outputted synthetic datasets are within the synthetic-data directory


# Directory Structure
Explanation of the directory structure.
- **myvenv:** virtual environment initialization
- **example-files**: contains example xml, yaml, and csv files for user understanding of how to use the synthetic data generator
- **scripts:** contains all executable python code for xml parsing and synthetic data generation
- **xml-files:** where users input xml files produced from forms
- **yaml-files:** contains empty .yaml files outputted from xml-parse.py. Users must manually fill out each .yaml file in this directory.
  - **default-text:** contains user inputted text files which have comma-separated string values which are sampled from in the data generator. Every string field in a .yaml file must contain a path to a specific file in this directory to sample values from.
- **synthetic-data:** contains outputted synthetic data files in the form of .csv

# YAML Structure
The yaml files will need to be manually filled out by users in a specific format. The very first line in the yaml will contain a *rows* key which takes in the number of dataset entries to be generated.\
\
Following this first line, each field will contain a section containing its type, distribution, and constraints. Examples of properly formatted yamls can be found in the *example-files* directory.\
\
Shown below is a sample snippet:

```
rows: 20
_id: 
  constraints: ~
  distribution: 
    a: 0
    b: 1234
    name: uniform
  type: int
birth_date: 
  constraints: 
    max: 2021
    min: 1950
  distribution: ~
  type: date
date_of_birth: 
  constraints: 
    max: 1960
    min: 1900
  distribution: ~
  type: date
```


# Datatype Keys

## Floats 
Float values are sampled from 8 supported distributions generated by numpy.random sampling: normal, lognormal, uniform, binomial, poisson, beta, gamma, and exponential. 
Users input desired data types, distribution names and parameters, and constraints in a YAMl file. The inputs are parsed and passed through the float generator.

The inputs for a YAML file are detailed below. 
- **Type:** The type of data the user wish to generate. In this case, the type is float.
- **Distribution:** The name of the distribution the user wishes generate the data from and its corresponding parameters. 
- **Constraints(optional):** The maximum and minimum values the user wishes to keep the generated data between. 

The supported distribution names and parameters are:
* normal: mean, std
* lognormal: mean, std
* uniform: a, b 
* binomial: n, p 
* poisson: lam 
* beta: alpha, beta 
* gamma: shape, scale 
* exponential: lam 

Examples of user inputs in a YAML file are shown:
```
heart_rate:
  constraints:
    min: 50
    max: 150
  distribution: 
    name: normal
    mean: 90
    std: 5
  type: float
```
```
blood_pressure:
  constraints:
    min: null
    max: 150
  distribution: 
    name: poisson
    lam : 120
  type: float
```

## Integers 
Integers are sampled using a Bernoulli distribution, as well as the 8 distributions used in the float generator function.
The int_generator function takes in a distribution, constraints, and size, which users can input in a YAML file. 

- **Type:** int
- **Distribution:** Bernoulli(p) and supported float distributions.
- **Constraints(optional):** The maximum and minimum values the user wishes to keep the generated data between. 

Examples of user inputs in a YAML file are shown:
```
patient_id:
  constraints: ~
  distribution: 
    name: bernoulli
    p: 0.5
  type: int
```
## Strings

Strings are randomly sampled using discrete integer probability distributions. Strings to sample from are specified by a comma-delineated .txt file 
in ./yaml-files/default-text/. This file should be referenced in the `string` attribute for the data column. Distributions supported include all distributions supported for integers.

Example:
```
province:
  constraints: ~
  distribution:
  name: normal
    mean: 50
    std: 2
  strings: ./default-text/province.txt
  type: string
```
Example of `province.txt`:
```
Alberta, British Columbia, Manitoba, New Brunswick, Newfoundland and Labrador, Nova Scotia, Ontario, Prince Edward Island, Quebec, Saskatchewan
```

## Dates 

- **Type:** Dates are being generated as a DateTime object.
- **Distribution:** Dates are not being sampled from any type of distribution. 
- **Constraints:** Users should input a range of years, in the form of a minimum year and a maximum year. Dates will be generated between this range of years.  -

Examples of user inputs in a YAML file are shown:
```
birthdate:
  constraints:
    min: 1900
    max: 2000
  distribution: ~
  type: date
```



# Current Issues/Further Improvements
* Dates are randomly generated without distribution.
* Does not take into constraints regarding relationship between birthdate and deathdate
* Do not currently have a multiselect datatype

# Project Background
For a number of reasons, Medic would like to have a means of creating realistic synthetic datasets. First, the data collected by the CHT are sensitive and contain Personal Identifiable Information (PII) and Protected Health Information (PHI), and cannot be shared with partner organizations without signing DUAs/NDAs. Having artificial versions that resemble real datasets would allow Medic to share data with data science partners and/or publish them in open repositories. Second, it would be nice to use realistic datasets when testing new models, analyses or features. Synthetic datasets could also facilitate QA work and dashboard building. Ideally, the tool is able to generate data fitting a schema generated from the source code of a CHT application.

# Contributors
**Data Science Society @ Berkeley - Social Good Committee Spring 2021** 
* Steven Chen - schen1822@berkeley.edu 
* Andi Halim - andihalim@berkeley.edu
* Jae Hee Koh - jaeheekoh@berkeley.edu
* Rithik Goli - rithikgoli@berkeley.edu
* Ingrid Chien - ingrid070401@berkeley.edu
* Spencer Jenkins - spencerrjenkins@berkeley.edu








