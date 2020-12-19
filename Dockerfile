# Pull official base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Configure server and install dependencies
RUN pip install --upgrade pip setuptools


# Copy and install pip dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy django project
COPY . /usr/src/app

# Set work directory
WORKDIR /usr/src/app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]
