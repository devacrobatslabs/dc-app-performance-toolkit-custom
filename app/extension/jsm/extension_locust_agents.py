import re
import time
from locustio.common_utils import init_logger, jsm_agent_measure, run_as_specific_user  # noqa F401
from util.conf import JSM_SETTINGS

logger = init_logger(app_type='jsm')


@jsm_agent_measure('locust_agent_app_specific_action')
# @run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    r = locust.get('/app/get_endpoint', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    token_pattern_example = '"token":"(.+?)"'
    id_pattern_example = '"id":"(.+?)"'
    token = re.findall(token_pattern_example, content)  # get TOKEN from response using regexp
    id = re.findall(id_pattern_example, content)    # get ID from response using regexp

    logger.locust_info(f'token: {token}, id: {id}')  # log info for debug when verbose is true in jsm.yml file
    if 'assertion string' not in content:
        logger.error(f"'assertion string' was not found in {content}")
    assert 'assertion string' in content  # assert specific string in response content

    body = {"id": id, "token": token}  # include parsed variables to POST request body
    headers = {'content-type': 'application/json'}
    r = locust.post('/app/post_endpoint', body, headers, catch_response=True)  # call app-specific POST endpoint
    content = r.content.decode('utf-8')
    if 'assertion string after successful POST request' not in content:
        logger.error(f"'assertion string after successful POST request' was not found in {content}")
    assert 'assertion string after successful POST request' in content  # assertion after POST request

@jsm_agent_measure("locust_agent_app_property_action")
@run_as_specific_user(username=JSM_SETTINGS.admin_login, password=JSM_SETTINGS.admin_password)
def app_property_action(locust):
    TEST_PROPERTY = 'mytest'

    body = {"anyvalue": time.time()}  # include parsed variables to POST request body
    headers = {
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
    r = locust.post(f"/rest/performance-objectives-for-jira/1.0/api/properties/{TEST_PROPERTY}", 
                    json=body, headers=headers, catch_response=True)  # call app-specific POST endpoint
    # logger.info(f'App Save Custom Property [{TEST_PROPERTY}] HTTP: {r.status_code}') 
    # the record might be created or updated
    if r.status_code != 201 and r.status_code != 200:
        logger.error(f"App Save Custom Property Unexpected response code: {r.status_code}")
    assert r.status_code == 201 or r.status_code == 200  # assertion after POST request

    r = locust.get(f"/rest/performance-objectives-for-jira/1.0/api/properties/{TEST_PROPERTY}", catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    if r.status_code != 200:
        logger.error(f"App Get Custom Property Unexpected response code: {r.status_code}")
    assert r.status_code == 200  # assertion after GET request

    # if TEST_VALUE not in content:
    #     logger.error(f"'{TEST_VALUE}' was not found in {content}")
    # assert TEST_VALUE in content  # assert specific string in response content


@jsm_agent_measure("locust_agent_app_license_action")
def app_license_action(locust):
    r = locust.get('/plugins/servlet/narasyst-performance-objectives/license', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    # logger.locust_info(f'App license check Locust Info')  
    # logger.info(f'App license check') 
    if 'valid' not in content:
        logger.error(f"'valid' was not found in {content}")
    assert 'valid' in content  # assert specific string in response content
