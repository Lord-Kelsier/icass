FROM python

WORKDIR /App

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "simulate.py", "5000"]