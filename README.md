## Introduction
Analyzr is a web-based application to analyze twitter keywords, images and tweet reports.

## How to run



 #### Install python pip, virtualenv and nginx

    sudo apt-get install python-pip virtualenv nginx -y
    
  #### Change directory to project folder 
  

    cd analyzr/   

 
#### Activate virtual environment

    virtualenv myenv
    source myenv/bin/activate


#### Install the dependencies via requirements.txt file and 

    sudo pip install -r requirements.txt
    sudo pip install flask gunicorn

#### To run locally

    gunicorn --bind 0.0.0.0:8000 wsgi:app

#### To run over nginx

##### Follow the following commands
 

    sudo vi /etc/nginx/sites-available/flask

###### Copy this onto the opened file
```
    server {
    listen 80;
    location / {
	    includeproxy_params;
	    proxy_pass http://127.0.0.1:8000
	    }
	 }
```
```
    sudo vi /etc/systemd/system/app.service
```
###### Add the following code
```
    [Unit]
    
    Description=Gunicorn instance to serve cs6030Project
    
    After=network.target
    
      
    
    [Service]
    
    User=ubuntu
    
    Group=www-data
    
    WorkingDirectory=/home/ubuntu/cs6030Project
    
    Environment="PATH=/home/ubuntu/cs6030Project/myenv/bin"
    
    ExecStart=/home/ubuntu/.local/bin/gunicorn -workers 3 --bind unix$
    
      
    
    [Install]
    
    WantedBy=multi-user.target
```
   
   ##### Start and enable our app configuration
   
    sudo systemctl start app
    sudo systemctl enable app

    sudo ln -s /etc/nginx/sites-available/flask /etc/nginx/sites-enabled/flask

    sudo /etc/init.d/nginx restart
    

## Technologies Used

- Bootstrap  
- jQuery  
- Google Charts  
- HTML5 and CSS3
- Flask with gunicorn and NGINX
- EC2
- FireBase
- Simple Storage Service (S3)
- Google FireBase   
- CloudWatch
- Twitter Streaming API
- Google Data Studio  
- Google Cloud Vision
- Kairos Facial Recognition  
- Elastic Load Balancer (ELB)  
- AWS AutoScaling  
- Identity and Access Management (IAM)• CloudFormation  
- Elastic Block Storage (EBS)  
- Google Analytics

### Developer

- Rohit Bandooni
