# AWS S3 CLOUDFRONT PIPELINE
This pipeline is setup for React apps that are hosted in an S3 bucket with a cloudfront distribution and route53 DNS

## How the pipeline works
CI will make sure your application builds (on both pull requests and pushes to the main branch), then create a new version when merged based on MAJOR, MINOR or PATCH specified in the merge commit
    
CD will build your application again and deploy the build to an s3 bucket, as well as provision a cloudfront distribution and connect that to your route53 dns

## Onboarding
1. Copy the .github and IAC folders into the root of your project
2. Create a role in AWS that has permissions to create an s3 bucket, cloudfront distribution, ACM certificates, and IAM roles
3. Generate a token and save it in your repository secrets 
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
4. Buy a AWS route53 domain name then save the following values to your repository variables
    - DOMAIN_NAME
    - ROUTE53_ZONE_ID