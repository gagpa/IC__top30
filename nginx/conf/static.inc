index index.html;

try_files $uri /index.html;

location ~* \.(?:css|js)$ {
  try_files $uri =404;
  expires 7d;
  add_header Cache-Control "public";
}

location ~ ^.+\..+$ {
  try_files $uri =404;
}

include conf/gzip.inc;
