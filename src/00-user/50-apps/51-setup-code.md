# Setup source code repository

## Git Repository

Your project should be version controlled with git which can be done, if it wasn't cloned already, by running `git init` in the directory of your project.

### Example Python Flask App

We'll create an example python flask app which we'll set up for production through. In a new directory, create the following files:

- `app.py`
  ```python
  import flask
  import os
  from dotenv import load_dotenv
  load_dotenv()

  app = flask.Flask(__name__)

  @app.route('/', methods=['GET'])
  def index():
    return f"Hello {os.environ['YOURAPP_WHAT']}!"

  if __name __ == '__main__':
    app.run(host='127.0.0.1', port=5000)
  ```
- `.env.example`
  ```
  YOURAPP_WHAT=world
  ```
- `.env`
  ```
  # this doesn't get pushed, it can have things like
  #  private API keys
  YOURAPP_WHAT=world
  ```
- `.gitignore`
  ```
  .DS_Store
  .env
  ```
- `requirements.txt`
  ```
  python-dotenv
  flask
  gunicorn
  ```
- `README.md`
  ```md
  # Your App Name
  Your app description

  ## Development
  `cp .env.example .env`
  `pip install -r requiements.txt`
  `python app.py`
  
  View the site at <http://localhost:5000>
  ```

Finally:
```bash
# ensure the directory is a github repo
git init
# commit the README
git add README.md
git commit -m "Initial commit"
# commit the code
git add app.py requirements.txt .env.example .gitignore 
git commit -m "Initial code base"
# if you haven't already, create a blank repo on github for your project
# connect to github
git remote add origin git@github.com:org-or-your-username/your-project-repo
# push to github
git push -u origin main
# NOTE: some systems use `master` instead of main
```
