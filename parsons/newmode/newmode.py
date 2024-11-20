from parsons.utilities.api_connector import APIConnector
from parsons.utilities import check_env
from parsons import Table
import logging
import time

logger = logging.getLogger(__name__)

API_URL = "https://engage.newmode.net/api/"


class NewMode(object):
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
            The api version to use. Defaults to v2.1
    Returns:
        NewMode Class
    """

    def __init__(self, api_user=None, api_password=None, api_version="v2.1"):
        self.base_url = check_env.check("NEWMODE_API_URL", API_URL)
        self.api_user = check_env.check("NEWMODE_API_USER", api_user)
        self.api_password = check_env.check("NEWMODE_API_PASSWORD", api_password)
        self.api_version = check_env.check("NEWMODE_API_VERSION", api_version)
        self.headers = {"Content-Type": "application/json"}
        self.url = f"{self.base_url}{self.api_version}/"
        self.client = APIConnector(
            self.api_url_with_version,
            auth=(self.api_user, self.api_password),
            headers=self.headers,
        )

    def base_request(
        self,
        endpoint,
        method,
        requires_csrf=True,
        params={},
    ):

        url = endpoint

        if requires_csrf:
            csrf = self.get_csrf_token()
            self.headers["X-CSRF-Token"] = csrf

        response = None
        if method == "GET":
            response = self.client.get_request(url=url, params=params)
        elif method == "PATCH":
            response = self.client.patch_request(url=url, params=params)
            # response.get("_embedded", {}).get(f"osdi:{object_name}")
        try:
            tbl = Table(response)
        except Exception as e:
            logger.error("Failed to convert API response json to Parsons Table")
            raise e
        return tbl

    def get_csrf_token(self, max_retries=10):
        """
        Retrieve a CSRF token for making API requests
        `Args:`
            max_retries: int
                The maximum number of attempts to get the CSRF token.
        `Returns:`
            The CSRF token.
        """
        for attempt in range(max_retries):
            try:
                response = self.base_request(
                    endpoint="session/token", method="GET", requires_csrf=False
                )
                return response
            except Exception as e:
                if attempt >= max_retries:
                    logger.error((f"Error getting CSRF Token after {max_retries} retries"))
                    raise e
                logger.warning(
                    f"Retry {attempt} at getting CSRF Token failed. Retrying. Error: {e}"
                )
                time.sleep(attempt + 1)

    def get_tools(self, params={}):
        """
        Retrieve all tools
        `Args:`
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing tools data.
        """
        response = self.base_request(endpoint="tool", method="GET", params=params)
        return response

    def get_tool(self, tool_id, params={}):
        """
        Retrieve a specific tool by ID
        `Args:`
            tool_id: str
                The ID of the tool to retrieve.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing the tool data.
        """
        response = self.base_request(
            endpoint=f"tool/{tool_id}", method="GET", params=params
        )
        return response

    def lookup_targets(self, tool_id, search=None, params={}):
        """
        Lookup targets for a given tool
        `Args:`
            tool_id: str
                The ID of the tool to lookup targets for.
            search: str
                The search criteria (optional).
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing target data.
        """
        endpoint = f"lookup/{tool_id}"
        if search:
            endpoint += f"/{search}"
        response = self.base_request(endpoint=endpoint, method="GET", params=params)
        return response

    def get_action(self, tool_id, params={}):
        """
        Get action information for a specific tool
        `Args:`
            tool_id: str
                The ID of the tool to get action information for.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing action data.
        """
        response = self.base_request(
            endpoint=f"action/{tool_id}", method="GET", params=params
        )
        return response

    def run_action(self, tool_id, payload, params={}):
        """
        Run a specific action for a tool
        `Args:`
            tool_id: str
                The ID of the tool to run the action for.
            payload: dict
                The data to post to run the action.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing posted outreach information.
        """
        response = self.base_request(
            endpoint=f"action/{tool_id}", method="PATCH", payload=payload, params=params
        )
        return response

    def get_target(self, target_id, params={}):
        """
        Retrieve a specific target by ID
        `Args:`
            target_id: str
                The ID of the target to retrieve.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing target data.
        """
        response = self.base_request(
            endpoint=f"target/{target_id}", method="GET", params=params
        )
        return response

    def get_campaigns(self, params={}):
        """
        Retrieve all campaigns
        `Args:`
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing campaigns data.
        """
        response = self.base_request(endpoint="campaign", method="GET", params=params)
        return response

    def get_campaign(self, campaign_id, params={}):
        """
        Retrieve a specific campaign by ID
        `Args:`
            campaign_id: str
                The ID of the campaign to retrieve.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing campaign data.
        """
        response = self.base_request(
            endpoint=f"campaign/{campaign_id}", method="GET", params=params
        )
        return response

    def get_organizations(self, params={}):
        """
        Retrieve all organizations
        `Args:`
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing organizations data.
        """
        response = self.base_request(
            endpoint="organization", method="GET", params=params
        )
        return response

    def get_organization(self, organization_id, params={}):
        """
        Retrieve a specific organization by ID
        `Args:`
            organization_id: str
                The ID of the organization to retrieve.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing organization data.
        """
        response = self.base_request(
            endpoint=f"organization/{organization_id}", method="GET", params=params
        )
        return response

    def get_services(self, params={}):
        """
        Retrieve all services
        `Args:`
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing services data.
        """
        response = self.base_request(endpoint="service", method="GET", params=params)
        return response

    def get_service(self, service_id, params={}):
        """
        Retrieve a specific service by ID
        `Args:`
            service_id: str
                The ID of the service to retrieve.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing service data.
        """
        response = self.base_request(
            endpoint=f"service/{service_id}", method="GET", params=params
        )
        return response

    def get_targets(self, params={}):
        """
        Retrieve all targets
        `Args:`
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing targets data.
        """
        response = self.base_request(endpoint="target", method="GET", params=params)
        return response

    def get_outreaches(self, tool_id, params={}):
        """
        Retrieve all outreaches for a specific tool
        `Args:`
            tool_id: str
                The ID of the tool to get outreaches for.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing outreaches data.
        """
        params["nid"] = str(tool_id)
        response = self.base_request(
            endpoint="outreach", method="GET", requires_csrf=False, params=params
        )
        return response

    def get_outreach(self, outreach_id, params={}):
        """
        Retrieve a specific outreach by ID
        `Args:`
            outreach_id: str
                The ID of the outreach to retrieve.
            params: dict
                Query parameters to include in the request.
        `Returns:`
            Parsons Table containing outreach data.
        """
        response = self.base_request(
            endpoint=f"outreach/{outreach_id}", method="GET", params=params
        )
        return response
    