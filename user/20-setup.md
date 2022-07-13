# Setup Repo for Dokku Deployment

Dokku can be used to deploy an app in several ways:
- [A repository with Dockerfile](https://dokku.com/docs/deployment/builders/dockerfiles/) (Recommended)
- [Heokuish Buldpack](https://dokku.com/docs/deployment/builders/herokuish-buildpacks/) (Recommended by dokku, but not by us)

## Docker deployment

[Docker](https://www.docker.com/) is used extensively by our lab and is useful beyond heroku, it allows you to prepare your app in a container which can be launched in a number of different platforms. Dokku will recognize a `Dockerfile` in the root of your repository and automatically build it and deploy it for you, thus ensuring your application will run as intended in production is a matter of constructing a Dockerfile.

With docker installed, you can build and test your own `Dockerfile` with:
```bash
docker build -t yourimage .
# -p [your-system-port]:[the-container-port]
docker run -p 5000:5000 -it yourimage

# your site should then be visible at http://localhost:5000
```

### Example Static Website Dockerfile

`index.html` is the entrypoint to the web application and will be shown if someone goes to your app without any url path.

- `your-app/app/index.html`
  ```html
  <html>
  <body>
    Hello World!
  </body>
  </html>
  ```
- `your-app/Dockerfile`
  ```Dockerfile
  # this base image is designed to serve a website in /usr/share/nginx/html/
  FROM nginx

  # assuming your static website is in the directory app
  COPY app /usr/share/nginx/html/
  ```

### Example Python Flask Dockerfile

We use gunicorn to serve the flask app in production instead of the app itself which can be launched in development mode by running `python app.py`.

- `your-app/app.py`
  ```python
  import flask

  app = flask.Flask(__name__)

  @app.route('/', methods=['GET'])
  def index():
    return 'Hello World!'

  if __name __ == '__main__':
    app.run(host='127.0.0.1', port=5000)
  ```
- `your-app/requirements.txt`
  ```txt
  flask
  gunicorn
  ```
- `your-app/Dockerfile`
  ```Dockerfile
  # this base image has python setup and ready to go
  FROM python

  # install dependencies
  COPY requirements.txt /app/requirements.txt
  RUN pip install -r /app/requirements.txt

  # add source to app
  COPY . /app

  # the port your app uses -- this is essential for dokku deployment
  EXPOSE 5000

  # what to do when the container starts
  CMD gunicorn --bind 0.0.0.0:5000 app:app
  ```
