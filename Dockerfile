FROM python:3.8-slim

# Uncomment this to compile and render the old frontend
# COPY --from=neuralet/smart-social-distancing:latest-frontend /frontend/build /srv/frontend

COPY requirements.txt /web-socket-example/
WORKDIR /web-socket-example

RUN python3 -m pip install --upgrade pip setuptools==41.0.0 && pip install -r requirements.txt
COPY web-socket-example/ /web-socket-example

CMD ["python3", "web.py"]