import requests
from utils import get_env_var
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from supabase import create_client, Client
import json

url=get_env_var("SUPABASE_URL")
key=get_env_var("SUPABASE_KEY")

supabase:Client=create_client(url, key)

response=(supabase.table("curr").select("*").execute())

currnews=(supabase.table("storeart").select("url").eq("num", response.data[0]["num"]).execute())

response = (
    supabase.table("curr")
    .update({"num": response.data[0]["num"] + 1})
    .eq("num", response.data[0]["num"])
    .execute()
)
urlsum= "https://prod.api.market/api/v1/pipfeed/parse/extract"

payload =json.dumps({"url": currnews.data[0]["url"]})

headers = {
    'x-magicapi-key': get_env_var("PIPFEED_API_KEY"),
    'content-type': "application/json"
    }


res = requests.post(urlsum, data=payload, headers=headers)
article_text = res.json().get("text")




model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")


# News anchor-style system prompt
system_template = (
    "You are a professional news anchor. Given a raw news article, your job is to rewrite it as a spoken script for a live news broadcast. "
    "The output should be clear, natural, and easy to speak aloud; use conversational but professional language like a real newsreader; "
    "maintain factual accuracy and include only the key details; avoid repeating metadata like author names or publication timestamps; "
    "and be free of filler phrases like \"in this article\" or \"according to the source.\" Your output will be used verbatim by a voice-based AI avatar. "
    "Do not include any stage directions, comments, or headers. Just output the clean spoken version of the article."
    "The information of the article should be conveyed in less than 30 seconds of speech and should be as interesting as possible. "
    "Add \"You won't believe what just happened\" at the start of the article to grab the audience's attention. "
)

# Build prompt and invoke model
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", article_text)
])

messages = prompt_template.format_messages() 
response = model.invoke(messages)            

print(response.content)
