FROM python:3.8-slim

# Copy Python module
COPY ./apl_api /usr/src/api/apl_api/

# Install dependencies
COPY ./requirements.txt /usr/src/api/
WORKDIR /usr/src/api/
RUN pip install --no-cache-dir -r /usr/src/api/requirements.txt

# Expose the port used to access the API
EXPOSE 5000

# Run the application
CMD cd /usr/src/api/ && python3 -m apl_api
