import logging

logger = logging.getLogger(__name__)


class Events(object):

    def __init__(self, van_connection):

        self.connection = van_connection

    def get_events(self, code_ids=None, event_type_ids=None, rep_event_id=None,
                   starting_after=None, starting_before=None, district_field=None,
                   expand=['locations', 'codes', 'shifts', 'roles', 'notes',
                           'onlineForms']):
        """
        Get events.

        `Args:`
            code_ids: str
                Filter by code id
            event_type_ids: str
                Filter by event_type_ids
            rep_event_id: str
                Filters to recurring events that are recurrences the passed event id.
            starting_after: str
                Events beginning after ``iso8601`` formatted date.
            starting_before: str
                Events beginning before ``iso8601`` formatted date.
            district_field: str
                Filter by district field
            page_size: str
                Not Implemented
            expand : list
                A list of nested jsons to include in returned event
                object. Can be ``locations``, ``codes``, ``shifts``,
                ``roles``, ``notes``, ``onlineForms``.
        `Returns:`
            Parsons Table
                See :ref:`parsons-table` for output options.
        """

        url = self.connection.uri + 'events/'

        if expand:
            expand = ','.join(expand)

        args = {'codeIds': code_ids,
                'eventTypeIds': event_type_ids,
                'inRepetitionWithEventId': rep_event_id,
                'startingAfter': starting_after,
                'startingBefore': starting_before,
                'districtFieldValue': district_field,
                'top': 50,
                '$expand': expand
                }

        logger.info('Getting events...')
        events = self.connection.request_paginate(url, args=args)
        logger.debug(events)
        logger.info(f'Found {events.num_rows} events.')

        return events

    def get_event(self, event_id, expand=['locations', 'codes', 'shifts', 'roles',
                                          'notes', 'onlineForms']):
        """
        Get an event.

        `Args:`
            event_id: int
                The event id.
            expand: list
                A list of nested jsons to include in returned event
                object. Can be ``locations``, ``codes``, ``shifts``,
                ``roles``, ``notes``, ``onlineForms``.
        `Returns:`
            Parsons Table
                See :ref:`parsons-table` for output options.
        """

        url = self.connection.uri + 'events/{}'.format(event_id)

        if expand:
            expand = ','.join(expand)

        logger.info(f'Getting event {event_id}...')
        event = self.connection.request(url, args={'$expand': expand})
        logger.debug(event)
        logger.info(f'Found event {event_id}.')

        return event

    def create_event(self, name, short_name, start_date, end_date, event_type_id,
                     roles, shifts=None, description=None, editable=False,
                     publicly_viewable=False, location_ids=None, code_ids=None, notes=None,
                     district_field_value=None, voter_registration_batches=None):
        """
        Create an event

        `Args:`
            name: str
                A name for this event, no longer than 500 characters.
            short_name: str
                A shorter name for this event, no longer than 12 characters.
            start_date: str
                The start date and time for this event.
            end_date: str
                The end date and time for this event that is after ``start_date``
            event_type_id: int
                A valid event type id.
            roles: list
                A list of valid role ids that correspond the with the event type.
            shifts:
                A list of dicts with shifts formatted as:

                .. highlight:: python
                .. code-block:: python

                    [
                        {
                         'name': 'Shift 1',
                         'start_time': '12-31-2018T12:00:00',
                         'end_time': '12-31-2018T13:00:00'
                        }
                        {
                         'name': 'Shift 2',
                         'start_time': '12-31-2018T13:00:00',
                         'end_time': '12-31-2018T14:00:00'
                        }
                    ]

            description: str
                An optional description for this Event, no longer than 500 characters.
            editable: boolean
                If ``True``, prevents modification of this event by any users other than the
                user associated the API key. Setting this to true effectively makes
                the event read-only in the VAN interface.
            publicly_viewable: boolean
                Used by NGP VAN’s website platform to indicate whether this event can be
                viewed publicly.
            location_ids: list
                A list of location_ids where the event is taking place
            code_ids: list
                A list of codes that are applied to this event for organizational purposes. Note
                that at most one source code and any number of tags, may be applied to an event.
            notes: list
                A list of notes
        `Returns:`
            The event code
        """

        url = self.connection.uri + 'events/'

        if shifts is None:
            shifts = [{'name': 'Default Shift',
                       'startTime': start_date,
                       'endTime': end_date}]
        else:
            shifts = [{'name': s['name'],
                       'startTime': s['start_time'],
                       'endTime': s['end_time']} for s in shifts]

        event = {'name': name,
                 'shortName': short_name,
                 'description': description,
                 'startDate': start_date,
                 'endDate': end_date,
                 'eventType': {'eventTypeId': event_type_id},
                 'isOnlyEditableByCreatingUser': str(editable).lower(),
                 'isPubliclyViewable': publicly_viewable,
                 'notes': notes,
                 'shifts': shifts,
                 'roles': [{'roleId': r} for r in roles],
                 'districtFieldValue': district_field_value,
                 'voterRegistrationBatches': voter_registration_batches
                 }

        if location_ids:
            event['locations'] = [{'locationId': l} for l in location_ids],

        if code_ids:
            event['codes'] = [{'codeID': c} for c in code_ids]

        logger.info('Creating new event...')
        event_code = self.connection.request(
            url, req_type="POST", post_data=event, raw=True)
        logger.debug(event)
        logger.info(f'Event {event_code} created.')

        return event_code

    def delete_event(self, event_id):
        """
        Delete an event.

        `Args:`
            event_id: int
                The event id.
        `Returns:`
            ``None``
        """

        url = self.connection.uri + 'events/{}'.format(event_id)

        logger.info(f'Deleting event {event_id}...')
        old_event = self.connection.request(url, req_type="DELETE", raw=True)
        logger.info(f'Event {event_id} deleted.')

        return old_event

    def add_event_shift(self, event_id, shift_name, start_time, end_time):
        """
        Add shifts to an event

        `Args:`
            event_id: int
                The event id.
            shift_name: str
                The name of the shift
            start_time: str
                The start time for the shift.
            end_time: str
                The end time of the shift.
        `Returns:`
            ``None``
        """

        url = self.connection.uri + 'events/{}/shifts'.format(event_id)

        shift = {'name': shift_name,
                 'startTime': start_time,
                 'endTime': end_time
                 }

        logger.info(f'Adding shifts to event {event_id}...')
        shifts = self.connection.request(
            url, req_type="POST", post_data=shift, raw=True)
        logger.info('Finished adding shifts.')

        return shifts

    def get_event_types(self):
        """
        Get event types.

        `Returns:`
            Parsons Table
                See :ref:`parsons-table` for output options.
        """

        url = self.connection.uri + 'events/types'

        logger.info(f'Getting event types...')
        types = self.connection.request(url)
        logger.debug(types)
        logger.info(f'Found {types.num_rows} event types')

        return types
