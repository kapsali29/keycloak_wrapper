import requests
import json
import requests
from urllib.parse import urljoin

from keycloak_wrapper.keycloak_patterns import USER_TOKEN, WELL_KNOWN, USER_INFO, USER_INTROSPECTION, ADMIN_REALM_USERS, \
    ADMIN_USERS_COUNT, ADMIN_GET_USER, ADMIN_CLIENTS, ADMIN_GET_CLIENT, ADMIN_CLIENT_ROLES, \
    ADMIN_ASSIGN_USER_CLIENT_ROLES


def access_token(keycloak_url, realm, client_id, client_secret, username, password):
    """
    keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    realm: KEYCLOAK REALM NAME
    client_id: KEYCLOAK CLIENT NAME
    client_secret: KEYCLOAK CLIENT SECRET
    username: KEYCLOAK user's USERNAME
    password: KEYCLOAK user's PASSWORD
    """
    params = {"realm-name": realm}
    payload = {"username": username, "password": password, "grant_type": "password", "client_id": client_id,
               "client_secret": client_secret}
    response = requests.post(url=urljoin(keycloak_url, USER_TOKEN).format(**params), data=payload).json()
    return response


def well_known(keycloak_url, realm, access_token):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param access_token: KEYCLOAK user's ACCESS_TOKEN
    :return: WELL KNOWN KEYCLOAK ENDPOINTS
    """
    params = {"realm-name": realm}
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url=urljoin(keycloak_url, WELL_KNOWN).format(**params), headers=headers).json()
    return response


def user_info(keycloak_url, realm, access_token):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param access_token: KEYCLOAK user's ACCESS_TOKEN
    :return: KEYCLOAK USER INFORMATION
    """
    params = {"realm-name": realm}
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url=urljoin(keycloak_url, USER_INFO).format(**params), headers=headers).json()
    return response


def introspect(keycloak_url, realm, client_id, client_secret, access_token):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param client_id: KEYCLOAK CLIENT NAME
    :param client_secret: KEYCLOAK CLIENT SECRET
    :param access_token: KEYCLOAK user's ACCESS_TOKEN
    :return: KEYCLOAK USER DETAILED INFORMATION
    """
    params = {"realm-name": realm}
    payload = {"token": access_token, "client_id": client_id, "client_secret": client_secret}
    response = requests.post(url=urljoin(keycloak_url, USER_INTROSPECTION).format(**params), data=payload).json()
    return response


def realm_users(keycloak_url, realm, admin_token):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm:  KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :return: list of realm users
    """
    params = {"realm-name": realm}
    headers = {"Authorization": "Bearer " + admin_token}
    response = requests.get(url=urljoin(keycloak_url, ADMIN_REALM_USERS).format(**params), headers=headers).json()
    return response


def realm_users_count(keycloak_url, realm, admin_token):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm:  KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :return: number of realm users
    """
    params = {"realm-name": realm}
    headers = {"Authorization": "Bearer " + admin_token}
    response = requests.get(url=urljoin(keycloak_url, ADMIN_USERS_COUNT).format(**params), headers=headers).json()
    return response


def user_keycloak_id(keycloak_url, realm, admin_token, username):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :param username: keycloak username
    :return: KEYCLOAK USER ID
    """
    users = realm_users(keycloak_url, realm, admin_token)
    for user in users:
        this_user_name = json.dumps(user["username"]).strip('"')
        if this_user_name == username:
            return json.dumps(user["id"]).strip('"')
    return None


def get_user(keycloak_url, realm, admin_token, username):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :param username: keycloak username
    :return: KEYCLOAK USER ID
    """
    user_id = user_keycloak_id(keycloak_url, realm, admin_token, username)
    params = {"realm-name": realm, "id": user_id}
    headers = {"Authorization": "Bearer " + admin_token}
    response = requests.get(url=urljoin(keycloak_url, ADMIN_GET_USER).format(**params), headers=headers).json()
    return response


def user_attributes(keycloak_url, realm, admin_token, username):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :param username: keycloak username
    :return: KEYCLOAK USER attributes
    """

    user = get_user(keycloak_url, realm, admin_token, username)
    if "attributes" in user.keys():
        return user['attributes']
    else:
        return None


def realm_clients(keycloak_url, realm, admin_token):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm:  KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :return: realm clients
    """
    params = {"realm-name": realm}
    headers = {"Authorization": "Bearer " + admin_token}
    response = requests.get(url=urljoin(keycloak_url, ADMIN_CLIENTS).format(**params), headers=headers).json()
    return response


def client_keycloak_id(keycloak_url, realm, admin_token, client_name):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm:  KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :param client_name: client name
    :return: client internal keycloak id
    """
    clients = realm_clients(keycloak_url, realm, admin_token)
    for client in clients:
        if client_name == client['clientId']:
            return client["id"]
    return None


