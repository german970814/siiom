Provisioning a new site
-----------------------

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv
* ImageMagick

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg. staging.my-domain.com

## Start job
* see gunicorn.template.conf
* replace SITENAME with, eg. staging.my-domain.com

## Folder structure
Assume we have a user account at /home/username

/home/username/webapps/nginx
└── SITENAME
   ├── database
   ├── source
   ├── static
