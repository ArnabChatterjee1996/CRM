import requests
from cache_memoize import cache_memoize
from rest_framework import status

from crm.logging import logging
from crm.apiUtils import ApiUtils

globals()['api_utils'] = ApiUtils()

class IntegrationManager:
    @staticmethod
    def search_person_manager(authorization,id,name):
        try:
            logging.info("Entering method : search_person_manager for person with id : {} and name : {}".format(id,name))
            if id is None and name is not None:
                url = "{}".format(api_utils.search_person_by_name_url)
                header_params = {'authorization': authorization}
                params = {'term':name}
                logging.info("Starting API call for person with name : {}".format(name))
                response_from_api = requests.get(url,params=params,headers=header_params)
            else:
                url = "{}{}".format(api_utils.detail_person_url,id)
                header_params = {'authorization': authorization}
                logging.info("Starting API call for person with id : {}".format(id))
                response_from_api = requests.get(url, headers=header_params)
            logging.info("API call ended for person with id : {} and name : {}".format(id,name))
            logging.info("API call ended for person with id : {} and name : {}, response : {}".format(id,name,response_from_api.json()))
            logging.info("Exiting method : search_person_manager")
            return response_from_api
        except Exception as e:
            logging.error("Some error occurred in method : search_person_manager. Exception : {} ".format(e))
            raise Exception(e)

    @staticmethod
    def update_person_manager(authorization,id,data):
        try:
            logging.info("Entering method : update_person_manager for person with id : {} with data : {}".format(id,data))
            url = "{}{}".format(api_utils.detail_person_url, id)
            header_params = {'authorization': authorization}
            logging.info("Starting API call for person with id : {}".format(id))
            response_from_api = requests.put(url, headers=header_params,data=data)
            logging.info("API call ended for person with id : {} , response : {}".format(id,response_from_api.json()))
            logging.info("Exiting method : update_person_manager")
            return response_from_api
        except Exception as e:
            logging.error("Some error occurred in method : update_person_manager. Exception : {} ".format(e))
            raise Exception(e)

    @staticmethod
    def add_note_for_person_manager(authorization,data):
        try:
            logging.info("Entering method : update_person_manager for person with id : {} with data : {}".format(data.get('person_id'),data))
            url = "{}".format(api_utils.add_note_url)
            header_params = {'authorization': authorization,'Content-Type':'application/x-www-form-urlencoded'}
            logging.info("Starting API call for person with id : {}".format(data.get('person_id')))
            response_from_api = requests.post(url, headers=header_params, data=data)
            logging.info("API call ended for person with id : {} , response : {}".format(data.get('person_id'), response_from_api.json()))
            logging.info("Exiting method : update_person_manager")
            return response_from_api
        except Exception as e:
            logging.error("Some error occurred in method : update_person_manager. Exception : {} ".format(e))
            raise Exception(e)


