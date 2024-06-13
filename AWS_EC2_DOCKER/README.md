# EC2 Docker pipeline

pipeline for deploying a simple docker application to an ec2 instance

------------
## CI/CD
This project contains CI and CD pipelines.

Since I am only working with one environment I decided I want to manually trigger the CD pipeline every time I want to delpoy the application. 

### CI Steps
- Building and Linting - This step occurs on every pull request and merge to ensure that the code being pushed to the main branch is not broken and is using proper syntax
- Terraform Build - Similarly to the applicaiton build step, this step runs a terraform plan on the infrastructure to make sure that there are no terraform code errors before deployment
- Version and publish - the last step of the CI pipeline only happens on merge to the main branch. After all of the preliminary builds, there is a new version created and a new image is pushed to docker hub. The versioning format is sematic versioning and the user has the option to pass MAJOR or PATCH into the title of the merge to increment a major or patch version. The default incrememnt is minor

### CD Steps






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