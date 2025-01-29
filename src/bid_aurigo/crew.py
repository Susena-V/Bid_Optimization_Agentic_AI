from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
from bid_aurigo.tools.search import SearchTools
import os
from bid_aurigo.tools.custom_tool import HumanTool
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
from dotenv import load_dotenv
load_dotenv()
gkey=os.getenv('GEMINI_API_KEY')
skey=os.getenv('SERPER_API_KEY')
fireapi="fc-b713432bb02d476e9a70032e5a2a70ab"
#llm = LLM(model="gemini/gemini-1.5-pro-latest",api_key=gkey)
composio_toolset = ComposioToolSet(api_key="ympg95k8oaqmcwuulue69g")
toolsearch= composio_toolset.get_tools(actions=['YOUSEARCH_YOU_SEARCH'])

from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
    PDFSearchTool,
    FirecrawlSearchTool)

# tool = WebsiteSearchTool(
#     config=dict(
#         llm=dict(
#             provider="groq", 
#             config=dict(
#                 model="llama-3.3-70b-versatile",
#                 api_key='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' 
#             ),
#         ),
#         embedder=dict(
#             provider="google", 
#             config=dict(
#                 model="models/embedding-001",
#                 task_type="retrieval_document",
#             ),
#         ),
#     ) 
# )

pdf_tool= PDFSearchTool(pdf="Proper/bid-aurigo/bid_aurigo/quarterly-lnt.pdf",
    config=dict(
        llm=dict(
            provider="groq", 
            config=dict(
                model="llama-3.3-70b-versatile",
                api_key='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' 
            ),
        ),
        embedder=dict(
            provider="google", 
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
            ),
        ),
    ) 
)


pdf_tool2= PDFSearchTool(pdf="Proper/bid-aurigo/bid_aurigo/quarterly-lnt.pdf",
    config=dict(
        llm=dict(
            provider="groq", 
            config=dict(
                model="llama-3.3-70b-versatile",
                api_key='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' 
            ),
        ),
        embedder=dict(
            provider="google", 
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
            ),
        ),
    ) 
)

composio_toolset = ComposioToolSet(api_key="ympg95k8oaqmcwuulue69g")
#news_tools = composio_toolset.get_tools(actions=['HACKERNEWS_SEARCH_POSTS'])

@CrewBase
class BidAurigo():
    """Bid Optimization Crew for Construction Projects"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def integrated_project_analysis_agent(self) -> Agent:
        return Agent(
            llm = LLM(model="ollama/qwen2.5-coder:7b",base_url="http://localhost:11434"),
            config=self.agents_config['integrated_project_analysis_agent'],
            tools=[HumanTool(),SearchTools.search_internet],
            verbose=True )
    
    @agent
    def cost_estimation_agent(self) -> Agent:
        return Agent(
            llm = LLM(model="ollama/qwen2.5-coder:7b",base_url="http://localhost:11434"),
            config=self.agents_config['cost_estimation_agent'],
            tools=[pdf_tool,SearchTools.search_internet],
			verbose=True
   	)

    @agent
    def bid_optimization_agent(self) -> Agent:
        return Agent(
            llm = LLM(model="ollama/qwen2.5-coder:7b",base_url="http://localhost:11434"),
            config=self.agents_config['bid_optimization_agent'],
            tools=[SearchTools.search_internet], 
            verbose=True
        )

    @agent
    def dashboard_agent(self) -> Agent:
        return Agent(
            llm = LLM(model="ollama/qwen2.5-coder:7b",base_url="http://localhost:11434"),
            config=self.agents_config['dashboard_agent'],
            tools=[SearchTools.search_internet], 
            verbose=True
        )

    @task
    def integrated_project_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['integrated_project_analysis_task']
        )

    @task
    def cost_estimation_task(self) -> Task:
        return Task(
            config=self.tasks_config['cost_estimation_task'],
            depends_on=[self.integrated_project_analysis_task],
            output_file='cost_estimation_report.md'
        )

    @task
    def bid_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['bid_optimization_task'],
            depends_on=[ self.cost_estimation_task,pdf_tool2]
        )

    @task
    def dashboard_task(self) -> Task:
        return Task(
            config=self.tasks_config['dashboard_task'],
            depends_on=[self.bid_optimization_task],
            output_file='dashboard_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Bid Optimization crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
