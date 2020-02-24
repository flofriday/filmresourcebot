# Deployment
This is how I deploy the bot, and this may not work for you.

I deploy the bot on a raspberry pi 3B, where it runs inside a docker container.
Therefore, this repository has some specific files for that.

## My Steps
1. Install Docker
`curl -sSL https://get.docker.com | sh`
2. Create a docker volume for the container to use
`docker volume create filmresourcebot-volume`
3. Install Gitlab Runner
```
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
sudo apt-get install gitlab-runner
```
4. Register a GitLab Runner (Make sure that you use the shell executor and no tags)
5. In the settings for CI/CD go to Variables. Then add a new one with Type=File
Key=CONFIG. For the value you fill in the example-config.json with all your 
login credentials from the different services and just copy the json.
