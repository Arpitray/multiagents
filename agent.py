from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from toold import web_search, scrap_url
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatMistralAI(model="mistral-small-latest", temperature=0.7, max_tokens=2048)

#1st agent 
def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search],
      
    )
    
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrap_url],
    )          
    
#writer chain

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that writes a comprehensive report based on the provided information."),
    ("human", """Based on the following information, write a detailed report:
     Topic: {topic}
     Research Findings: {research}
     
     Structure the report as:
     -Introduction
     -Key Findings
     -Conclusion
     Sources (list all the urls used for research)
     Be detailed and ensure the report is well-structured and informative.
     """)
])

writer_chain = writer_prompt | llm | StrOutputParser()

# critic chain

critics_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that critiques reports for accuracy and completeness."),
    ("human", """Please critique the following report:
    Report: {report}
    Respond in thiis exact format:
    Score (0-10):
    Strenghts:
    - ...
    - ...
    Areas to improve:
    - ...
    - ...
    one line verdict:
    ...
     
     """)
])

critic_chain = critics_prompt | llm | StrOutputParser()