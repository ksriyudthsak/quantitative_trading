
# #### jupyter notebook
# run docker
docker build -t trading-jupyter .

# run docker with current path mounted
docker run -p 8888:8888 --name trading-jupyter --rm -itd -v "$(pwd):/mnt" trading-jupyter 

# access docker
docker exec -it <container_id> /bin/bash

# open jupyter notebook
http://localhost:8888


# #### dashboard
# build
docker-compose up -d --build

# rebuild 
docker-compose up -d --remove-orphans --force-recreate --build 

# run
docker-compose exec trading-app zsh -c "python src/app_main.py"

