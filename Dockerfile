FROM ubuntu

RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    git

RUN mkdir -p wordle_solver \
    && git clone https://github.com/angelicalola-danhaive/Wordle.git wordle_solver/

WORKDIR /wordle_solver

RUN pip install -r requirements.txt

