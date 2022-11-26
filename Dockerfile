FROM python:3.8-slim-bullseye
LABEL maintainer="tornikeonoprishvili@gmail.com"
RUN apt update && apt-get install git ffmpeg -y
WORKDIR /code/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
ENV PORT=8999
EXPOSE ${PORT}
# CMD gradio app
CMD uvicorn app:demo.app --reload --port ${PORT} --log-level warning