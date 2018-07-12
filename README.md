# cs467

SSH onto flip:
  ssh <username>@access.engr.oregonstate.edu

Install a virtual environment:
  python3 -m venv venv

Start the virtual environment
  source venv/bin/activate

Update pip (package installer):
  pip install --upgrade pip

Install libraries:
  pip install <library>

Save required libraries/versions:
  pip freeze > requirements.txt

Install requirements on another console/venv/machine:
  pip install -r requirements.txt
