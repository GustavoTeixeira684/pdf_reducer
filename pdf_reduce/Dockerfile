FROM python:latest
WORKDIR /app
RUN pip3 install --no-cache-dir flask
RUN apt update -y
RUN apt install -y ghostscript
COPY temp_files /app/temp_files
COPY main.py /app/
EXPOSE 5002
CMD [ "python3", "/app/main.py"]