# Readme

## Running the script
create virtual env:

source venv/bin/activate

run script:

cd src && py script.py

run jupyter lab:

```
jupyter lab
```

## Santander

- download the .xls file from the website. This is actually an html table so best to rename it to .html and stick it in /data. Add it to the appropriate place

Callout: midata files are not utf-8, and they only allow you to download a 12 month interval ending last month. Most likely this is not what you need

Callout: santander exports are not utf-8

```zsh
file oct.html 
oct.html: HTML document, ISO-8859 text, with very long lines (1540)
```

it is good to specify the charset




## Commitlint
Common types according to commitlint-config-conventional (based on the Angular convention) can be:

    build
    chore
    ci
    docs
    feat
    fix
    perf
    refactor
    revert
    style
    test
