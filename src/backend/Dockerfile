FROM python:3.10.13

WORKDIR /src/backend
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# create dir
RUN mkdir -p src/backend
COPY . ./src/backend
CMD ["uvicorn", "src.backend.main:app"]