import requests
import json
import pandas as pd

base_url = 'https://www.rebeccaminkoff.com/en-ma/products.json?limit=250&page='

product_list = []

for page in range(1, 11):  # Change the range as needed
    url = base_url + str(page)
    r = requests.get(url)
    data = r.json()

    for item in data['products']:
        product_id = item['id']
        title = item['title']
        published_at = item['published_at']
        created_at = item['created_at']
        updated_at = item['updated_at']
        vendor = item['vendor']
        product_type = item['product_type']
        tags = item['tags']
        
        for variant in item['variants']:
            variant_id = variant['id']
            sku = variant['sku']
            requires_shipping = variant['requires_shipping']
            taxable = variant['taxable']
            featured_image = variant['featured_image']
            available = variant['available']
            price = variant['price']
            grams = variant['grams']
            compare_at_price = variant['compare_at_price']
            position = variant['position']
            product_id_variant = variant['product_id']
            
            for image in item['images']:
                try:
                    imagesrc = image['src']
                except:
                    imagesrc = 'None'
            
            product = {
                'id': product_id,
                'title': title,
                'published_at': published_at,
                'created_at': created_at,
                'updated_at': updated_at,
                'vendor': vendor,
                'product_type': product_type,
                'tags': tags,
                'variants': variant_id,
                'sku': sku,
                'requires_shipping': requires_shipping,
                'taxable': taxable,
                'featured_image': featured_image,
                'available': available,
                'price': price,
                'grams': grams,
                'compare_at_price': compare_at_price,
                'position': position,
                'product_id': product_id_variant,
                'image': imagesrc
            }
    
            product_list.append(product)

df = pd.DataFrame(product_list)
df.to_csv('helm_data5.csv', index=False)  # Save the data to a CSV file
