FROM python:3.12-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app/

# install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# COPY Project Files
COPY ./src .

# Run Container
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]
