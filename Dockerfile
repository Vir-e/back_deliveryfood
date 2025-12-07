FROM img-base-back:1.0

USER root

RUN apk add --no-cache build-base libffi-dev \
&& pip install pipenv \
&& apk del build-base libffi-dev \
&& rm -rf /var/cache/apk/*

USER vir

COPY ./Pipfile .

EXPOSE 5000

RUN pipenv install

CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]
