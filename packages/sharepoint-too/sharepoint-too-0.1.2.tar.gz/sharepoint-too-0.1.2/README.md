# SharePoint Too
Author:Tim Santor <tsantor@xstudios.agency>

## Overview
This module will handle authentication for your SharePoint Online/O365 site, allowing you to make straightforward HTTP requests from Python. It extends the commonly used Requests module, meaning that returned objects are familliar, easy to work with and well documented. Leverages [requests_ntlm](https://github.com/requests/requests-ntlm) for authentication.

Inspired by [Sharepy](https://github.com/JonathanHolvey/sharepy) which seems to no longer be maintained.

**NOTE:** Currently handles dealing with SharePoint Lists via handy shortcut methods, but you can currently also call `sp.get(url, *args, **kwargs)` and `sp.post(url, *args, **kwargs)` with manually assembled SharePoint REST URLs and it will work.

## Installation
SharePoint Too can be installed from the Python Package Index, PyPI.

    pip install sharepoint-too

## Initiate a SharePoint session

    from sharepoint_too import SharePointSession
    sp = SharePointSession("example.sharepoint.com")

## Make an API call

    r = sp.get_lists()

This will return a Requests `response` object. See the [requests documentation](http://docs.python-requests.org/en/master/) for details. By default, the headers `accept: application/json;odata=verbose` and` content-type: application/json;odata=verbose` are sent with all requests, so API responses will be formatted as JSON where available.

Headers can be added or overridden by supplying a dictionary to the relevant method:

    r = sp.get_lists(headers={"Accept": "application/atom+xml"})

Currently the `post()` method will send a `x-requestdigest` header, allowing modifications to be made to SharePoint objects.

## Other available methods

    sp.get_list_metadata(weblist_url, list_guid=None, list_title=None)
    sp.get_list_entity_type(weblist_url, list_guid=None, list_title=None)
    sp.get_list_items(weblist_url, list_guid=None, list_title=None)
    sp.get_list_item(weblist_url, item_id, list_guid=None, list_title=None)
    sp.add_list_item(weblist_url, payload, list_guid=None, list_title=None)
    sp.update_list_item(weblist_url, item_id, data, list_guid=None, list_title=None)
    sp.upload(weblist_url, item_id, filename, list_guid=None, list_title=None)
    sp.delete_list_item(weblist_url, item_id, list_guid=None, list_title=None)

**NOTE:** Only `list_guid` or `list_title` need to be supplied, not both.

## Tests
Since the tests require a SharePoint account you'll need to supply private values in order to run the tests:

Create a file called `~/sharepoint_too/config.cfg`:

    [default]
    domain=
    user=
    pwd=
    site_url=https://example.sharepoint.com
    weblist_url=https://example.sharepoint.com/_api/web/lists
    list_title=
    list_guid=
    list_item_type=


Now you can run:

    python -m pytest tests/test_sharepoint_too.py

## Documentation
Documentation is available at TODO

## Requirements

- [requests](https://github.com/psf/requests)
- [requests_ntlm](https://github.com/requests/requests-ntlm)

# Issues
If you experience any issues, please create an [issue](https://bitbucket.org/tsantor/sharepoint-too/issues) on Bitbucket.
