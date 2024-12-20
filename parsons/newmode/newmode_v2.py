from parsons.utilities.oauth_api_connector import OAuth2APIConnector
from parsons.utilities import check_env
from parsons import Table
import logging

logger = logging.getLogger(__name__)

API_URL = "https://base.newmode.net/api/"
API_AUTH_URL = "https://base.newmode.net/oauth/token/"
API_CAMPAIGNS_URL = "https://base.newmode.net/"


class NewmodeV2(object):
    """
    Instantiate Class
    `Args`:
        api_user: str
            The username to use for the API requests. Not required if ``NEWMODE_API_URL``
            env variable set.
        api_password: str
            The password to use for the API requests. Not required if ``NEWMODE_API_PASSWORD``
            env variable set.
        api_version: str
            The api version to use. Defaults to v1.0
    Returns:
        NewMode Class
    """

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        api_version="v2.1",
    ):
        self.api_version = check_env.check("NEWMODE_API_VERSION", api_version)
        self.base_url = API_URL
        self.client_id = check_env.check("NEWMODE_API_CLIENT_ID", client_id)
        self.__client_secret = check_env.check(
            "NEWMODE_API_CLIENT_SECRET", client_secret
        )
        self.headers = {"content-type": "application/json"}

    def convert_to_table(self, data):
        """Internal method to create a Parsons table from a data element."""
        table = None
        if type(data) is list:
            table = Table(data)
        else:
            table = Table([data])

        return table

    def base_request(self, method, url, data=None, json=None, params={}):
        # response = None
        # if method == "GET":
        #     url, req_type, json=None, data=None, params=None)
        # try:
        response = self.client.request(
            url=url, req_type=method, json=json, data=data, params=params
        )
        response.raise_for_status()  # Raise an exception for bad status codes

        # except Exception as e:
        #     print("Request failed:")
        #     print("URL:", response.request.url)
        #     print("Method:", response.request.method)
        #     print("Headers:", response.request.headers)
        #     print("Body:", response.request.body)
        #     print("Error:", e)
        # print(f"url: {response.request.url}")
        # elif method == "POST":
        #     response = self.client.post_request(
        #         url=url, params=params, json=json, data=data
        # )
        # print(response)
        # Validate the response and lift up an errors.
        success_codes = [200, 201, 202, 204]
        self.client.validate_response(response)
        if response.status_code in success_codes:
            if self.client.json_check(response):
                return response.json()
            else:
                return response.status_code
        return response

    def converted_request(
        self,
        endpoint,
        method,
        supports_version=True,
        data=None,
        json=None,
        params={},
        convert_to_table=True,
    ):
        self.client = OAuth2APIConnector(
            uri=self.base_url,
            auto_refresh_url=API_AUTH_URL,
            client_id=self.client_id,
            client_secret=self.__client_secret,
            headers=self.headers,
            token_url=API_AUTH_URL,
            grant_type="client_credentials",
        )

        url = f"{self.api_version}/{endpoint}" if supports_version else endpoint
        response = self.base_request(
            method=method,
            url=url,
            json=json,
            data=data,
            params=params,
        )
        if not response:
            logging.warning(f"Empty result returned from endpoint: {endpoint}")
        if convert_to_table:
            return self.convert_to_table(response)
        else:
            return response

    def get_campaign(self, campaign_id, params={}):
        """
        Retrieve a specific campaign by ID.

        In v2, a campaign is equivalent to Tools or Actions in V1.
        `Args:`
            campaign_id: str
                The ID of the campaign to retrieve.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing campaign data.
        """
        endpoint = f"/campaign/{campaign_id}/form"
        response = self.converted_request(
            endpoint=endpoint,
            method="GET",
            params=params,
        )
        return response

    def get_campaigns(self, params={}):
        """
        Retrieve all campaigns
        In v2, a campaign is equivalent to Tools or Actions in V1.
        `Args:`
            organization_id: str
                ID of organization
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing campaigns data.
        """
        self.base_url = API_CAMPAIGNS_URL
        self.api_version = "jsonapi"
        self.headers = {
            "content-type": "application/vnd.api+json",
            "accept": "application/vnd.api+json",
            "authorization": "Bearer 1234567890",
        }
        endpoint = "action/action"
        response = self.converted_request(
            endpoint=endpoint,
            method="GET",
            params=params,
        )
        return response

    def get_recipient(
        self,
        campaign_id,
        street_address=None,
        city=None,
        postal_code=None,
        region=None,
        params={},
    ):
        """
        Retrieve a specific recipient by ID
        `Args:`
            campaign_id: str
                The ID of the campaign to retrieve.
            street_address: str
                Street address of recipient
            city: str
                City of recipient
            postal_code: str
                Postal code of recipient
            region: str
                Region (i.e. state/province abbreviation) of recipient
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing recipient data.
        """
        address_params = {
            "street_address": street_address,
            "city": city,
            "postal_code": postal_code,
            "region": region,
        }
        if all(x is None for x in address_params.values()):
            logger.error(
                "Please specify a street address, city, postal code, and/or region."
            )
            raise Exception("Incomplete Request")

        params = {
            f"address[value][{key}]": value
            for key, value in address_params.items()
            if value
        }
        response = self.converted_request(
            endpoint=f"campaign/{campaign_id}/target",
            method="GET",
            params=params,
        )
        return response

    def run_submit(self, campaign_id, json=None, data=None, params={}):
        """
        V2 only
        Pass a submission from a supporter to a campaign
        that ultimately fills in a petition,
        sends an email or triggers a phone call
        depending on your campaign type

        `Args:`
            campaign_id: str
                The ID of the campaign to retrieve.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing submit data.
        """

        json = {
            "action_id": campaign_id,
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "email": "test_abc@test.com",
            "opt_in": 1,
            "address": {"postal_code": "V6A 2T2"},
            "subject": "This is my subject",
            "message": "This is my letter",
        }

        response = self.converted_request(
            endpoint=f"campaign/{campaign_id}/submit",
            method="POST",
            data=data,
            json=json,
            params=params,
            convert_to_table=False,
        )
        return response

    def get_submissions(self, params={}):
        """
        Retrieve and sort submission and contact data
        for your organization using a range of filters
        that include campaign id, data range and submission status

        `Args:`
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing submit data.
        """
        response = self.converted_request(
            endpoint="submission", method="GET", params=params
        )
        return response
