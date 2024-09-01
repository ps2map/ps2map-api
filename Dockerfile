FROM python:3.12

COPY . /app
RUN pip install -r /app/requirements.txt

# TODO: Make the port configurable
EXPOSE 5000

WORKDIR /app
CMD ["python", "-m", "server"]
