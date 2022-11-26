FROM python:3.8-slim-bullseye
LABEL maintainer="tornikeonoprishvili@gmail.com"
WORKDIR /code/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
ENV PORT
EXPOSE ${PORT}
CMD gradio app