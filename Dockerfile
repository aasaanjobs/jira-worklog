FROM python:3.6.6-alpine

# Environament variables
ENV PYTHONUNBUFFERED 1

WORKDIR /app
# Install python packages
ADD ./requirements.txt /app
RUN pip install -r requirements.txt

# Copy source code
ADD . /app

EXPOSE 5000

CMD python app.py
