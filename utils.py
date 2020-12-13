import os
import scrapy
import json
import subprocess

def scrape_to_file(scrapper_filename, start_urls, out_json_filename):
    if os.path.exists(f"./{out_json_filename}"):
        os.remove(f"./{out_json_filename}")
    subprocess.run(['scrapy', 'crawl', scrapper_filename, "-a", f"start_urls={start_urls}", '-o', out_json_filename])