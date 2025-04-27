# Step 1: Use the official Python image as the base image
FROM python:3.10-bullseye

# Step 2: Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Step 3: Set working directory
WORKDIR /app

# Step 5: Copy requirements
COPY requirements.txt .

# Step 6: Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Step 7: Copy source code
COPY . .

# Step 8: Expose port
EXPOSE 8000

# Step 9: Command to run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]