import os
from dotenv import load_dotenv


if __name__ == "__main__":
    assert load_dotenv('scripts/.env')
    os.system(f'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {os.environ["ECR_REPO"]}')
    os.system('docker compose build')
    source_image_name = "ytdlp-webui"
    tag = f"{os.environ['ECR_REPO']}/tornikeo/webapps:latest"
    os.system(f"docker tag {source_image_name} {tag}")
    os.system(f"docker push {tag}")