from requests import request as _request
from parsons.etl.table import Table
import logging
from parsons.utilities import check_env
from parsons.utilities.api_connector import APIConnector

logger = logging.getLogger(__name__)

URI = 'https://api.securevan.com/v4/'


class VANConnector(object):

    def __init__(self, api_key=None, auth_name='default', db=None):

        self.api_key = check_env.check('VAN_API_KEY', api_key)

        if db == 'MyVoters':
            self.db_code = 0
        elif db in ['MyMembers', 'MyCampaign', 'EveryAction']:
            self.db_code = 1
        else:
            raise KeyError('Invalid database type specified. Pick one of:'
                           ' MyVoters, MyCampaign, MyMembers, EveryAction.')

        self.uri = URI
        self.db = db
        self.auth_name = auth_name
        self.auth = (self.auth_name, self.api_key + '|' + str(self.db_code))
        self.api = APIConnector(self.uri, auth=self.auth, data_key='items')

    def get_request(self, endpoint, **kwargs):

        r = self.api.get_request(self.uri + endpoint, **kwargs)
        data = self.api.data_parse(r)

        # Paginate
        while self.api.next_page_check_url(r):
            r = self.api.get_request(r[self.pagination_key], **kwargs)
            data.extend(self.api.data_parse(r))

        return data

    def post_request(self, endpoint, **kwargs):

        return self.api.post_request(self.uri + endpoint, **kwargs)

    def delete_request(self, endpoint, **kwargs):

        return self.api.delete_request(self.uri + endpoint, **kwargs)

    def patch_request(self, endpoint, **kwargs):

        return self.api.patch_request(self.uri + endpoint, **kwargs)

    def put_request(self, endpoint, **kwargs):

        return self.api.put_request(self.uri + endpoint, **kwargs)
