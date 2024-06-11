provider "aws" {
  region = "us-east-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_instance" "test" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI (HVM), SSD Volume Type
  instance_type = "t2.micro"
}

locals {
  playbook_vars = {
    docker_user = var.docker_user
    docker_pass = var.docker_pass
  }
}


data "cloudinit_config" "server_config" {
  gzip          = true
  base64_encode = true

  part {
    content_type = "text/cloud-config"
    content      = templatefile("${path.module}/templates/cloud-init.yaml",
      {
        playbook      = base64encode(file("${path.module}/playbooks/playbook.ansible.yaml"))
        playbook_vars = base64encode(jsonencode(local.playbook_vars))
      }
    )
  }

}
