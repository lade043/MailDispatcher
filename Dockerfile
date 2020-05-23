FROM python

#copy all the (necesary) parts
COPY . .

#install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#run
CMD ["python", "./MailDispatcher.py"]
