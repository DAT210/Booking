FROM python:3.6


RUN mkdir /app

WORKDIR /app


COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
# Run app.py when the container launches
CMD ["python", "./src/__init__.py"]
