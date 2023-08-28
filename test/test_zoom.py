import unittest
from test.utils import assert_matching_tables

import requests_mock
from parsons import Table, Zoom

ACCOUNT_ID = "fakeAccountID"
CLIENT_ID = "fakeClientID"
CLIENT_SECRET = "fakeClientSecret"

ZOOM_URI = "https://api.zoom.us/v2/"
ZOOM_AUTH_CALLBACK = "https://zoom.us/oauth/token"


class TestZoom(unittest.TestCase):
    @requests_mock.Mocker()
    def setUp(self, m):
        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        self.zoom = Zoom(ACCOUNT_ID, CLIENT_ID, CLIENT_SECRET)

    @requests_mock.Mocker()
    def test_get_users(self, m):
        user_json = {
            "page_count": 1,
            "page_number": 1,
            "page_size": 30,
            "total_records": 1,
            "users": [
                {
                    "id": "C5A2nRWwTMm_hXyJb1JXMh",
                    "first_name": "Bob",
                    "last_name": "McBob",
                    "email": "bob@bob.com",
                    "type": 2,
                    "pmi": 8374523641,
                    "timezone": "America/New_York",
                    "verified": 1,
                    "dept": "",
                    "created_at": "2017-10-06T15:22:34Z",
                    "last_login_time": "2020-05-06T16:50:45Z",
                    "last_client_version": "",
                    "language": "",
                    "phone_number": "",
                    "status": "active",
                }
            ],
        }

        tbl = Table(
            [
                {
                    "id": "C5A2nRWwTMm_hXyJb1JXMh",
                    "first_name": "Bob",
                    "last_name": "McBob",
                    "email": "bob@bob.com",
                    "type": 2,
                    "pmi": 8374523641,
                    "timezone": "America/New_York",
                    "verified": 1,
                    "dept": "",
                    "created_at": "2017-10-06T15:22:34Z",
                    "last_login_time": "2020-05-06T16:50:45Z",
                    "last_client_version": "",
                    "language": "",
                    "phone_number": "",
                    "status": "active",
                }
            ]
        )

        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        m.get(ZOOM_URI + "users", json=user_json)
        assert_matching_tables(self.zoom.get_users(), tbl)

    @requests_mock.Mocker()
    def test_get_meeting_participants(self, m):
        participants = {
            "page_count": 1,
            "page_size": 30,
            "total_records": 4,
            "next_page_token": "",
            "participants": [
                {
                    "id": "",
                    "user_id": "16778240",
                    "name": "Barack Obama",
                    "user_email": "",
                    "join_time": "2020-04-24T21:00:26Z",
                    "leave_time": "2020-04-24T22:24:38Z",
                    "duration": 5052,
                    "attentiveness_score": "",
                },
                {
                    "id": "",
                    "user_id": "16779264",
                    "name": "",
                    "user_email": "",
                    "join_time": "2020-04-24T21:00:45Z",
                    "leave_time": "2020-04-24T22:24:38Z",
                    "duration": 5033,
                    "attentiveness_score": "",
                },
            ],
        }

        tbl = Table(
            [
                {
                    "id": "",
                    "user_id": "16778240",
                    "name": "Barack Obama",
                    "user_email": "",
                    "join_time": "2020-04-24T21:00:26Z",
                    "leave_time": "2020-04-24T22:24:38Z",
                    "duration": 5052,
                    "attentiveness_score": "",
                },
                {
                    "id": "",
                    "user_id": "16779264",
                    "name": "",
                    "user_email": "",
                    "join_time": "2020-04-24T21:00:45Z",
                    "leave_time": "2020-04-24T22:24:38Z",
                    "duration": 5033,
                    "attentiveness_score": "",
                },
            ]
        )

        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        m.get(ZOOM_URI + "report/meetings/123/participants", json=participants)
        assert_matching_tables(self.zoom.get_past_meeting_participants(123), tbl)

    @requests_mock.Mocker()
    def test_get_meeting_registrants(self, m):
        registrants = {
            "page_count": 1,
            "page_size": 30,
            "total_records": 4,
            "next_page_token": "",
            "registrants": [
                {
                    "id": "",
                    "user_id": "16778240",
                    "name": "Barack Obama",
                    "user_email": "",
                    "purchasing_time_frame": "Within a month",
                    "role_in_purchase_process": "Not involved",
                },
                {
                    "id": "",
                    "user_id": "16779264",
                    "name": "",
                    "user_email": "",
                    "purchasing_time_frame": "Within a month",
                    "role_in_purchase_process": "Not involved",
                },
            ],
        }

        tbl = Table(
            [
                {
                    "id": "",
                    "user_id": "16778240",
                    "name": "Barack Obama",
                    "user_email": "",
                    "purchasing_time_frame": "Within a month",
                    "role_in_purchase_process": "Not involved",
                },
                {
                    "id": "",
                    "user_id": "16779264",
                    "name": "",
                    "user_email": "",
                    "purchasing_time_frame": "Within a month",
                    "role_in_purchase_process": "Not involved",
                },
            ]
        )

        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        m.get(ZOOM_URI + "meetings/123/registrants", json=registrants)
        assert_matching_tables(self.zoom.get_meeting_registrants(123), tbl)

    @requests_mock.Mocker()
    def test_get_user_webinars(self, m):
        webinars = {
            "page_count": 1,
            "page_size": 30,
            "total_records": 4,
            "next_page_token": "",
            "webinars": [
                {
                    "uuid": "dsghfkhaewfds",
                    "id": "",
                    "host_id": "24654130000000",
                    "topic": "My Webinar",
                    "agenda": "Learn more about Zoom APIs",
                    "type": "5",
                    "duration": "60",
                    "start_time": "2019-09-24T22:00:00Z",
                    "timezone": "America/Los_Angeles",
                    "created_at": "2019-08-30T22:00:00Z",
                    "join_url": "https://zoom.us/0001000/awesomewebinar",
                },
                {
                    "uuid": "dhf8as7dhf",
                    "id": "",
                    "host_id": "24654130000345",
                    "topic": "My Webinar",
                    "agenda": "Learn more about Zoom APIs",
                    "type": "5",
                    "duration": "60",
                    "start_time": "2019-09-24T22:00:00Z",
                    "timezone": "America/Los_Angeles",
                    "created_at": "2019-08-30T22:00:00Z",
                    "join_url": "https://zoom.us/0001000/awesomewebinar",
                },
            ],
        }

        tbl = Table(
            [
                {
                    "uuid": "dsghfkhaewfds",
                    "id": "",
                    "host_id": "24654130000000",
                    "topic": "My Webinar",
                    "agenda": "Learn more about Zoom APIs",
                    "type": "5",
                    "duration": "60",
                    "start_time": "2019-09-24T22:00:00Z",
                    "timezone": "America/Los_Angeles",
                    "created_at": "2019-08-30T22:00:00Z",
                    "join_url": "https://zoom.us/0001000/awesomewebinar",
                },
                {
                    "uuid": "dhf8as7dhf",
                    "id": "",
                    "host_id": "24654130000345",
                    "topic": "My Webinar",
                    "agenda": "Learn more about Zoom APIs",
                    "type": "5",
                    "duration": "60",
                    "start_time": "2019-09-24T22:00:00Z",
                    "timezone": "America/Los_Angeles",
                    "created_at": "2019-08-30T22:00:00Z",
                    "join_url": "https://zoom.us/0001000/awesomewebinar",
                },
            ]
        )

        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        m.get(ZOOM_URI + "users/123/webinars", json=webinars)
        assert_matching_tables(self.zoom.get_user_webinars(123), tbl)

    @requests_mock.Mocker()
    def test_get_past_webinar_participants(self, m):
        participants = {
            "page_count": 1,
            "page_size": 30,
            "total_records": 4,
            "next_page_token": "",
            "participants": [
                {
                    "id": "",
                    "user_id": "sdfjkldsf87987",
                    "name": "Barack",
                    "user_email": "riya@sdfjkldsf87987.fdjfhdf",
                    "join_time": "2019-02-01T12:34:12.660Z",
                    "leave_time": "2019-03-01T12:34:12.660Z",
                    "duration": "20",
                },
                {
                    "id": "",
                    "user_id": "sdfjkldsfdfgdfg",
                    "name": "Joe",
                    "user_email": "riya@sdfjkldsf87987.fdjfhdf",
                    "join_time": "2019-02-01T12:34:12.660Z",
                    "leave_time": "2019-03-01T12:34:12.660Z",
                    "duration": "20",
                },
            ],
        }

        tbl = Table(
            [
                {
                    "id": "",
                    "user_id": "sdfjkldsf87987",
                    "name": "Barack",
                    "user_email": "riya@sdfjkldsf87987.fdjfhdf",
                    "join_time": "2019-02-01T12:34:12.660Z",
                    "leave_time": "2019-03-01T12:34:12.660Z",
                    "duration": "20",
                },
                {
                    "id": "",
                    "user_id": "sdfjkldsfdfgdfg",
                    "name": "Joe",
                    "user_email": "riya@sdfjkldsf87987.fdjfhdf",
                    "join_time": "2019-02-01T12:34:12.660Z",
                    "leave_time": "2019-03-01T12:34:12.660Z",
                    "duration": "20",
                },
            ]
        )

        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        m.get(ZOOM_URI + "report/webinars/123/participants", json=participants)
        assert_matching_tables(self.zoom.get_past_webinar_participants(123), tbl)

    @requests_mock.Mocker()
    def test_get_webinar_registrants(self, m):
        registrants = {
            "page_count": 1,
            "page_size": 30,
            "total_records": 4,
            "next_page_token": "",
            "registrants": [
                {
                    "id": "",
                    "email": "barack@obama.com",
                    "first_name": "Barack",
                    "last_name": "Obama",
                    "address": "dsfhkdjsfh st",
                    "city": "jackson heights",
                    "country": "US",
                    "zip": "11371",
                    "state": "NY",
                    "phone": "00000000",
                    "industry": "Food",
                    "org": "Cooking Org",
                    "job_title": "Chef",
                    "purchasing_time_frame": "1-3 months",
                    "role_in_purchase_process": "Influencer",
                    "no_of_employees": "10",
                    "comments": "Looking forward to the Webinar",
                    "custom_questions": [
                        {
                            "title": "What do you hope to learn from this Webinar?",
                            "value": "Look forward to learning how you come up with recipes and services",  # noqa: E501
                        }
                    ],
                    "status": "approved",
                    "create_time": "2019-02-26T23:01:16.899Z",
                    "join_url": "https://zoom.us/webinar/mywebinariscool",
                },
                {
                    "id": "",
                    "email": "joe@biden.com",
                    "first_name": "Joe",
                    "last_name": "Biden",
                    "address": "dsfhkdjsfh st",
                    "city": "jackson heights",
                    "country": "US",
                    "zip": "11371",
                    "state": "NY",
                    "phone": "00000000",
                    "industry": "Food",
                    "org": "Cooking Org",
                    "job_title": "Chef",
                    "purchasing_time_frame": "1-3 months",
                    "role_in_purchase_process": "Influencer",
                    "no_of_employees": "10",
                    "comments": "Looking forward to the Webinar",
                    "custom_questions": [
                        {
                            "title": "What do you hope to learn from this Webinar?",
                            "value": "Look forward to learning how you come up with recipes and services",  # noqa: E501
                        }
                    ],
                    "status": "approved",
                    "create_time": "2019-02-26T23:01:16.899Z",
                    "join_url": "https://zoom.us/webinar/mywebinariscool",
                },
            ],
        }

        tbl = Table(
            [
                {
                    "id": "",
                    "email": "barack@obama.com",
                    "first_name": "Barack",
                    "last_name": "Obama",
                    "address": "dsfhkdjsfh st",
                    "city": "jackson heights",
                    "country": "US",
                    "zip": "11371",
                    "state": "NY",
                    "phone": "00000000",
                    "industry": "Food",
                    "org": "Cooking Org",
                    "job_title": "Chef",
                    "purchasing_time_frame": "1-3 months",
                    "role_in_purchase_process": "Influencer",
                    "no_of_employees": "10",
                    "comments": "Looking forward to the Webinar",
                    "custom_questions": [
                        {
                            "title": "What do you hope to learn from this Webinar?",
                            "value": "Look forward to learning how you come up with recipes and services",  # noqa: E501
                        }
                    ],
                    "status": "approved",
                    "create_time": "2019-02-26T23:01:16.899Z",
                    "join_url": "https://zoom.us/webinar/mywebinariscool",
                },
                {
                    "id": "",
                    "email": "joe@biden.com",
                    "first_name": "Joe",
                    "last_name": "Biden",
                    "address": "dsfhkdjsfh st",
                    "city": "jackson heights",
                    "country": "US",
                    "zip": "11371",
                    "state": "NY",
                    "phone": "00000000",
                    "industry": "Food",
                    "org": "Cooking Org",
                    "job_title": "Chef",
                    "purchasing_time_frame": "1-3 months",
                    "role_in_purchase_process": "Influencer",
                    "no_of_employees": "10",
                    "comments": "Looking forward to the Webinar",
                    "custom_questions": [
                        {
                            "title": "What do you hope to learn from this Webinar?",
                            "value": "Look forward to learning how you come up with recipes and services",  # noqa: E501
                        }
                    ],
                    "status": "approved",
                    "create_time": "2019-02-26T23:01:16.899Z",
                    "join_url": "https://zoom.us/webinar/mywebinariscool",
                },
            ]
        )

        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        m.get(ZOOM_URI + "webinars/123/registrants", json=registrants)
        assert_matching_tables(self.zoom.get_webinar_registrants(123), tbl)

    @requests_mock.Mocker()
    def test_get_meeting_poll(self, m):
        poll = {
            "id": 1,
            "status": "started",
            "anonymous": "False",
            "poll_type": 1,
            "questions": [
                {
                    "answer_max_character": 1,
                    "answer_min_character": 1,
                    "answer_required": "False",
                    "answers": "Larry David's Curb Your Enthusiasm",
                    "case_sensitive": "True",
                    "name": "Secret Truth",
                    "prompts": [
                        {
                            "prompt_question": "What's the secret truth of the universe?",
                            "prompt_right_answers": [
                                "Pizza delivery",
                                "Larry David's Curb Your Enthusiasm",
                            ],
                        }
                    ],
                    "rating_max_label": "",
                    "rating_max_value": 1,
                    "rating_min_label": "",
                    "rating_min_value": 0,
                    "right_answers": "",
                    "show_as_dropdown": False,
                    "type": "short_answer",
                }
            ],
        }

        tbl = Table(
            [
                {
                    "answer_max_character": 1,
                    "answer_min_character": 1,
                    "answer_required": "False",
                    "answers": "Larry David's Curb Your Enthusiasm",
                    "case_sensitive": "True",
                    "name": "Secret Truth",
                    "prompts": [
                        {
                            "prompt_question": "What's the secret truth of the universe?",
                            "prompt_right_answers": [
                                "Pizza delivery",
                                "Larry David's Curb Your Enthusiasm",
                            ],
                        }
                    ],
                    "rating_max_label": "",
                    "rating_max_value": 1,
                    "rating_min_label": "",
                    "rating_min_value": 0,
                    "right_answers": "",
                    "show_as_dropdown": False,
                    "type": "short_answer",
                }
            ]
        )

        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        m.get(ZOOM_URI + "meetings/123/polls/1", json=poll)
        assert_matching_tables(self.zoom.get_meeting_poll(123, 1), tbl)

    @requests_mock.Mocker()
    def test_get_meeting_all_polls(self, m):
        polls = {
            "polls": [
                {
                    "id": 1,
                    "status": "started",
                    "anonymous": "False",
                    "poll_type": 1,
                    "questions": [
                        {
                            "answer_max_character": 1,
                            "answer_min_character": 1,
                            "answer_required": "False",
                            "answers": "Larry David's Curb Your Enthusiasm",
                            "case_sensitive": "True",
                            "name": "Secret Truth",
                            "prompts": [
                                {
                                    "prompt_question": "What's the secret truth of the universe?",
                                    "prompt_right_answers": [
                                        "Pizza delivery",
                                        "Larry David's Curb Your Enthusiasm",
                                    ],
                                }
                            ],
                            "rating_max_label": "",
                            "rating_max_value": 1,
                            "rating_min_label": "",
                            "rating_min_value": 0,
                            "right_answers": "",
                            "show_as_dropdown": False,
                            "type": "short_answer",
                        }
                    ],
                },
                {
                    "id": 2,
                    "status": "started",
                    "anonymous": "False",
                    "poll_type": 1,
                    "questions": [
                        {
                            "answer_max_character": 1,
                            "answer_min_character": 1,
                            "answer_required": "False",
                            "answers": "Mets",
                            "case_sensitive": "True",
                            "name": "Play ball",
                            "prompts": [
                                {
                                    "prompt_question": "Best NY baseball team?",
                                    "prompt_right_answers": ["Mets"],
                                }
                            ],
                            "rating_max_label": "",
                            "rating_max_value": 1,
                            "rating_min_label": "",
                            "rating_min_value": 0,
                            "right_answers": "",
                            "show_as_dropdown": True,
                            "type": "short_answer",
                        }
                    ],
                },
            ]
        }

        tbl = Table(
            [
                {
                    "id": 1,
                    "status": "started",
                    "anonymous": "False",
                    "poll_type": 1,
                    "questions": [
                        {
                            "answer_max_character": 1,
                            "answer_min_character": 1,
                            "answer_required": "False",
                            "answers": "Larry David's Curb Your Enthusiasm",
                            "case_sensitive": "True",
                            "name": "Secret Truth",
                            "prompts": [
                                {
                                    "prompt_question": "What's the secret truth of the universe?",
                                    "prompt_right_answers": [
                                        "Pizza delivery",
                                        "Larry David's Curb Your Enthusiasm",
                                    ],
                                }
                            ],
                            "rating_max_label": "",
                            "rating_max_value": 1,
                            "rating_min_label": "",
                            "rating_min_value": 0,
                            "right_answers": "",
                            "show_as_dropdown": False,
                            "type": "short_answer",
                        }
                    ],
                },
                {
                    "id": 2,
                    "status": "started",
                    "anonymous": "False",
                    "poll_type": 1,
                    "questions": [
                        {
                            "answer_max_character": 1,
                            "answer_min_character": 1,
                            "answer_required": "False",
                            "answers": "Mets",
                            "case_sensitive": "True",
                            "name": "Play ball",
                            "prompts": [
                                {
                                    "prompt_question": "Best NY baseball team?",
                                    "prompt_right_answers": ["Mets"],
                                }
                            ],
                            "rating_max_label": "",
                            "rating_max_value": 1,
                            "rating_min_label": "",
                            "rating_min_value": 0,
                            "right_answers": "",
                            "show_as_dropdown": True,
                            "type": "short_answer",
                        }
                    ],
                },
            ]
        )

        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        m.get(ZOOM_URI + "meetings/123/polls", json=polls)
        assert_matching_tables(self.zoom.get_meeting_all_polls(123), tbl)

    @requests_mock.Mocker()
    def test_get_webinar_poll(self, m):
        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        m.get(ZOOM_URI + "/webinars/123/polls/456", json={})

    @requests_mock.Mocker()
    def test_get_webinar_all_polls(self, m):
        m.post(ZOOM_AUTH_CALLBACK, json={"access_token": "fakeAccessToken"})
        m.get(ZOOM_URI + "/webinars/123", json={})
