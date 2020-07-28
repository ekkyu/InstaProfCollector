# -*- coding: utf-8 -*-

import json
import re
import csv
import os
import requests
from typing import Dict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pprint
  
f2= open("user_id.json")
list_user_name = json.load(f2)


class InstaProfCollector:
    
    def __init__(self):
        self.file_pass = "img/{}.png"
        self.plofile_data = {}
        self.instagram_plofile_url = "https://www.instagram.com/{}/"
        self.label = ["id", "url", "biography", "country", "post_num", "follow", "follower", "hashtag_12post"]
        self.post_num_hashtag = 12

    def download_img(self, url, user_name):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            save_file_name = self.file_pass.format(user_name)
            with open(save_file_name, 'wb') as f:
                f.write(r.content)

    def get_jsondata_from_username(self, user_name_i):
        url = self.instagram_plofile_url.format(user_name_i)
        self.plofile_data['url'] = url
        response = requests.get(url, verify=False)

        soup = BeautifulSoup(response.content, 'html.parser') # 'lxml'  -> 'html.parser' 
        js = soup.find("script", text=re.compile("window._sharedData")).text
        json_data = json.loads(js[js.find("{"):js.rfind("}")+1]);
        #pprint.pprint(json_data)
        return json_data
    
    def get_plofile_data_from_jsondata(self, json_data):
        user_data = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        timeline_media = user_data['edge_owner_to_timeline_media'][ 'edges']
        self.plofile_data['url'] = user_data['profile_pic_url']
        self.plofile_data['biography'] = user_data['biography']        
        self.plofile_data['country'] = json_data['country_code']
        self.plofile_data['post_num'] = user_data['edge_owner_to_timeline_media']['count']
        self.plofile_data['follow'] = user_data['edge_follow']['count']
        self.plofile_data['follower'] = user_data['edge_followed_by']['count']
        
        hashtag = []
        for i in range(min(self.post_num_hashtag, int(self.plofile_data['post_num']))):
            try:
                text = timeline_media[i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
                hashtag.append(self.text2hashtag(text))
            except:
                pass
        self.plofile_data['hashtag_12post'] = self.flatten(hashtag)
        
    def text2hashtag(self, text):
        pattern = "\#[^(\ ¥\#¥\n)]*"
        return re.findall(pattern, text)
    
    def flatten(self, nested_list):
        """2重のリストをフラットにする関数"""
        return [e for inner_list in nested_list for e in inner_list]
        
    def save_idlist2json_file(self, data):
        file_name = "data.json"
        fw = open(file_name,'w')
        json.dump(data, fw, indent=4)        
        
    def write2csv(self, row_data):
        if not os.path.exists('data.csv'):
            with open('data.csv', 'w') as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(self.label)    
        with open('data.csv', 'a') as f_csv:
            writer = csv.DictWriter(f_csv, self.label)
            writer.writerow(row_data)
        
    def main_loop(self, list_user_name):
        for user_num_i, user_name_i in enumerate(list_user_name):
            self.plofile_data['id'] = user_name_i
            json_data = self.get_jsondata_from_username(user_name_i)
            self.get_plofile_data_from_jsondata(json_data)
            self.download_img(self.plofile_data['url'], user_name_i)   
            self.write2csv(self.plofile_data)
            
if __name__ == '__main__':
    pc = InstaProfCollector()
    pc.main_loop(list_user_name)
