import core_initial
import query_validate
import anchorbank
import logging
import os
import pandas as pd
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
logging.FileHandler("gtab_log.log"),
])

if __name__ == "__main__":
    my_path = "june_current_us"
    logging.info("loading core...takes a moment")
    t = core_initial.GTAB(dir_path=my_path)
    date = datetime.date(2024, 7, 14)
    week_ago = date - datetime.timedelta(days=7)
    date_md = date.strftime('%m-%d')


    if not os.path.exists(f"{date}_gtab"):
        os.mkdir(f"{date}_gtab")
    logging.info(f'gtab range from {week_ago} to {date}')

    anchorbank.main(week_ago, date)
    t.set_active_gtab(f"google_anchorbank_geo=US_timeframe={week_ago} {date}.tsv")

    for root, dir, files in os.walk('queries'):
        logging.info("getting queries to search...")
        df = pd.DataFrame()
        for file in files:
            if f'@{date_md}' in file:
                filepath = os.path.join(root,file)
                temp_df = pd.read_csv(filepath)
                df = pd.concat([df, temp_df])
    df.to_csv(f'{date}_gtab/{date}_aggregatedDf.csv')
    
    queryList = df['summarized-query'].to_list()
    logging.info(f"length of query List: {len(queryList)}")
    query_validate.main(t, queryList, date, 1)