# PurgeDB
This application is a tool to purge the MySQL database.
It can be used with crontab to purging automatically.

## Installing
Download the source code and run below command :

  ``` shell
  python setup.py install
  ```
  
or 

  ```shell
  pip install .
  ```
 
## Running

 syntax:
    purgedb <config file>
    
i.e:

  ```shell 
  purgedb /root/config.json
  ```

## Config file

Config file is a json format file same as the sample.json
