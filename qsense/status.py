# Copyright (c) 2021 Matteo Redaelli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
