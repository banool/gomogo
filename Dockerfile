FROM node:14.2.0

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install -y parallel

# Install backend
RUN apt-get install -y python python-pip
RUN pip install -r data/requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install UI
RUN npm install

EXPOSE 5000
EXPOSE 5001

ENV PORT 5000
ENV BACKEND_PORT 5001

ENTRYPOINT ./run.sh 
