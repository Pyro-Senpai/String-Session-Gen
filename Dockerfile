# (©)Pyro-Senpai

# Use a more recent Python runtime
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run bot.py when the container launches
CMD ["python", "bot.py"]