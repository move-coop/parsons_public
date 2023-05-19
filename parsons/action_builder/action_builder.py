import json
from parsons import Table
from parsons.utilities import check_env
from parsons.utilities.api_connector import APIConnector
import logging

API_URL = 'https://{subdomain}.actionbuilder.org/api/rest/v1'

class ActionBuilder(object):
    """
    `Args:`
        api_token: str
            The OSDI API token
        subdomain: str
            The part of the UI URL preceding '.actionbuilder.org'
        campaign: str
            Optional. The 36-character "interact ID" of the campaign whose data is to be retrieved
            or edited. Can also be supplied in individual methods in case multiple campaigns need
            to be referenced.
    """
    
    def __init__(self, api_token=None, subdomain=None, campaign=None):
        self.api_token = check_env.check('ACTION_BUILDER_API_TOKEN', api_token)
        self.headers = {
            "Content-Type": "application/json",
            "OSDI-API-Token": self.api_token
        }
        self.api_url = API_URL.format(subdomain=subdomain)
        self.api = APIConnector(self.api_url, headers=self.headers)
        self.campaign = campaign
        
    def _campaign_check(self, campaign):
        final_campaign = campaign or self.campaign            
        if not final_campaign:
            raise ValueError('No campaign provided!')
            
        return final_campaign
    
    def _get_page(self, campaign, object_name, page, per_page=25, filter=None):
        # returns data from one page of results
        if per_page > 25:
            per_page = 25
            logger.info("Action Builder's API will not return more than 25 entries per page. \
            Changing per_page parameter to 25.")
        params = {
            "page": page,
            "per_page": per_page,
            "filter": filter
        }
        
        campaign = self._campaign_check(campaign)
        url = f'campaigns/{campaign}/{object_name}'
        
        return self.api.get_request(url=url, params=params)
    
    def _get_entry_list(self, campaign, object_name, limit=None, per_page=25, filter=None):
        # returns a list of entries for a given object, such as people, tags, or actions
        # Filter can only be applied to people, petitions, events, forms, fundraising_pages,
        # event_campaigns, campaigns, advocacy_campaigns, signatures, attendances, submissions,
        # donations and outreaches.
        # See Action Builder API docs for more info: https://www.actionbuilder.org/docs/v1/index.html
        count = 0
        page = 1
        return_list = []
        while True:
            response = self._get_page(campaign, object_name, page, per_page, filter=filter)
            page = page + 1
            response_list = response.get('_embedded', {}).get(f"osdi:{object_name}")
            if not response_list:
                return Table(return_list)
            return_list.extend(response_list)
            count = count + len(response_list)
            if limit:
                if count >= limit:
                    return Table(return_list[0:limit])
    
    def get_campaign_tags(self, campaign=None, limit=None, per_page=25, filter=None):
        """
        Retrieve all tags (i.e. custom field values) within provided limit and filters
        `Args:`
            campaign: str
                Optional. The 36-character "interact ID" of the campaign whose data is to be
                retrieved or edited. Not necessary if supplied when instantiating the class.
            limit: int
                The number of entries to return. When None, returns all entries.
            per_page: int
                The number of entries per page to return. 25 maximum and default.
            filter
                The OData query for filtering results. E.g. "modified_date gt '2014-03-25'".
                When None, no filter is applied.
        `Returns:`
            Parsons Table of full set of tags available in Action Builder.
        """
        
        return self._get_entry_list(campaign, 'tags', limit=limit, per_page=per_page, filter=filter)
    
    def get_tag_by_name(self, tag_name, campaign=None):
        """
        Convenience method to retrieve data on a single tag by its name/value
        `Args:`
            tag_name: str
                The value of the tag to search for.
            campaign: str
                Optional. The 36-character "interact ID" of the campaign whose data is to be
                retrieved or edited. Not necessary if supplied when instantiating the class.
        `Returns:`
            Parsons Table of data found on tag in Action Builder from searching by name.
        """
        
        filter = f"name eq '{tag_name}'"
        
        return self.get_campaign_tags(campaign=campaign, filter=filter)
    
    def insert_new_tag(self, tag_name, tag_field, tag_section, campaign=None):
        """
        Load a new tag value into Action Builder. Required before applying the value to any entity
        records.
        `Args:`
            tag_name: str
                The name of the new tag, i.e. the custom field value.
            tag_field: str
                The name of the tag category, i.e. the custom field name.
            tag_section: str
                The name of the tag section, i.e. the custom field group name.
            campaign: str
                Optional. The 36-character "interact ID" of the campaign whose data is to be
                retrieved or edited. Not necessary if supplied when instantiating the class.
        `Returns:`
            Dict containing Action Builder tag data.
        """
        
        campaign = self._campaign_check(campaign)
        url = f'campaigns/{campaign}/tags'
        
        data = {
            "name": tag_name,
            "action_builder:field": tag_field,
            "action_builder:section": tag_section
        }
        
        return self.api.post_request(url=url, data=json.dumps(data))
    
    def upsert_entity(self, entity_type=None, identifiers=None, data=None, campaign=None):
        """
        Load or update an entity record in Action Builder based on whether any identifiers are
        passed.
        `Args:`
            entity_type: str
                The name of the record type being inserted. Required if identifiers are not
                provided.
            identifiers: list
                The list of strings of unique identifiers for a record being updated. ID strings
                will need to begin with the origin system, followed by a colon, e.g.
                `action_builder:abc123-...`.
            data: dict
                The details to include on the record being upserted, to be included as the value
                of the `person` key. See
                [documentation for the Person Signup Helper](https://www.actionbuilder.org/docs/v1/person_signup_helper.html#post)
                for examples, and
                [the Person endpoint](https://www.actionbuilder.org/docs/v1/people.html#field-names)
                for full entity object composition.
            campaign: str
                Optional. The 36-character "interact ID" of the campaign whose data is to be
                retrieved or edited. Not necessary if supplied when instantiating the class.
        `Returns:`
            Dict containing Action Builder entity data.
        """ # noqa: E501
        
        if {entity_type, identifiers} == {None}:
            error_msg = 'Must provide either entity_type (to insert a new record) '
            error_msg += 'or identifiers (to update an existing record)'
            raise ValueError(error_msg)
            
        if not isinstance(data, dict):
            data = {}
            
        name_check = [key for key in data.get('person', {}) if key in ('name', 'given_name')]
        if identifiers is None and not name_check:
            raise ValueError('Must provide name or given name if inserting new record')
            
        campaign = self._campaign_check(campaign)
            
        url = f'campaigns/{campaign}/people'
            
        if 'person' not in data:
            data['person'] = {}
            
        if identifiers:
            if isinstance(identifiers, str):
                identifiers = [identifiers]
            identifiers = [f'action_builder:{x}' if ':' not in x else x for x in identifiers]
            data['person']['identifiers'] = identifiers
        
        if entity_type:
            data['person']['action_builder:entity_type'] = entity_type

        return self.api.post_request(url=url, data=json.dumps(data))
    
    def add_tags_to_record(self, identifiers, tag_name, tag_field, tag_section, campaign=None):
        """
        Add a tag (i.e. custom field value) to an existing entity record in Action Builder. The
        tag, along with its category/field and section/group, must already exist unless it is a
        date field.
        `Args:`
            identifiers: list
                The list of strings of unique identifiers for a record being updated. ID strings
                will need to begin with the origin system, followed by a colon, e.g.
                `action_builder:abc123-...`.
            tag_name: str
                The name of the new tag, i.e. the custom field value.
            tag_field: str
                The name of the tag category, i.e. the custom field name.
            tag_section: str
                The name of the tag section, i.e. the custom field group name.
            campaign: str
                Optional. The 36-character "interact ID" of the campaign whose data is to be
                retrieved or edited. Not necessary if supplied when instantiating the class.
        `Returns:`
            Dict containing Action Builder entity data of the entity being tagged.
        """
        
        # Ensure all tag args are lists
        tag_name = tag_name if isinstance(tag_name, list) else [tag_name]
        tag_field = tag_field if isinstance(tag_field, list) else [tag_field]
        tag_section = tag_section if isinstance(tag_section, list) else [tag_section]
        
        # Use lists of tuples to identify length ordering
        lengths = []
        lengths.append(('name', len(tag_name)))
        lengths.append(('field', len(tag_field)))
        lengths.append(('section', len(tag_section)))

        ordered_lengths = sorted(lengths, key=lambda x: x[1], reverse=True)
        sorted_keys = [x[0] for x in ordered_lengths]
        
        # Raise an error if there are fewer specific items provided than generic
        if sorted_keys[0] != 'name':
            raise ValueError('Not enough tag_names provided for tag_fields or tag_sections')
            
        if sorted_keys[1] != 'field':
            raise ValueError('Not enough tag_fields provided for tag_sections')
            
        # Construct tag data
        tag_data = [{
            "action_builder:name": x,
            "action_builder:field": tag_field[min(i, len(tag_field) - 1)],
            "action_builder:section": tag_section[min(i, len(tag_section) - 1)],
        } for i, x in enumerate(tag_name)]
                       
        data = {"add_tags": tag_data}
                       
        return self.upsert_entity(identifiers=identifiers, data=data, campaign=campaign)
    
    def upsert_connection(self, identifiers, tag_data=None, campaign=None):
        """
        Load or update a connection record in Action Builder between two existing entity records.
        Only one connection record is allowed per pair of entities, so if the connection already
        exists, this method will update, but will otherwise create a new connection record.
        `Args:`
            identifiers: list
                The list of strings of unique identifiers for records being connected. ID strings
                will need to begin with the origin system, followed by a colon, e.g.
                `action_builder:abc123-...`. Requires exactly two identifiers.
            tag_data: list
                List of dicts of tags to be added to the connection record (i.e. Connection Info).
                See [documentation on Connection Helper](https://www.actionbuilder.org/docs/v1/connection_helper.html#post)
                for examples.
            campaign: str
                Optional. The 36-character "interact ID" of the campaign whose data is to be
                retrieved or edited. Not necessary if supplied when instantiating the class.
        `Returns:`
            Dict containing Action Builder connection data.
        """ # noqa: E501
        
        if not isinstance(identifiers, list):
            raise ValueError('Must provide identifiers as a list')
            
        if len(identifiers) != 2:
            raise ValueError('Most provide exactly two identifiers')
            
        campaign = self._campaign_check(campaign)
        
        url = f'campaigns/{campaign}/people/{identifiers[0]}/connections'
        
        data = {
            "connection": {
                "person_id": identifiers[1]
            }
        }
        
        if tag_data:
            if isinstance(tag_data, dict):
                tag_data = [tag_data]
                
            if not isinstance(tag_data[0], dict):
                raise ValueError('Must provide tag_data as a dict or list of dicts')
                
            data["add_tags"] = tag_data

        return self.api.post_request(url=url, data=json.dumps(data))