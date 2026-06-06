import pandas as pd
from lida import Manager, TextGenerationConfig, llm
from pprint import pprint

from src.Settings import settings


class DataAnalyzer:
    def __init__(self):
        self.lida_llm = llm(provider=settings.model_provider)
        self.lida = Manager(text_gen=self.lida_llm)
        self.textgen_config = TextGenerationConfig(
            n=1,
            model=settings.model_name,
            temperature=0.0,
            use_cache=True,
            max_tokens=2048
        )
        
    def summarize_df(self, df: pd.DataFrame) -> dict:
        summary = self.lida.summarize(df, textgen_config=self.textgen_config)
        
        return summary
    
    
    def generate_goals(self, summary: str, n: int = 7) -> list:
        goals = self.lida.goals(summary, n=n, textgen_config=self.textgen_config)
        
        # show goals.
        for i, goal in enumerate(goals, start=1):
            print(f"Goal No. {i}:")
            pprint(goal)
            print("#" * 50)
        
        return goals
    
    
    def visualize_goal(self, summary: str, goal: str) -> list:
        charts = self.lida.visualize(
            summary=summary, 
            goal=goal, 
            library="plotly",
            textgen_config=self.textgen_configsc
        )
        
        if charts:
            print("Charts:")
            for chart in charts:
                print(chart)
        else:
            print("No charts generated.")
        
        return charts