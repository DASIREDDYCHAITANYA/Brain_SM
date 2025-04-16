FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY extract_and_index.py .

CMD ["python", "extract_and_index.py"]
