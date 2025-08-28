# generate_dockerfile.py

import os

# Ścieżka do katalogu projektu
project_dir = r"C:\Users\slast\OneDrive\Pulpit\docker_happ\HAppY_pro"

# Zawartość pliku Dockerfile
dockerfile_content = """# Use official Python image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy all project files into container
COPY . /app

# Install required Python libraries
RUN pip install --no-cache-dir pandas plotly scikit-learn matplotlib seaborn

# Default command when container runs
CMD ["python", "happiness_map.py"]
"""

# Ścieżka do pliku Dockerfile
dockerfile_path = os.path.join(project_dir, "Dockerfile")

# Zapis pliku
with open(dockerfile_path, "w") as f:
    f.write(dockerfile_content)

print(f"Dockerfile has been created at: {dockerfile_path}")
