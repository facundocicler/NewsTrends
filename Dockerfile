FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

COPY lambda/ .

RUN pip install --upgrade pip && pip install -r requirements.txt && python -m spacy download es_core_news_sm

COPY . .

CMD ["lambda_function.lambda_handler"]
