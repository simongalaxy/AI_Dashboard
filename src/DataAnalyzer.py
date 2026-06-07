import os
import pandas as pd
from lida import Manager, TextGenerationConfig, llm
from pprint import pprint

from src.Settings import settings

# load env settings. 
os.environ["OPENAI_BASE_URL"] = settings.openai_api_base
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

class DataAnalyzer:
    def __init__(self):
        self.text_gen = llm(
            provider=settings.model_provider,
            model=settings.model_name
        )
        self.lida = Manager(text_gen=self.text_gen)
        self.textgen_config = TextGenerationConfig(
            n=1,
            temperature=0.0,
            use_cache=True,
            max_tokens=4096
        )   
        
    def summarize_df(self, df: pd.DataFrame) -> dict:
        summary = self.lida.summarize(df)
        
        print(f"Data Type of Summary: {type(summary)}")
        print("Summary of the DataFrame:")
        pprint(summary)
        print("#" * 50)
        print("\n")
        
        return summary
    
    
    def generate_goals(self, summary: dict, n: int, persona: str) -> list:
        goals = self.lida.goals(
            summary, 
            n=n, 
            textgen_config=self.textgen_config,
            persona=persona
        )
        
        print(f"Data Type of Goals: {type(goals)}")
        
        # show goals.
        print("Generated Goals:")
        for i, goal in enumerate(goals, start=1):
            print(f"Goal No. {i}:")
            print(goal)
            print("#" * 50)
        
        return goals
    
    
    def explain_goal(self, chart) -> str:
        
        explanations = self.lida.explain(
            textgen_config=self.textgen_config,
            code = chart.code
        )

        print("Explanations:")
        for i, explanation in enumerate(explanations, start=1):
            print(f"Explanation No. {i}:")
            pprint(explanation)
            print("#" * 50)
        
        return explanations
    
    
    def visualize_goal(self, summary: dict, goals: list) -> list:
        
        all_charts = []
        
        for i, goal in enumerate(goals, start=1):
            print(f"Visualizing Goal No. {i}...")
            try:
                charts = self.lida.visualize(
                    summary=summary, 
                    goal=goal, 
                    library="plotly",
                    textgen_config=self.textgen_config
                )
                if charts:
                    print(f"Charts for Goal No. {i}:")
                    for chart in charts:
                        print(chart)
                        explanations = self.explain_goal(chart)
                        all_charts.append(chart)
                else:
                    print(f"No charts generated for Goal No. {i}.")
            except Exception as e:
                print(f"Error visualizing Goal No. {i}: {e}")
        
        return all_charts
    
    
 
