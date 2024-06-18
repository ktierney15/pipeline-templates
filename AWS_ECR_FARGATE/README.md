# AWS ECR FARGATE PIPELINE

This is a simple CI/CD pipeline that allows you to push a docker image to AWS Elastic Container Registry to be leveraged by AWS fargate
  
[Link to AWS documentation for setting up ecr/ecs](https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-amazon-elastic-container-service )

## How the pipeline works
Once onboarded, you will have a cloudformation stack consisting of a fargate cluster that scales up and down (and load balances) based on the websites traffic.   
    
The onboarding consists of creating your ECR repository and running the two cloudformation templates to stand up the stack. 
Once onboarded, CI/CD takes care of the rest of the work.    
   
When you create a pull request, the CI pipeline will build your container to make sure there are no build errors. Once it is confirmed your image builds,
you can merge and the CI pipeline will version and tag your application based oin your merge commit message (MAJOR, MINOR, PATCH).   
   
When you are ready to promote a version to production you can run CD (from the tag/ref that you want to deploy) and it will build and push that image to your ECR registry and redeploy the task definition

## Onboarding
1. create ecr repository (name it the name of your repository)

```bash
aws ecr create-repository \
    --repository-name MY_ECR_REPOSITORY \
    --region MY_AWS_REGION
```

2. Copy the following into your Github repository
- .github folder
- templates folder
- Dockerfile (or create your own)
- nginx.conf (if its an nginx container)

3. add templates/* to your .gitignore file

4. Make sure the following resources exist in AWS:
- A VPC
- 2 subnets in that VPC (in two different availability zones)
- a route53 DNS record
- your ECR repository that you created in step 1

5. Run the first cloudformation template with the following command:
```bash
aws cloudformation create-stack --stack-name STACK_NAME --template-body file://template1.yaml --capabilities CAPABILITY_NAMED_IAM \
--parameters ParameterKey=VPCID,ParameterValue=YOUR_VPC_ID \
ParameterKey=Subnet1ID,ParameterValue=YOUR_SUBNET_1_ID \
ParameterKey=Subnet2ID,ParameterValue=YOUR_SUBNET_2_ID \
ParameterKey=DomainName,ParameterValue=YOUR_DOMAIN_NAME.com \
ParameterKey=Image,ParameterValue=YOUR_IMAGE \
ParameterKey=Name,ParameterValue=YOUR_RESOURCE_NAME 
```
Note: You will have to manually validate the certificate in certificate manager while the stack is being created

6. Run the second cloudformation template with the following command:
```bash
aws cloudformation update-stack --stack-name STACK_NAME --template-body file://template2.yml --capabilities CAPABILITY_NAMED_IAM \
--parameters ParameterKey=VPCID,ParameterValue=YOUR_VPC_ID \
ParameterKey=Subnet1ID,ParameterValue=YOUR_SUBNET_1_ID \
ParameterKey=Subnet2ID,ParameterValue=YOUR_SUBNET_2_ID \
ParameterKey=DomainName,ParameterValue=YOUR_DOMAIN_NAME.com \
ParameterKey=Image,ParameterValue=YOUR_IMAGE \
ParameterKey=Name,ParameterValue=YOUR_RESOURCE_NAME 
```


## Branching strategy
The branching strategy that this pipeline is based on is a simple 2 branch strategy:   
- **develop** branch for development  
- **main** branch that runs CI on push   

When the developer creates a pull request from develop to main, a PR check runs. if it passes you can merge your code to main and the CI pipeline will run. From there it will create a tag and you can only deploy from those tags.

## CI steps
- checkout - checks out code
- docker build/run - builds and runs container (PR validation)
- git tag - gets the latest tag
- get commit message - parses merge commit message for MAJOR, MINOR, or PATCH
- set increment type - sets variable based off of the commit message
- semantic Versioning - determines new version
- tag new version - tags the new version

## CD steps
- pre-check - checks to see if you are running the pipeline from a proper version that is tagged (and not a branch)
- print name - logs the app name and version being deployed
- checkout - checks out repository based on specified ref
- configure AWS credentials - signs into AWS
- login to ECR - logs into Amazon ECR
- build/tag/push - builds tags and pushes the docker image to ECR (currently stores it as latest)
- download task definition - downloads current task definition from AWS
- update image in task definition - fills in the new image ID in the task definition
- deploy task definition - deploys the task definition to AWS fargate