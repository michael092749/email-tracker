<<<<<<< HEAD
# email-tracker
=======
﻿# Email Tracker

Get notified when your email gets read by using a tracking pixel and a NGINX web server.

## How it works

An email containing a 1x1 tracking pixel is sent in the email. When the receiver opens the email, their browser will send a GET request to our server, which will process this event and send us a text message alert. The tracker.py file is used to send emails and the watcher.py file is used to listen for GET requests on the server.

## How to DIY

### 1. Setup

1. Setup your webserver with Amazon AWS and Nginx as setup [here](https://aws.plainenglish.io/creating-an-ec2-instance-installing-an-nginx-webserver-8b0ab5ba10a9)
   User data to use to setup server installation:

```
#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install nginx1 -y
sudo amazon-linux-extras enable nginx1
sudo systemctl start nginx

```

2. Download this github repo
3. Go to [Google App Passwords](https://myaccount.google.com/apppasswords) to generate an app passwords which will be used to send emails from your Gmail account.
4. Update the credentials in cred.py file with your gmail details
5. Update the main function in tracker.py with the recipent email and the email subject.
6. Update the HTML email body accordingly
7. Save the tracking `pixel.png` and the `watcher.py` file (which monitors for GET requests and sends SMS) on the server

### 2. Server Configuration

1. SSH into server
2. Edit the Nginx config `/etc/nginx/nginx.conf`accordingly. First to accept the query string for processing:
   ```
   http {
   log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
   '"$http_user_agent" "$query_string" "$http_x_forwarded_for"';
   ```
   Then add a new location field in the server and update the alias path to that of your pixel.png :

```
    location /tracking-pixel{
                alias /home/ec2-user/tracker/pixel.png;
                access_log /var/log/nginx/pixel-access.log main;
                default_type "image/png";

                expires -1;
                  add_header 'Cache-Control' 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';
                # Set headers to prevent caching
                add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";
                add_header Pragma "no-cache";
                add_header Expires "0";

                }
    }
```

The headers prevent caching, thus the tracking pixel will always be requested from our server.

3. Save and exit the file. Then, change the user permissions so that the nginx user can access the files, example :

```
sudo chmod +x /home /home/ec2-user /home/ec2-user/tracker

```

4. Test for errors in the config file and restart the nginx server:

```
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Twilio

On the webserver:

1. Make a Twilio account
2. In the server shell, edit env variables with:

```
   export TWILIO_ACCOUNT_SID="YOUR_SID"

   export TWILIO_ACCOUNT_AUTH="YOUR_AUTH"
```

based on your respective SID and AUTH from Twilio

### 4. Server Listener

On the web server:

1. Edit `to` and `from` variables to be your to and from numbers in `watcher.py`.
2. Run `python3 watcher.py` once you have installed the requirements in requirements.txt, to ensure no errors.
3. Run the program in the background to listen for requests, even when the SSH session is closed :

```
nohup python3 watcher.py
```

### 4. Send email

On any device:

1. Fill in credentials in cred.py
2. Change the `LINK` of the tracking pixel to be your server's IP address followed by `\tracking-pixel
3. Edit email subject, HTML body and recipicent variables in `tracker.py`
4. Send the email by running `python3 tracker.py`

### 5. Done!

Now when the receiver opens the email, you'll get a text letting you know that it was opened!
>>>>>>> 254271c (Updated README)
