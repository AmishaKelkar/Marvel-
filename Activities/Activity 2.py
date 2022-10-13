import hashlib
import requests
import datetime
import pandas as pd
from pprint import pprint as pp
import warnings
warnings.simplefilter(action='ignore',category=FutureWarning)

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

limit=100
final_results = pd.DataFrame()
import string
letters_no=list(string.ascii_lowercase+string.digits)
letters_no.remove('0')
for c in letters_no:
    #params['nameStartsWith']=c
    params = {'ts': timestamp, 'apikey': pub_key, 'hash': hash_params(), 'nameStartsWith' :c,'limit':limit};
    res = requests.get('https://gateway.marvel.com:443/v1/public/characters',
                       params=params, )

    results = res.json()
    #print(results)
    df_characters = pd.DataFrame(results["data"]["results"])
    final_results = final_results.append(df_characters)
    
df_characters=final_results

def ret_avail(x):
    t = x['available']
    return t

df_characters['number_of_events'] = df_characters.apply(lambda x: ret_avail(x.events), axis = 1)
df_characters['number_of_series'] = df_characters.apply(lambda x: ret_avail(x.series), axis = 1)
df_characters['number_of_stories'] = df_characters.apply(lambda x: ret_avail(x.stories), axis = 1)
df_characters['number_of_comics'] = df_characters.apply(lambda x: ret_avail(x.comics), axis = 1)
df_characters = df_characters.rename(columns = {'id':'character_id', 'name':'character_name'})
df_characters_final = df_characters[['character_name','number_of_events', 'number_of_series', 'number_of_stories',
       'number_of_comics','character_id']]
df_characters_final