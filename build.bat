del ".\docker\raw\dockerdist\*.py" /s /f /q
xcopy "*.py" ".\docker\raw\dockerdist" /Y /F
xcopy "./entrypoint.sh" "./docker/raw/dockerdist/" /Y /F
xcopy "./requirements.txt" "./docker/raw/" /Y /F

cd docker
docker-compose.exe -f .\googlethon.yml up -d --build
cd ..
