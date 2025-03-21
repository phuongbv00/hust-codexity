# Use the specified base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the necessary files into the container
COPY . .

RUN pip install -r requirements.txt

# Set the entrypoint command
CMD ["python", "main.py"]

EXPOSE 8081
