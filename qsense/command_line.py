#!/usr/bin/env python3
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

import json
import logging
import fire
import qsAPI
from pyqlikengine.engine import QixEngine
import qsense


def connect_qix_engine(host, certfile, keyfile, ca_certs, user_directory, user_id):
    """connect to the qix engine"""
    user_directory = user_directory
    user_id = user_id
    qixe = QixEngine(
        url=host,
        user_directory=user_directory,
        user_id=user_id,
        ca_certs=ca_certs,
        certfile=certfile,
        keyfile=keyfile,
    )
    return qixe


class Qsense:
    """qsense is a python library and command line tool for Qliksense administrators"""

    def get(self, host, certificate, path, port=4242):
        """generic get http from Qlik (qrs, qps,..)"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate, port=port)
        ## find unpublished apps
        resp = qrs.driver.get(path)
        if resp.ok:
            return json.dumps(resp.json())
        else:
            return resp

    def find_users_with_unpublished_apps(
        self,
        host,
        certificate,
        threshold=100,
    ):
        """Find users with too many unpublished apps"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        filter = "published eq False"
        ## find unpublished apps
        apps = qrs.driver.get(
            "/qrs/app/full",
            {"filter": filter},
        ).json()
        logging.debug("Found %d apps." % len(apps))
        ## extract owner IDs from apps
        users = list(map(lambda a: a["owner"]["name"] + "|" + a["owner"]["id"], apps))

        ## frequency
        users_freq = qsense.utils.count_frequency(users)
        ## filter highest values
        threshold = int(threshold)

        for u, count in users_freq.items():
            u_name = u.split("|")[0]
            u_id = u.split("|")[1]
            if count > threshold:
                logging.info("%s: %d" % (u, count))

    def add_entity(self, host, certificate, entity, filename, newid=False):
        """add a new entity (user, stream, dataconnection,...)"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)

        with open(filename) as f:
            bodies = json.load(f)
        if not bodies:
            logging.error("Cannot read body from filename. Bye")
            return
        if not isinstance(bodies, list):
            logging.error("A list json object was expected. Bye")
            return
        for body in bodies:
            if newid:
                if "id" in body.keys():
                    logging.debug(
                        "Removing the ID {id} from the entity".format(id=body["id"])
                    )
                    del body["id"]
            logging.debug("Adding entity {entity}".format(entity=entity))
            logging.debug(body)
            result = qrs.driver.post("/qrs/{entity}".format(entity=entity), data=body)
            logging.debug(result)
            # logging.debug(result.json())

    def update_entity(self, host, certificate, entity, filename):
        """update an entity (user, stream, dataconnection,...)"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)

        with open(filename) as f:
            bodies = json.load(f)
        if not bodies:
            logging.error("Cannot read body from filename. Bye")
            return
        if not isinstance(bodies, list):
            logging.error("A list json object was expected. Bye")
            return
        for body in bodies:
            id = body["id"]
            logging.debug(
                "Updating resource {entity} with id {id}".format(entity=entity, id=id)
            )
            logging.debug(body)
            result = qrs.driver.put(
                "/qrs/{entity}/{id}".format(entity=entity, id=id), data=body
            )
            logging.debug(result)
            logging.debug(result.json())

    def get_entity(self, host, certificate, entity, id="full", filter=None):
        """Get a specific entity by ID or entity list or count"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        result = qrs.driver.get(
            "/qrs/{entity}/{id}".format(entity=entity, id=id),
            {"filter": filter},
        ).json()
        print(json.dumps(result))

    def healthcheck(self, host, certificate, port=4747):
        """Get a specific entity by ID or entity list or count"""
        qps = qsAPI.QPS(proxy=host, certificate=certificate, port=port)
        result = qps.driver.get("/healthcheck")
        print(json.dumps(result.json()))

    def deallocate_unused_analyzer_licenses(self, host, certificate, days, dryrun=True):
        """Deallocate analyzer license not used for N days"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.license.deallocate_unused_analyzer_licenses(qrs, days, dryrun)

    def deallocate_analyzer_licenses_for_professionals(
        self, host, certificate, dryrun=True
    ):
        """Deallocate analyzer license fom users with a professional license"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.license.deallocate_analyzer_licenses_for_professionals(qrs, dryrun)

    def delete_removed_exernally_users(
        self, host, certificate, user_directory, dryrun=True
    ):
        """Delete users that were removed externally (from active directory?)"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.users.delete_removed_exernally_users(qrs, user_directory, dryrun)

    def export_apps(
        self, host, certificate, target_path, filter="stream.name ne 'None'"
    ):
        """Export (published or passing any other filter) applications to qvd files"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.apps.export_by_filter(qrs, target_path=target_path, pFilter=filter)

    def get_users(self, host, certificate):
        """Get users with groups"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.users.get_users_and_groups(qrs)

    def find_old_apps(
        self,
        host,
        certificate,
        modified_days=1000,
        last_reload_days=1000,
        published=False,
        target_path=".",
        save_meta=True,
        skipdata=True,
        export=False,
        delete=False,
    ):
        """Find old apps using 'modified_date' and 'last_reload_time' filters:
        then you can export them or delete or notify via email the owners"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        return qsense.apps.find_old_apps(
            qrs,
            modified_days,
            last_reload_days,
            published=published,
            target_path=target_path,
            save_meta=save_meta,
            skipdata=skipdata,
            export=export,
            delete=delete,
        )

    def open_doc(
        self,
        host,
        certfile,
        keyfile,
        ca_certs,
        app_id,
        user_directory="internal",
        user_id="sa_repository",
    ):
        """Load an app in memory, useful for preloading an app / cacha warmer"""
        qixe = connect_qix_engine(
            host, certfile, keyfile, ca_certs, user_directory, user_id
        )
        result = qsense.apps.open_doc(qixe, app_id)
        return result

    def get_app_script(
        self,
        host,
        certfile,
        keyfile,
        ca_certs,
        app_id,
        user_directory="internal",
        user_id="sa_repository",
    ):
        """Extract the ETL script from an app"""
        qixe = connect_qix_engine(
            host, certfile, keyfile, ca_certs, user_directory, user_id
        )
        script = qsense.apps.get_script(qixe, app_id)
        return script

    def get_app_dataconnections(
        self,
        host,
        certfile,
        keyfile,
        ca_certs,
        app_id,
        user_directory="internal",
        user_id="sa_repository",
    ):
        """Extract the dataconnections found in the app script"""
        script = self.app_get_script(
            host, certfile, keyfile, ca_certs, app_id, user_directory, user_id
        )
        return qsense.apps.extract_dataconnections_from_text(script)

    def update_custom_property_with_users_list(
        self,
        host,
        certificate,
        custom_property_name,
        user_directory,
        dryrun=True,
        threshold=100,
    ):
        """update the values of a custom property with the list of all qliksense users"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        return qsense.custom_property.update_custom_property_with_users_list(
            qrs, custom_property_name, user_directory, dryrun, threshold
        )


def main():
    """main"""
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(Qsense)


if __name__ == "__main__":
    main()
