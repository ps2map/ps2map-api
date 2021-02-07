FROM python:3.8-slim

# Copy Python module
COPY ./apl_api /usr/src/api/

# Install dependencies
COPY ./requirements.txt /usr/src/api/
RUN pip install --no-cache-dir -r /usr/src/api/requirements.txt

# Expose the port used to access the API
EXPOSE 5000

# Update working directory
WORKDIR /usr/src/api/

# Run the application
CMD ["python3", "-m", "apl_api"]
