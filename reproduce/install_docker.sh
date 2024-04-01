#!/bin/bash

# Check if Docker is already installed
if which docker &> /dev/null; then
  echo "Docker is already installed."
  exit 0
fi

# Update package lists
sudo apt-get update

# Install prerequisites
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker repository GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update package lists again (to reflect new repository)
sudo apt-get update

# Install Docker engine
sudo apt-get install -y docker-ce

# Add current user to Docker group (for easier access without sudo)
sudo usermod -aG docker $USER

# Verify Docker installation
echo "Docker version: $(docker version --short)"

echo "**Please log out and log back in for the changes to take effect.**"
echo "**After logging back in, you can run Docker commands without sudo.**"

echo "Docker installation complete!"