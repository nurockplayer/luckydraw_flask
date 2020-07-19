FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y apt-utils python3 python3-pip mysql-client python3-dev build-essential libssl-dev libffi-dev zsh git-core\
    && apt-get purge -y --auto-remove

COPY requirements.txt /root/
RUN pip3 install -r /root/requirements.txt

RUN git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh \
    && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc \
    && chsh -s /bin/zsh
