FROM php:5.6-fpm  

ENV REFRESHED_AT 2016-01-17
ENV PHPREDIS_VERSION=2.2.7

RUN apt-get update && apt-get install -y libmcrypt-dev  
#RUN docker-php-ext-install phpredis

RUN cd /usr/src/php/ext \
    && curl -q https://codeload.github.com/phpredis/phpredis/tar.gz/$PHPREDIS_VERSION | tar -xz \
    && docker-php-ext-install phpredis-$PHPREDIS_VERSION

#COPY php.ini /usr/local/etc/php/

ADD . /var/www/html

CMD ["php-fpm"]