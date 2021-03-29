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

import logging
import qsAPI


def update_custom_property_with_users_list(
    qrs, custom_property_name, user_directory, dryrun=True, threshold=100
):
    """Update a custom property (usually UserAccess) with the list of Qliksense users. There is a threshold,
    just to be sure that at least a fixes nunber of user should be found before updating teh custom property
    """
    result = qrs.driver.get(
        "/qrs/custompropertydefinition/full",
        {"filter": "name eq '{name}'".format(name=custom_property_name)},
    ).json()
    assert len(result) == 1
    user_access = result[0]
    logging.debug(
        "Found custom property with id="
        + user_access["id"]
        + " and name="
        + user_access["name"]
    )
    logging.info("extracting all qliksense users...")
    users = qrs.UserGet(
        pFilter="userDirectory eq '{directory}' and removedExternally eq False".format(
            directory=user_directory
        )
    )
    logging.info("Found {tot} users".format(tot=len(users)))
    if len(users) < check_count:
        logging.warning(
            "The custom poperty will not be updated: too few users, the threshold is {threshold}".format(
                threshold=threshold
            )
        )
        return
    names = list(map(lambda u: u["userId"], users))

    user_access["choiceValues"] = names
    if not dryrun:
        return qrs.driver.put(
            "/qrs/CustomPropertyDefinition/{id}".format(id=user_access["id"]),
            data=user_access,
        )
