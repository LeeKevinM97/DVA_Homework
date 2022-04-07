import http.client
import json
import csv
import itertools
import collections
from collections import Counter


#############################################################################################################################
# cse6242 
# All instructions, code comments, etc. contained within this notebook are part of the assignment instructions.
# Portions of this file will auto-graded in Gradescope using different sets of parameters / data to ensure that values are not
# hard-coded.
#
# Instructions:  Implement all methods in this file that have a return
# value of 'NotImplemented'. See the documentation within each method for specific details, including
# the expected return value
#
# Helper Functions:
# You are permitted to write additional helper functions/methods or use additional instance variables within
# the `Graph` class or `TMDbAPIUtils` class so long as the originally included methods work as required.
#
# Use:
# The `Graph` class  is used to represent and store the data for the TMDb co-actor network graph.  This class must
# also provide some basic analytics, i.e., number of nodes, edges, and nodes with the highest degree.
#
# The `TMDbAPIUtils` class is used to retrieve Actor/Movie data using themoviedb.org API.  We have provided a few necessary methods
# to test your code w/ the API, e.g.: get_movie_cast(), get_movie_credits_for_person().  You may add additional
# methods and instance variables as desired (see Helper Functions).
#
# The data that you retrieve from the TMDb API is used to build your graph using the Graph class.  After you build your graph using the
# TMDb API data, use the Graph class write_edges_file & write_nodes_file methods to produce the separate nodes and edges
# .csv files for use with the Argo-Lite graph visualization tool.
#
# While building the co-actor graph, you will be required to write code to expand the graph by iterating
# through a portion of the graph nodes and finding similar artists using the TMDb API. We will not grade this code directly
# but will grade the resulting graph data in your Argo-Lite graph snapshot.
#
#############################################################################################################################

global checker

class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]


    def add_node(self, id: str, name: str) -> None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        # Search self.nodes for existing node already, if not found, append self.nodes with new node
        global checker
        if (id, name) not in self.nodes:
            self.nodes.append((id, name))
            checker = True
        #    print("Append checker: " + str(checker))
        else:
            checker = False
        #    print("Append checker: " + str(checker))
        return None


    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        if source == target:
            return None
        # Search self.edges for existing edge (a,b) or (b,a), if not found, append self.edges with new edge
        if (((source, target) not in self.edges) and ((target, source) not in self.edges)):
            self.edges.append((source, target))
        return None


    def total_nodes(self) -> int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        # Integer return from length of self.nodes
        return len(self.nodes)


    def total_edges(self) -> int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        # Integer return from length of self.edges
        return len(self.edges)


    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        # For each actor ID, we want to see how many edges are attached to said node
        # Each actor ID, search through self.edges on both source and target to determine quantity of edges on that node
        # Create a dictionary, then return only max degrees?
        degs = {}
        maxs = {}
        non_leaf_nodes = {}

        #for i in range(0, len(self.nodes)):
        #    degree = 0
        #    for j in range(0, len(self.edges)):
        #        if self.nodes[i][0] == self.edges[j][0] or self.nodes[i][0] == self.edges[j][1]:
        #            degree += 1
        #    degs[self.nodes[i][0]] = degree

        for id, name in self.nodes:
            degree = 0
            for source, target in self.edges:
                if id == source or id == target:
                    degree += 1
            degs[id] = degree

        max_deg = max(degs.values())
        for key, value in degs.items():
            if int(value) > 1:
                non_leaf_nodes[key] = value
        for key, value in degs.items():
            if int(value) == max_deg:
                maxs[key] = value
        print("Leaf Nodes: ", len(non_leaf_nodes))
        print(maxs)
        return maxs


    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)


    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)


    # Do not modify
    def write_edges_file(self, path="edges.csv")->None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")


    # Do not modify
    def write_nodes_file(self, path="nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")



