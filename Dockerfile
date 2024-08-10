# Use Python's alpine image
FROM python:3.12-alpine

# Set the working directory
WORKDIR /code

# Set up project
COPY src src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Set the entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
