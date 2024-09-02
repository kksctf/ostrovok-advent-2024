FROM perl:5.32

WORKDIR /usr/src/app

RUN cpan Mojolicious Crypt::DES Digest::MD5 Crypt::JWT Crypt::PRNG
COPY . .

CMD ["morbo", "app.pl", "-m", "production", "-l", "http://*:5000"]