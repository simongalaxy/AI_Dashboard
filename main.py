import os
import pandas as pd

from src.DataProcessor import load_data_from_xml, preprocess_data, show_data_info
from src.DataAnalyzer import DataAnalyzer
from src.Settings import settings



def main():
    # load settings.
    print("Loading settings...")
    print(f"Model Name: {settings.model_name}")
    print(f"Model Provider: {settings.model_provider}")
    print(f"API Base: {settings.api_base}")

    # load data from the XML file.
    url = "https://www.cepu.gov.hk/en/filestore/ppr-granted.xml"
    
    df_raw = load_data_from_xml(url=url)
    df = preprocess_data(df_raw)
    show_data_info(df)

    # initialize the DataAnalyzer.
    analyzer = DataAnalyzer()
    
    # summarize the data.
    summary = analyzer.summarize_df(df)
    print("Summary:")
    for i, item in enumerate(summary, start=1):
        print(f"{i}. {item}")
    
    
if __name__ == "__main__":
    main()
