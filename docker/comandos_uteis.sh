#Lista containers com filtro
docker container ls -f 'status=exited' -f 'status=dead' | awk '{print $4 " " $5}' | grep months

#Remove imagens com status dangling
docker rmi $(docker images -f dangling=true -q)