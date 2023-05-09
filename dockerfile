# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set an environment variable
ENV MY_VARIABLE=
ENV TOKEN='852053528:AAEOdgDErcNtHbbK2E-80uSFmF5tsCeJdSc'
ENV DEBUG=True
ENV DATABASE_URL='mysql://o0o1vr0hworagxo8ehdp:pscale_pw_TNVjf1YgB4OMXcwseOUYAwahFNGhWm8TU2ehfwcjgml@aws.connect.psdb.cloud/testdb?sslaccept=strict'
ENV FIXIE_URL='fixie:VjzhkGz7rYAoEhc@speedway.usefixie.com:1080'

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define the command to run the app when the container starts
CMD ["python", "fcx_trader_test.py"]
