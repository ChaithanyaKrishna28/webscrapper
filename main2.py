'''
Items to scrape
• Product URL
• Product Name
• Product Price
• Rating
• Number of reviews
'''



from bs4 import BeautifulSoup
import requests
import csv

import time

def get_soup(url):
    headers = {"User-Agent":"Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebit/537.36 (KTHML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    while True:
        try:
            response = requests.get(url,headers=headers)
            response.raise_for_status()  # raise an error if the request was not successful
            break  # break out of the while loop if the request was successful
        except requests.exceptions.HTTPError as e:
            print(f"Received {e.response.status_code} error for {url}")
            if e.response.status_code == 503:
                print("Retrying after 5 seconds...")
                time.sleep(5)
            else:
                raise  # re-raise the exception if it is not a 503 error
    soup = BeautifulSoup(response.content,"html.parser")
    return soup


def scrape_page(page_num):
    url = f"https://www.amazon.in/s?k=bags&page={page_num}&crid=2M096C61O4MLT&qid=1679410486&sprefix=ba%2Caps%2C358&ref=sr_pg_{page_num}"
    print(f"Scraping page {page_num}: {url}")
    soup = get_soup(url)

    data = []
    print(url)
    #product name
    name = soup.find_all('span',{"class":"a-size-medium a-color-base a-text-normal"}) 
    bag_names = []   
    for i in name:
        #print(i.text.strip())
        bag_names.append(i.text.strip()) 

    #product urls
    link = soup.find_all("a",{"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
    all_links = []
    for j in link:
        link1 = "https://amazon.in"+j['href']
        all_links.append(link1)

    #product price
    prices = soup.find_all('span',{'class':'a-price-whole'})
    prices_list = []
    for p in prices:
        cost =p.text.strip()
        prices_list.append(cost)

    #product rating
    rate = soup.find_all('span',{'class':'a-icon-alt'})
    ratings_list= []
    for r in rate:
        ratings_list.append(r.text.strip())

    #product review count
    rev = soup.find_all('span',{"class":"a-size-base s-underline-text"})
    review_count = []           
    for item in rev:
        review_count.append(item.text[1:-1])


    for i in range(min(len(all_links), len(bag_names))):
        new_dict = { 
            'PRODUCT NAME':bag_names[i],
            'PRODUCT URLS':all_links[i] if i < len(all_links) else "",
            'PRODUCT PRICE':prices_list[i] if i < len(prices_list) else "",
            'PRODUCT RATING':ratings_list[i] if i < len(ratings_list) else "",
            'REVIEW COUNT':review_count[i][1:-1] if i < len(review_count) else ""
        }
        data.append(new_dict)
    print(len(data))
    print(f"Scraped {len(data)} items on page {page_num}")
    return data
def scrape_pages(start_page, end_page):
    master_data = []
    for page_num in range(start_page, end_page + 1):
        data = scrape_page(page_num)
        master_data += data
    return master_data



data=scrape_pages(1, 20)


# Scrape the data and store it in a list
# Define the headers for the CSV file
headers = ["PRODUCT NAME", "PRODUCT URLS", "PRODUCT PRICE", "PRODUCT RATING", "REVIEW COUNT"]

# Write the data to a CSV file
with open("amazon_bags3.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
