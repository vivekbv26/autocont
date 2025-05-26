from supabase import create_client, Client
from utils import get_env_var   
url=get_env_var("SUPABASE_URL")
key=get_env_var("SUPABASE_KEY")
supabase: Client = create_client(url, key)
response = (
    supabase.storage
    .from_("audio")
    .create_signed_url(
        "output.mp3", 
        600
    ))
print(response["signedURL"])