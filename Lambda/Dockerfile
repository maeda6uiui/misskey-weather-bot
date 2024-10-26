FROM public.ecr.aws/lambda/python:3.10

COPY main.py common.py requirements.txt ${LAMBDA_TASK_ROOT}
COPY ./Data/* ${LAMBDA_TASK_ROOT}/Data/

RUN pip install -r requirements.txt

CMD ["main.lambda_handler"]
