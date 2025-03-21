# Dockerfile for excuteItelration.py

FROM python:3.12

# Set the working directory
WORKDIR /app/evaluate

# Copy the script into the container
COPY excuteItelration.py .

# Install any necessary dependencies (if applicable)
# RUN pip install -r requirements.txt
RUN pip install requests

# Command to run the script
CMD ["python", "excuteItelration.py"]
