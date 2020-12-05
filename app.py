#!/usr/bin/env python3

from aws_cdk import core

from lambda_docker.lambda_docker_stack import LambdaDockerStack

app = core.App()

name = app.node.try_get_context("name")
account = app.node.try_get_context("aws-account")
region = app.node.try_get_context("aws-region")

aws_env = core.Environment(account=account, region=region)

infra_stack = LambdaDockerStack(
    app, 
    f"{name}-infra-stack", 
    env=aws_env, 
    name=name,description="Lambda on custom Docker/Efs/Streamlit"
)

app.synth()
