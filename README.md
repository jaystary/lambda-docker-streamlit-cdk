# Scalable ML Inference Pattern for CPU bound requests through Lambda + Custom Containers via CDK
![architecture](https://user-images.githubusercontent.com/34389140/101266377-9b745000-374e-11eb-8efa-c37fec3b0caf.png)
[AWS Lambda – Container Image Support](https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/)

This repo creates a CDK Stack that includes:
- a shared filesystem (EFS)  
- a Lambda bound to an API Gateway and EFS 
- a Streamlit UI deployed onto a Fargate Service accessible through an Application Load Balancer (Optional)
 
## Usecases ---> on-demand Microservices
Considering the evolution of Lambda within AWS, 
- the possibility to always keep Lambdas "warm",  
- the ability to mount persitant storage   
- fast execution times compared to other providers  
it allows for new microservice patterns that can be chained together as non-provisioned application that seamlessly scales.

A specific usecase for ML in that instance can be to run ML Inference Patterns for CPU bound requests but more general it can be anything that interacts on a request/response pattern.

Currently there is no logic implemented aside from some dummy code to demonstrate some functionality.

Streamlit is optional (and commented out) and could be replaced by any application / webserver

To use Streamlit, uncomment the code in /lambda_docker/lambda_docker_stack.py that indicates Streamlit.

## What is AWS CDK

[AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) allows to define infrastructre as code. This project uses Python as language.

In order to use this repo, an AWS Account is required, [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed and configured as well as [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) installed.

**This repo will incur costs on an AWS Account**

### A few prerequisits on AWS CDK
AWS CDK has few important commands:
- **cdk deploy** (Deploys infrastructure)
- **cdk destroy** (Destroy deployed infrastructure)
- **cdk diff** (Similiar to a git diff shows differences between deployed and current stacks)
- **cdk ls** (Lists all the stacks/infrastructure in an app)
- **cdk synth** (Synthesizes and prints Cloudformation template)

Under the hood, CDK translates stacks into Cloudformation templates, and these cloudformation templates get created within AWS.

A best practice is to deploy/develop into a sandbox account initally for testing.

#### Issue with ECS Tasks for redeployment (currently WiP).

With Streamlit active, which runs as a Task on ECS Fargate, if the stack gets redeployed into an actively running stack, it currently does not shut down the first task properly which makes the deployment stuck.

Should this be the case, look up ECS, select the relevant cluster, select tasks, stop all running tasks and delete the cluster manually. Should there be already a job pending, it might then become unstuck and continue or after deletion you can cdk deploy again. This depends on the state of the deployment, but either way will work.


## Structure
This project contains 3 core components:
- **lambda_docker** - contains the CDK code that deploys the infrastructure
- **model** - custom container which the Lambda function utilizes. Additionally an example mount to EFS and how to use it
- **streamlit-docker** - contains a streamlit instance exposed by a application load balancer and connected to the API Gateway to access the Lambda + EFS mount


## How to use
From the root folder of this project - set up an environnment (Linux/Mac)
```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### Configure the project name and your AWS account in cdk.json
This repo assumes eu-central-1 as region but obv can be used in any other region as well.
This allows to deploy the project onto multiple cloud accounts by switching out the account name e.g.:
```
"aws-account": "YOUR AWS ACCOUNT #",
"name" : "demo",
"aws-region" : "eu-central-1"
```

Bootstrap CDK onto AWS (only needs to be done once)
```
cdk bootstrap aws://YOUR AWS ACCOUNT #/eu-central-1
```

Check that the stack is visible 
```
$ cdk ls
```

Deploy the stack:
```
$ cdk deploy stack_name
```

The inital deploy will take some time as it has to build everything from ground up:
- Building the infrastructure  
- Building the Containers and pushing deploying them  

If an update is required and the stack is live, it is possible to update the running stack simply by:
```
$ cdk deploy stack_name
```

![Deployment](https://user-images.githubusercontent.com/34389140/101266376-9b745000-374e-11eb-8d39-361919fe1c1c.png)

Once this process is complete, it will display the URLs in the console. These URLs change with every new redeploy.

![Deployed](https://user-images.githubusercontent.com/34389140/101266375-9adbb980-374e-11eb-8f51-bad454117ad3.png)

### Requests for Lambda invocation
This will post a message and respond with a timestamped messages:
```
curl --location --request POST 'URL' \
--header 'Content-Type: application/json' \
--data-raw 'Hello World'
```

This will return all messages currently in EFS:
```
curl --location --request GET 'URL' \
--data-raw ''
```

Data gets persisted to EFS

### Destroying the stack
After being done with the stack, it needs to be destroyed otherwise it keeps incurring costs.

```
$ cdk destroy stack_name
```

Currently the EFS Filesystem is configured as
```
removal_policy=core.RemovalPolicy.DESTROY
```
which means, all data will get destroyed when the stack gets destroyed. Remounting a stack to an existing Filesystem in case of a redeployment is not currently implemented in the current code but is possible by creating a seperate EFS Filesystem in a seperate stack and mounting via filesystem id:

```
taskdef.add_volume(
    name=f"{name}-volume",  
    efs_volume_configuration=ecs.EfsVolumeConfiguration(
            file_system_id=EFS_ID
    ))
```

## Debugging
A custom log group is created within Cloudwatch for Lambda invocations /aws/lambda/name

This contains all Lambda execution details

## Further resources and examples on CDK
[AWS CDK offical examples](https://github.com/aws-samples/aws-cdk-examples)  
[CDK Workshop](https://cdkworkshop.com/)  
[A collection of CDK Patterns](https://github.com/cdk-patterns/)  
[More CDK Patterns](https://github.com/kolomied/awesome-cdk)  
[CDK Well Architected Pillars](https://cdkpatterns.com/patterns/well-architected/)  
