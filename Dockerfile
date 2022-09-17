FROM ubuntu:latest


COPY requirements.txt ./

RUN apt update
RUN apt upgrade -y
RUN apt install pip  -y
RUN apt install postgresql -y


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python ./setup_db.py

CMD ["python", "./main.py"]