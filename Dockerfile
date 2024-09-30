FROM --platform=linux/amd64 jenkins/inbound-agent:alpine

USER root

WORKDIR /app

RUN apk update && \
    apk add --no-cache \
    python3 \
    py3-pip \
    py3-virtualenv \
    bash \
    sshpass \
    curl \
    iputils \
    netcat-openbsd

RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install ansible

COPY  ping.yaml http.yaml https.yaml inventory hostnames.var check_script.sh ldap.yaml generate_html_report.py /app/

ENV ANSIBLE_HOST_KEY_CHECKING=False

RUN chmod +x check_script.sh

CMD ["/app/check_script.sh"]