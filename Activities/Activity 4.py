import hashlib
import requests
import datetime
import pandas as pd
from pprint import pprint as pp
import string

timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
pub_key = 'cd1801ea0846d8d7660589467e5c93ab'
priv_key = 'cf528fb5ffdf9a1e0ec379d2e1ea50e37d042cb2'

final_results = pd.DataFrame()
def hash_params():
    """ Marvel API requires server side API calls to include
    md5 hash of timestamp + public key + private key """

    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{priv_key}{pub_key}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()

    return hashed_params


def marvel_character(apikey,hash_prm,nameStartsWith):
    try:
        limit=100
        params = {'ts': timestamp, 'apikey':apikey , 'hash': hash_prm, 'nameStartsWith' :nameStartsWith,'limit':limit};
        res = requests.get('https://gateway.marvel.com:443/v1/public/characters',params=params)
        results = res.json()
        #print(results)
        df_characters = pd.DataFrame(results["data"]["results"])
        return df_characters
    except Exception as e:
        print(e)
        print("Parameters not found")


final_results = pd.DataFrame() 


letters_no=list(string.ascii_lowercase+string.digits)
letters_no.remove('0')
for c in letters_no:
    temp=marvel_character(pub_key,hash_params(),c)
    final_results = final_results.append(temp)
final_results


def ret_avail(x):
    t = x['available']
    return t

final_results['number_of_events'] = final_results.apply(lambda x: ret_avail(x.events), axis = 1)
final_results['number_of_series'] = final_results.apply(lambda x: ret_avail(x.series), axis = 1)
final_results['number_of_stories'] = final_results.apply(lambda x: ret_avail(x.stories), axis = 1)
final_results['number_of_comics'] = final_results.apply(lambda x: ret_avail(x.comics), axis = 1)
final_results = final_results.rename(columns = {'id':'character_id', 'name':'character_name'})
final_results_final = final_results[['character_name','number_of_events', 'number_of_series', 'number_of_stories',
       'number_of_comics','character_id']]
final_results_final

def ret_filtered_df(df,col,condition,filter_val):
    marvel_filter=lambda x, condition,filter_val: x if eval(f'{x}{condition}{filter_val}') else ''
    df[col]=df[col].apply(marvel_filter,args=(condition,filter_val))
    df=df[df[col].notnull()]
    return df


import numpy as np
ret_filtered_df(final_results_final,'number_of_stories','>','5')