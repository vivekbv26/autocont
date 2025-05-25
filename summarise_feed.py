import requests

url= "https://prod.api.market/api/v1/pipfeed/parse/extract"

payload = "{\"url\":\"https://techcrunch.com/2022/04/18/web-scraping-legal-court/\"}"

headers = {
    'x-magicapi-key': "SOME_STRING_VALUE",
    'content-type': "application/json"
    }


res = requests.post(url, data=payload, headers=headers)
data = res.read()

print(data.decode("utf-8"))