#!/usr/bin/env python
# coding: utf-8

# # FMD Analysis ver10
# 
# 使用Perspective API分析文本毒性

# In[1]:


import json
import pickle
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# 输出DataFrame时显示所有的列
pd.set_option('display.max_columns', None)
# 输出DataFrame时每行显示完整的内容
pd.set_option('display.max_colwidth', None)

def load_variable(filename):
    f = open(filename, 'rb')
    r = pickle.load(f)
    f.close()
    return r


# In[3]:


# 存取用户推文数据
user_texts_ver2 = pd.read_csv("English_retweets_contain_3media_groupby_author.csv")
#pickle.dump(user_texts_ver2_py311, open("pkl/user_texts_ver2_py311.pkl", 'wb'))
#user_texts_ver2 = load_variable("pkl/user_texts_ver2_py311.pkl")


# In[4]:


# 访问API的函数体
from googleapiclient import discovery

def perspective_analyze(text):

    API_KEY = '***'

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {}
        }
    }

    return client.comments().analyze(body=analyze_request).execute()


# In[6]:


# 使用API分析
user_texts_ver2['perspective_api_results'] = ''
for i in user_texts_ver2.index:
    try:
        user_texts_ver2['perspective_api_results'][i] = perspective_analyze(user_texts_ver2['text'][i])
    except:
        pass    # 为了不让特殊错误使程序暂停，出错时直接pass掉
        #print('failed:', end='')
    # 以下被注释掉的代码用来计数
    #if i != 0 and i % 20 == 0:
        #print('\n', end='')
    #print(i, end=' ')


# In[ ]:


# 保存文件
user_texts_ver2.to_csv("user_texts_with_perspective_api_results.csv", index=False)


# In[ ]:


pass

