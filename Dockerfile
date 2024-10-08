# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY par_parser.py .
COPY spec.json .

# Copy the tests directory
COPY tests/ ./tests/

# Copy the make.bat file (for Windows compatibility)
COPY make.bat .

# Set the environment variable to run Python in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Command to run the parser
CMD ["python", "par_parser.py"]