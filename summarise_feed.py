import requests
from utils import get_env_var
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate


url= "https://prod.api.market/api/v1/pipfeed/parse/extract"

payload = "{\"url\":\"https://economictimes.indiatimes.com/news/international/us/trump-ally-marjorie-taylor-greene-gets-into-a-fight-with-elon-musks-xai-bot-grok-users-royally-troll-her/articleshow/121382628.cms\"}"

headers = {
    'x-magicapi-key': get_env_var("PIPFEED_API_KEY"),
    'content-type': "application/json"
    }


res = requests.post(url, data=payload, headers=headers)
print(res.json().get("text"))

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

system_template = "Translate the following from English into {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
