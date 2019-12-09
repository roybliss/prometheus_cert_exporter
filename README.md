# prometheus_cert_exporter

Domain/SSL cert expire time check exporter

### requirement

- python3
- pip install pyopenssl prometheus_client

### usage

./cert_exporter.py --help

```
Usage: cert_exporter.py -i <host> -p <port> -f <host.ini>
help:
    -i,--interval       grab interval time(default:60 seconds)
    -p,--port           exporter listen port(default:9602)
    -f,--file           hosts list config use ini format(default:/config/host.ini)
    -h,--help           Usage help
```

### Domain/SSL host

You need to configure your target domains/hosts in host.ini fist like this below(default path：config/host.ini):

```ini
;example hosts
[example]
host = www.example.com
port = 443
ssltype = domain

[host2]
host = 19.168.1.130
port = 9443
ssltype = sslport
```

- host：Domain/SSL hostname or IP
- port：SSL port
- ssltype：Custom prometheus label for different type you want to set(default："domain")

### metrics

- EXPIRE_DAY: The remaining days of the cert expired

labels：

- expiry_date：The day when the cert expired
- ssltype：'ssltype' you defined in host.ini
- target：domain/ssl host

metrics will show EXPIRE_DAY like this:

```shell
[root@centos01 ~]# curl localhost:9602/metrics
# HELP EXPIRE_DAY remaining days of the host certificate.
# TYPE EXPIRE_DAY gauge
EXPIRE_DAY{expiry_date="2028-12-02 08:06:26",ssltype="domain",target="www.example.com:443"} 3281.0
EXPIRE_DAY{expiry_date="2028-12-02 08:06:26",ssltype="sslport",target="19.168.1.130:9443"} 3281.0
```

### dokcer run

Please build docker image with [Dockerfile](https://github.com/roybliss/prometheus_cert_exporter/blob/master/Dockerfile) first, then run like this：

```shell
docker run -d \
    --name cert_exporter \
    -p 9602:9602 \
    -v /opt/cert_exporter/host.ini:/config/host.ini \
    cert_exporter:1.0
```