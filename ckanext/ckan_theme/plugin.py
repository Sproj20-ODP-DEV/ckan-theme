import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import requests
import json
import socket


def most_popular_datasets():
    '''
    A function to return top 4 datasets based on popularity

    '''

    # Get the ip address
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)

    # Make the HTTP request.
    try:
        url = 'http://' + \
            str(ip_addr) + '/api/3/action/package_search?sort=views_recent+desc&rows=4'
        response = requests.get(url)

        assert response.status_code == 200
    except:
        raise Exception("Sorry, Broken API call")

    # Use the json module to load CKAN's response into a dictionary.
    response_dict = response.json()

    # Check the contents of the response.
    assert response_dict['success'] is True
    results = response_dict['result']['results']

    return results


class Ckan_ThemePlugin(plugins.SingletonPlugin):
    # IConfigurer
    plugins.implements(plugins.IConfigurer)

    # Declare that this plugin will implement ITemplateHelpers.
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'ckan_theme')

    def get_helpers(self):
        '''Register the most_popular_datasets() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'ckan_theme_most_popular_datasets': most_popular_datasets}
