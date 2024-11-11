# Checkers
    An online Checkers game that utilizes AWS for different parts of it. 
    
# Contributors

* Jeffery Eisenhardt - eisenhardtj
* Trevor Gray - trevor-gray17
* Brandon Yang - CloudUki
* Nathaniel Hajel - nateh17

# Deployment

You **must** first create a security group that allows ssh, http, and an inbound rule with the port 8080

Then you can create your EC2 instance, selecting that security group you just made in the "Select existing security group"

After the instance is created, you want to clone the repo and inside of ~/Checkers/templates, you want to edit the index.html and replace the s3 bucket names with the name of your bucket

Then sudo `chmod +x deploy.sh` and then run the deploy script with `./deploy.sh`
