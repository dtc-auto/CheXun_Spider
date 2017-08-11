# -*- coding: utf-8 -*-
import csv

def start_urls():
    with open(r'D:\office\office\venv_CheXun\CheXun_Spider\CheXun_Spider\spiders\CheXun_serie.csv', 'r') as f:
        csv_file = csv.DictReader(f)
        #return csv_file
        url = []
        for row in csv_file:
            url.append(row['serie_url'])
        return url
