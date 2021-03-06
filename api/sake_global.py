import requests
from bs4 import BeautifulSoup

def get_all_products_details_single_page_from_url(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    all_products_info = soup.find_all('div',attrs = {'class','sake-list__meta-box__right'})
    products_details_single_page = []
    for i in range(len(all_products_info)):
        sake_details = {"title": all_products_info[i].find(class_="sake-list__meta__title").contents[0],
                    "type": all_products_info[i].find(class_="sake-list__meta__sake-type").contents[1].contents[0],
                    "rice": all_products_info[i].find(class_="sake-list__meta__rice").contents[1].contents[0],
                    "polish_percentage": all_products_info[i].find(class_="sake-list__meta__percent").contents[1].contents[0],
                    "alcohol": all_products_info[i].find(class_="sake-list__meta__alcohol-level").contents[1].contents[0]
                   }
        products_details_single_page.append(sake_details)
    return products_details_single_page

def sake_global_fetch_data():
    print("Sake global started to fetch")
    all_urls = []
    for i in range(1,8):
        url = "https://sake-global.com/products/page/{}/?lang=en".format(i)
        all_urls.append(url)
    print("Length of urls is {}.".format(len(all_urls)))
    all_products_info=[]
    product_counter = 0
    for url in all_urls:
        all_products_info.append(get_all_products_details_single_page_from_url(url))
        product_counter += 1
        percentage =round((product_counter / len(all_urls)) * 100, 1)
        print('Processed {}% of contents'.format(percentage))
    all_products_info_result = [product for single_page_products in all_products_info for product in single_page_products]
    return all_products_info_result
