# Microservice / API Blueprint

Work In Progress...

 - [Documentation](docs/index.md)



### Run devserver

    media-preflight-api runserver 0.0.0.0:8080



### Run as uWSGI Service

    uwsgi --http :8080 --module app.wsgi --virtualenv ~/srv/media-preflight-api



### Create Service/API Account

    ./manage.py api_extra_cli create_service_user -e <email-address> # optional --token/-t




## Install Liquidsoap

### OSX / OPAM

#### Install OPAM with Homebreew

    brew install opam
    opam init
    
    # NOTE! restart shell or
    source ~/.ocamlinit
    
#### Install OPAM Packages

    opam install taglib mad lame vorbis cry
    
    
    
#### Checkout & Build Liquidsoap


    git clone https://github.com/savonet/liquidsoap.git
    cd liquidsoap
    git checkout tags/1.3.1
    git submodule init
    git submodule update
    
    opam pin add liquidsoap .
