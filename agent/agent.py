# Assemble tools, retriever, and LLM into a LangChain agent
import os
import config
from langchain_openai import ChatOpenAI
from tools import transaction_tools
from rag import vector_loader

from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, AgentExecutor
from langchain.prompts import PromptTemplate 
from langchain.agents import ConversationalAgent
#from langchain_community.agents import create_react_agent

from langchain.agents import create_tool_calling_agent


def get_agent():

    vector_store = vector_loader.get_vector_store()
    
    tools = [
        Tool(
            name="TransactionDetails",
            func=transaction_tools.get_transaction_by_id,
            description="Retrieve transaction details by transaction ID"
        ),
        Tool(
            name="RefundPolicySearch",
            func=lambda q: "\n".join(doc.page_content for doc in vector_store.similarity_search(q, k=3)),
            description="Search refund policy for relevant information"
        )
    ]

    # agent = create_react_agent(llm, tools, prompt)
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = config.OPENAI_KEY

    ChatOpenAI.model_rebuild() 
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    
    refund_prompt = PromptTemplate.from_template(
        "You are an assistant that helps users with their refund requests. "
        "You will be provided with a transaction ID and refund policy. "
        "The tool TransactionDetails will return the transaction details. "
        "The tool RefundPolicySearch has the vector database of the refund policy. "
        "Use the tools to answer if Transaction ID {Input} is eligible for refund. "
        "If a refund is not possible, provide a reason. Give the reason in a sentence or two, maximum 3" \
        "Thought:{agent_scratchpad}"
    )

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=refund_prompt
        )
    agent.name = "RefundAgent"
    
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor
    

    


    
    
    
    
        

