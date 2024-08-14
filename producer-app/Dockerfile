FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and the application code
COPY requirements.txt requirements.txt
COPY functions.py functions.py
COPY producer-main.py producer-main.py

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Run the application
CMD ["python", "producer-main.py"]