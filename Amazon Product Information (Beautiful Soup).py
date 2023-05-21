import os

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv

s = HTMLSession()
first_page_utl = 'https://www.amazon.co.uk/s?k=dslr+camera&i=black-friday'


def parse_html(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup


def get_last_page(soup):

    last_page_num = soup.find('span', class_='s-pagination-item s-pagination-disabled')
    last_page_num = int(last_page_num.text)
    return last_page_num


def get_data(soup):
    data = []
    product_boxes = soup.find_all('div', class_='a-section a-spacing-small a-spacing-top-small')
    for product_box in product_boxes:
        product_name = product_box.find('span', class_='a-size-medium a-color-base a-text-normal')

        rating_box = product_box.find('div', class_='a-section a-spacing-none a-spacing-top-micro')
        if product_name is not None and rating_box is not None:
            product_name = product_name.text
            rating = rating_box.find('span', class_='a-icon-alt')
            if rating is not None:
                rating = rating.text
            else:
                rating = "No rating available"
            data.append((product_name, rating))
    return data


if 'c' not in globals():
    c = 0
# cnt: int = 0


def write_data(data):
    global c
    csv_file = 'product_data.csv'

    if c == 0:
        if os.path.isfile(csv_file):
            # Delete the existing CSV file
            os.remove(csv_file)
            c += 1

    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Check if the file is empty (no header row)
        is_file_empty = file.tell() == 0
        if is_file_empty:
            writer.writerow(['Product Name', 'Rating'])
        writer.writerows(data)

    print("Data has been written to", csv_file)


# PARSE HTML FOR FIRST PAGE
first_page_soup = parse_html(first_page_utl)
first_page_data = get_data(first_page_soup)
write_data(first_page_data)

# Capture the last page number
last_page = get_last_page(first_page_soup)
print(last_page)

# Iterating from page Two to Last page
# for i in range(2, last_page + 1):
for i in range(2, last_page + 1):
    pagination = 'https://www.amazon.co.uk/s?k=dslr+camera&i=black-friday&bbn=161428031&page=' + str(
        i) + '&qid=1684401387&ref=sr_pg_' + str(i)

    next_page_soup = parse_html(pagination)
    pagination_data = get_data(next_page_soup)
    write_data(pagination_data)
