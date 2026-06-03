import os
import pandas as pd
from lida import Manager, TextGenerationConfig, llm

from pprint import pprint


# load and pre-process the data, and save it to a CSV file.
def load_and_preprocess_data(url: str) -> pd.DataFrame:
    df = pd.read_xml(url, parser="lxml")
    
    # pre-process the data here if needed.
    report_period_cols = ["Financial_year", "Round"]
    project_no_cols = ["Year", "Institution_code", "Item_no", "Batch_no"]
    
    df[report_period_cols] = df["report-period"].str.split("(", expand=True, n=1)
    df[project_no_cols] = df["project-no"].str.split(".", expand=True, n=len(project_no_cols)-1)
    
    df["Round"] = df["Round"].str.replace(")", "")
    df["Financial_year"] = df["Financial_year"].str.strip()
    df.drop(columns=["report-period", "project-no"], inplace=True)
    
    
    print(df.head(6))
    print(df.info())
    
    # save the dataframe to a CSV file.
    df.to_csv("./data/ppr-granted.csv", index=False)
    
    return df


def main():
    # load data from the XML file.
    url = "https://www.cepu.gov.hk/en/filestore/ppr-granted.xml"
    
    df = load_and_preprocess_data(url)
    
    # create a manager and a text generation config.
    OLLAMA_MODEL_NAME = "phi4-mini:3.8b"
    OLLAMA_API_BASE ="http://localhost:11434/v1"
    
    os.environ["OPENAI_BASE_URL"] = OLLAMA_API_BASE
    os.environ["OPENAI_API_KEY"] = "ollama"
    
    lida_llm = llm(provider="openai")
    
    lida=Manager(text_gen=lida_llm)
    
    textgen_config = TextGenerationConfig(
        n=1,
        model=OLLAMA_MODEL_NAME,
        temperature=0.0,
        use_cache=True
    )
    
    # generate insight.
    summary = lida.summarize(df, textgen_config=textgen_config)
    print("Summary:")
    pprint(summary)
    
    # generate goals.
    goals = lida.goals(summary, n=7, textgen_config=textgen_config)
    print("Goals:")
    for i, goal in enumerate(goals, start=1):
        print(f"Goal No. {i}:")
        pprint(goal)
        
        # try:
        #     action_plan = lida.action_plan(goal, textgen_config=textgen_config)
        #     print("Action Plan:")
        #     print(action_plan)
        # except Exception as e:
        #     print(f"Error generating action plan for Goal No. {i}: {e}")
        # print("-" * 50)
        
        charts = lida.visualize(
            summary=summary, 
            goal=goal, 
            library="plotly",
            textgen_config=textgen_config
        )
        
        if charts:
            print("Charts:")
            for chart in charts:
                print(chart)
        else:
            print("No charts generated.")
        print("=" * 50) 
        
        
    
    # # generate visualization.
    # viz = lida.visualize(df, textgen_config=textgen_config)
    # print("Visualization:")
    # print(viz)

    
    
if __name__ == "__main__":
    main()
