# healing-hearts-minds-bot
A custom bot for the Healing Hearts Minds Discord server.

## Setup and Quickstart
### Install System Dependencies
Make sure you have the following dependencies installed and available on your system:
* [Git](https://git-scm.com/): any recent version.
	* [GH CLI (the GitHub CLI)](https://cli.github.com/) (optional): any recent version.
* [CPython](https://www.python.org/): version 3.12 or higher.
* [pipx](https://github.com/pypa/pipx): any recent version.
	* Use the `ensurepath` subcommand as described in the installation documentation so you can run `pipx` from anywhere.
* [Docker](https://www.docker.com/) (optional): any recent version.
	* [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/) (if running Windows): any recent version.
* [flyctl (the Fly.io CLI)](https://fly.io/docs/flyctl/): any recent version.
	* The [installation docs](https://fly.io/docs/hands-on/install-flyctl/) recommend installing via OS-specific scripts.
	* You may wish to alternatively download the [latest binary](https://github.com/superfly/flyctl/releases/latest) for your OS and place it on the path.
	* You should only need to follow the instructions through signing up/logging in.

### Clone the Repo
With Git:

```shell
git clone https://github.com/leibylucw/healing-hearts-minds-bot.git
cd healing-hearts-minds-bot
```

Or with gh:

```shell
gh repo clone leibylucw/healing-hearts-minds-bot
cd healing-hearts-minds-bot
```

### Install pre-commit and Git Hooks
This repository requires [pre-commit](https://pre-commit.com/) for managing Git hooks.  Start by installing it with:

```shell
pipx install pre-commit
```

Then install the hooks from the root directory of the repository:

```shell
pre-commit install
```

## Development
The backend is written in Python using Discord's official SDK, [discord.py](https://discordpy.readthedocs.io/en/stable/). You may develop against the code base either using a system-wide Python installation, or Docker.

**NOTE**: Documentation for development conventions and practices to follow and how the app is structured will be written soon.

### A Note About Secrets
All secrets and other config are expected to be stored in `.env`. First, copy the `.env-sample` to a `.env`. Then, work with @leibylucw to supply the necessary values.

### With System-Wide Python Installation
#### Create a Virtual Environment (virtualenv)
Using a virtual environment (virtualenv) is necessary when developing against the project. This ensures that `healing-hearts-minds-bot` has its own isolated environment, separate from your global Python and Pip, to manage its dependencies and such. It is assumed in the subsequent system-wide sections that you have created and activated one. To create one:

```shell
python -m venv .venv
```

#### Activate the Virtualenv
For Command Prompt on Windows:

```cmd
.\.venv\Scripts\activate.bat
```

For PowerShell on Windows:

```powershell
.\.venv\Scripts\activate.ps1
```

**NOTE**: You may be able to use the generic `activate` script (with no extension) to activate the virtualenv with:

```shell
.\.venv\Scripts\activate
```

For Linux/MacOS:

```sh
source .venv/bin/activate
```

To deactivate the virtualenv on all platforms:

```shell
deactivate
```

#### Install Requirements
Next, upgrade Pip and install requirements:

```shell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Run the App
Run the app with Python:

```shell
python /src/hhmBot/hhm.py
```

### With Docker
Because our production deployment uses Docker, you can also develop the project locally with Docker. This means you do not have to create a virtual environment as outlined in the system-wide Python installation instructions above. One of Docker’s strong suits is containerizing applications, which allows you to spin up containers that have everything an app needs to run. In short, the repository includes the necessary Docker configuration for you to easily spin up the container and run the app without needing to configure anything further. You can learn more [here](https://www.docker.com/why-docker/).

There is a `Dockerfile` that defines a custom image for the bot's purposes. It manages copying files, installing requirements, and invoking the app for you.

There is also a `compose.yml` configuration file that defines the container required to run the application. It builds the image using the Dockerfile and spins up the container.

#### Spin Up the Container
You can use the Docker compose tool to build the custom `healing-hearts-minds-bot` image and spin up a container using `compose.yml`. To do so, run:

```shell
docker compose up -d
```

To verify it spun up correctly, you may consult the container's logs:

```shell
docker compose logs discord
```

This command displays the logs for the `discord` service outlined in `compose.yml`. You should see some initialization text and confirmation that the bot is logged in.

To take down the container (using the optional `-v` flag to remove all associated volumes at the end of the command):

```shell
docker compose down
```

The `docker compose up -d` command implicitly builds the image from the `Dockerfile`, but if you wish to rebuild it, run:

```shell
docker compose build --no-cache
```

To view the list of Docker images, run:

```shell
docker images
```

You should see an entry named `healing-hearts-minds-bot`.

You may wish to modify the `Dockerfile` to follow better Docker practices/conventions, or if the app's infrastructure/dependencies changes. Rebuilding an image, however, leaves dangling image entries labeled as `<none>`. You can remove these entries with:

```shell
docker image prune -f
```

### General Development Notes
You will notice from the various configuration files in the repo that there are several tools to ensure certain code hygiene and quality conventions are enforced. You may wish to become familiar with these tools and the coding style configurations therein. For more info, please refer to:
* [Ruff](https://github.com/astral-sh/ruff): used for code linting and formatting
* [pre-commit](https://github.com/pre-commit/pre-commit): used for managing pre-commit hooks

## Deployment
### Fly Setup
The app is deployed to [Fly.io](https://fly.io/) under the healing-hearts-minds organization.

The repository contains a Fly config file named `fly.toml`. It defines the Fly app configuration (e.g.: app name, Dockerfile to build the app, number of shared CPUs, etc), and leverages the `Dockerfile` to spin up a container that runs the app upon deployment.

If you are not yet a member of the `healing-hearts-minds` organization, work with @leibylucw to get you proper access.

Make sure you are logged into your account that is a member of the `healing-hearts-minds` organization. Verify with:

```shell
flyctl auth whoami
flyctl orgs list
```

You should first see your email address and then the names of the organizations you belong to, including `healing-hearts-minds`.

### Redeploy to Fly
To redeploy the app to Fly (e.g.: to introduce production-ready changes), run the following flyctl command:

```shell
flyctl deploy
```

###  Recreating the App
Should the app ever need to be recreated, it is recommended to do so as outlined below.

#### Destroy and Recreate the App
First, destroy the app entirely and then create a new one:

```shell
flyctl apps destroy healing-hearts-minds-bot
flyctl apps create healing-hearts-minds-bot --org healing-hearts-minds
```

#### Set Secrets and Deploy
You need to import the environment variables from the `.env` you filled out earlier.

For CMD on Windows:

```cmd
flyctl secrets import < .env
```

For PowerShell on Windows:

```powershell
Get-Content .env | flyctl secrets import
```

For Linux/MacOS:

```sh
flyctl secrets import < .env
```

And finally, deploy the app:

```shell
flyctl deploy
```

**NOTE**: While you could use a command like `flyctl launch --org healings-hearts-minds`, it might modify the `fly.toml` file. Modifications are not recommended because the `fly.toml` is already correctly configured as committed to the repository.
