#!/usr/bin/env bash

rm -f *.json
for i in *.index; do
    scrapy crawl domains -s DOMAIN_LIST=$i -o ${i/%index/json}
done
