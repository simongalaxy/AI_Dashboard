import os
import pandas as pd
from lida import Manager, TextGenerationConfig, llm
from pprint import pprint

from src.Settings import settings

# load env settings.
    
os.environ["API_BASE"] = settings.api_base
os.environ["API_KEY"] = settings.api_key

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
            max_tokens=2048
        )
        # setting for using hugging face.
        # os.environ["HF_TOKEN"] = settings.huggingface_token
        
        # self.lida_llm = llm(
        #     provider=settings.model_provider, 
        #     token=settings.huggingface_token, 
        #     device_map="cpu",
        #     low_cpu_mem_usage=True,
        #     torch_dtype="bfloat16"
        # )
        # self.lida = Manager(text_gen=self.lida_llm)
        
            
        
    def summarize_df(self, df: pd.DataFrame) -> dict:
        summary = self.lida.summarize(df)
        
        for i, item in enumerate(summary, start=1):
            print(f"Summary No. {i}:")
            pprint(item)
            print("#" * 50)
        
        return summary
    
    
    def generate_goals(self, summary: str, n: int) -> list:
        goals = self.lida.goals(summary, n=n, textgen_config=self.textgen_config)
        
        # show goals.
        for i, goal in enumerate(goals, start=1):
            print(f"Goal No. {i}:")
            pprint(goal)
            print("#" * 50)
        
        return goals
    
    
    def explain_goal(self, chart) -> str:
        explanations = self.lida.explain(
            textgen_config=self.textgen_config,
            code = chart.code
        )

        for i, explanation in enumerate(explanations, start=1):
            print(f"Explanation No. {i}:")
            pprint(explanation)
            print("#" * 50)
        
        return explanations
    
    
    def visualize_goal(self, summary: str, goals: list) -> list:
        for i, goal in enumerate(goals, start=1):
            print(f"Visualizing Goal No. {i}...")
        
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
            else:
                print(f"No charts generated for Goal No. {i}.")
        
        return charts
    
    
 
