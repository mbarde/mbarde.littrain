.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

===============
mbarde.littrain
===============

Usage
--------

- Install Addon
- Upload EPub
- Call view `read-epub` on EPub file



Installation
------------

Install mbarde.littrain by adding it to your buildout:

    [buildout]

    ...

    eggs =
        mbarde.littrain


and then running ``bin/buildout``

Install language model for spacy:

```
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz
```

(see https://spacy.io/usage/models#download-pip)


Contribute
----------

- Issue Tracker: https://github.com/collective/mbarde.littrain/issues
- Source Code: https://github.com/collective/mbarde.littrain


Development
----------

```
virtualenv --clear -p python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
buildout bootstrap
bin/buildout -n -c buildout.cfg code-analysis:return-status-codes=True code-analysis:flake8-max-line-length=100
```

License
-------

The project is licensed under the GPLv2.
