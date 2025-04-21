# Use official Python Alpine image
FROM python:3.12-alpine

# Set work directory
WORKDIR /app

# Install build dependencies for pip packages (if needed)
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set the environment variable for the database path
ENV DATABASE_PATH=sqlite:///data/ss_entries.db

# Ensure the /data directory exists
RUN mkdir -p /data

# Expose port if needed (uncomment if your app serves HTTP)
# EXPOSE 8000

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Command to run your main script
CMD ["python", "main.py"]
