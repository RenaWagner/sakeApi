import requests
from bs4 import BeautifulSoup

def get_sake_type(sake_clean_list):
    for i in range(len(sake_clean_list)):
        type_boolean = sake_clean_list[i].startswith('TYPE')
        if type_boolean == True:
            sake_type = sake_clean_list[i + 1][2:]
    return sake_type

def get_sake_alcohol(sake_clean_list):
    sake_alcohol = ''
    for i in range(len(sake_clean_list)):
        alcohol_boolean = sake_clean_list[i].startswith('ALC')
        if alcohol_boolean == True:
            sake_alcohol = sake_clean_list[i+1]
    return sake_alcohol

def get_sake_rice(sake_clean_list):
    sake_rice = ''
    for i in range(len(sake_clean_list)):
        if sake_clean_list[i] == 'RICE':
            sake_rice = sake_clean_list[i+1][2:]
    return sake_rice

def get_sake_rice_milling(sake_clean_list):
    sake_rice_milling = ''
    for i in range(len(sake_clean_list)):
        rice_milling_boolean = sake_clean_list[i].startswith('RICE MILLING')
        if rice_milling_boolean == True:
            sake_rice_milling = sake_clean_list[i+1][2:]   
    return sake_rice_milling

def get_sake_details(product_info):
    sake_title=product_info.find(class_="product-title").contents[0]
    sake_description=product_info.find(class_="product-short-description").find('p')
    sake_clean_list= list(sake_description.stripped_strings)
    sake_details = {"title": sake_title,
                "type": get_sake_type(sake_clean_list),
                "rice":get_sake_rice(sake_clean_list),
                "polish_percentage": get_sake_rice_milling(sake_clean_list),
                "alcohol": get_sake_alcohol(sake_clean_list),
               }
    return sake_details

def get_clean_list_from_url(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser').body
    product_info = soup.find('div',attrs = {'class','product-info'})
    return product_info

def get_sake_details_from_url(url):
    product_info = get_clean_list_from_url(url)
    if product_info is not None:
        details = get_sake_details(product_info)
    print("fetched product HTML")
    return details

def get_url(single_box):
    single_url = single_box.a['href']
    return single_url

def axis_plan_fetch_data():
    global_url = "https://sake.axisplan.com/sake-list/"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    global_req = requests.get(global_url, headers=headers)
    global_soup = BeautifulSoup(global_req.text, 'html.parser').body
    all_single_boxes = global_soup.find_all("div", {"class": "product-small box"})
    all_urls = [get_url(single_box) for single_box in all_single_boxes]
    print(all_urls)

    all_products_info = [get_sake_details_from_url(link) for link in all_urls]
    return all_products_info


