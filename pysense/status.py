import qsAPI
import requests

def engine(host, scheme, port, timeout, vproxy="", headers=[]):
    ##  https://help.qlik.com/en-US/sense-developer/February2020/Subsystems/EngineAPI/Content/Sense_EngineAPI/GettingSystemInformation/HealthCheckStatus.htm
    ## TODO authentication
    path="/{vproxy}/engine/healthcheck/".format(vproxy=vproxy)
    url = "{scheme}://{host}:{port}{path}".format(scheme=scheme, host=host, port=port)
    get_and_return_status(url, timeout)

def get_and_return_status(url, timeout):
    r = requests.get(url, timeout=timeout)
    return r.status_code

def hub(url, timeout):
    get_and_return_status(url, timeout)

def proxy(host, scheme, port, timeout):
    ## https://help.qlik.com/en-US/sense-developer/February2020/Subsystems/ProxyServiceAPI/Content/Sense_ProxyServiceAPI/ProxyServiceAPI-Introduction.htm
    path="/qps/user"
    url = "{scheme}://{host}:{port}{path}".format(scheme=scheme, host=host, port=port)
    get_and_return_status(url, timeout)


def repository_service(host, port, certificate):
    ## qps = ...
    "TODO"
