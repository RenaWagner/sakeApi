from sake_global import get_all_products_details_from_all_urls

def fetch_data():
    result_sake_global = get_all_products_details_from_all_urls()
    for i in range(1,6):
        print(result_sake_global[i])