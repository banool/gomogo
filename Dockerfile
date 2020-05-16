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

# Backend port. Internally, 5001.
EXPOSE 10011
# UI port. Internally, 5000.
EXPOSE 10010

ENV BACKEND_PORT 5001
ENV PORT 5000

ENTRYPOINT ./run.sh 
