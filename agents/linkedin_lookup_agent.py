from dotenv import load_dotenv
load_dotenv()

from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools import get_tavily_profile_url
def lookup(name: str):
	llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
	template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                              Your answer should contain only a URL"""

	prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

	tools_for_agent = [Tool(
		name="Crawl Google 4 linkedin profile",
		func=get_tavily_profile_url,# python function,
		description="useful when you need Linkedin profile URL",
	)]

	react_prompt = hub.pull("hwchase17/react")
	agent = create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
	agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

	result = agent_executor.invoke(input={"input":prompt_template.format_prompt(name_of_person=name)})

	linkedin_profile_url=result["output"]
	return linkedin_profile_url



if __name__=="__main__":
	linkedin_url = lookup(name="Daksh Patel USC")
	print(linkedin_url)