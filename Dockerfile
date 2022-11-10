FROM python:3.9
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip3 install cryptography -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["python", "app.py"]
