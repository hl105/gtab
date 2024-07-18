import logging
import os
import pandas as pd
import time
import csv
import random
import core_initial
import datetime

def main(t, queryList, date, retry):
    """Gets calibrated google trends information per query using the 
    appropriate anchorbank that was set active above."""
    count=0
    if not retry:
        with open(f'{date}_gtab/{date}-gtabData-test.csv','w') as f:
            writer = csv.DictWriter(f,["query"])
        with open(f'{date}_gtab/{date}-validQueries.csv', 'w') as f:
            w = csv.writer(f, delimiter='\n')
            w.writerow(["query"])
        with open(f'{date}_gtab/{date}-badQueries.csv','w') as f:
            writer = csv.DictWriter(f, ["query"])
            writer.writeheader()
        with open('processed.csv','w') as f:
            writer = csv.DictWriter(f,["query"])
            writer.writeheader()
    while True:
        processed = []
        if os.path.isfile('processed.csv'):
            with open('processed.csv','r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    processed.append(row['query'])
        if set(queryList) == set(processed):
            break
        for i, query in enumerate(queryList):
            if query not in processed:
                try:
                    logging.info(f"processing {i}th query: {query}")
                    q = t.new_query(query)
                    with open('processed.csv','a') as f:
                            writer = csv.DictWriter(f,["query"])
                            writer.writerow({'query':query})
                    try:
                        count=0
                        q['query'] = q['max_ratio'].apply(lambda x: query)
                        csvInfo = q.to_csv()
                        csvLines = csvInfo.split('\n')
                        with open(f'{date}_gtab/{date}-gtabData-test.csv', 'a') as f: #append info to csv file (not sure if this is the best way to do this but it works)
                            w = csv.writer(f, delimiter='\n')
                            for line in csvLines[1:]:
                                if line != "": #sometimes there were empty lines, so exclude those 
                                    w.writerow([line])
                        with open(f'{date}_gtab/{date}-validQueries.csv', 'a') as f:
                            w = csv.writer(f, delimiter='\n')
                            w.writerow([query])
                        time.sleep(random.randint(5,15))
                    except Exception as e:
                        logging.info(e)
                        with open(f'{date}_gtab/{date}-badQueries.csv','a') as f:
                            writer = csv.DictWriter(f, ["query"])
                            writer.writerow({'query': query})
                except Exception as e: #'bad query' exception (not enough google trends data)
                    logging.info(f"Outer exception: {e}")
                    time.sleep(random.randint(10,20))
                    break
