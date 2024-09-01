## To start it, you do this


1. method 

  `docker compose up -d` or `docker-compose up -d` 

  ( depends on your docker compose version)

  than open your browser `http://localhost:8501`

2. method 

  `/bin/bash start.sh`  your browser will be open automatically

3. method 

`docker build -t my_streamlit_app .`

`docker run -p 8501:8501 my_streamlit_app`
 

