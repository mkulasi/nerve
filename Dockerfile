FROM centos:7

ARG TARGET_FOLDER=/opt/nerve

RUN yum install epel-release -y && \
    yum update -y && \
    yum install -y gcc && \
    yum install -y redis && \
    yum install -y python3 && \
    yum install -y python3-pip && \
    yum install -y python3-devel && \
    yum install -y wget && \
    yum clean all


RUN wget https://nmap.org/dist/nmap-7.80-1.x86_64.rpm
RUN rpm -ivh nmap-7.80-1.x86_64.rpm

RUN mkdir /opt/nerve

ADD bin $TARGET_FOLDER/bin
ADD core $TARGET_FOLDER/core
ADD db $TARGET_FOLDER/db
ADD install $TARGET_FOLDER/install
ADD logs $TARGET_FOLDER/logs
ADD reports $TARGET_FOLDER/reports
ADD rules $TARGET_FOLDER/rules
ADD static $TARGET_FOLDER/static
ADD templates $TARGET_FOLDER/templates
COPY config.py $TARGET_FOLDER
COPY main.py $TARGET_FOLDER
COPY requirements.txt $TARGET_FOLDER
COPY start.sh $TARGET_FOLDER

WORKDIR $TARGET_FOLDER/

RUN pip3 install --user -r requirements.txt
RUN chmod 755 main.py
RUN chmod 755 start.sh
ENTRYPOINT ["/opt/nerve/start.sh"]

EXPOSE 8080/tcp
