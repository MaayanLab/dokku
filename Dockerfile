FROM python as builder
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
RUN jupyter-book build /app/

FROM nginx
COPY --from=builder /app/_build/html /usr/share/nginx/html/