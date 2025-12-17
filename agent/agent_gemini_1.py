from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import LLMChain
from langchain_classic.prompts import PromptTemplate
from langchain_classic.tools import Tool
from langchain_classic.agents import initialize_agent, AgentType

#gemini key created from google AI studio
mykey = "AIzaSyDub1undfAxUNgoZFjbP1a2qMsWbG1X2co"
#initialize llm model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=mykey)

#######################################
# **** Simple agent
# Define a simple prompt for the agent
template1 = """
  You are an AI assistant with expertise in data analysis and automation.
  Answer the following question:
  Question: {question}
"""
#prepare the prompt and setup a chain without tool
prompt1 = PromptTemplate(template=template1, input_variables=["question"])
chain = LLMChain(prompt=prompt1, llm=llm)
# launch a query
query1 = "does science has a path to self-realization? Give a short answer."
response1 = chain.run(question=query1)
print(f"Agent response: {response1}")
#######################################

#######################################
# **** Agent with tool use capability
#make a function that llm can use as a tool to get stock price
import yfinance as yf
def get_stock_value(stock_symbol):
  stock = yf.Ticker(stock_symbol)
  return stock.history(period="1d")["Close"][0]
# make the tool available to the llm model
tool = Tool.from_function(func=get_stock_value, name="GetStockVal", description="Gets the stock price for a given symbol, like SNPS")
tools = [tool]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    system_message="You are a helpful financial assistant and tell the stock-prices using the GetStockVal tool."
)
# launch a query to chain_with_tool
query2 = "what is the stock-price of SNPS?"
response2 = agent.run(query2)
print(f"Agent response: {response2}")
