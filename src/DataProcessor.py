import pandas as pd


def load_data_from_xml(url: str) -> pd.DataFrame:
    df = pd.read_xml(url, parser="lxml")
    
    return df


# load and pre-process the data, and save it to a CSV file.
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.copy()
    # pre-process the data here if needed.
    report_period_cols = ["Financial_year", "Round"]
    project_no_cols = ["Year", "Institution_code", "Item_no", "Batch_no"]
    
    df[report_period_cols] = df["report-period"].str.split("(", expand=True, n=1)
    df[project_no_cols] = df["project-no"].str.split(".", expand=True, n=len(project_no_cols)-1)
    
    df["Round"] = df["Round"].str.replace(")", "")
    df["Financial_year"] = df["Financial_year"].str.strip()
    df.drop(columns=["report-period", "project-no"], inplace=True)

    # save the dataframe to a CSV file.
    df.to_csv("./data/ppr-granted.csv", index=False)
    
    
    return df


def show_data_info(df: pd.DataFrame) -> None:
    print("Data Info:")
    print(df.info())
    print("\nData Sample:")
    print(df.head(5))
    print("#" * 50)
    print("\n")
    
    return
