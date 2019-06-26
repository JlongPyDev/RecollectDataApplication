import urllib
import urllib2
import json


def getServiceList(server, port, adminUser, adminPass, token=None):
    ''' Function to get all services
    Requires Admin user/password, as well as server and port (necessary to construct token if one does not exist).
    If a token exists, you can pass one in for use.
    Note: Will not return any services in the Utilities or System folder
    '''

    if token is None:
        token = gentoken(server, port, adminUser, adminPass)

    services = []
    folder = ''
    URL = "http://{}:{}/arcgis/admin/services{}?f=pjson&token={}".format(server, port, folder, token)

    serviceList = json.loads(urllib2.urlopen(URL).read())

    # Build up list of services at the root level
    for single in serviceList["services"]:
        services.append(single['serviceName'] + '.' + single['type'])

    # Build up list of folders and remove the System and Utilities folder (we dont want anyone playing with them)
    folderList = serviceList["folders"]
    folderList.remove("Utilities")
    folderList.remove("System")

    if len(folderList) > 0:
        for folder in folderList:
            URL = "http://{}:{}/arcgis/admin/services/{}?f=pjson&token={}".format(server, port, folder, token)
            fList = json.loads(urllib2.urlopen(URL).read())

            for single in fList["services"]:
                services.append(folder + "//" + single['serviceName'] + '.' + single['type'])

    print services
    return services


def gentoken(server, port, adminUser, adminPass, expiration=60):
    # Re-usable function to get a token required for Admin changes

    query_dict = {'username': adminUser,
                  'password': adminPass,
                  'expiration': str(expiration),
                  'client': 'requestip'}

    query_string = urllib.urlencode(query_dict)
    url = "http://{}:{}/arcgis/admin/generateToken".format(server, port)

    token = json.loads(urllib.urlopen(url + "?f=json", query_string).read())

    if "token" not in token:
        print token['messages']
        exit()
    else:
        # Return the token to the function which called for it
        return token['token']


def stopStartServices(server, port, adminUser, adminPass, stopStart, serviceList, token=None):
    ''' Function to stop, start or delete a service.
    Requires Admin user/password, as well as server and port (necessary to construct token if one does not exist).
    stopStart = Stop|Start|Delete
    serviceList = List of services. A service must be in the <name>.<type> notation
    If a token exists, you can pass one in for use.
    '''

    # Get and set the token
    if token is None:
        token = gentoken(server, port, adminUser, adminPass)

    # modify the services(s)
    for service in serviceList:
        op_service_url = "http://{}:{}/arcgis/admin/services/{}/{}?token={}&f=json".format(server, port, service, stopStart, token)
        status = urllib2.urlopen(op_service_url, ' ').read()

        if 'success' in status:
            print (str(service) + " === " + str(stopStart))
        else:
            print status

    return



