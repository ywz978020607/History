

	server {
		listen 80 default_server;
		listen [::]:80 default_server;
	
	root /var/www/html;
	
	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html Login.html;
	
	server_name _;
	
	location / {
	            autoindex on;
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ =404;
	}
	
	location  /f46059/ {
	    proxy_pass http://localhost:8001/;
	    proxy_redirect  off;
	    proxy_set_header Host $host;
	    proxy_set_header X-Real-IP $remote_addr;
	    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	
	    }
	
	location ~ ^/webhome {
	    #跳转
	    rewrite ^/webhome  http://$http_host/F46059/django1/web/templatesweball/Login.html redirect;
	    
	    }
	
	}
