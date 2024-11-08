# Checkers
    An online Checkers game that utilizes AWS for different parts of it. 
    
# Contributors

* Jeffery Eisenhardt - eisenhardtj
* Trevor Gray - trevor-gray17
* Brandon Yang - CloudUki
* Nathaniel Hajel - nateh17

# Manual Deployment

You **must** first create a security group that allows ssh, http, and an inbound rule with the port 8080

Then you can create your EC2 instance, selecting that security group you just made in the "Select existing security group"

Before you click "Launch instance", expand the "Advanced details" tab and copy in the contents from "deploy.sh" in the repo
