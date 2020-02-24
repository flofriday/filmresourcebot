FROM python:3.8-alpine

WORKDIR /app

# Install dependencies
RUN apk add gcc g++ make libffi-dev openssl-dev
RUN pip install praw python-telegram-bot requests

# Copy the rest of source files
COPY . .

# Start point of the container
CMD ["python", "./main.py"]
