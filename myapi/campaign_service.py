import pandas as pd
import json
import numpy as np
from myapi.db import *

def get_users_data():
    user_query= '''select id, name,email, balance from users;'''
    # Fetch all rows from the result
    result = db_fetch(user_query)
    users_df = pd.DataFrame(result['rows'], columns=result['columns'])
    users_df.dropna()
    return users_df


def get_leads_data():
    # define the query for campaigns_df
    leads_query =  '''
                    SELECT campaign_id, count(id) as leads FROM campaign_leads
                    where campaign_id is not null group by campaign_id ;
                    '''

    # execute the campaigns query and create campaigns_df
    leads_result = db_fetch(leads_query)
    leads_df = pd.DataFrame(leads_result['rows'], columns=leads_result['columns'])
    leads_df['campaign_id'] = leads_df['campaign_id'].astype("Int64")
    leads_df.dropna()
    return leads_df 


