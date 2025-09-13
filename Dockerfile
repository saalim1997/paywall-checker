# Use official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

RUN mkdir -p /data

# Copy dependency files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY ./src ./src
COPY ./main.py ./
COPY ./static ./static

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]