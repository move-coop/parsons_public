import os
import unittest
import unittest.mock as mock
from parsons.surveygizmo.surveygizmo import SurveyGizmo, Table
import logging

logger = logging.getLogger(__name__)

class TestSurveyGizmo(unittest.TestCase):

    def setUp(self):
        os.environ['SURVEYGIZMO_API_TOKEN'] = 'MYFAKEAPITOKEN'
        os.environ['SURVEYGIZMO_API_TOKEN_SECRET'] = 'MYFAKETOKENSECRET'
        os.environ['SURVEYGIZMO_API_VERSION'] = 'MYFAKEVERSION'

        self.surveygizmo = SurveyGizmo()
        self.surveygizmo._client = mock.MagicMock()

    def test_get_surveys_single_page(self):
        self.surveygizmo._client.api.survey.list.return_value = self._get_surveys_return_single_page()

        actual_surveys = self.surveygizmo.get_surveys()

        self.assertEqual(2, actual_surveys.num_rows)


    def _get_surveys_return_single_page(self):
        return {
                "result_ok": True,
                "total_count": "1461",
                "page": 1,
                "total_pages": 1,
                "results_per_page": 50,
                "data": [
                    {
                        "id": "1234567",
                        "team": "433737",
                        "type": "Standard Survey",
                        "status": "Launched",
                        "created_on": "2017-04-24 10:44:23",
                        "modified_on": "2017-04-24 10:58:20",
                        "title": "Survey",
                        "statistics": {
                            "Partial": 4,
                            "Complete": 2
                            },
                        "links": {
                            "edit": "[Link to Build Tab]",
                            "publish": "[Link to Share Tab]",
                            "default": "[Default Share Link]"
                            }
                        },
                    {
                        "id": "1234568",
                        "team": "433737",
                        "type": "Standard Survey",
                        "status": "Launched",
                        "created_on": "2017-04-24 09:53:01",
                        "modified_on": "2017-04-24 09:53:55",
                        "title": "Survey",
                        "statistics": {
                            "Partial": 1
                            },
                        "links": {
                            "edit": "[Link to Build Tab]",
                            "publish": "[Link to Share Tab]",
                            "default": "[Default Share Link]"
                            }
                        }
                    ]
                }
