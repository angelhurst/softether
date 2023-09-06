FROM ubuntu:22.04 

RUN apt-get update -y \
    && apt-get install build-essential gnupg2 gcc make -y

WORKDIR /app

# RUN wget  https://github.com/SoftEtherVPN/SoftEtherVPN_Stable/releases/download/v4.39-9772-beta/softether-vpnserver-v4.39-9772-beta-2022.04.26-linux-x64-64bit.tar.gz
COPY softether-vpnserver-v4.39-9772-beta-2022.04.26-linux-x64-64bit.tar.gz /app
RUN  tar -xvzf softether-vpnserver-v4.39-9772-beta-2022.04.26-linux-x64-64bit.tar.gz

WORKDIR  /app/vpnserver
RUN make 

WORKDIR /app
RUN mv vpnserver /usr/local/

WORKDIR  /usr/local/vpnserver/ 
    
RUN  chmod 600 * \
    && chmod 700 vpnserver \
    && chmod 700 vpncmd 

COPY vpnserver  /etc/init.d/

RUN mkdir /var/lock/subsys \
    && chmod 755 /etc/init.d/vpnserver

# RUN /etc/init.d/vpnserver start 

# RUN update-rc.d vpnserver defaults


# CMD ["/etc/init.d/vpnserver", "start"]

FROM softether:2
