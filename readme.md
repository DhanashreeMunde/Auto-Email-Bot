# Auto Emailing System
### Create a virtual environment
Go to the project root folder and enter the following commands in the terminal.
The first line creates a python virtual environment named virtual_environment.
The second line activates the environment.
The third line upgrades the pip version.
```
python3 -m venv virtual_environment
source virtual_environment/bin/activate
pip install --upgrade pip
```
### Install the required python libraries
```
pip install -r requirements.txt
```
### Running the application
This application will be run using the wsgi development server. If you want to productionise the application, please use a server like gunicorn
```
python start.py
```
