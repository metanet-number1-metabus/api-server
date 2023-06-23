sudo docker-compose down;
yes | sudo docker system prune;
yes | sudo docker image prune;
sudo docker build --no-cache -t bus-api . && sudo docker-compose up -d
sleep 3
sudo docker ps -a