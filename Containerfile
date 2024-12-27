FROM registry.access.redhat.com/ubi9/python-312

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt && pip3 install --upgrade pip

COPY app.py .

EXPOSE 8000

CMD ["python3","app.py"]
