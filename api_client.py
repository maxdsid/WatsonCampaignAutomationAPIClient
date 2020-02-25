# Imports
from datetime import datetime
import requests
from .xml_generator import WatsonXmlGenerator
import xmltodict


class WatsonApiClient:
    """
    This class is a Watson Campaign Automation XML API Client
    Details: https://developer.ibm.com/customer-engagement/docs/watson-marketing/ibm-engage-2/watson-campaign-automation-platform/xml-api/api-xml-overview/
    Supported API calls (more coming):
    - Calculate Query
    - Get Job Status
    - Export List/Query
    - Purge Data
    """
    def __init__(self, api_auth_url, client_id, client_secret, refresh_token, ibm_api_url):
        """
        The initialize method generates OAUTH2 token for further API calls
        :param api_auth_url: pod number based url for authentication, e.g. 'http://api7.ibmmarketingcloud.com/oauth'
        :param client_id: client id, can be obtained from your Watson Admin
        :param client_secret: client secret, can be obtained from your Watson Admin
        :param refresh_token: refresh token, can be obtained from your Watson Admin
        :param ibm_api_url: pod number based url for api calls, e.g. 'https://api7.ibmmarketingcloud.com/XMLAPI'
        ! Due to migration from Watson to Acoustic, urls might be different in the future
        """
        self.log = []
        self.log.append(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Generating Authentication Token')
        token_url = f"{api_auth_url}/token?grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}"
        get_token = requests.request('POST', token_url)
        access_token = get_token.text.split('"')[3]
        self.headers = {'Content-Type': 'text/xml', 'Authorization': 'bearer ' + access_token}
        self.api_url = ibm_api_url
        self.generator = WatsonXmlGenerator()

    def __str__(self):
        return f'Watson Campaign Automation API Client'

    def __send_request(self, xml):
        """
        Internal method that sends request to XML API
        :param xml: xml string
        :return: result in parsed format, e.g. list or dict
        """
        data = requests.request('POST', self.api_url,
                                data=xml,
                                headers=self.headers)
        return xmltodict.parse(data.content.decode())

    def calculate_query(self, query_id):
        """
        Calculate the number of contacts for a query
        :param query_id: id of the query
        :return: results, e.g. error or success and job id
        """
        return self.__send_request(self.generator.calculate_query(query_id=query_id))

    def get_job_status(self, job_id):
        """
        Monitor the status of a job after the data job is initiated
        :param job_id: Identifies a Job that is created and scheduled as a result of another API call.
        :return: Either WAITING, RUNNING, CANCELLED, ERROR, COMPLETE
        """
        return self.__send_request(self.generator.job_status_check(job_id=job_id))

    def export_list(self, target_id,
                     columns,
                     export_format='CSV',
                     export_type='ALL'):
        """
        This method is used to export a Contact List, Query or database
        :param target_id: Unique identifier for the database, query, or contact list
        :param columns: List of the names of columns to export.  EMAIL and RECIPIENT_ID will be added if not there
        :param export_format: either 'CSV' (default), 'TAB' or 'PIPE'
        :param export_type: either 'ALL' (default), 'OPT_IN', 'OPT_OUT', 'UNDELIVERABLE'
        :return: results, e.g. error or success and job id
        """
        return self.__send_request(self.generator.export_query(target_id, columns, export_format, export_type))

    def purge_data(self, target_id, source_id):
        """
        This method deletes all records from a database, suppression, seed, test or contact list (target) based on the contacts that exist in a specific database, contact list, or query (source)
        :param target_id: The ID of the database, Suppression, Seed, Test, or Contact List being purged.
        :param source_id: The ID of the database, Suppression, Seed, Test, or Contact List, or Query that is used to determine which records are deleted.
        :return: results, e.g. error or success and job id
        """
        return self.__send_request(self.generator.purge_data(target_id, source_id))
