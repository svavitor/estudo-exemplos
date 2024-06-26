

- [Redirecionado  http://  para https://](#redirecionado-http-para-https)
- [Redirecionando non-www para www](#redirecionando-non-www-para-www)
- [Redirecionando uma aplicação executando em outro host para o apache host usando ProxyPass](#redirecionando-uma-aplicação-executando-em-outro-host-para-o-apache-host-usando-proxypass)

---

### Redirecionando https://exemplo.com/subdir para https://exemplo.com/subdir/

```

RewriteEngine On
RewriteRule /subdir$ https://%{HTTP_HOST}/subdir/ [L,R=301]

```

### Automaticamente retry quando conexão não for 200

```

RewriteEngine On
RewriteCond %{ENV:REDIRECT_STATUS} !=200
RewriteCond %{TIMEOUT} >0
RewriteRule ^/(.*)$ http://%{HTTP_HOST}/$1 [P,L]

```

### Redirecionado  http://  para https://

```

RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

```

Redireciona permanentemente (301) para https, esse permanente pode ser removido apagando cache do navegador.

---
### Redirecionando non-www para www

```

RewriteEngine On
RewriteCond %{HTTP_HOST} ^exemplo\.com [NC]
RewriteRule ^(.*)$ http://www.exemplo.com/$1 [L,R=301]

```
[NC] transforma o endereço para case-insensitive, eXEMplo.com seria redirecionado para www.exemplo.com.

### Redirecionando www para non-www

```

RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\.exemplo\.com [NC]
RewriteRule ^(.*)$ https://exemplo.com/$1 [L,R=301]

```

---

### Redirecionando uma aplicação executando em outro host para o apache host usando ProxyPass

```

<VirtualHost *:80>
    ServerName app.webapps.com.br
    ProxyPass / http://meuapp.com:7070/
    ProxyPassReverse / http://meuapp.com:7070/
</VirtualHost>

```

ProxyPass direciona as solicitações para a URL do app e ProxyPassReverse garante que os cabeçalhos HTTP de resposta da aplicação sejam ajustados para serem enviados de volta ao cleinte.

---

### Ignorando URLs no ProxyPass

Ao usar proxypass pode ser necessário ignorar alguma URL, para que ela não seja redirecionada para o HOST da aplicação
```

ProxyPass /esta_no_apache !

```
Este caminho não seria redirecionado para o meuapp.com:7070 por exemplo.



Reinicie com: apachectl graceful ou systemctl restart apache2/httpd
