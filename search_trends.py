from newsapi import NewsApiClient
from utils import get_env_var

newsapi= NewsApiClient(api_key=get_env_var("NEWSAPI_API_KEY"))

sources = newsapi.get_sources()
# print(sources)
all_articles = newsapi.get_everything(q='latest technology and science news',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)
print(all_articles)