class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key


    def get_movie_cast(self, movie_id:str, limit:int=None, exclude_ids:list=None) -> list:
        """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param string movie_id: a numerical movie_id
        :param integer limit: maximum number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If after excluding, there are fewer cast members than the specified limit, then return the remaining members (excluding the ones whose order values are outside the limit range). 
            If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
            If after excluding, the limit is not specified, then return all remaining cast members."
            e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded,
            return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'id': 97909 # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit, ...}, ... ]
                Note that this is an example of the structure of the list and some of the fields returned by the API.
                The result of the API call will include many more fields for each cast member.

        Important: the exclude_ids processing should occur prior to limiting output.
        """
        # Get movie cast for a Movie ID - optional:  exclude cast or limit quantity of cast
        # Parameters:  string movie_id | integer limit
        # Limit is a restriction on order, LIMIT = 5 means Order < 5
        # 

        # Connect API for get-movie-credits
        conn = http.client.HTTPSConnection("api.themoviedb.org")
        conn.request("GET", "/3/movie/{0}/credits?api_key={1}&language=en-US".format(movie_id, self.api_key))
        resp = conn.getresponse()
        #print(resp.status, resp.reason)
        if (resp.status == 200):
            # Grabs API data and reads as a json string, then deserialize JSON String into a Python Dictionary
            raw_cast = json.loads(resp.read())["cast"]
            limit_cast = []
            cast = []
            # Iterates through API "Cast" Dictionary and filters order < limit
            if limit is not None:
                for i in range(0, len(raw_cast)):
                    if raw_cast[i]["order"] < limit:
                        limit_cast.append(raw_cast[i])
            else:
                for i in range(0, len(raw_cast)):
                    limit_cast.append(raw_cast[i])
            # Exclusion list needs to be removed from the results
            if exclude_ids is not None:
                for i in range(0, len(limit_cast)):
                    if limit_cast[i]["id"] not in exclude_ids:
                        cast.append(limit_cast[i])
            else:
                for i in range(0, len(limit_cast)):
                    cast.append(limit_cast[i])
        return cast


    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
        :rtype: list
            return a list of dicts, one dict per movie credit with the following structure:
                [{'id': 97909 # the id of the movie credit
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """
        # Connect API for get-movie-credits
        conn = http.client.HTTPSConnection("api.themoviedb.org")
        conn.request("GET", "/3/person/{0}/movie_credits?api_key={1}&language=en-US".format(person_id, self.api_key))
        resp = conn.getresponse()
        #print(resp.status, resp.reason)
        if (resp.status == 200):
            # Grabs API data and reads as a json string, then deserialize JSON String into a Python Dictionary
            raw_cast = json.loads(resp.read())["cast"]
            cast = []
            # Iterates through API "Raw Cast" Dictionary and filters vote average < threshold
            if vote_avg_threshold is not None:
                for i in range(0, len(raw_cast)):
                    if raw_cast[i]["vote_average"] >= vote_avg_threshold:
                        cast.append(raw_cast[i])
            else:
                for i in range(0, len(raw_cast)):
                    cast.append(raw_cast[i])
        return cast


#############################################################################################################################
#
# BUILDING YOUR GRAPH
#
# Working with the API:  See use of http.request: https://docs.python.org/3/library/http.client.html#examples
#
# Using TMDb's API, build a co-actor network for the actor's/actress' highest rated movies
# In this graph, each node represents an actor
# An edge between any two nodes indicates that the two actors/actresses acted in a movie together
# i.e., they share a movie credit.
# e.g., An edge between Samuel L. Jackson and Robert Downey Jr. indicates that they have acted in one
# or more movies together.
#
# For this assignment, we are interested in a co-actor network of highly rated movies; specifically,
# we only want the top 3 co-actors in each movie credit of an actor having a vote average >= 8.0.
# Build your co-actor graph on the actor 'Laurence Fishburne' w/ person_id 2975.
#
# You will need to add extra functions or code to accomplish this.  We will not directly call or explicitly grade your
# algorithm. We will instead measure the correctness of your output by evaluating the data in your argo-lite graph
# snapshot.
#
# GRAPH SIZE
# With each iteration of your graph build, the number of nodes and edges grows approximately at an exponential rate.
# Our testing indicates growth approximately equal to e^2x.
# Since the TMDB API is a live database, the number of nodes / edges in the final graph will vary slightly depending on when
# you execute your graph building code. We take this into account by rebuilding the solution graph every few days and
# updating the auto-grader.  We establish a bound for lowest & highest encountered numbers of nodes and edges with a
# margin of +/- 100 for nodes and +/- 150 for edges.  e.g., The allowable range of nodes is set to:
#
# Min allowable nodes = min encountered nodes - 100
# Max allowable nodes = max allowable nodes + 100
#
# e.g., if the minimum encountered nodes = 507 and the max encountered nodes = 526, then the min/max range is 407-626
# The same method is used to calculate the edges with the exception of using the aforementioned edge margin.
# ----------------------------------------------------------------------------------------------------------------------
# BEGIN BUILD CO-ACTOR NETWORK
#
# INITIALIZE GRAPH
#   Initialize a Graph object with a single node representing Laurence Fishburne
#
# BEGIN BUILD BASE GRAPH:
#   Find all of Laurence Fishburne's movie credits that have a vote average >= 8.0
#   FOR each movie credit:
#   |   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
#   |
#   |   FOR each movie cast member:
#   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
#   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actress) node
#   |   |   and each new node (co-actor/co-actress)
#   |   END FOR
#   END FOR
# END BUILD BASE GRAPH
#
#
# BEGIN LOOP - DO 2 TIMES:
#   IF first iteration of loop:
#   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
#   ELSE
#   |    nodes = The nodes added in the previous iteration:
#   ENDIF
#
#   FOR each node in nodes:
#   |  get the movie credits for the actor that have a vote average >= 8.0
#   |
#   |   FOR each movie credit:
#   |   |   try to get the 3 movie cast members having an 'order' value between 0-2
#   |   |
#   |   |   FOR each movie cast member:
#   |   |   |   IF the node doesn't already exist:
#   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
#   |   |   |   ENDIF
#   |   |   |
#   |   |   |   IF the edge does not exist:
#   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)
#   |   |   |   ENDIF
#   |   |   END FOR
#   |   END FOR
#   END FOR
# END LOOP
#
# Your graph should not have any duplicate edges or nodes
# Write out your finished graph as a nodes file and an edges file using:
#   graph.write_edges_file()
#   graph.write_nodes_file()
#
# END BUILD CO-ACTOR NETWORK
# ----------------------------------------------------------------------------------------------------------------------

# Exception handling and best practices
# - You should use the param 'language=en-US' in all API calls to avoid encoding issues when writing data to file.
# - If the actor name has a comma char ',' it should be removed to prevent extra columns from being inserted into the .csv file
# - Some movie_credits may actually be collections and do not return cast data. Handle this situation by skipping these instances.
# - While The TMDb API does not have a rate-limiting scheme in place, consider that making hundreds / thousands of calls
#   can occasionally result in timeout errors. If you continue to experience 'ConnectionRefusedError : [Errno 61] Connection refused',
#   - wait a while and then try again.  It may be necessary to insert periodic sleeps when you are building your graph.
  

def return_name()->str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    GT_Username = "klee876"
    return GT_Username


def return_argo_lite_snapshot()->str:
    """
    Return the shared URL of your published graph in Argo-Lite
    """
    url = "https://poloclub.github.io/argo-graph-lite/#b04d4e1e-6092-4bce-8efa-3db5e38ce830"
    return url



# You should modify __main__ as you see fit to build/test your graph using  the TMDBAPIUtils & Graph classes.
# Some boilerplate/sample code is provided for demonstration. We will not call __main__ during grading.

if __name__ == "__main__":

    # API Key
    tmdb_api_utils = TMDBAPIUtils(api_key='c935d5c3baf9bbff7e1ba2ff5c73ea5f')

    # Initialize Graph
    graph = Graph()

    # Base node (id , person) -> find all movie credits from base node with > 8.0 vote avg
    graph.add_node(id='2975', name='Laurence Fishburne')
    credits = tmdb_api_utils.get_movie_credits_for_person(graph.nodes[0][0], 8.0)
    # For each movie credit, we want to get order 0-2, main 3 actors
    # Begin BASE GRAPH
    for i in range(0, len(credits)):
        casts = []
        casts = tmdb_api_utils.get_movie_cast(credits[i]["id"], 3)
        for j in range(0, len(casts)):
            graph.add_node(str(casts[j]["id"]), casts[j]["name"].replace(",", ""))
            graph.add_edge(graph.nodes[0][0], str(casts[j]["id"]))

    # Loop twice
    nodes_add = []
    global checker
    checker = True
    for x in range(0,2):
        if x == 0:
            nodes = graph.nodes.copy()
        else:
            nodes = nodes_add.copy()
        for n in range(0,len(nodes)):
            credits = tmdb_api_utils.get_movie_credits_for_person(graph.nodes[n][0], 8.0)
            for i in range(0, len(credits)):
                casts = tmdb_api_utils.get_movie_cast(credits[i]["id"], 3)
                for j in range(0, len(casts)):
                    #if (str(casts[j]["id"]),"*") not in graph.nodes:
                    #    graph.add_node(str(casts[j]["id"]), casts[j]["name"].replace(",", ""))
                    #    nodes_add.append((str(casts[j]["id"]), casts[j]["name"].replace(",", "")))
                    #graph.add_edge(str(graph.nodes[n][0]), str(casts[j]["id"]))
                    graph.add_node(str(casts[j]["id"]), casts[j]["name"].replace(",", ""))
                    #print("Loop checker: " + str(checker))
                    if checker == True:
                        nodes_add.append((str(casts[j]["id"]), casts[j]["name"].replace(",", "")))
                    graph.add_edge(str(graph.nodes[n][0]), str(casts[j]["id"]))
    # call functions or place code here to build graph (graph building code not graded)
    # Suggestion: code should contain steps outlined above in BUILD CO-ACTOR NETWORK
    graph.max_degree_nodes()
    graph.write_edges_file()
    graph.write_nodes_file()

    # If you have already built & written out your graph, you could read in your nodes & edges files
    # to perform testing on your graph.
    # graph = Graph(with_edges_file="edges.csv", with_nodes_file="nodes.csv")