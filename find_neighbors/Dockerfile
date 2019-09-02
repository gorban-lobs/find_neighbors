FROM python:3.6

EXPOSE 8080

WORKDIR /find_neighbors/

COPY requirements.txt /find_neighbors/requirements.txt
RUN pip install -r requirements.txt

COPY . /find_neighbors/

CMD python app.py
