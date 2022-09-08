FROM python:3.10.6-slim-bullseye

RUN useradd -m pythonuser

RUN groupadd pythongroup

WORKDIR /app

COPY . .

RUN chown -R pythonuser.pythongroup /app

USER pythonuser

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5205

CMD [ "python", "./main.py" ]