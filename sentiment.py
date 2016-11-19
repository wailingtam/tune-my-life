import requests

_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key = 'd1b04792863949d493c06b8f2f32df9f'


def processRequest(json, headers):
    result = None

    while True:

        response = requests.request('post', _url, json=json, headers=headers)

        if response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content

        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()['error']['message']))

        break

    return result


def analize(imgUrl):
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/json'

    json = {'url': imgUrl}

    result = processRequest(json, headers)

    return result


def analyze_multiple(imgs):
    return [analize(img) for img in imgs]
