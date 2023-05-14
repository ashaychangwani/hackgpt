from langchain.chains import LLMSummarizationCheckerChain
from langchain.chat_models import ChatOpenAI
import os
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents import load_tools
import io
import contextlib

class FactChecker:
    def __init__(self):
        x=3
        llm = ChatOpenAI(temperature=0.7, model_name = 'gpt-3.5-turbo', openai_api_key=os.getenv("OPENAI_API_KEY"))
        tools = load_tools(["serpapi", "llm-math"], llm=llm, serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
        self.agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        self.prompt_factcheck = """
            You are a professional article fact checker. 
            Can you fact check this article: "{text}"
            Perform the fact check by listing down the "factual" statements that the article author claim to be true into bullet points, and present this points.
            Then for each point, find out whether they are true by cross checking with other websites.
            Finally, present the end result by giving a verdict for each point whether they are true or not, and also present the website used for the cross check.
        """
    
    def check(self, text):
        captured_output = io.StringIO()
        print(self.prompt_factcheck.format(text=text))
        article_final = self.agent.run(self.prompt_factcheck.format(text=text))
        print(article_final)
        return article_final