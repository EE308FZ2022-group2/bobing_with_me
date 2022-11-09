FROM python:3.9
ADD ./bobing /app
WORKDIR /app
RUN pip install -r requirement.txt
CMD ["python", "run.py"]