# qSense

*qsense* is a python library and command line tool for QLIK QlikSense. It contains some useful functions for administrators/developers of QLiksense

It is built on top of the python libraries [qsAPI](https://github.com/rafael-sanz/qsAPI) and [pyqlikengine](https://github.com/qliknln/pyqlikengine)

# Installation

pip install qsense

# Usage

```bash
NAME
	qsense - qsense is a python library and command line tool for Qliksense administrators

SYNOPSIS
	qsense COMMAND

DESCRIPTION
	qsense is a python library and command line tool for Qliksense administrators

COMMANDS
	COMMAND is one of the following:

	 add_entity
	   add a new entity (user, stream, dataconnection,...)

	 deallocate_analyzer_licenses_for_professionals
	   Deallocate analyzer license fom users with a professional license

	 deallocate_unused_analyzer_licenses
	   Deallocate analyzer license not used for N days

	 delete_removed_exernally_users
	   Delete users that were removed externally (from active directory?)

	 delete_user_session
	   delete user session

	 entity
	   Get a specific entity by ID or entity list or count

	 export_apps
	   Export (published or passing any other filter) applications to qvd files

	 get
	   generic get http from Qlik (service can be qrs or qps)

	 get_app_connections
	   Extract the connections from an app

	 get_app_dataconnections
	   Extract the dataconnections found in the app script

	 get_app_script
	   Extract the ETL script from an app

	 healthcheck
	   Get a specific entity by ID or entity list or count

	 old_apps
	   Find old apps using 'modified_date' and 'last_reload_time' filters: then you can export them or delete or notify via email the owners

	 open_doc
	   Load an app in memory, useful for preloading an app / cacha warmer

	 post
	   NOT TESTED: generic post http to Qlik (service can be qrs or qps)

	 update_custom_property_with_users_list
	   update the values of a custom property with the list of all qliksense users

	 update_entity
	   update an entity (user, stream, dataconnection,...)

	 user_sessions
	   user sessions

	 users
	   Get users with groups

	 users_with_unpublished_apps
	   Find users with too many unpublished apps
```

Look at the source file qsense/command_line.py for details

# Examples

## Changing all data connections after a file server migration

```bash
JSONFILE=ds-shares.json
rm $JSONFILE

qsense get_entity qlikserver.redaelli.org client.pem dataconnection --filter "connectionstring sw '\\\\\\\amzn'" | jq '.' > $JSONFILE

sed  -e 's/amznfsx94rgsb1e/amznfsxe9chyjel/g' ${JSONFILE} > new-${JSONFILE}

qsense update_entity qlikserver.redaelli.org client.pem dataconnection new-${JSONFILE}
```
