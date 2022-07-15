from api_v1.base.client_requests import RequestBody


class NewEventRequest(RequestBody):
    start_date: int
    end_date: int
