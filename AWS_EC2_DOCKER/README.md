# EC2 Docker pipeline

pipeline for deploying a simple docker application to an ec2 instance

**Disclaimer: This pipeline style works better if you are using persisting self hosted runners or terraform cloud workspaces**   
  
**The purpose of terraform is to maintain state and this pipeline currently does not do that**

We can get away with it in this case because we are only creating a few resources which will generally go unchanged - and we have a workflow to delete all of the resources with the CLI

Unfortunately, this means before running CD you always have to run the destroyServer workflow

------------
## CI/CD
This project contains CI and CD pipelines.

Since I am only working with one environment I decided I want to manually trigger the CD pipeline every time I want to deploy the application. 

### CI Steps
- Building and Linting - This step occurs on every pull request and merge to ensure that the code being pushed to the main branch is not broken and is using proper syntax
- Terraform Build - Similarly to the application build step, this step runs a terraform plan on the infrastructure to make sure that there are no terraform code errors before deployment
- Version and publish - the last step of the CI pipeline only happens on merge to the main branch. After all of the preliminary builds, there is a new version created and a new image is pushed to docker hub. The versioning format is sematic versioning and the user has the option to pass MAJOR or PATCH into the title of the merge to increment a major or patch version. The default increment is minor

### CD Steps
- Pre-check - checks to see if you are running the pipeline from a proper version that is tagged
- Checkout - Checks out the repository - mainly for the IAC folder for CD
- Setup terraform - install terraform on the runner
- init and apply - run a terraform init and apply on your terraform files

### Onboarding
1. add the .github and IAC folders to your repository
2. create a Dockerhub repository to push your images to (and name it after your Github repository)
3. create a Dockerfile - there is an example in this repository but it can be whatever you want it to be
4. replace "app-name" with your application in the clout init template (or parameterize it if you choose)
5. replace "app-name" with your application in the ansible playbook (or parameterize it if you choose)
6. replace anything you need to in the ansible playbook or terraform module  
    examples:   
        - change the port mappings if need be in the ansible playbook  
        - change your AWS region or ami id

#### Optional
- parameterize more of the main.tf / add variables to the varibales.tf
    - ex: instance type, ami, etc...
- add DNS to the main.tf
- create an outputs.tf file and return information about your resources

### File breakdown
.github/workflows/CI.yaml - CI pipeline
.github/workflows/CD.yaml - CD pipeline
.github/workflows/destroyServer.yaml - will destroy the server if you need to take it down
.github/scripts/sem-ver.py - sematic versioning python script for CI
   
IAC/playbooks/playbook.ansible.yaml - configures the server to run the docker container and exposes it to a port
IAC/templates/cloud-init.yaml - cloud init file. runs ansible playbook on boot
IAC/main.tf - main terraform code
IAC/variables.tf - terraform variables



-----------------
# Deleting the infrastructure via CLI
These are the commands you have to run if you want to manually delete the infrastructure

```bash
aws iam remove-role-from-instance-profile --instance-profile-name 'ssm_instance_profile' --role-name 'ssm_role'
aws iam detach-role-policy --role-name 'ssm_role' --policy-arn 'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'
aws iam delete-role --role-name 'ssm_role'
aws iam delete-instance-profile --instance-profile-name 'ssm_instance_profile'
aws ec2 delete-security-group --group-id <group-id>
aws ec2 terminate-instances --instance-ids <instance-id>
```