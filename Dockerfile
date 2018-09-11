
# Use an official Python runtime as a parent image
FROM python:2.7.15

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install requests 
COPY test.xml test.xml
COPY docker-compose.yml docker-compose.yml
#ENV xml 0
#ENV p 0
#ENV t 0
#ENV g 0

ENTRYPOINT ["python", "test.py"]
# Run app.py when the container launches
#CMD ["sh","-c", "python test.py test.xml ${p} ${t} ${g:+$g}"]
