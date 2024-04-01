#!/bin/bash

# Check if Terraform is already installed
if terraform -h &> /dev/null; then
  echo "Terraform is already installed."
  exit 0
fi

# Update package lists
sudo apt-get update

# Install required packages (curl for download and unzip for unpacking)
sudo apt-get install -y curl unzip

# Download the latest Terraform version for Linux amd64 architecture
LATEST_URL="https://releases.hashicorp.com/terraform/1.7.5/terraform_1.7.5_linux_amd64.zip"

# Download Terraform
curl -o /tmp/terraform.zip "$LATEST_URL"

# Create installation directory (optional, adjust path if needed)
mkdir -p /usr/local/bin

# Unzip Terraform
unzip /tmp/terraform.zip -d /usr/local/bin

# Add Terraform to PATH (optional, but recommended for easy access)
if [[ ! $(grep 'export PATH=/usr/local/bin:$PATH' ~/.bashrc) ]]; then
  echo 'export PATH=/usr/local/bin:$PATH' >> ~/.bashrc
fi

# Verify Terraform installation
echo "Installed: $(terraform version)"

# Source the .bashrc file to update PATH immediately (optional)
# source ~/.bashrc

echo "Terraform installation complete!"