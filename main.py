import os, json
import pandas as pd
from pprint import pprint

from src.DataProcessor import load_data_from_xml, preprocess_data, show_data_info
from src.DataAnalyzer import DataAnalyzer
from src.Settings import settings
from src.logger import Logger


def main():
    
    # load settings.
    print("Loading settings...")
    pprint(settings.model_dump())

    # initiate logger.
    logger = Logger(__name__).get_logger()

    # load data from the XML file.
    url = "https://www.cepu.gov.hk/en/filestore/ppr-granted.xml"
    
    df_raw = load_data_from_xml(url=url)
    df = preprocess_data(df_raw)
    show_data_info(df)

    # goals settings:
    total_goals = 10
    persona = "An Operationn Manager who monitors overall situation of a funding scheme"
    
    # initialize the DataAnalyzer.
    analyzer = DataAnalyzer(logger=logger)
    
    # summarize the data.
    summary = analyzer.summarize_df(df)
    
    # generate goals based on the summary.
    goals = analyzer.generate_goals(summary=summary, n=total_goals, persona=persona)
    
    # visualize the first goal.
    charts = analyzer.visualize_goal(summary=summary, goals=goals)


# program entry point.
if __name__ == "__main__":
    main()
