#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests 
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date


# In[ ]:


##-date-##
today = date.today()
formated_date = today.strftime("%d-%m-%Y")

##-dataframe and display options--##
df = pd.DataFrame(columns = ['Item Name','Item Price'])
pd.set_option('display.max_colwidth', None)


# In[ ]:


##-Creating dictionaries-##
category_set = ['Computers', 'Phone_Parts', 'Air_Conditioners', 'PC_Accessories', 'Televisions', 'Photo_Video', 
                'Tablets', 'Audio', 'Navigation', 'Phones', 'Home_Utilities', 'Miscellaneous']
page_category = ['https://www.olx.bg/elektronika/kompyutri/?page=',
                 'https://www.olx.bg/elektronika/aksesoari-chasti-za-telefoni/?page=',
                 'https://www.olx.bg/elektronika/klimatitsi/?page=',
                 'https://www.olx.bg/elektronika/kompyutrni-aksesoari-chasti/?page=',
                 'https://www.olx.bg/elektronika/televizori/?page=',
                 'https://www.olx.bg/elektronika/foto-video/?page=',
                 'https://www.olx.bg/elektronika/tableti-chettsi/?page=',
                 'https://www.olx.bg/elektronika/audio-tehnika/?page=',
                 'https://www.olx.bg/elektronika/navigatsiya/?page=',
                 'https://www.olx.bg/elektronika/telefoni/?page=',
                 'https://www.olx.bg/elektronika/domakinski-uredi/?page=',
                 'https://www.olx.bg/elektronika/drugi/?page=']

page_category_number = list(range(1, 13))
df_list = ["df" + str(i) for i in range(1,26)]


# In[ ]:


##-Providing the end-user with a paginated list of categories to choose from-##
pgn_index = -1
print("Please select a number for the Electronics category you'd like to scrape.")
for x in page_category:
    pgn_index += 1
    print(str(page_category_number[pgn_index]) + '. ' + x)


# In[ ]:


##-Taking user input-##
user_category = input()
user_category = int(user_category)
user_category = user_category - 1


# In[ ]:


##-Generating a placeholder-list for dataframes-##
cat_index = 0
category_set[cat_index] = [x + "_" + category_set[user_category] for x in df_list]


# In[ ]:


##-Setting indices to loop through every page in the respective category (25 pages per default)-##
page_number = 0
cat_index = 0
df_index = -1

try:
    while df_index < 24:
        ##-Setting the indices for iteration-##
        df_index += 1
        page_number += 1
        
        ##-Web-scraping-##
        url = (page_category[user_category] + str(page_number))
        reqs = requests.get(url + str(page_number))
        soup = BeautifulSoup(reqs.content, 'html.parser')
        results = soup.find_all('strong')
        
        ##-Converting scraped results to string; erasing tags, cleansing data; filtering lists-##
        resultslist = str(results)
        resultslist = resultslist.split("</strong>,")
        resultslist = resultslist[3:-6] 
        resultslist = [e[9:] for e in resultslist] 
        items = resultslist[::2]
        prices = resultslist[1::2]
        prices = [e[:-4] for e in prices] 
        
        ##-Creating the dataframe and assigning the lists' values to the columns-##
        category_set[cat_index][df_index] = pd.DataFrame(columns = ['Item Name','Item Price'])
        category_set[cat_index][df_index]['Item Name'] = pd.Series(items)
        category_set[cat_index][df_index]['Item Price'] = pd.Series(prices)
except: IndexError
pass


# In[ ]:


##-Appending all dataframes to a single dataset-##
cat_index = 0
combined_data = pd.concat(category_set[cat_index])    

##-Dropping duplicates, adding a currency column, defining float type, rounding output to the second decimal point-##
combined_data = combined_data.drop_duplicates()
combined_data['Currency'] = 'BGN'
combined_data['Item Price'] = combined_data['Item Price'].astype(float)
combined_data['Item Price'] = combined_data['Item Price'].round(2)
combined_data

# In[ ]:


##-A function for Excel's column width-##
def format_col_width(ws):
    ws.set_column('A:A', 75)
    ws.set_column('B:B', 25)
    ws.set_column('C:C', 25)

##-Exporting the results to an .XLSX file-##
writer = pd.ExcelWriter(formated_date +  '_OLX_BG_' + category_set[user_category] + '_Category' + '.xlsx', engine='xlsxwriter') 
combined_data.to_excel(writer, sheet_name=category_set[user_category], index=False)
workbook  = writer.book
worksheet = writer.sheets[category_set[user_category]]
format_col_width(worksheet)
writer.save()
