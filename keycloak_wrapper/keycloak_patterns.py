USER_TOKEN = "realms/{realm-name}/protocol/openid-connect/token"
WELL_KNOWN = "realms/{realm-name}/.well-known/openid-configuration"
USER_INFO = "realms/{realm-name}/protocol/openid-connect/userinfo"
USER_INTROSPECTION = "realms/{realm-name}/protocol/openid-connect/token/" + \
    "introspect"

# These URLS are used with Realm's admin credentials
ADMIN_REALM_USERS = "admin/realms/{realm-name}/users"
ADMIN_USERS_COUNT = "admin/realms/{realm-name}/users/count"
ADMIN_GET_USER = "admin/realms/{realm-name}/users/{id}"
ADMIN_CLIENTS = "admin/realms/{realm-name}/clients"
ADMIN_GET_CLIENT = "admin/realms/{realm-name}/clients/{id}"
ADMIN_CLIENT_ROLES = "admin/realms/{realm-name}/clients/{id}/roles"
ADMIN_ASSIGN_USER_CLIENT_ROLES = "admin/realms/{realm-name}/users/{id}/" + \
    "role-mappings/clients/{client-id}"
ADMIN_AUTH = "auth/realms/{realm-name}/protocol/openid-connect/token"
