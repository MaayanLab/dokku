FROM python AS builder
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD ./src /app
RUN jupyter-book toc from-project /app > /app/_toc.yml
RUN jupyter-book build /app/

FROM nginx
COPY --from=builder /app/_build/html /usr/share/nginx/html/