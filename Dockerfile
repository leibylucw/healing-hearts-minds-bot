# Use Python's alpine image
FROM python:3.12-alpine

# Set the working directory
WORKDIR /code

# Copy project files
COPY src .
COPY requirements.txt .

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin

# Install project dependencies
RUN pip install -r requirements.txt

# Set entrypoint script permissions
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
