import time

from google.oauth2 import service_account
from google_auth_httplib2 import AuthorizedHttp

from pygsheets.authorization import _SCOPES


class HttpPool:
    def __init__(self, service_accounts, scopes=_SCOPES):
        self.__loop_over = False
        self.__pool = []
        self.__current_http_idx = 0
        for account in service_accounts:
            credentials = service_account.Credentials.from_service_account_file(
                account, scopes=scopes
            )
            http = AuthorizedHttp(credentials)
            self.__pool.append(http)
        super().__init__()

    def get_http_instance(self, errored=False):
        if errored:
            if self.__loop_over:
                time.sleep(100)
                self.__loop_over = False
            self.__current_http_idx += 1
            if self.__current_http_idx > len(self.__pool):
                self.__loop_over = True
                self.__current_http_idx = 0
        return self.__pool[self.__current_http_idx]
