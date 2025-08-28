# Use official Python image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy all project files into container
COPY . /app

# Install required Python libraries
RUN pip install --no-cache-dir pandas plotly scikit-learn matplotlib seaborn

# Default command when container runs
CMD ["python", "happiness_map.py"]
