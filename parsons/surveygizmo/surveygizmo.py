import logging
import surveygizmo
from parsons.etl import Table
from parsons.utilities import check_env

logger = logging.getLogger(__name__)


class SurveyGizmo(object):
    """
    Instantiate SurveyGizmo Class

    `Args:`
        api_token:
            The SurveyGizmo-provided application token. Not required if
            ``SURVEYGIZMO_API_TOKEN`` env variable set.

        api_token:
            The SurveyGizmo-provided application token. Not required if
            ``SURVEYGIZMO_API_TOKEN_SECRET`` env variable set.

        api_version:
            The version of the API that you would like to use. Not required if
            ``SURVEYGIZMO_API_VERSION`` env variable set.
            Default v5

    `Returns:`
        SurveyGizmo Class
    """

    def __init__(self, api_token=None, api_token_secret=None, api_version='v5'):
        self.api_token = check_env.check('SURVEYGIZMO_API_TOKEN', api_token)
        self.api_token_secret = check_env.check('SURVEYGIZMO_API_TOKEN_SECRET', api_token_secret)
        self.api_version = check_env.check('SURVEYGIZMO_API_VERSION', api_version)

        self._client = surveygizmo.SurveyGizmo(
                api_version=self.api_version,
                api_token=self.api_token,
                api_token_secret=self.api_token_secret
                )

    def get_surveys(self):
        """
        Get a table of lists under the account.

        `Args:`
            None

        `Returns:`
            Table Class
        """

        r = self._client.api.survey.list()
        data = r['data']

        while r['page'] < r['total_pages']:
            r = self._client.api.survey.list(page=(r['page']+1))
            data.extend(r['data'])

        tbl = Table(data).remove_column('links')
        tbl.unpack_dict('statistics', prepend=False)

        logger.info(f"Found {tbl.num_rows} surveys.")

        return tbl

    def get_survey_responses(self, survey_id, page=None):
        """
        Get the responses for a given survey.

        `Args:`
            survey_id: string
                The id of survey for which to retrieve the responses.

        `Returns:`
            Table Class
        """

        r = self._client.api.surveyresponse.list(survey_id)
        logger.info(f"{survey_id}: {r['total_count']} responses.")
        data = r['data']

        if not page:
            while r['page'] < r['total_pages']:
                r = self._client.api.surveyresponse.list(survey_id, page=(r['page']+1))
                data.extend(r['data'])
                logger.info(f"{survey_id}: Retrieving {r['page']} of {r['total_count']}.")

        tbl = Table(data).add_column('survey_id', survey_id, index=1)

        return tbl
