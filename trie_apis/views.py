from .models import LocationTrieDb
from django.http import HttpResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from ratelimit.decorators import ratelimit
from rest_framework.permissions import IsAuthenticated
import json


def search_helper(prefix, node_id, current_index=0, string_location=''):
    try:
        node_instance = LocationTrieDb.objects.get(pk=node_id)
    except Exception as e:
        return []
    if node_instance is None:
        return []
    string_location += node_instance.node_value
    if current_index >= len(prefix):
        ret_list = []
        if node_instance.is_end:
            ret_list.append((string_location, node_instance.popularity))
        for i in range(len(node_instance.children)):
            ret_list += search_helper(prefix, node_instance.children[i],
                                      current_index+1, string_location)
        return ret_list
    else:
        if prefix[current_index] != node_instance.node_value:
            return []
        ret_list = []
        if node_instance.is_end and current_index == len(prefix)-1:
            ret_list.append((string_location, node_instance.popularity))
        for i in range(len(node_instance.children)):
            if current_index < len(prefix)-1 and \
                    prefix[:current_index + 2] == node_instance.children[i]:
                ret_list += search_helper(prefix, node_instance.children[i],
                                          current_index + 1, string_location)
            elif current_index >= len(prefix)-1:
                ret_list += search_helper(prefix, node_instance.children[i],
                                          current_index + 1, string_location)
        return ret_list


@ratelimit(key='ip', rate='10/s', method=ratelimit.ALL, block=True)
def search(request):
    try:
        if request.method == 'GET':
            prefix = request.GET.get('term')

            auto_complete_suggestions = []
            node_instance = LocationTrieDb.objects.get(pk='0')
            print('hwllo')
            for i in range(len(node_instance.children)):
                auto_complete_suggestions += search_helper(prefix=prefix,
                                                           node_id=node_instance.children[i],
                                                           current_index=0, string_location='')
            auto_complete_suggestions.sort()
            auto_complete_suggestions_dict = []
            for location in auto_complete_suggestions:
                auto_complete_suggestions_dict.append({'location': location[0],
                                                       'popularity': location[1]})
            json_result = json.dumps({"list_of_suggestions": auto_complete_suggestions_dict})
            return HttpResponse(json_result, content_type="application/json",
                                status=status.HTTP_200_OK)
        else:
            return HttpResponse('Wrong request format', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(e, content_type='test/plain', status=status.HTTP_400_BAD_REQUEST)


@ratelimit(key='ip', rate='50/s', method=ratelimit.ALL, block=True)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@csrf_exempt
def add(request):
    try:
        if request.method == 'POST':

            location = str(request.POST.get('location'))
            popularity = str(request.POST.get('popularity'))

            try:
                current_node_instance = LocationTrieDb.objects.get(pk='0')
            except Exception as e:
                new_node = LocationTrieDb()
                new_node.node_id = '0'
                new_node.is_end = False
                new_node.children = []
                new_node.save()
                current_node_instance = new_node

            prefix_string = ''
            for i in location:
                prefix_string += i
                if prefix_string in current_node_instance.children:
                    current_node_instance = LocationTrieDb.objects.get(pk=prefix_string)
                else:
                    new_node = LocationTrieDb()
                    new_node.node_id = prefix_string
                    new_node.is_end = False
                    new_node.children = []
                    new_node.node_value = i
                    current_node_instance.children.append(prefix_string)
                    current_node_instance.save()
                    new_node.save()
                    current_node_instance = new_node

            current_node_instance.popularity = popularity

            if not current_node_instance.is_end:
                current_node_instance.is_end = True
                current_node_instance.save()
                return HttpResponse('Location added successfully', status=status.HTTP_200_OK)
            else:
                return HttpResponse('Location already exists',
                                    status=status.HTTP_208_ALREADY_REPORTED)
        else:
            return HttpResponse('Wrong request format', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(e, content_type='test/plain', status=status.HTTP_400_BAD_REQUEST)


@ratelimit(key='ip', rate='50/s', method=ratelimit.ALL, block=True)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@csrf_exempt
def change_popularity(request):
    try:
        if request.method == 'POST':

            location = str(request.POST.get('location'))
            popularity = str(request.POST.get('popularity'))

            try:
                current_node_instance = LocationTrieDb.objects.get(pk=location)
                current_node_instance.popularity = popularity
                current_node_instance.save()
                return HttpResponse('Popularity Updated', status=status.HTTP_200_OK)
            except Exception as e:
                return HttpResponse('Location does not exist. Add location first.',
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse('Wrong request format', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(e, content_type='test/plain', status=status.HTTP_400_BAD_REQUEST)


def delete_location_helper(location, current_index, current_node):
    if current_index == len(location):
        if not current_node.is_end:
            raise Exception('Location does not exist')
        current_node.is_end = False
        if len(current_node.children) == 0:
            current_node.delete()
            return True
        else:
            current_node.save()
            return False

    prefix = location[:current_index+1]
    if prefix not in current_node.children:
        raise Exception('Location does not exist')
    can_delete = delete_location_helper(location, current_index+1,
                                        LocationTrieDb.objects.get(pk=prefix))
    if can_delete:
        if len(current_node.children) == 1:
            current_node.delete()
            return True
        else:
            print(current_node, prefix)
            current_node.children.remove(prefix)
            current_node.save()
            return False
    else:
        return False


@ratelimit(key='ip', rate='10/s', method=ratelimit.ALL, block=True)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@csrf_exempt
def delete_location(request):
    try:
        if request.method == 'POST':
            location = str(request.POST.get('location'))
            node_instance = LocationTrieDb.objects.get(pk='0')
            try:
                delete_location_helper(location, 0, node_instance)
            except Exception as e:
                return HttpResponse(e, content_type='test/plain',
                                    status=status.HTTP_404_NOT_FOUND)
            return HttpResponse('Location deleted successfully', status=status.HTTP_200_OK)
        else:
            return HttpResponse('Wrong request format', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(e, content_type='test/plain', status=status.HTTP_400_BAD_REQUEST)