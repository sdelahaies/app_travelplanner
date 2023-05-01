# to build
# docker image build . -t app-travelplanner:latest

# to run
# docker run -p 8050:8050 app-travelplanner

# to push todockerhub
#docker login --username usernam
#docker tag app-travelplanner:latest sdelahaies/app-travelplanner:latest
#docker push sdelahaies/app-travelplanner:latest

# to run in vm
# docker pull ...

# and go to 


FROM python:3.10-slim-bullseye
WORKDIR /app-travelplanner

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

COPY ./ ./

EXPOSE 8050

RUN pip3 install -r requirements.txt

CMD ["python3", "./app.py"]