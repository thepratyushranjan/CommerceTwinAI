import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from modules.support.tools import search_knowledge_base, get_order_status, escalate_to_human
from shared.config import config

def get_agent():
    """Initializes and returns the LangGraph ReAct agent."""
    config.validate()
    
    # Initialize the LLM (using Flash for speed and cost efficiency in support)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=config.GOOGLE_API_KEY,
        temperature=0
    )
    
    # Define the toolset
    tools = [search_knowledge_base, get_order_status, escalate_to_human]
    
    # Load system prompt
    with open("prompts/agent_system.txt", "r") as f:
        system_prompt = f.read()
    
    # Create the ReAct agent
    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent

def run_agent(message: str, history: list = None):
    """
    Runs the agent with the given message and history.
    Returns a dict with response, tool_calls, and trace.
    """
    agent = get_agent()
    
    # Format history for LangChain/LangGraph if needed
    # history should be a list of BaseMessage objects or compatible dicts
    inputs = {"messages": history + [("user", message)] if history else [("user", message)]}
    
    # Execute agent
    result = agent.invoke(inputs)
    
    # Extract the last message (agent response)
    messages = result["messages"]
    last_message = messages[-1]
    
    # Robustly extract text from content
    content = last_message.content
    if isinstance(content, list):
        # Join all text parts, ignoring metadata like signatures
        text_response = "".join([part["text"] for part in content if isinstance(part, dict) and "text" in part])
    else:
        text_response = str(content)
    
    # Extract tool calls and trace
    tool_calls = []
    trace = []
    
    for msg in messages:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                tool_calls.append({
                    "tool": tc['name'],
                    "args": tc['args']
                })
        # If it's a ToolMessage, it contains the output of a tool
        if msg.type == 'tool':
            trace.append({
                "tool": msg.name,
                "output": msg.content
            })

    return {
        "response": text_response,
        "tool_calls": tool_calls,
        "trace": trace,
        "all_messages": messages
    }
