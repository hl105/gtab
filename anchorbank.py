import core_initial
import logging


# set up logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
logging.FileHandler("gtab_log.log"),
])



my_path = "summer"
t = core_initial.GTAB(dir_path=my_path)

def main(week_ago, date):
    #now = datetime.now().strftime('%Y-%m-%d')
    t.set_options(pytrends_config={"geo": "US", "timeframe": f"{week_ago} {date}"}) 
    while True:
        try:
            if t.create_anchorbank() == None: 
                break #returns when we're done with all queries
        except Exception as e:
            logging.error(f"Outer Error: {e}")
            