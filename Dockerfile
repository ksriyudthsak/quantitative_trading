FROM python:3.8

USER root

RUN apt-get -qq -y update && \
    apt-get -qq -y upgrade && \
    apt-get -qq -y install \
        wget \
        curl \
        git \
        make \
        sudo \
	r-base \
        bash-completion && \
    apt-get -y autoclean && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt-get/lists/*
RUN apt-get install -y vim less
RUN apt-get install -y zsh less
RUN sudo apt-get -qq -y install screen

# Create user "docker" with sudo powers
RUN useradd -m docker && \
    usermod -aG sudo docker && \
    usermod -G root docker && \
    echo '%sudo ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers && \
    cp /root/.bashrc /home/docker/ && \
    mkdir /home/docker/data && \
    chown -R --from=root docker /home/docker

SHELL [ "/bin/bash", "-c" ]

EXPOSE 8888

RUN pip install --upgrade --no-cache-dir pip setuptools wheel && \
    pip install --no-cache-dir numpy jupyter && \
    pip install --no-cache-dir matplotlib==3.2
RUN pip install Cython
RUN pip install pandas
RUN pip install plotly==4.14.3
RUN pip install scipy
RUN pip install dash==1.21.0
RUN pip install scikit-learn
RUN pip install pyarrow
RUN pip install fastparquet
RUN pip install statsmodels
RUN pip install psutil

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install
RUN pip install TA-Lib
RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

# Use C.UTF-8 locale to avoid issues with ASCII encoding
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# ENV HOME /home/docker
# Have Jupyter notebooks launch without additional command line options
RUN jupyter notebook --generate-config && \
    sed -i -e "/allow_root/ a c.NotebookApp.allow_root = True" ${HOME}/.jupyter/jupyter_notebook_config.py && \
    sed -i -e "/custom_display_url/ a c.NotebookApp.custom_display_url = \'http://localhost:8888\'" ${HOME}/.jupyter/jupyter_notebook_config.py && \
    sed -i -e "/c.NotebookApp.ip/ a c.NotebookApp.ip = '*'" ${HOME}/.jupyter/jupyter_notebook_config.py && \
    sed -i -e "/open_browser/ a c.NotebookApp.open_browser = False" ${HOME}/.jupyter/jupyter_notebook_config.py && \
    sed -i -e "/c.NotebookApp.token/ a c.NotebookApp.token = ''" ${HOME}/.jupyter/jupyter_notebook_config.py

RUN chown -R --from=root docker ${HOME}

# Install yfinance
RUN pip install yfinance

# Install backtrader
RUN pip install backtrader backtrader_plotting
RUN pip install git+https://github.com/quantopian/pyfolio

# CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=*", "--allow-root"]

EXPOSE 8001
CMD ["bash"]
