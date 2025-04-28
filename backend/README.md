# Backend

## nginx example
```bash
cat /etc/nginx/sites-enabled/token-randomizer

server {
    listen		89;

    server_name		_;

    location / {
			proxy_pass http://127.0.0.1:5003/;
    }
}
```