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

import re
import logging
import qsAPI
from .systemrule import *


def extract_mail(u):
    """Extract the mail attribute from the user dictionary"""
    logging.debug(f"Extract mail from user {u}")
    if not u:
        logging.error("User is empty")
        return None
    if not "attributes" in u:
        logging.error("User without 'attribute' key")
        return None

    mails = list(filter(lambda a: a["attributeType"] == "Email", u["attributes"]))
    if len(mails) > 0:
        result = mails[0]["attributeValue"]
        logging.debug(result)
        return result
    else:
        logging.error("No mail found for user ")
        return None


def find_mail_from_user_id(qrs, id):
    users = qrs.UserGet(pFilter="id eq %s" % id)
    if len(users) != 1:
        logging.error(f"Cannot find a user with ID={id}")
        mail = None
    else:
        mail = extract_mail(users[0])
    return mail


def delete_removed_exernally_users(qrs, user_directory, dryrun=True):
    users = qrs.UserGet(
        pFilter=f"userDirectory eq '{user_directory}' and removedExternally eq True"
    )
    logging.warning("Users to be deleted: %s" % len(users))
    for u in users:
        logging.warning("User to be deleted: %s" % u["name"])
        if not dryrun:
            qrs.UserDelete(u["id"])


def extract_user_groups(user, groupFilter="^QLIKSENSE_"):
    if "attributes" in user.keys():
        for a in user["attributes"]:
            groupname = a["attributeValue"]
            if re.match(groupFilter, groupname, re.IGNORECASE):
                yield (grouname)


def user_info(qrs, user_id, resources, access):
    users = qrs.UserGet(pFilter=f"userId eq '{user_id}'")
    logging.debug(users)
    if len(users) == 0:
        logging.warning(f"UserId {userid} not found!")
        yield {"Missing userId": userid}
        return

    user = users[0]

    ## user info

    for field in [
        "name",
        "createdDate",
        "inactive",
        "removedExternally",
        "blacklisted",
        "deleteProhibited",
        "roles",
    ]:
        yield {field: user[field]}

    ## License

    param = {"filter": f"user.userId eq '{user_id}'"}
    for typ in ["analyzer", "professional"]:
        lic = qrs.driver.get(f"/qrs/license/{typ}accesstype/count", param=param).json()
        yield {f"{typ} license": True if lic["value"] == 1 else False}

    ## access to resources

    iduser = user["id"]
    for resource in resources:
        resp = accessible_objects(qrs, resource, iduser, access)
        result = list(map(lambda r: r["name"], resp))
        yield {f"{resource} {access} access": result}


def user_sessions(hosts, certificate, usergroup, userid, vproxies=""):
    for server in hosts.split(","):
        for vproxy in vproxies.split(","):
            qps = qsAPI.QPS(proxy=server, certificate=certificate)
            print(f"{server}  : {vproxy}")
            print(qps.GetUser(usergroup, user).json())
