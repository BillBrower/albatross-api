#--------------------------------------------------------------
# TogglPy is a non-cluttered, easily understood and implemented
# library for interacting with the Toggl API.
#--------------------------------------------------------------
from base64 import b64encode
# parsing json data
import json, requests

#---------------------------------------------
# Class containing the endpoint URLs for Toggl
#---------------------------------------------
class Endpoints():
    @staticmethod
    def CLIENT_PROJECTS(cid):
        return "https://www.toggl.com/api/v8/clients/{}/projects".format(cid)
    CLIENTS = "https://www.toggl.com/api/v8/clients"
    REPORT_WEEKLY = "https://toggl.com/reports/api/v2/weekly"
    REPORT_DETAILED = "https://toggl.com/reports/api/v2/details"
    REPORT_SUMMARY = "https://toggl.com/reports/api/v2/summary"
    TAGS = "https://toggl.com/api/v8/me?since=0&reason=initial+load&with_related_data=true&is_mobile=false&clientversion=4.5.0"
    WORKSPACES = "https://www.toggl.com/api/v8/workspaces"

#-------------------------------------------------------
# Class containing the necessities for Toggl interaction
#-------------------------------------------------------
class Toggl():
    # template of headers for our request
    headers = {
        "Authorization": "",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "python/urllib",
    }

    # default API user agent value
    user_agent = "getalbatross.com"

    #-------------------------------------------------------------
    # Auxiliary methods
    #-------------------------------------------------------------

    def decodeJSON(self, jsonString):
        return json.JSONDecoder().decode(jsonString)

    #-------------------------------------------------------------
    # Methods that modify the headers to control our HTTP requests
    #-------------------------------------------------------------
    def setAPIKey(self, APIKey):
        '''set the API key in the request header'''
        # craft the Authorization
        authHeader = APIKey + ":" + "api_token"
        authHeader = "Basic " + b64encode(authHeader.encode()).decode('ascii').rstrip()

        # add it into the header
        self.headers['Authorization'] = authHeader

    def setUserAgent(self, agent):
        '''set the User-Agent setting, by default it's set to TogglPy'''
        self.user_agent = agent

    #------------------------------------------------------
    # Methods for directly requesting data from an endpoint
    #------------------------------------------------------

    def request(self, endpoint, parameters=None):
        """make a request to the toggle api at a certain endpoint and return the page data as a parsed JSON dict"""
        if parameters == None:
            return requests.get(endpoint, headers=self.headers).json()
        else:
            if 'user_agent' not in parameters:
                parameters.update( {'user_agent' : self.user_agent,} ) # add our class-level user agent in there
            return requests.get(endpoint, headers=self.headers, params=parameters).json()

    #-----------------------------------
    # Methods for getting tag data
    #-----------------------------------
    def getTags(self):
        """return all the tags for a user"""
        response = self.request(Endpoints.TAGS)
        if 'tags' not in response['data']:
            return []
        return response['data']['tags']

    #-----------------------------------
    # Methods for getting workspace data
    #-----------------------------------
    def getWorkspaces(self):
        """return all the workspaces for a user"""
        return self.request(Endpoints.WORKSPACES)

    def getWorkspace(self, name=None, id=None):
        """return the first workspace that matches a given name or id"""
        workspaces = self.getWorkspaces() # get all workspaces

        # if they give us nothing let them know we're not returning anything
        if name == None and id == None:
            print("Error in getWorkspace(), please enter either a name or an id as a filter")
            return None

        if id == None: # then we search by name
            for workspace in workspaces: # search through them for one matching the name provided
                if workspace['name'] == name:
                    return workspace # if we find it return it
            return None # if we get to here and haven't found it return None
        else: # otherwise search by id
            for workspace in workspaces: # search through them for one matching the id provided
                if workspace['id'] == int(id):
                    return workspace # if we find it return it
            return None # if we get to here and haven't found it return None

    #--------------------------------
    # Methods for getting client data
    #--------------------------------
    def getClients(self):
        """return all clients that are visable to a user"""
        clients = self.request(Endpoints.CLIENTS)
        if clients is None:
            return []
        return clients

    def getClient(self, name=None, id=None):
        """return the first workspace that matches a given name or id"""
        clients = self.getClients() # get all clients

        # if they give us nothing let them know we're not returning anything
        if name == None and id == None:
            print("Error in getClient(), please enter either a name or an id as a filter")
            return None

        if id == None: # then we search by name
            for client in clients: # search through them for one matching the name provided
                if client['name'] == name:
                    return client # if we find it return it
            return None # if we get to here and haven't found it return None
        else: # otherwise search by id
            for client in clients: # search through them for one matching the id provided
                if client['id'] == int(id):
                    return client # if we find it return it
            return None # if we get to here and haven't found it return None

    def getClientProjects(self, client_id=None):
        """return all projects for the given client that are visable to a user"""
        if client_id == None:
            print("Error in getClientProjects(), please enter a clint id as a filter")
            return None
        return self.request(Endpoints.CLIENT_PROJECTS(client_id))

    #---------------------------------
    # Methods for getting reports data
    #---------------------------------
    def getWeeklyReport(self, data):
        """return a weekly report for a user"""
        return self.request(Endpoints.REPORT_WEEKLY, parameters=data)

    def getWeeklyReportPDF(self, data, filename):
        """save a weekly report as a PDF"""
        # get the raw pdf file data
        filedata = self.requestRaw(Endpoints.REPORT_WEEKLY + ".pdf", parameters=data)

        # write the data to a file
        with open(filename, "wb") as pdf:
            pdf.write(filedata)

    def getDetailedReport(self, data):
        """return a detailed report for a user"""
        return self.request(Endpoints.REPORT_DETAILED, parameters=data)

    def getDetailedReportPDF(self, data, filename):
        """save a detailed report as a pdf"""
        # get the raw pdf file data
        filedata = self.requestRaw(Endpoints.REPORT_DETAILED + ".pdf", parameters=data)

        # write the data to a file
        with open(filename, "wb") as pdf:
            pdf.write(filedata)

    def getSummaryReport(self, data):
        """return a summary report for a user"""
        return self.request(Endpoints.REPORT_SUMMARY, parameters=data)

    def getSummaryReportPDF(self, data, filename):
        """save a summary report as a pdf"""
        # get the raw pdf file data
        filedata = self.requestRaw(Endpoints.REPORT_SUMMARY + ".pdf", parameters=data)

        # write the data to a file
        with open(filename, "wb") as pdf:
            pdf.write(filedata)