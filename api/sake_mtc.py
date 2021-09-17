import requests
from bs4 import BeautifulSoup

def get_sake_product_info_from_url(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser').body
    product_info = soup.find(id="productDetails")
    return product_info

def get_sake_type(product_details):
    sake_type = ''
    for i in range(len(product_details.contents)):
        sake_content = product_details.contents[i].get_text()
        sake_type_boolean = sake_content.startswith('Class:')
        if sake_type_boolean == True:
            sake_type_raw = product_details.contents[i]
            sake_type = sake_type_raw.get_text()[7:]
    return sake_type


def get_sake_rice(product_details):
    sake_rice = ''
    for i in range(len(product_details.contents)):
        sake_content = product_details.contents[i].get_text()
        sake_rice_boolean = sake_content.startswith('Rice:')
        if sake_rice_boolean == True:
            sake_rice_raw = product_details.contents[i] 
            sake_rice = sake_rice_raw.get_text()[6:]
    return sake_rice

def get_sake_rice_milling(product_details):
    sake_rice_milling = ''
    for i in range(len(product_details.contents)):
        sake_content = product_details.contents[i].get_text()
        sake_rice_milling_boolean = sake_content.startswith('Rice-Polishing Ratio:')
        if sake_rice_milling_boolean == True:
            sake_rice_milling_raw = product_details.contents[i] 
            sake_rice_milling = sake_rice_milling_raw.get_text()[22:]
    return sake_rice_milling


def get_sake_details(product_info):
    product_title = product_info.find(class_="product-title").text
    product_details = product_info.find(class_="product-excerpt")
    sake_type = get_sake_type(product_details)
    sake_rice = get_sake_rice(product_details)
    sake_rice_milling = get_sake_rice_milling(product_details)
    sake_details = {"title": product_title,
                    "type": sake_type,
                    "rice": sake_rice,
                    "polish_percentage": sake_rice_milling,
                    "alcohol": "",
                   }
    return sake_details

def sake_mtc_fetch_data():
    global_page_url = "https://www.mtcsake.com/sake"
    global_req = requests.get(global_page_url)
    global_soup = BeautifulSoup(global_req.text, 'html.parser').body
    main_content = global_soup.find("div", {"id": "productList"})
    all_links = []
    base_url = "https://www.mtcsake.com"
    for a in main_content.find_all("a", href=True):
        if a.text:
            specific_url=a['href']
            each_url= f'https://www.mtcsake.com{specific_url}'
            all_links.append(each_url)
    print("print all URLs fetched")
    all_products_info = [get_sake_product_info_from_url(link) for link in all_links]
    all_products_details = []
    for product_info in all_products_info:
        if product_info is not None:
            sake_detail = get_sake_details(product_info)
            all_products_details.append(sake_detail)
    print(all_products_details)
    return all_products_details

