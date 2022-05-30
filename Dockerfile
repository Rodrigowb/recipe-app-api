# Define the name of the image we will be using
FROM python:3.9-alpine3.13
# Define the maintainer
LABEL maintainer="app.rodwanderley.com"

# Define that we don not want buffer console
ENV PYTHONBUFFERED 1

# Copy the requirements of that machine to /tmp/requirements.txt (docker image)
COPY ./requirements.txt /tmp/requirements.txt
# Copy the dev requirements
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Copy the app directory (Django App)
COPY ./app /app
# Set the work directory
WORKDIR /app
# Expose port 800 on the container when run the container  
EXPOSE 800 

# Set the development env
ARG DEV=false

# Run command to install dependencies on the machine
# Create only one layer by running only one run block
# Create a new venv (avoid conflicts inside the image)
RUN python -m venv /py && \
  # Upgrade pip
  /py/bin/pip install --upgrade pip && \
  # Install dependencies to install psycopg2 (orm for psql)
  apk add --update --no-cache postgresql-client && \
  apk add --update --no-cache --virtual .tmp-build-deps \
  build-base postgresql-dev musl-dev && \
  # Install requirements file
  /py/bin/pip install -r /tmp/requirements.txt && \
  # Shell script
  if [ $DEV = "true" ]; \
  then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
  fi && \
  # Remove the tmp directory (remove extra dependencies; keep light)
  rm -rf /tmp && \
  apk del .tmp-build-deps && \
  # Add a new user inside the image (best practice not use the root user inside the image)
  # Don't run your application in a full access user
  adduser \
  --disabled-password \
  --no-create-home \
  # User name
  django-user

#  Update the env variable inside the image; define executable directory
ENV PATH="/py/bin:$PATH"

# Specify the user that we are using (NOT THE ROOT USER)
USER django-user
