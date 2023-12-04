import pandas as pd
from joblib import Parallel,delayed
import sys
sys.path.append('/root/anaconda3/envs/Project6/lib/python3.8/site-packages')

from tqdm import tqdm
tqdm.pandas(desc='bar')
import logging

from googleapiclient import discovery
API_KEY = ''
client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)
def get_perspective(text):
    analyze_request = {
      'comment': { 'text': text},
      'requestedAttributes': {
          'TOXICITY': {}, 
      }
    }
    
    try:

        perspective_dic = client.comments().analyze(body=analyze_request).execute()
        summaryScore= perspective_dic['attributeScores']['TOXICITY']['summaryScore']['value']
    except Exception as e:
        logging.warning(Exception)
        summaryScore = e
    
    return summaryScore

#score=get_perspective('i live here, i kill cats. Cats must die.')
df=pd.read_csv('user_text4.csv')
df=df[df['text'].notna()]
df=df.groupby(by='user_screen_name').agg(text=("text", lambda x: ",".join(set(x))))
#old_toxity=pd.read_csv('../Project6/Toxity/data.csv')

interval=100
dflst = [df[i:i+interval] for i in range(0,df.shape[0],interval)]

for eachdf in tqdm(dflst):
  #Parallel(n_jobs=1)(delayed(sqrt)(i**2) for i in range(10))
  toxicitylst=Parallel(n_jobs=4)(delayed(get_perspective)(x) for x in eachdf['text'])

  data=pd.DataFrame(toxicitylst,columns=['TOXICITY'])
  #dfdata=pd.concat([eachdf.reset_index('inplace=True'),data],axis=1)
  data.to_csv('wenlu_toxicity.csv',mode='a')