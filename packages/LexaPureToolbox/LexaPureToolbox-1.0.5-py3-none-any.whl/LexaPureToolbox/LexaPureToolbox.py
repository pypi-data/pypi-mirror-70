import requests
import math
import pymysql
import datetime as dt
import sys
from slacker import Slacker


class KonnectiveToolbox:
    def __init__(self, username, password):
        self.baseurl = 'https://api.konnektive.com/'
        self.username = username
        self.password = password

    def create_url(self, endpoint=None):
        if endpoint is not None:
            return '{}{}/query/?loginId={}&password={}'.format(self.baseurl, endpoint, self.username, self.password)
        else:
            raise Exception('Endpoint is not defined.')

    def get_json(self, url, method='GET', *args):
        arg = '&'.join(args)
        baseURL = '&'.join([url, arg])
        print('Base URL: {}\n'.format(baseURL))

        if 'page=' in arg:
            r = requests.request(method, baseURL)
            return r.json()

        _list = []
        page = 1
        while True:
            url = '&'.join([baseURL, 'page={}'.format(page)])
            _json = requests.request(method, url).json()
            totalResults = _json['message']['totalResults']
            resultsPerPage = _json['message']['resultsPerPage']
            maxPage = math.ceil(int(totalResults) / int(resultsPerPage))

            if page > maxPage:
                print('\n')
                return _list

            comp = int((page / maxPage) * 100)
            remain = 100 - comp
            sys.stdout.write('\rProcessing page {} of {}[{}{}]'.format(page, maxPage, '#' * comp, '.' * remain))
            sys.stdout.flush()

            for _data in _json['message']['data']:
                _list.append(_data)
            page += 1

    def checkIfNone(self, value, _type='STR'):
        if _type == 'STR' and value is not None:
            return '"{}"'.format(value)
        elif _type == 'INT' and value is not None:
            return value
        elif value is None:
            return 'NULL'
        elif _type == 'STR' and len(value) == 0:
            return 'NULL'
        else:
            return 'NULL'

    def remError(self, value):
        if value is None:
            return None

        errorChars = {
            '"': "'",
            '\\': '/',
            '\u200b': '',
            '\u2105': 'c/o',
            '\u0101': 'a'
        }

        for errorChar in errorChars:
            value = value.replace(errorChar, errorChars.get(errorChar))

        return value


class OntraportToolbox:
    def __init__(self, version=1, api_key='', api_appid=''):
        self.version = version
        self.api_key = api_key
        self.api_appid = api_appid
        self.base_url = 'https://api.ontraport.com/'
        self.headers = {'Api-Key': api_key, 'Api-Appid': api_appid}

    def get_request(self, endpoint, **kwargs):
        url = f'{self.base_url}{self.version}/{endpoint}'
        params = ''
        for kwarg in kwargs:
            params += f'{kwarg}={kwargs.get(kwarg)}&'

        url = f'{url}?{params[:-1]}' if len(kwargs) != 0 else url
        r = requests.get(url, headers=self.headers)
        print(f'Response: {r.status_code} {r.reason} | URL: {url}')
        return r


class MySQLToolbox:
    def __init__(self, sqlPath, host, user, password, db):
        self.sqlPath = sqlPath
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def readQuery(self, qry, _type):
        if _type == 'f':
            with open('{}{}'.format(self.sqlPath, qry), 'r') as f:
                fString = f.read()
        elif _type == 'q':
            fString = qry
        else:
            raise Exception('Invalid readFile type.')

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        cursor.execute(fString)
        data = cursor.fetchall()
        db.close()

        return data

    def runQuery(self, qry):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()

        try:
            # Execute the SQL command
            cursor.execute(qry)
            db.commit()
            return 'Passed'
        except Exception as e:
            db.rollback()
            return 'Failed', e
        finally:
            db.close()

    def createQuery(self, table=None, values=None, dups=None):
        if table is None or values is None:
            raise Exception('Error in creating query. The following are required:\n\tTable Name\n\tValues')

        if dups is not None:
            return 'INSERT INTO {}.{} VALUES\n{}\nON DUPLICATE KEY UPDATE\n{}'.format(self.db, table, values, dups)
        else:
            return 'INSERT INTO {}.{} VALUES\n{}'.format(self.db, table, values)

    def stringfy(self, _string):
        if _string is None or _string == '' or _string == 'NULL':
            return 'NULL'
        else:
            if "'" in _string:
                _string = _string.replace("'", '\\"')
            return "'{}'".format(str(_string))

    def convert_date(self, dateString, fromFormat, toFormat):
        if dateString is None:
            return 'NULL'
        else:
            dateString = dt.datetime.strptime(dateString, fromFormat)
            return self.stringfy(dt.datetime.strftime(dateString, toFormat))

    def convert_unix_datetime(self, unix_int, _format='%Y-%m-%d %H:%M:%S'):
        if unix_int == '' or unix_int is None or unix_int == 0 or unix_int == '0':
            return 'NULL'

        try:
            unix_int = unix_int.replace("'", '') if "'" in unix_int else unix_int
            return dt.datetime.utcfromtimestamp(int(unix_int)).strftime(_format)
        except Exception as err:
            raise Exception(err)



class slackToolbox:
    def __init__(self, _key, _channel):
        self._key = _key
        self._channel = _channel

    def send_message(self, scriptname='-', funcname='-', description='-'):
        _message = 'Python File: {}\n' \
                   'Function Name: {}\n' \
                   'Description: {}'.format(scriptname, funcname, description)
        slack = Slacker(self._key)
        slack.chat.post_message(self._channel, _message)

    def send_info(self, description='-'):
        _message = f'Information: {description}'
        slack = Slacker(self._key)
        slack.chat.post_message(self._channel, _message)
