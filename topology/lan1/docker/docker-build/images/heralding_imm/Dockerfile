FROM python:3.8-slim-buster as base

# Aggiorna il sistema e installa le dipendenze
RUN apt-get update \
    && apt-get install -y libpq-dev gcc libssl-dev \
    && apt-get clean \
    && pip install --user --no-cache-dir -r requirements.txt

# Installa una versione più recente di OpenSSL
RUN apt-get install -y libssl1.1

COPY . .
RUN python setup.py install --user

FROM python:3.8-slim-stretch

# Copia solo i file necessari dalla build precedente
COPY --from=base /root/.local /root/.local
COPY --from=base /usr/lib/x86_64-linux-gnu/libssl.so.1.1 /usr/lib/x86_64-linux-gnu/

ENV PATH=/root/.local/bin:$PATH

CMD ["heralding"]
EXPOSE 21 22 23 25 80 110 143 443 465 993 995 1080 2222 3306 3389 5432 5900
