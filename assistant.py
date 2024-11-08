import langgraph
from datetime import datetime
from langchain_groq import ChatGroq
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from assistant_tools import search_products
# Load environment variables from a .env file
load_dotenv()


# # Connection parameters
# conn_params = {
#     "host": os.getenv("DB_HOST"),        # Replace with your host
#     "port": os.getenv("DB_PORT") ,           # Default port for PostgreSQL
#     "database": os.getenv("DB_DATABASE"),  # Replace with your database name
#     "user": os.getenv("DB_USER"),    # Replace with your username
#     "password": os.getenv("DB_PASSWORD") # Replace with your password
# }

# # Establish a connection
# try:
#     # Connect to PostgreSQL server
#     conn = psycopg2.connect(**conn_params)
#     print("Connected to the PostgreSQL database")

#     # Create a cursor object
#     cursor = conn.cursor()

#     # Example query: fetch the first 5 rows from products table
#     cursor.execute("SELECT * FROM amazon_products LIMIT 5;")
#     rows = cursor.fetchall()

#     # Display the results
#     for row in rows:
#         print(row)

#     # Close the cursor and connection
#     cursor.close()
#     conn.close()
#     print("Connection closed")

# except Exception as error:
#     print(f"Error: {error}")
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_DATABASE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph.message import AnyMessage, add_messages


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]



class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            user_id = configuration.get("user_id", None)
            state = {**state, "user_info": user_id}
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}

llm = ChatGroq(
    model="llama-3.1-70b-versatile",  # Specify the model name
    temperature=1,             # Set the desired temperature
    max_tokens=7999,              # Define the maximum number of tokens
    timeout=10,                  # Set a timeout in seconds
    max_retries=2                # Number of retries in case of errors
)

primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful amazon shopping assistant."
            " Use the provided tools to search for products and other information to assist the user's queries. "
            " When searching, be persistent. Expand your query bounds if the first search returns no results. "
            " If a search comes up empty, expand your search before giving up."
            "\n\nCurrent user:\n<User>\n{user_info}\n</User>"
            "\nCurrent time: {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)


tools = [search_products]
assistant_runnable = primary_assistant_prompt | llm.bind_tools(tools)

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from utils import create_tool_node_with_fallback , _print_event
builder = StateGraph(State)


# Define nodes: these do the work
builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(tools))
# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

import shutil
import uuid

# Let's create an example conversation a user might have with the assistant
tutorial_questions = [
    "Hi",
    "suggest me some good .",
    "and keyboards as well"
]

# Update with the backup file so we can restart from the original place in each section

thread_id = str(uuid.uuid4())

config = {
    "configurable": {
       
        "user_id": "1",
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}


_printed = set()
for question in tutorial_questions:
    events = graph.stream(
        {"messages": ("user", question)}, config, stream_mode="values"
    )
    for event in events:
        _print_event(event, _printed)
        