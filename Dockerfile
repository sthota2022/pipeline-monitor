FROM python:3.7


#install os modules
RUN apt update -y && \
    apt install telnet -y && \
    apt install cron -y && \
    apt install vim -y && \
    rm -rf /var/lib/apt/lists/*


#copy source code
RUN mkdir /scripts_dir

COPY . /scripts_dir

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip3 install -r /scripts_dir/requirements.txt

RUN echo "* * * * * /bin/foo.sh" >> /var/spool/cron/crontabs/root
RUN echo "*/1 * * * * /scripts_dir/monitor_jobs.sh 1>/tmp/monitor_jobs.out 2>&1" >> /var/spool/cron/crontabs/root
ENTRYPOINT ["./scripts_dir/start_cron.sh" ]
