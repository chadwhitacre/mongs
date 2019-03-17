FROM python:3

WORKDIR /app
COPY . /app
RUN python -m pip install -r requirements.txt

ENV PORT 80
EXPOSE 80
CMD python -m launch
