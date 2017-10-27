import pandas as pd
import numpy as np
import glob as glob
import pandas as pd
import requests
import json

def crime_counts_by_msoa(directory, crime_type = 'All'):
    """This function reads UK crime files and returns a Pandas dataframe."""
    crimes = pd.DataFrame(columns=['Month', 'LSOA code', 'LSOA name', 'Crime type', 'MSOA'])
    for file in glob.glob(directory + '/*.csv'):
        crime = pd.read_csv(file, usecols=[1,7,8,9], dtype={'Month': 'str', 'LSOA code': 'str', 'LSOA name': 'str', 'Crime type': 'str'})
        crime['MSOA'] = crime['LSOA name'].str[:-1]
        crimes = crimes.append(crime)
    if crime_type != 'All':
        crimes = crimes.loc[crimes['Crime type'] == crime_type]
    return crimes.groupby(['MSOA']).size().reset_index(name='crimes')

def load_residents():
    _residents = pd.read_csv('data/residents/census-msoa-residents.csv', dtype={'msoa': 'str', 'residents': 'int64'}, usecols=[1,4])
    _residents.columns = ['MSOA', 'residents']
    return _residents

def get_crimes_and_residents(crimes, residents):
    """This function takes the crimes and residents data frames and returns a dataframe with the crime / residents ratio"""
    crime_and_residents = pd.merge(residents, crimes, on='MSOA', how='inner')
    crime_and_residents['ratio'] = crime_and_residents.apply(lambda row: row[2] / row[1], axis=1)
    return crime_and_residents

def post_code_lookup(postcode):
    """This function returns some extra information about a
    UK post code such as LSOA, MSOA, outcode and incode."""
    pc = postcode.replace(' ', '')
    try:
        response = requests.get('http://api.postcodes.io/postcodes/' + pc)
        if response.status_code == 200:
            jsonResponse = response.json()
            return [jsonResponse['result']['outcode'], jsonResponse['result']['incode'], jsonResponse['result']['msoa'], jsonResponse['result']['lsoa']]
    except UnicodeDecodeError:
        print('error')

def plants():
    """This function loads, slices and de de-duplicates 
    meat manifacturing implants from the UK regulation three sections.
    It also parses the postcode and spits into incode and outcode."""
    sections = []
    for section_name in ['section_i', 'section_ii', 'section_iii']:
        section = pd.read_csv('data/sections/' + section_name + '.csv', usecols=[0, 1,6], dtype={'Postcode': 'str'})
        section = section[pd.notnull(section['Postcode'])]
        section_with_parsed_postcode = section['Postcode'].apply(post_code_lookup).apply(pd.Series)
        section_with_parsed_postcode.columns = ['outcode', 'incode', 'msoa', 'lsoa']
        full_section = pd.concat([section, section_with_parsed_postcode], axis=1)
        full_section = full_section[pd.notnull(full_section['outcode'])]
        sections.append(full_section)
    return pd.concat(sections).drop_duplicates(['Approval Number'])