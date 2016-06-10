# PyLint WebServer

Responds to Webhooks from GitHub:
- New Pull Request
- Push to existing Pull Request

1. It clones the repository at the branch and commit in the pull request.
2. It reads the file pylint_modules.txt from the root of the repository.
3. It runs pylint on all modules mentioned in that file.
4. It comments on the pull request with the pylint output.

# Installation
1. Check-out this repository to your server.
2. Install the required python packages.

# Configuration
Create a config.json (see config.json.example) file and fill in the port,
username and password. It is recommended to limit the read permissions of this
file so other users on the system cannot access the Github user account
credentials in this file. Preferably you would create a new user account for
this service.

# Running
 python plws
