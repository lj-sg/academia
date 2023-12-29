# Start your image with a node base image
FROM python:3.12-alpine3.19

ENV PYTHONUNBUFFERED=1
# The /app directory should act as the main application directory
WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev tk-dev \
    && pip install --upgrade pip

# Copy the app package and package-lock.json file
COPY ./ requirements.txt ./


# Install node packages, install serve, build the app, and remove dependencies at the end
RUN pip install -r requirements.txt


COPY ./ ./

EXPOSE 8000

# Start the app using serve command
CMD [ "python", "manage.py", "runserver","0.0.0.0:8000" ]