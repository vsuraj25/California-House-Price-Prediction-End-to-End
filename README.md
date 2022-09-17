# Machine-Learning-Project
Machine Learning Project

Hi, This is my machine learning project
## Software and Requirements##

1. [Github](https://github.com)
2. [Heroku](https://id.heroku.com/login)
3. [VS Code IDE](https://code.visualstudio.com/)
4. [Git Cli](https://git-scm.com/downloads)



Creating Conda Environment
'''
conda create -p venv python==3.7 -y
'''

Command for installing all the modules in requirements.txt
'''
pip install -r requirements.txt
'''

To add a file to the git 
'''
git add <file_name>
'''

To add all the changes to git
'''
git add .
'''

TO check status of git
'''
git status
'''

To create version/commit all changes in git
'''
git commit -m "Message"
'''

To send or save version to github
'''
git push origin main
'''

To check remote url(Origin link)
'''
get remote -v
'''

To Setup CI/CD Pipeline in Heroku we need 3 information
'''
HEROKU_EMAIL
HEROKU_API_KEY
HEROKU_APP_NAME

To get the main branch name
'''
get branch
'''

BUILD DOCKER IMAGE
'''
docker build -t <imagename>:<tagname> .
'''
>Note: Image name for docker must be lowercase

RUN DOCKER IMAGE
'''
docker run - p 5000:5000 -e PORT=5000 9f8774e25b3d
'''

TO CHECK RUNNING CONTAINER
'''
docker ps
'''

TO STOP A DOCKER CONTAINER
'''
docker stop <container_id>
'''