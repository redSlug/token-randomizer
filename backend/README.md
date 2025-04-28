# Backend

## nginx example
```bash
cat /etc/nginx/sites-enabled/token-randomizer

server {
    server_name		random-backend.dynamicdisplay.xyz;

    location / {
			proxy_pass http://127.0.0.1:5003/;
    }
}
```