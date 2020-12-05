FROM public.ecr.aws/lambda/python:3.6

RUN pip install onnx==1.5.0

COPY deployment/app.py requirements.txt ./
RUN pip3 install -r requirements.txt
CMD ["app.lambdaHandler"]