import json
import logging
import requests

from parsons.etl.table import Table
from parsons.utilities import check_env

logger = logging.getLogger(__name__)


class OpenField:
    """
    Instantiate the OpenField class

    `Args:`
        domain: str
            The OpenField domain (e.g. ``org-name.openfield.ai``)
            Not required if ``OPENFIELD_DOMAIN`` env variable set.
        username: str
            The authorized OpenField username.
            Not required if ``OPENFIELD_USERNAME`` env variable set.
        password: str
            The authorized OpenField user password.
            Not required if ``OPENFIELD_PASSWORD`` env variable set.
    """

    _default_headers = {
        "content-type": "application/json",
        "accepts": "application/json",
    }

    def __init__(self, domain=None, username=None, password=None):
        self.domain = check_env.check("OPENFIELD_DOMAIN", domain)
        self.username = check_env.check("OPENFIELD_USERNAME", username)
        self.password = check_env.check("OPENFIELD_PASSWORD", password)
        self.conn = self._conn()

    def _conn(self, default_headers=None):
        if default_headers is None:
            default_headers = self._default_headers
        client = requests.Session()
        client.auth = (self.username, self.password)
        client.headers.update(default_headers)
        return client

    def _base_endpoint(self, endpoint, entity_id=None):
        # Create the base endpoint URL

        url = f"https://{self.domain}.openfield.ai/api/v1/{endpoint}/"

        if entity_id:
            return f"{url}{entity_id}/"
        return url

    def _base_get(
        self,
        endpoint,
        entity_id=None,
        exception_message=None,
        params=None,
    ):
        # Make a general GET request

        resp = self.conn.get(
            self._base_endpoint(endpoint, entity_id),
            params=params,
        )
        if resp.status_code >= 400:
            raise Exception(self.parse_error(resp, exception_message))
        return resp.json()

    def _base_post(self, endpoint, data, exception_message=None):
        # Make a general POST request

        resp = self.conn.post(
            self._base_endpoint(endpoint),
            data=json.dumps(data),
        )

        if resp.status_code >= 400:
            raise Exception(self.parse_error(resp, exception_message))

        # Not all responses return a json
        try:
            return resp.json()

        except ValueError:
            return None

    def _base_put(
        self,
        endpoint,
        entity_id=None,
        data=None,
        params=None,
        exception_message=None,
    ):
        # Make a general PUT request

        endpoint = self._base_endpoint(endpoint, entity_id)

        resp = self.conn.put(endpoint, data=json.dumps(data), params=params)

        if resp.status_code >= 400:
            raise Exception(self.parse_error(resp, exception_message))

        # Not all responses return a json
        try:
            return resp.json()

        except ValueError:
            return None

    def _base_delete(self, endpoint, entity_id=None, exception_message=None):
        # Make a general DELETE request

        resp = self.conn.delete(self._base_endpoint(endpoint, entity_id))

        if resp.status_code >= 400:
            raise Exception(self.parse_error(resp, exception_message))

        # Not all responses return a json
        try:
            return resp.json()

        except ValueError:
            return None

    def parse_error(self, resp, exception_message):
        """
        Parse error responses from the API
        """
        message = f"Status {str(resp.status_code)}"
        if exception_message:
            message += exception_message

        try:
            json = resp.json()
            return message + "\n" + str(json)
        except ValueError:
            return message

    def retrieve_person(self, person_id):
        """
        Get a person.

        `Args:`
            person_id: int
                The id of the record.
        `Returns`:
            JSON object
        """

        return self._base_get(
            endpoint="people",
            entity_id=person_id,
            exception_message="Person not found",
        )

    def list_people(
        self,
        page=1,
        page_size=100,
        search=None,
        ordering=None,
        **kwargs,
    ):
        """
        List people

        `Args:`
            page: integer
                A page number within the paginated result set.
            page_size: integer
                Number of results to return per page.
                Defaults to 100
            search: string
                A search term.
            ordering: string
                Which field to use when ordering the results.
            **kwargs:
                Optional arguments to pass to the client. A full list can be
                found in the `OpenField API docs
                <https://openfield.ai/wp-content/uploads/2024/02/redoc-static.html#tag/people/operation/listPeoples>

        `Returns:`
            Parsons.Table
                The people data.
        """

        res = self._base_get(
            endpoint="people",
            params={
                "page": page,
                "page_size": page_size,
                "search": search,
                "ordering": ordering,
                **kwargs,
            },
        )

        return Table(res["results"])

    def create_person(self, person):
        """
        Create a person.

        `Args:`
            person: dict
                Shape of the record
                `Full list of fields
                <https://openfield.ai/wp-content/uploads/2024/02/redoc-static.html#tag/people/operation/createPeople>`_
        `Returns:`
            JSON object
        """

        return self._base_post(
            endpoint="people",
            data=person,
            exception_message="Could not create person",
        )

    def bulk_upsert_people(self, people):
        """
        Given a list of objects, tries the match the object with a provided ID.
        Otherwise, creates a new record for a person without an ID match.

        `Args:`
            people: list of dicts
                List containing the records
                `Full list of fields
                <https://openfield.ai/wp-content/uploads/2024/02/redoc-static.html#tag/people/operation/createPeople>`_
        `Returns:`
            Parsons.Table
                The people data.
        """

        res = self._base_post(
            endpoint="people/bulk-upsert",
            data=people,
        )

        return Table(res)

    def update_person(self, person_id, data):
        """
        Updates a person.

        `Args:`
            person_id: int
                The id of the record.
            data: dict
                Person data to update
                `Full list of fields
                <https://openfield.ai/wp-content/uploads/2024/02/redoc-static.html#tag/people/operation/createPeople>`_
        `Returns:`
            JSON object
        """

        return self._base_put(
            endpoint="people",
            entity_id=person_id,
            data=data,
        )

    def destroy_person(self, person_id):
        """
        Delete a person.

        `Args:`
            person_id: int
                The id of the record.
        `Returns`:
            None
        """

        return self._base_delete(
            endpoint="people",
            entity_id=person_id,
            exception_message="Person not found",
        )

    def retrieve_label(self, label_id):
        """
        Get a label

        `Args:`
            label_id: int
                The id of the record.
        `Returns`:
            JSON object
        """

        return self._base_get(
            endpoint="labels",
            entity_id=label_id,
            exception_message="Label not found",
        )

    def list_labels(
        self,
        page=1,
        page_size=100,
        search=None,
        ordering=None,
        **kwargs,
    ):
        """
        List labels

        `Args:`
            page: integer
                A page number within the paginated result set.
            page_size: integer
                Number of results to return per page.
                Defaults to 100
            search: string
                A search term.
            ordering: string
                Which field to use when ordering the results.
            **kwargs:
                Optional arguments to pass to the client. A full list can be
                found in the `OpenField API docs
                <https://openfield.ai/wp-content/uploads/2024/02/redoc-static.html#tag/labels/operation/listLabels>`_

        `Returns:`
            Parsons.Table
                The labels data.
        """

        res = self._base_get(
            endpoint="labels",
            params={
                "page": page,
                "page_size": page_size,
                "search": search,
                "ordering": ordering,
                **kwargs,
            },
        )

        return Table(res["results"])

    def create_label(self, name, description):
        """
        Create a label.

        `Args:`
            name: string <= 100 characters
                label name
            description: string <= 255 characters
                label description
        `Returns:`
            JSON object
        """

        return self._base_post(
            endpoint="labels",
            data={
                "name": name,
                "description": description,
            },
            exception_message="Could not create label",
        )

    def apply_person_label(self, person_id, label_id):
        """
        Apply a label to a person.

        `Args:`
            person_id: int
                ID of the person
            label_id: int
                ID of the label
        `Returns:`
            JSON object
        """

        return self._base_post(
            endpoint="people-labels",
            data={"person_id": person_id, "label_id": label_id},
        )

    def bulk_apply_people_labels(self, data):
        """
        Bulk apply labels to people.

        `Args:`
            data: list of dicts with keys `person_id` and `label_id`
        `Returns:`
            JSON object
        """

        return self._base_post(
            endpoint="people-labels/bulk-upsert",
            data=data,
        )

    def remove_person_label(self, person_id, label_id):
        """
        Remove a label from a person.

        `Args:`
            person_id: int
                ID of the person
            label_id: int
                ID of the label
        `Returns:`
            JSON object
        """

        return self._base_delete(
            endpoint="people-labels",
            params={"person_id": person_id, "label_id": label_id},
        )
