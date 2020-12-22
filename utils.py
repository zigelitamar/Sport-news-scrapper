import os
import scrapy
import json
import subprocess

def scrape_to_file(scrapper_filename, start_urls, out_json_filename):
    if os.path.exists(f"./{out_json_filename}"):
        os.remove(f"./{out_json_filename}")
    subprocess.run(['scrapy', 'crawl', scrapper_filename, "-a", f"start_urls={start_urls}", '-o', out_json_filename])

def fix_date(date):
    splitted_date = date.split(' ')
    time = splitted_date[1]
    year_month_date = splitted_date[0].split('-')
    year = year_month_date[0]
    month = year_month_date[1]
    day = year_month_date[2]

    return f"{day}/{month}/{year} {time}"