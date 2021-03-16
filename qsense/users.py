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
import re
import logging

def delete_removed_exernally_users(qrs, user_directory, dryrun=True):
        users = qrs.UserGet(pFilter="userDirectory eq '%s' and removedExternally eq True" % user_directory)
        logging.warning("Users to be deleted: %s" % len(users))
        for u in users:
              logging.warning("User to be deleted: %s" % u["name"])
              if not dryrun:
                    qrs.UserDelete(u['id'])

def export_users_and_groups(qrs, pFilter="removedExternally ne True", pUserID="full", groupFilter="^QLIKSENSE_", userAttribute="name", sep="\t"):
    users = qrs.UserGet(pFilter=pFilter, pUserID=pUserID)
    for u in users:
        if "attributes" in u.keys():
            for a in u["attributes"]:
                groupname = a["attributeValue"]
                if re.match(groupFilter, groupname, re.IGNORECASE):
                    print("{name}{sep}{groupname}\n".format(name=u[userAttribute],
                                                              groupname=groupname,
                                                              sep=sep))


def user_sessions(hosts, certificate, usergroup, userid, vproxies=""):
    for server in hosts.split(","):
        for vproxy in vproxies.split(","):
            qps=qsAPI.QPS(proxy=server, certificate=certificate)
            print(server + " : " + vproxy)
            print(qps.GetUser(usergroup, user).json())
