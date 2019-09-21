"""NGPVAN Code Endpoints"""
import petl
from parsons.etl.table import Table
import logging

logger = logging.getLogger(__name__)


class Codes(object):

    def __init__(self, van_connection):

        self.connection = van_connection

    def get_codes(self, name=None, supported_entities=None, parent_code_id=None,
                  code_type=None):
        """
        Get codes.

        `Args:`
            name : str
                Filter by name of code
            supported_entities : str
                Filter by supported entities
            parent_code_id : str
                Filter by parent code id
            code_type : str
                Filter by code type
        `Returns:`
            Parsons Table
                See :ref:`parsons-table` for output options.
        """

        args = {'name': name,
                'supportedEntities': supported_entities,
                'parentCodeId': parent_code_id,
                'codeType': code_type,
                '$top': 200
                }

        url = self.connection.uri + 'codes'

        c = self.connection.request_paginate(url, args=args)
        logger.debug(c)
        logger.info(f'Found {c.num_rows} codes.')

        return c

    def get_code(self, code_id):
        """
        Get code.

        `Args:`
            code_id : int
                The code id.
        `Returns:`
            Parsons Table
                See :ref:`parsons-table` for output options.
        """

        url = self.connection.uri + 'codes/{}'.format(code_id)

        c = self.connection.request(url)
        logger.debug(c)
        logger.info(f'Found code {code_id}.')

        return c

    def get_code_types(self):
        """
        Get code types.

        `Returns:`
            Parsons Table
                See :ref:`parsons-table` for output options.
        """

        url = self.connection.uri + 'codeTypes'

        ct = Table(petl.fromcolumns([self.connection.request(url, raw=True).json()],
                                    header=['code_type']))
        logger.debug(ct)
        logger.info(f'Found {ct.num_rows} code types.')

        return ct

    def create_code(self, name=None, parent_code_id=None, description=None,
                    code_type='SourceCode', supported_entities=None):
        """
        Create a code

        `Args:`
            name: str
                The name of the code
            parent_code_id: int
                A unique identifier for this Code’s parent
            description: str
                A description for this Code, no longer than 200 characters
                and may be null.
            code_type: str
                Determines whether a Code is a Tag or Source Code. Valid values are ``Tag`` and
                ``SourceCode``. Default is SourceCode.
            supported_entities: list
                A list of dicts that enumerate the searchability and applicability rules of the
                code. You can find supported entities with the :meth:`code_supported_entities`

                .. highlight:: python
                .. code-block:: python

                    [
                        {
                         'name': 'Event',
                         'is_searchable': True,
                         'is_applicable': True
                        }
                        {
                         'name': 'Locations',
                         'start_time': '12-31-2018T13:00:00',
                         'end_time': '12-31-2018T14:00:00'
                        }
                    ]
        """

        url = self.connection.uri + 'codes'

        if supported_entities:

            se = [{'name': s['name'],
                   'isSearchable': s['is_searchable'],
                   'is_applicable': s['is_applicable']} for s in supported_entities]

        post_data = {"parentCodeId": parent_code_id,
                     "name": name,
                     "codeType": code_type,
                     "supportedEntities": se,
                     "description": description}

        c = self.connection.request(url, req_type="POST", post_data=post_data)
        logger.debug(c)
        logger.info(f'Code {c} created')
        return c

    def update_code(self, code_id, name=None, parent_code_id=None, description=None,
                    code_type='SourceCode', supported_entities=None):
        """
        Update a code.

        `Args:`
            code_id: int
                The code id.
            name: str
                The name of the code.
            parent_code_id: int
                A unique identifier for this code’s parent.
            description: str
                A description for this code, no longer than 200 characters.
            code_type: str
                The code type. ``Tag`` and ``SourceCode`` are valid values.
            supported_entities: list
                A list of dicts that enumerate the searchability and applicability rules of the
                code. You can find supported entities with the :meth:`code_supported_entities`

                .. highlight:: python
                .. code-block:: python

                    [
                        {
                         'name': 'Event',
                         'is_searchable': True,
                         'is_applicable': True
                        }
                        {
                         'name': 'Locations',
                         'start_time': '12-31-2018T13:00:00',
                         'end_time': '12-31-2018T14:00:00'
                        }
                    ]
        """

        url = self.connection.uri + 'codes/{}'.format(code_id)

        post_data = {}

        if name:
            post_data['name'] = name
        if parent_code_id:
            post_data['parentCodeId'] = parent_code_id
        if code_type:
            post_data['codeType'] = code_type
        if description:
            post_data['description'] = description

        if supported_entities:

            se = [{'name': s['name'],
                   'isSearchable': s['is_searchable'],
                   'is_applicable': s['is_applicable']} for s in supported_entities]
            post_data['supportedEntities'] = se

        c = self.connection.request(url, req_type="PUT", post_data=post_data)
        logger.debug(c)
        logger.info(f'Code {code_id} updated.')
        return c

    def delete_code(self, code_id):
        """
        Delete a code.

        `Args:`
            code_id: int
                The code id.
        `Returns:`
            ``(204, 'No Content')`` if successful
        """

        url = self.connection.uri + 'codes/{}'.format(code_id)

        logger.info(f'Deleting code {code_id}...')
        c = self.connection.request(url, req_type="DELETE", raw=True)
        logger.info(f'Code {code_id} deleted.')
        return c

    def get_code_supported_entities(self):
        """
        Get code supported entities.

        `Returns:`
            Parsons Table
                See :ref:`parsons-table` for output options.
        """

        url = self.connection.uri + 'codes/supportedEntities'

        logger.info(f'Getting code supported entities...')
        cse = Table(petl.fromcolumns([self.connection.request(url, raw=True).json()],
                                     header=['supported_entities']))
        logger.debug(cse)
        logger.info(f'Found {cse.num_rows} code supported entities.')

        return cse
