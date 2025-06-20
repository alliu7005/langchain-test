import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
from langchain import hub
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_structured_chat_agent, initialize_agent, AgentType
from agentops import init, end_session
from pydantic import BaseModel

MODEL=os.environ['MODEL']
HOST=os.environ['HOST']



def get_spotify_creds():
    token = os.environ["TOKEN"]
    return spotipy.Spotify(auth=token)

def retrieve_artist_id(artist_name: str) -> str:
    """Retrieve the Spotify ID of an artist given their name."""
    results = get_spotify_creds().search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    if not items:
        raise ValueError(f"No artist found with name {artist_name}")
    return items[0]['id']

def retrieve_tracks(artist_id: str, num_tracks: int) -> list:
    """Retrieve the top tracks of an artist given their Spotify ID."""
    top_tracks = get_spotify_creds().artist_top_tracks(artist_id)
    return [track['name'] for track in top_tracks['tracks'][:num_tracks]]

@tool
def get_music_recommendations(artists: list, tracks: int) -> list:
    """Get music recommendations based on a list of artists and the number of tracks requested."""
    final_tracks = []
    print("ARTISTS:", artists)
    print("TRACKS:", tracks)
    for artist in artists:
        artist_id = retrieve_artist_id(artist)
        artist_tracks = retrieve_tracks(artist_id, min(tracks, 10))
        final_tracks.extend(artist_tracks)
    random.shuffle(final_tracks)
    print(final_tracks)
    return final_tracks[:tracks]

# Initialize LLM with OpenAI's API
llm = ChatOllama(model=MODEL, base_url=HOST)
tools = [get_music_recommendations]

system_prompt = """You are a music recommendation assistant. You have access to the following tools:
{tool_names}
{tools}

When you think, use the format:

Thought: your reasoning here

When you decide to call a tool, output exactly:

Action:
```json
{{"action": "{action}", "action_input": {tool_input}}}
Begin!"""

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    MessagesPlaceholder(variable_name="tool_names"),
    MessagesPlaceholder(variable_name="tools"),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create the agent with LangChain using the pulled prompt
#a = create_structured_chat_agent(llm, tools, prompt)
#agent = AgentExecutor.from_agent_and_tools(agent=a, tools=tools, verbose=True, max_iterations=2, early_stopping_method="generate", return_only_outputs=True)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    prompt=prompt,
    verbose=True,
)


class Query(BaseModel):
    prompt: str


def query_agent(query:Query):
    input_data = {"input": query.prompt}
    response = agent.run(input_data)
    return response


