# qSense

*qsense* is a python library and command line tool for QLIK QlikSense. It contains some useful functions for administrators/developers of QLiksense

It uses the python library [qsAPI](https://github.com/rafael-sanz/qsAPI) for connecting to the QLiksense Repository APIs

# Installation

pip install qsense

# Usage

Look at the file qsense/command_line.py for details

```
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

	 app_get_script
	   Extract the ETL script from an app

	 deallocate_analyzer_licenses_for_professionals
	   Deallocate analyzer license fom users with a professional license

	 deallocate_unused_analyzer_licenses
	   Deallocate analyzer license not used for N days

	 delete_removed_exernally_users
	   Delete users that were removed externally (from active directory?)

	 export_apps
	   Export (published or passing any other filter) applications to qvd files

	 export_users
	   Export users and his/her groups

	 find_app_dataconnections
	   Extract the dataconnections an app

	 find_old_apps
	   Find old apps using 'modified_date' and 'last_reload_time' filters: then you can export them or delete or notify via email the owners

	 find_users_with_unpublished_apps
	   Find users with too many unpublished apps

	 get
	   generic get http from Qlik (qrs, qps,..)

	 get_entity
	   Get a specific entity by ID or entity list or count

	 healthcheck
	   Get a specific entity by ID or entity list or count

	 open_doc
	   load the app in memory

	 update_custom_property_with_users_list
	   update the value of a custom property with the list of all qliksense users

	 update_entity
	   update an entity (user, stream, dataconnection,...)
```
