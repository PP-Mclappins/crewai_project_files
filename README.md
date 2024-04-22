This repo houses easy-start templates for use within the CREWAI Framework.

To get setup with ollama open a terminal and run: 

curl -fsSL https://ollama.com/install.sh | sh

use 'ollama pull "model name" to bring down models from the library: 

https://ollama.com/library
_________
Next, Sign up for a free account on https://serper.dev and create an API key to use within the attached scripts.

Once you've pulled your models, and grabbed your API key:

you can get started by simply pasting the model names and the API key into their respective locations inside the .py files i've setup.
_________

To install CREWAI on Ubuntu: 

sudo apt install python3-full python3-pip
____
Create a project directory on your home folder and CD to it: 

Example:

cd /home/User/crewai-venv
______
Next set up a python virtual environment: 

python3 -m venv /home/user/crewai-venv

Then activate the environment:

source /home/user/crewai-venv/bin activate
_______

Once activated follow the install process on https://docs.crewai.com

_______

After the scripts are tailored with your API key and chosen models, you can save them into the VENV folder, and then either run them from the command line or from a terminal in vs code.







