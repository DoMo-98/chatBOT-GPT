# We use the base image of Python 3.11.4 with Alpine 3.18
FROM python:3.11.4-alpine3.18

# Set the working directory in the container
WORKDIR /app

# Copy the files from the current directory to the container
COPY . /app

# Update the package indexes and then install ffmpeg
RUN apk update && apk add ffmpeg

# Set permissions for the app directory and create a non-root user
RUN chmod -R 444 app/ && adduser --disabled-password appuser

# Switch to the non-root user
USER appuser

# Update PATH to include user local bin directory
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Execute the Python program
CMD ["python", "app/main.py"]
