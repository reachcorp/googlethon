#!/usr/bin/env bash
rm -rf ./docker/context/dockerdist/*
mkdir -p ./docker/context/dockerdist/
cp -Rf ./googlethon.iml ./docker/context/dockerdist/
cp -Rf ./googlethon.py ./docker/context/dockerdist/
cp -Rf ./Search.py ./docker/context/dockerdist/
cp -Rf ./SearchFactory.py ./docker/context/dockerdist/
cp -Rf ./SearchImage.py ./docker/context/dockerdist/
cp -Rf ./SearchNews.py ./docker/context/dockerdist/
cp -Rf ./SearchUrl.py ./docker/context/dockerdist/
cp -Rf ./entrypoint.sh ./docker/context/dockerdist/
cp -Rf ./requirements.txt ./docker/context/dockerdist/
cp -Rf ./.google-cookie ./docker/context/dockerdist/

docker-compose -f ./docker/googlethon.yml build
