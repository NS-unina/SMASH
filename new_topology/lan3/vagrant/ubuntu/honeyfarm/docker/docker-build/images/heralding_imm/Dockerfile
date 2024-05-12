FROM python:3.8-slim-buster as base

COPY . .
RUN apt-get update \
    && apt-get install -y libpq-dev gcc libssl-dev \
    && apt-get clean \
    && pip install --user --no-cache-dir -r requirements.txt
    
# Installa una versione più recente di OpenSSL

RUN python setup.py install --user

FROM python:3.8-slim-buster
COPY --from=base /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

CMD ["heralding"]
EXPOSE 21 22 23 25 80 110 143 443 465 993 995 1080 2222 3306 3389 5432 5900