def get_client(keycloak_url, realm, admin_token, client_name):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm:  KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :param client_name: client name
    :return: client internal keycloak id
    """
    keycloak_id = client_keycloak_id(keycloak_url, realm, admin_token, client_name)
    params = {"realm-name": realm, "id": keycloak_id}
    headers = {"Authorization": "Bearer " + admin_token}
    response = requests.get(url=urljoin(keycloak_url, ADMIN_GET_CLIENT).format(**params), headers=headers).json()
    return response


def client_roles(keycloak_url, realm, admin_token, client_name):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm:  KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :param client_name: client name
    :return: client internal keycloak id
    """
    keycloak_id = client_keycloak_id(keycloak_url, realm, admin_token, client_name)
    params = {"realm-name": realm, "id": keycloak_id}
    headers = {"Authorization": "Bearer " + admin_token}
    response = requests.get(url=urljoin(keycloak_url, ADMIN_CLIENT_ROLES).format(**params), headers=headers).json()
    return response


def create_role(keycloak_url, realm, admin_token, client_name, new_role_name):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :param client_name: client name
    :param new_role_name: role name
    :return:
    """
    keycloak_id = client_keycloak_id(keycloak_url, realm, admin_token, client_name)
    params = {"realm-name": realm, "id": keycloak_id}
    headers = {"Authorization": "Bearer " + admin_token, "Content-Type": "application/json"}
    payload = {"name": new_role_name, "clientRole": "True"}
    response = requests.post(url=urljoin(keycloak_url, ADMIN_CLIENT_ROLES).format(**params), headers=headers,
                             data=json.dumps(payload)).status_code
    return response


def get_role_id(keycloak_url, realm, admin_token, client_name, role_name):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :param client_name: client name
    :param role_name: role name
    :return: role id
    """
    roles = client_roles(keycloak_url, realm, admin_token, client_name)
    for role in roles:
        if role_name == role['name']:
            return role["id"]
    return None


def assign_role_to_user(keycloak_url, realm, admin_token, client_name, role_name, username):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :param client_name: client name
    :param role_name: role name
    :param username: keycloak username
    :return:
    """
    role_id = get_role_id(keycloak_url, realm, admin_token, client_name, role_name)
    keycloak_id = client_keycloak_id(keycloak_url, realm, admin_token, client_name)
    user_id = user_keycloak_id(keycloak_url, realm, admin_token, username)
    headers = {"Authorization": "Bearer " + admin_token, "Content-Type": "application/json"}
    params = {"realm-name": realm, "id": user_id, "client-id": keycloak_id}
    payload = [{"id": role_id, "name": role_name}]
    response = requests.post(url=urljoin(keycloak_url, ADMIN_ASSIGN_USER_CLIENT_ROLES).format(**params),
                             headers=headers, data=json.dumps(payload)).status_code
    return response


def user_roles(keycloak_url, realm, client_name, client_secret, access_token):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param client_name: keycloak client name
    :param client_secret: client secret
    :param access_token: user's access token
    :return:
    """
    introspection = introspect(keycloak_url, realm, client_name, client_secret, access_token)
    if client_name in introspection['resource_access'].keys():
        return introspection['resource_access'][client_name]["roles"]
    else:
        return "the current user has not roles"


def refresh_token(keycloak_url, realm, client_name, client_secret, refresh_token):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param client_name: keycloak client name
    :param client_secret: keycloak client name
    :param refresh_token: user's refresh token
    :return:
    """
    params = {"realm-name": realm}
    payload = {"client_id": client_name, "grant_type": "refresh_token", "refresh_token": refresh_token,
               "client_secret": client_secret}
    response = requests.post(url=urljoin(keycloak_url, USER_TOKEN).format(**params), data=payload).json()
    return response


def create_user(keycloak_url, realm, admin_token, payload):
    """

    :param keycloak_url: KEYCLOAK URL (http://xxxxx/auth)
    :param realm: KEYCLOAK REALM NAME
    :param admin_token: REALM Admin access token
    :parame payload: POST REQUEST PAYLOAD
    :return: KEYCLOAK USER ID
    """
    params = {"realm-name": realm}
    headers = {"Authorization": "Bearer " + admin_token, "Content-Type": "application/json",
               "Accept": "application/json"}
    response = requests.post(url=urljoin(keycloak_url, ADMIN_REALM_USERS).format(**params), headers=headers,
                             data=json.dumps(payload)).status_code
    return response
