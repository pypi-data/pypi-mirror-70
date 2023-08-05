import requests

root_url = 'https://tryhackme.com'


class THM(object):
    """
    TryHackMe API Wrapper
    """

    def __init__(self, credentials=None):
        """
        Initializes the API Wrapper

        :type credentials: dict
        :param credentials: (Optional) Credentials for use with authenticated requests
        """

        self.session = requests.Session()

        # if (credentials is not None) and (type(credentials) == dict):
        #     if ('username' in credentials) and ('password' in credentials):
        #         self.__login(credentials)

        print(self.get_stats())

    def get_stats(self) -> dict:
        """
        Returns public and cloneable room count and current user count

        :return: Dict containing mentioned values
        """

        path = f'{root_url}/api/getstats'

        try:
            r = self.session.get(path)

            if r.status_code == 200:
                return r.json()
            else:
                raise Exception('HTTP Response was not 200')
        except Exception as err:
            raise err
