import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.helpers import url_for,facets
import ckan.lib.helpers as h
import ckan.plugins as p
from ckan.common import c
import ckan.lib
from ckan.logic import get_action


import requests
import json

def get_orgs():
    '''
    A function to get the list of all the orgs
    '''
    try:
        url = url_for('api.action',ver=3,logic_function='organization_list',_external=True);
        response = requests.get(url)
        
        assert response.status_code == 200
    except:
        raise Exception("No Organizations to show")
    
    return response.json()['result']

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
    #IRoutes
    plugins.implements(plugins.IRoutes, inherit=True)
    #IFacets
    plugins.implements(plugins.IFacets)

    def dataset_facets(self, facets_dict, package_type):
        del facets_dict['groups']
        del facets_dict['license_id']

        return facets_dict
    
    def organization_facets(self,facets_dict, organization_type, package_type):
        return facets_dict


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
        return {
            'most_popular_datasets': most_popular_datasets,
            'get_orgs':get_orgs                
            }
