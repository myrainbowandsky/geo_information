import pandas as pd
import subprocess
import json
from tqdm import tqdm
tqdm.pandas(desc='Geodecoder bar:')
from joblib import Parallel, delayed

def geofunc(_place):
    '''
    _place:str
    '''

    try:
        _command = "nominatim search --query " + _place
    
        # 使用subprocess运行命令
        _result = subprocess.run(_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        _jsonobj = json.loads(_result.stdout)
        
        _temp_result = _jsonobj[0]['display_name']
        
        _temp_lst = _temp_result.split(', ')
        
        _target = [x for x in _temp_lst if x in states_lst][0]
    
        return _target

    except:

        return None
# 读入美国州信息，用以匹配
states = pd.read_csv("../wenlu/geo_information-main/states.csv")#文件目录指定好
states_lst=states['State'].tolist()

place_not_found = pd.read_csv("../wenlu/place_not_found.csv",index_col= [0],nrows=300)#文件目录指定好

#Places=place_not_found['place_name'].tolist()

interval = 100
chunks=[place_not_found[i:i+interval] for i in range(0, len(place_not_found),interval)]

for each_df in tqdm(chunks):

    #eachdf['state'] = eachdf['place_name'].progress_apply(lambda x: geofunc(x))
    lst=Parallel(n_jobs = 5)(delayed(geofunc)(x) for x in tqdm(each_df['place_name'].to_list()))
    
    each_df['state']=lst
    
    each_df.to_csv('Parellel_dataframe.csv',mode='a')
    #place_not_found.loc[,:'state'] = lst
    #print(each_df)

    #pd.DataFrame(lst,columns=['state']).to_csv("parallel_states.csv",mode = "a") # 分快保存到同一文件，mode = a
    
    