import json

import requests
import responses

from callcenterapp.serializers import JiraIssueSerializer


# JIRA issue classes.

class Project(object):
    def __init__(self, key):
        self.key = key


class IssueType(object):
    def __init__(self, name):
        self.name = name


class Fields(object):
    def __init__(self, project, summary, description, issuetype):
        self.project = project
        self.summary = summary
        self.description = description
        self.issuetype = issuetype


class JiraIssue(object):
    def __init__(self, fields):
        self.fields = fields


@responses.activate
def create_issue(server_base_url, username, password, project_key, summary, description, issue_type_name):
    """
    Method to create a JIRA issue using a project key and field names.

    :param server_base_url: base url of JIRA server
    :param username: JIRA account username
    :param password: JIRA account password
    :param project_key: key metadata
    :param summary: issue summary string
    :param description: issue description string
    :param issue_type_name: kind of issue
    :return:
    """

    url = "{}/rest/api/2/issue/".format(server_base_url)

    # mocking the api call.
    responses.add(responses.POST, url,
                  json={"id": "39001", "key": "TEST-102", "self": "http://localhost:8080/rest/api/2/issue/39001"},
                  status=201)

    # the JIRA issue object.
    jira_issue = JiraIssue(fields=Fields(project=Project(key=project_key), summary=summary, description=description,
                                         issuetype=IssueType(name=issue_type_name)))
    serializer = JiraIssueSerializer(jira_issue)

    resp = requests.post(url, data=json.dumps(serializer.data), auth=(username, password))

    if resp.status_code != 201:
        print "ERROR: status {}".format(resp.status_code)
        return

    print '\n\n\n########################################## JIRA API CALLED ##########################################'
    print json.dumps(serializer.data, indent=4, sort_keys=True)
    print resp.json()
    print '########################################## JIRA API CALLED ##########################################\n\n\n'

    return resp.json()
