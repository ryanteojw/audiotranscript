FROM python:3.13.1-slim

# working directory in container
WORKDIR /app

# system dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# libraries in requirement.txt file
COPY requirements.txt .

# pip install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy the application
COPY . .

# expose the Flask port
EXPOSE 5000

# command to run the flask app
CMD ["python", "run.py"]
