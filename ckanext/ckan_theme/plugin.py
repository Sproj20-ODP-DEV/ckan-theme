import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.helpers import url_for

import requests
import json


def most_popular_datasets():
    '''
    A function to return top 4 datasets based on most views
    '''

    try:
        url = url_for('api.action', ver=3, logic_function='package_search',
                      _external=True, sort='views_recent desc', rows=4)
        response = requests.get(url)

        assert response.status_code == 200
    except:
        raise Exception("API endpoint did not respond correctly")

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
        return {'most_popular_datasets': most_popular_datasets}
