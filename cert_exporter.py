#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Domain/SSL Cert expire time check Exporter v1.0

__author__ = 'roy luo <358750776@qq.com>'

from prometheus_client import start_http_server, Gauge
import datetime
import sys
import time
import ssl
import OpenSSL
import getopt
import configparser


# define default args
interval_time = 60
server_port = 9602
host_file = '/config/host.ini'


# Create metrics object
EXPIRE_DAY = Gauge('EXPIRE_DAY','remaining days of the host certificate.', ['target', 'expiry_date', 'ssltype'])
usage = '''Check host/domain SSL Certificate Expire time
Usage: cert_exporter.py -i <host> -p <port> -f <host.ini>
help:
    -i,--interval       grab interval time(default:60 seconds)
    -p,--port           exporter listen port(default:9602)
    -f,--file           hosts list config use ini format(default:/config/host.ini)
    -h,--help           Usage help'''


if sys.argv[1:]:
    opts, args = getopt.getopt(sys.argv[1:], 'hi:p:f:', ['help', 'interval=', 'port=', 'file='])
    for opt, arg in opts:
        if opt in ('-i', '--interval'):
            interval_time = int(arg)
        elif opt in ('-p', '--port'):
            server_port = int(arg)
        elif opt in ('-f', '--file'):
            host_file = arg
        else:
            print(usage)
            exit()


def get_expire(host, port, ssltype):
    cert = ssl.get_server_certificate((host, port), ssl_version=ssl.PROTOCOL_TLSv1)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    expiry_date =x509.get_notAfter().decode()
    expire_format = datetime.datetime.strptime(expiry_date, r'%Y%m%d%H%M%SZ')
    remaining = (expire_format - datetime.datetime.utcnow()).days
    EXPIRE_DAY.labels("%s:%s" % (host, port), expire_format, ssltype).set(remaining)
    

class MyParse(configparser.ConfigParser):
    def as_dict(self):
        '''
        Change the instance of configparser.ConfigParser().read() to dict
        '''
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
        return d


# metrics grab function
def get_metric(conf_file):
    con = MyParse()
    con.read(conf_file, encoding='utf-8')
    conf_dict = con.as_dict()
    for section in conf_dict.keys():
        host = conf_dict[section]['host']
        port = conf_dict[section]['port']
        if conf_dict[section]['ssltype']:
            ssltype = conf_dict[section]['ssltype']
        else:
            ssltype = 'domain'
        try:
            get_expire(host, port, ssltype)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(server_port)
    # Generate some requests.
    while True:
        try:
            get_metric(host_file)
        except Exception as e:
            print(e)
        time.sleep(interval_time)
