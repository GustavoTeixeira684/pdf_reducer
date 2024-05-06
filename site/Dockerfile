FROM python:latest
WORKDIR /app
RUN pip3 install --no-cache-dir flask pandas requests
COPY templates /app/templates
COPY temp_files /app/temp_files
COPY log /app/log
COPY main.py /app/
EXPOSE 8080
CMD [ "python3", "/app/main.py"]