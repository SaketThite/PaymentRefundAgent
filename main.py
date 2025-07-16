# Entry point to run the AI agent
from agent.agent import get_agent


def main():
    transaction_id = "TXN0014B09E"
    agent_executor = get_agent()
    result = agent_executor.invoke({"Input": transaction_id})
    print(result)
    
    #result = transaction_tools.get_transaction_by_id("TXN00028091")
    #print(result)   

    

main()  

