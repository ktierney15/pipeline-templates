# AWS ECR FARGATE PIPELINE

[Link to AWS documentation for setting up ecr/ecs](https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-amazon-elastic-container-service )

## prerequisites
1. create ecr repository

```bash
aws ecr create-repository \
    --repository-name MY_ECR_REPOSITORY \
    --region MY_AWS_REGION
```

2. Create an Amazon ECS task definition, cluster, and service.

- For details, follow the Getting started wizard on the Amazon ECS console, or the Getting started guide in the Amazon ECS documentation.