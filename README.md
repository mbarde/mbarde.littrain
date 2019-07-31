# mbarde.littrain

## Usage

### Learn new books:
- Upload EPub file
- Call view `read-epub` on EPub file



Installation
------------

Install `mbarde.littrain` by adding it to your buildout:

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

Set up API
------------

Install `plone.retapi`

To fix CORS add following to buildout configuration (see https://github.com/plone/volto/blob/master/api/base.cfg#L24):

```
zcml-additional =
    <configure xmlns="http://namespaces.zope.org/zope"
               xmlns:plone="http://namespaces.plone.org/plone">
    <plone:CORSPolicy
      allow_origin="http://localhost:8081,http://127.0.0.1:8081"
      allow_methods="DELETE,GET,OPTIONS,PATCH,POST,PUT"
      allow_credentials="true"
      expose_headers="Content-Length,X-My-Header"
      allow_headers="Accept,Authorization,Content-Type,X-Custom-Header,Origin"
      max_age="3600"
      />
    </configure>
```

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
