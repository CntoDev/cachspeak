import json
import logging

import cachetclient.cachet as cachet

COMPONENT_DATA = {'id', 'name', 'status', 'created_at', 'updated_at', 'deleted_at', 'status_name'}
LAST_UPDATE_FIELD = 'updated_at'


class CachetAPI:
    """Provide interface to get Cachet components which status differs from a given list"""

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self._loaded = False
        self._components = []

    @property
    def components(self):
        """Fetch components from Cachet API and remove all fields not contained in COMPONENT_DATA"""
        if not self._loaded:
            request = cachet.Components(endpoint=self.endpoint)
            response = json.loads(request.get())
            components = tuple(response['data'])

            logging.info('retrieved status of %d components from Cachet', len(components))

            for component in components:
                for key in list(component.keys()):
                    if key not in COMPONENT_DATA:
                        del component[key]

            self._components = components
            self._loaded = True

        return self._components

    @staticmethod
    def find_matching_component(component, components_list):
        """Find component in a list by id, picking the last updated if multiple matches, None if nothing match"""
        matches = list(filter(lambda list_comp: list_comp['id'] == component['id'], components_list))
        if not matches:
            return None
        else:
            matches.sort(key=lambda comp: comp[LAST_UPDATE_FIELD], reverse=True)
            return matches[0]


    def updated_components(self, saved_components):
        """Return the components from Cachet that were updated compared to a given list of components"""
        for component in self.components:
            match_component = self.find_matching_component(component=component, components_list=saved_components)
            if not match_component:
                logging.debug('no saved status for component %d, considering its status updated', component['id'])
                yield component
            elif component['status'] != match_component['status']:
                logging.debug('component %d status has changed', component['id'])
                yield component
