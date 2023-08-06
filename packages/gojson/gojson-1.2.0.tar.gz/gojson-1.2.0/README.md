# gojson

A python client for https://db.neelr.dev/

## Usage

    # import library
    from gojson import Client
    
    # initialise client
    c = Client("521726728521c3df546d8ad699750d78")
    
    # add data
    c.store({'hello':'world'})

    # retrieve data
    c.retrieve()
    
    # delete data
    c.delete()

*see gojson/\_\_init__.py for more it's literally 19 lines*
