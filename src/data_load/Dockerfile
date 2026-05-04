FROM python:3.11-slim

WORKDIR /app

COPY src/data_load/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/data_load/data_load.py .
COPY data/ /app/data/

CMD ["python", "data_load.py"]