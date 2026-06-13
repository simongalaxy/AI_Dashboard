import os
import pandas as pd
from lida import Manager, TextGenerationConfig, llm
from pprint import pformat

from src.Settings import settings
from src.logger import Logger

# load env settings. 
os.environ["OPENAI_BASE_URL"] = settings.openai_api_base
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

class DataAnalyzer:
    def __init__(self, logger: Logger):
        self.logger = logger
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
        
        self.logger.info(f"Data Type of Summary: {type(summary)}")
        self.logger.info("Summary of the DataFrame: \n%s", pformat(summary))
        self.logger.info("#" * 50)
        self.logger.info("\n")
        
        return summary
    
    
    def generate_goals(self, summary: dict, n: int, persona: str) -> list:
        goals = self.lida.goals(
            summary, 
            n=n, 
            textgen_config=self.textgen_config,
            persona=persona
        )
        
        self.logger.info(f"Data Type of Goals: {type(goals)}")
        
        # show goals.
        self.logger.info("Generated Goals:")
        for i, goal in enumerate(goals, start=1):
            self.logger.info(f"Goal No. {i}:")
            self.logger.info(goal)
            self.logger.info("#" * 50)
        
        return goals
    
    
    def explain_goal(self, chart) -> str:
        
        explanations = self.lida.explain(
            textgen_config=self.textgen_config,
            code = chart.code
        )

        self.logger.info("Explanations:")
        for i, explanation in enumerate(explanations, start=1):
            self.logger.info(f"Explanation No. {i}: \n%s", pformat(explanation))
            self.logger.info("#" * 50)
        
        return explanations
    
    
    def visualize_goal(self, summary: dict, goals: list) -> list:
        
        all_charts = []
        
        for i, goal in enumerate(goals, start=1):
            self.logger.info(f"Visualizing Goal No. {i}...")
            try:
                charts = self.lida.visualize(
                    summary=summary, 
                    goal=goal, 
                    library="plotly",
                    textgen_config=self.textgen_config
                )
                if charts:
                    self.logger.info(f"Charts for Goal No. {i}:")
                    for chart in charts:
                        # print(chart)
                        explanations = self.explain_goal(chart)
                        all_charts.append(chart)
                else:
                    self.logger.info(f"No charts generated for Goal No. {i}.")
            except Exception as e:
                self.logger.info(f"Error visualizing Goal No. {i}: {e}")
        
        return all_charts
    
    
 
