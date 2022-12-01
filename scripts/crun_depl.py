import os
from dotenv import load_dotenv
if __name__ == "__main__":
    assert load_dotenv('scripts/.env')
    os.system('gcloud run deploy ytdlp-webui --source . --allow-unauthenticated --region us-east1 --min-instances 0 --quiet')