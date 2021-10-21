from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from crm.logging import logging
from .serializers import UpdatePersonSerializer,AddNoteForPersonSerializer
from integration.managers import IntegrationManager


## This method is only to check if the server is up
@api_view(['GET'])
def server_health(request):
    return Response({"health_status": "OK"}, status=status.HTTP_200_OK)

## This method is used to search persons based on their id or name.
## If id is provided , we'll search by ID itself but if ID is not provided
## and only name is provided , then we'll search with the name
@api_view(['GET'])
def search_person(request):
    try:
        logging.info("Entering method : search_person with request : {}".format(request.data))
        authorization = request.META.get('HTTP_AUTHORIZATION')
        id = request.GET.get('id')
        name = request.GET.get('name')
        if id is None:
            if name is None:
                return Response({"status": "Failure",
                                 "message": "Unable to search person because person id and name are both None",
                                 "data": None},
                                status=status.HTTP_400_BAD_REQUEST)
        person_search_details = IntegrationManager.search_person_manager(authorization,id=id,name=name)
        logging.info("Exiting method : search_person")
        if person_search_details.status_code==status.HTTP_404_NOT_FOUND:
            return Response({"status": "Failure",
                         "message": "Person not found",
                         "data":person_search_details.json()},
                        status=person_search_details.status_code)
        elif person_search_details.status_code==status.HTTP_200_OK:
            ## while searching with name even though there are no results, pipedrive API will show success
            ## However we feel that it's a failure and therefore checking if the data is null or not
            ## Only if the status code is 200 and data is not null , we'll mention it as a success response
            if person_search_details.json().get('data') is not None:
                return Response({"status": "Success",
                             "message": "Person found successfully",
                             "data":person_search_details.json()},
                            status=person_search_details.status_code)
            else:
                return Response({"status": "Failure",
                                 "message": "Person not found",
                                 "data": person_search_details.json()},
                                status=status.HTTP_404_NOT_FOUND)
        elif person_search_details.status_code==status.HTTP_401_UNAUTHORIZED:
            return Response({"status": "Unauthorized",
                         "message": "Person not found",
                         "data":person_search_details.json()},
                        status=person_search_details.status_code)
        else:
            logging.error(person_search_details)
            return Response({"status": "Failure",
                             "message": "Some error occurred while retrieving the data",
                             "data":person_search_details.json()},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logging.error("Some error occurred in method : search_person. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

## This method is used to update a person based on the ID
@api_view(['PUT'])
def update_person(request):
    try:
        logging.info("Entering method : update_person with request : {}".format(request.data))
        id = request.GET.get('id')
        if id is None:
            return Response({"status": "Failure",
                      "message": "Unable to update person because person id is None",
                      "data": None},
                     status=status.HTTP_400_BAD_REQUEST)
        data = UpdatePersonSerializer(data=request.data)
        if data.is_valid():
            authorization = request.META.get('HTTP_AUTHORIZATION')
            person_update_details = IntegrationManager.update_person_manager(authorization,id,data.validated_data)
            logging.info("Exiting method : update_person")
            if person_update_details.status_code == status.HTTP_404_NOT_FOUND:
                return Response({"status": "Failure",
                                 "message": "Unable to update person",
                                 "data": person_update_details.json()},
                                status=person_update_details.status_code)
            elif person_update_details.status_code == status.HTTP_200_OK:
                return Response({"status": "Success",
                                 "message": "Person updated successfully",
                                 "data": person_update_details.json()},
                                status=person_update_details.status_code)
            elif person_update_details.status_code == status.HTTP_401_UNAUTHORIZED:
                return Response({"status": "Unauthorized",
                                 "message": "Unable to update person",
                                 "data": person_update_details.json()},
                                status=person_update_details.status_code)
            else:
                logging.error(person_update_details)
                return Response({"status": "Failure",
                                 "message": "Some error occurred while retrieving the data",
                                 "data": person_update_details.json()},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logging.error("serializer errors for person with id : {}. Error : {}".format(id,data.errors))
            return Response({"status": "Failure",
                             "message": "Unable to update person because of serializer errors",
                             "data": data.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error("Some error occurred in method : update_person. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

## This method is used to add note for a person . ID is mandatory
## for this method
@api_view(['POST'])
def add_note_for_person(request):
    try:
        logging.info("Entering method : add_note_for_person with request : {}".format(request.data))
        data = AddNoteForPersonSerializer(data=request.data)
        if data.is_valid():
            authorization = request.META.get('HTTP_AUTHORIZATION')
            add_note_for_person_details = IntegrationManager.add_note_for_person_manager(authorization,data.validated_data)
            logging.info("Exiting method : add_note_for_person")
            if add_note_for_person_details.status_code == status.HTTP_400_BAD_REQUEST:
                return Response({"status": "Failure",
                                 "message": "Unable to add note for person",
                                 "data": add_note_for_person_details.json()},
                                status=add_note_for_person_details.status_code)
            elif add_note_for_person_details.status_code == status.HTTP_201_CREATED:
                return Response({"status": "Success",
                                 "message": "note added for person successfully",
                                 "data": add_note_for_person_details.json()},
                                status=add_note_for_person_details.status_code)
            elif add_note_for_person_details.status_code == status.HTTP_401_UNAUTHORIZED:
                return Response({"status": "Unauthorized",
                                 "message": "Unable to add note for person",
                                 "data": add_note_for_person_details.json()},
                                status=add_note_for_person_details.status_code)
            else:
                logging.error(add_note_for_person_details)
                return Response({"status": "Failure",
                                 "message": "Some error occurred while retrieving the data",
                                 "data": add_note_for_person_details.json()},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logging.error("serializer errors while adding note for person Error : {}".format(data.errors))
            return Response({"status": "Failure",
                             "message": "Unable to add note for person because of serializer errors",
                             "data": data.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error("Some error occurred in method : add_note_for_person. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)