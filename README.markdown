# cf-diff Cloud Formations Diff Tool
### Copyright 2014, Red Hat, Inc.

### What is this?

cf-diff is a utility to compare local vs. remote AWS CloudFormation
templates. I use cf-diff to determine if someone (maybe me) has been
fiddling around or doing things by hand with my CloudFormation managed
stacks before attempting a stack update.

### Installation

```
git clone git@github.com:abutcher/cf-diff.git
cd cf-diff
sudo python setup.py install
```

#### Requires:

* python-boto
* python-difflib
* python-termcolor

### Configuration (`~/.config/cf_diff/config`):

This file contains paths to your CloudFormation templates which
correspond to stack names in the EC2 console. Paths can be directories
for sparse templates or single json files. cf_diff will combine the
templates on disk using their names for sorting.

```
[DEFAULT]
location: ../
access_key: ACCESSKEY
secret_key: SECRETKEY
region: REGION

[NetworkProd]
location: /home/abutcher/rhat/cloudformation/network-aws-core-prod.d/

[NetworkStaging]
location: /home/abutcher/rhat/cloudformation/network-aws-core-stage.d/

[Utility-2b]
location: /home/abutcher/rhat/cloudformation/utility-aws-core-2b.json

[Utility-2a]
location: /home/abutcher/rhat/cloudformation/utility-aws-core-2a.json

[ProdCmsSystems]
location: /home/abutcher/rhat/cloudformation/cms_prod_systems.json
```

### Usage:

In this example, I've removed an ACL to my local template and there is
no diff with the remote template.

```
<abutcher>@(lovecoo)[~/rhat/cloudformation] 17:55:50  (cf-diff) 
$ cf-diff NetworkProd $ACCESS_KEY $SECRET_KEY
--- remote

+++ local

@@ -3889,12 +3889,6 @@

		  "FromPort": "5666",
		  "ToPort": "5666",
		  "CidrIp": "10.0.0.0/8"
-          },
-          {
-            "IpProtocol": "tcp",
-            "FromPort": "8139",
-            "ToPort": "8139",
-            "CidrIp": "10.0.0.0/8"
		}
	  ],
	  "SecurityGroupEgress": [
```
