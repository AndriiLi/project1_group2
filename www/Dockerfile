FROM python:3.12

RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    python3-h5py \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir -p /root/.streamlit
COPY ./.streamlit  /root/.streamlit

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]