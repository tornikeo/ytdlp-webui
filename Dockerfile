FROM python:3.8-slim-bullseye
LABEL maintainer="tornikeonoprishvili@gmail.com"
RUN apt update && apt-get install git ffmpeg -y
WORKDIR /code/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
ENV PORT=80
EXPOSE ${PORT}
CMD streamlit run --server.port ${PORT} app.py --browser.gatherUsageStats False