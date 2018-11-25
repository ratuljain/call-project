Getting started
---------------


## Run with:

```
$ git clone https://github.com/ratuljain/call-project.git && cd call-project
$ docker-compose up --build
```

Go to `127.0.0.1:8000/admin` to access the admin. The default username for the admin is `admin` and the password
is `fortheloveofgodpleaseuseagoodpassword`.

To run tests when the container is up.

```
$ docker-compose exec web python manage.py test callcenterapp.tests.test_api
```
    
Stack and version numbers used:

| Name             | Version    |
|----------------- | -----------|
| Docker           | 18.06.0-ce |
| Docker Compose   | 1.22.0     |
| Django           | 1.11.16    |


## Folder structure

```
$ tree -L 2 --dirsfirst  
.
├── callcenterapp
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_api.py             # Functional tests
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── jira_service.py             # contains JIRA api related stuff 
│   ├── models.py                   # contains the model classes
│   ├── serializers.py              # Serializers for models, custom serializer for JIRA payload
│   ├── signals.py                  # Contains post_save signal for PhoneCall model. Checks if Jira task to be created for an entry.
│   ├── urls.py
│   ├── views.py                    # API endpoint views
├── coopproject
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── docker
│   └── web
│       ├── Dockerfile              # Dockerfile for the webapp.
│       └── docker-entrypoint.sh
├── templates
├── venv
├── README.md
├── createsuperuser.py
├── db.sqlite3
├── docker-compose.yml
├── manage.py
├── notes
└── requirements.txt

```

## API Endpoints

* [Show All Phone Calls](http://127.0.0.1:8000/v1/calls/) : `GET /v1/calls/`
* [Create a new Phone Call](http://127.0.0.1:8000/v1/calls/) : `POST /v1/calls/`

### Post example:

The post payload can be directly posted at the bottom of `/v1/calls/` web page. If the payload matches any critera
a JIRA issue creation call is triggered. 

The JIRA API call result is directly logged on the console.

```
{
    "id": 81,
    "action": "action_1",
    "name": "call_1234",
    "data": {
        "id": 83,
        "event_timestamp": "2018-11-21T23:20:49Z",
        "queue_enter_time": "2018-11-21T23:20:52Z",
        "caller_id_num": "123",
        "caller_id_name": "johnnn",
        "queue_name": "queue_1",
        "queue_id": "4f6f3f76-4d5d-4f4b-a259-fd5d89e9c0ed",
        "session_id": "fa21bd8e-99fd-4452-83dd-ff261850646a",
        "event_name": "random",
        "recipient_id": "14fc164b-9322-4b3b-be64-ab08d7ba3bb8",
        "recipient_name": "Doe",
        "total_wait_time": 50
    }
}
```


#### Changing the summary and description string

The strings can be changed by going to `http://127.0.0.1:8000/admin/constance/config/`.

#### Adding more configurations

The JIRA threshold config can be added or changed by going to `http://127.0.0.1:8000/admin/callcenterapp/jiratriggerconfiguration/`.  