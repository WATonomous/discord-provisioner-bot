# discord-provisioner-bot

This is a simple Discord bot used to trigger WATO's infrastructure provisioning pipeline when a user joins the Discord server.

## Usage

```bash
docker build . -t discord-provisioner-bot
docker run --rm -it -e DISCORD_TOKEN=<DISCORD_TOKEN> -e GITHUB_TOKEN=<GITHUB_TOKEN> -e SENTRY_DSN=<SENTRY_DSN> discord-provisioner-bot
```

## Deployment

This bot is deployed to WATO's Kubernetes cluster. The deployment is managed in the internal [infra-config](https://github.com/watonomous/infra-config) repo.
