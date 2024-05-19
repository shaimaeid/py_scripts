from myapi.logger import mylogger
from flask import current_app as app
import requests
import pandas as pd
import os
import json

advertiser_id = os.environ.get('ADVERTISER_ID')
api_url = os.environ.get('API_URL')
access_token = os.environ.get('ACCESS_TOKEN')

def get_tiktok(endpoint ,data, filtering = {}):
  global api_url, access_token ,advertiser_id
  print(api_url)
  print(filtering)
  headers = {
      'Access-Token': access_token,
      'Content-Type': 'application/json'
  }
  filtering_str = json.dumps(filtering, ensure_ascii=False)
  api_full_url = f'{api_url}/{endpoint}?advertiser_id={advertiser_id}&filtering={filtering_str}'
  mylogger.info(filtering_str)
  response = requests.get(api_full_url, headers=headers)

  if response.status_code == 200:
    data = response.json()
    print(data)
    mylogger.info(data)
    df = pd.DataFrame(data['data']['list'])
    return df
  else:
    print('Error:', response.status_code)
    return None
  
def post_tiktok(endpoint ,data):
  global api_url, access_token ,advertiser_id
  print(api_url)

  headers = {
      'Access-Token': access_token,
      'Content-Type': 'application/json'
  }

  api_full_url = f'{api_url}/{endpoint}?advertiser_id={advertiser_id}'
  response = requests.post(api_full_url, headers=headers, json=data)

  if response.status_code == 200:
    data = response.json()
    print(data)
    mylogger.info(data)
    return True
  else:
    print('Error:', response.status_code)
    return None


def get_tiktok_campaign(data):
    endpoint='campaign/get/'
    # Get the campaign IDs from the request data
    campaign_ids = data["campaign_ids"]
   
    filtering = {"campaign_ids": campaign_ids}
    df = get_tiktok(endpoint , data ,  filtering)
    df = df[['campaign_id', 'campaign_name', 'budget','operation_status' ,'create_time']]
    return df

def create_tiktok_campaign(data):
    global api_url, access_token ,advertiser_id
    endpoint='campaign/create/'
    
    args = {
    "budget": 0.0,
    "budget_mode": "BUDGET_MODE_INFINITE",
    "campaign_type": "REGULAR_CAMPAIGN",
    "advertiser_id": advertiser_id,
    "objective_type": "LEAD_GENERATION",
    "campaign_name": "API shaimaa Py",
    "objective": "LANDING_PAGE"
    }
    result = post_tiktok(endpoint , args)
    return result

