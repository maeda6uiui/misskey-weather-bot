FROM public.ecr.aws/lambda/python:3.10

COPY main.py common.py logging_config.yaml requirements.txt ${LAMBDA_TASK_ROOT}
COPY ./Data/ ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

CMD ["main.lambda_handler"]
