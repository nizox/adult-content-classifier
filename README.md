Adult Content Classifier
========================

This project has been realized as part of the WEBMIN course at the
Department of Computer and Systems Sciences (DSV) of Stockholm University.

Parts
-----

The crawler directory contains the [Scrapy](http://scrapy.org/) project. 
osbf-lua-2.0.4 is the classification library. The pornfilter/www subdirectory
contains an extract of the server-side API exposing the classifier.
The client program is ready-to-use and requests an already hosted classifier.
