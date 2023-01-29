# -*- coding: utf-8 -*-

# Copyright (c) 2022, Harry van der Wolf. all rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.

# This file contains some variables/constants we want to keep out of our main program
# When wanting to download a sqlite3 database we want to have content-type/mime-type and chanrset
# https://some_webserver/Some_sqlite3.db    => application/x-sqlite3; charset=binary
# url = 'https://some_webserver'
# headers = {'Content-Type': 'application/x-sqlite3'}
# response = requests.get(url, headers=headers)

sqlite3_DB_file = "/home/hvdwolf/media/Public/p1meter/p1meter_data.db"
#sqlite3_DB_file = "./p1meter_data.db"
