from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
import os
from dotenv import load_dotenv
import boto3

load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Create a PDF knowledge source
pdf_source = PDFKnowledgeSource(
	file_paths=["live-streaming-on-aws-with-amazon-s3.pdf"]
)

session = boto3.Session(region_name="us-west-2")
bedrock_client = session.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'
)

from crewai_tools import (
    GithubSearchTool
)

github_tool = GithubSearchTool(
    gh_token=os.getenv('GITHUB_TOKEN'),
    github_repo='https://github.com/aws-solutions/live-streaming-on-aws-with-amazon-s3',
	content_types=['code', 'issue'], # Options: code, repo, pr, issue
	config=dict(
        llm=dict(
            provider="aws_bedrock", # 必须配置.aws/configure
            config=dict(
                model="anthropic.claude-3-5-sonnet-20240620-v1:0",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="aws_bedrock",
            config=dict(
                model="amazon.titan-embed-text-v2:0",
                task_type="retrieval_document",
				# session=session
                # title="Embeddings",
            ),
        ),
    )
)

@CrewBase
class RequirementAnalysis():
	"""LatestAiDevelopment crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools


	@agent
	def requirement_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['requirement_analyst'],
			knowledge_sources=[pdf_source],
			embedder={
				"provider": "bedrock",
				"config": {
					"model": "amazon.titan-embed-text-v2:0",
					"session": session  # 传递客户端实例
				}
			},
			verbose=1,
			max_iter=100,
			max_rpm=3
		)

	@agent
	def tech_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['tech_analyst'],
			tools=[github_tool],
			verbose=1,
			max_iter=100,
			max_rpm=3
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=1,
			max_iter=100,
			max_rpm=3
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def requirement_analyst_task(self) -> Task:
		return Task(
			config=self.tasks_config['requirement_analyst_task'],
		)
	
	@task
	def tech_analyst_task(self) -> Task:
		return Task(
			config=self.tasks_config['tech_analyst_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the RequirementAnalysis"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=1,
			memory=True,
			max_rpm=10,
			embedder={
				"provider": "bedrock",
				"config": {
					"model": "amazon.titan-embed-text-v2:0",
					"session": session  # 传递客户端实例
				}
			},
			# planning=True,
			# planning_llm="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
