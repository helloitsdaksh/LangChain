from langchain_community.tools.tavily_search import TavilySearchResults

def get_tavily_profile_url(name: str) -> str:
	search = TavilySearchResults()
	res = search.run(f"{name}")
	return res

