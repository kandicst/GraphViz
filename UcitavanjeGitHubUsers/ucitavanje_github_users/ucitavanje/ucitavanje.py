import random
from collections import OrderedDict

import requests
from core_module.services.ucitati import UcitatiService
from core_module.models import Node, Attribute, Link

# for api
tok = 'e1250f8e4e39d52b4e307e7901f2f26a222f4762 '
headers = {'Authorization': 'token %s' % tok}


class UcitavanjeGithub(UcitatiService):
    def __init__(self):
        self.queue = OrderedDict()
        self.visited_nodes = set()
        self.limit = 10
        self.current_depth = 0
        self.main_username = ""
        self.cached_users_json = {}

    @property
    def path_to_cached_files(self):
        return "plugin_data/" + self.identifier() + "/cached_files/"

    def naziv(self):
        return "Github korisnici i njihovi pratioci"

    def identifier(self):
        return "ucitavanje_github_usera"

    def form_fields(self):
        return [{"type": "text", "id": "username", "text": "Username", "value": "ssttefann"},
                {"type": "number", "id": "maxDepthLevel", "text": "Max depth level", "value": 2},
                {"type": "number", "id": "limit", "text": "Max number of followers per user", "value": 5},
                {"type": "checkbox", "id": "clearCache", "text": "Clear cache before loading users"}]

    def ucitati(self, parameters):
        Node.objects.all().delete()
        Link.objects.all().delete()
        Attribute.objects.all().delete()
        parameters = self.parse_parameters(parameters)
        self.load_users(*parameters)

    def load_users(self, main_username, max_depth, limit, clear_cache):
        """
        Loads users and their followers from github's api.
        For every user a Node and a number of Attribute objects
        (name, number of followings, number of followers, number of repos)
         will be created and saved to the database.
        For each user and for each of his followers a Link object
        (from a follower to the user) will be created.
        :param main_username: user from which the search will start
        :param max_depth: max distance from the root node (specified by main_username)
                            to any other node in the graph.
        :param limit: max number of followers to load per user
        :return: None
        """
        self.main_username = main_username
        self.limit = int(limit)
        max_depth = int(max_depth)
        self.queue = OrderedDict()
        self.queue[main_username] = 1
        self.visited_nodes = set()

        # clear the cache if the user requested it
        if clear_cache == 'true':
            self.cached_users_json = {}

        while self.queue:
            username, self.current_depth = self.queue.popitem(False)

            # ucitaj i kreiraj cvor za korisnika
            user_json = self.get_user_json_from_api_or_cache(username)

            # ako ne postoji korisnik izadji
            if not user_json:
                return

            user_node = self.get_or_create_user_node(user_json)

            if self.current_depth > max_depth:
                break

            # ucitaj pratioce
            self.load_followers(user_node, user_json["followers_url"])
            self.visited_nodes.add(user_node.name)

    def get_user_json_from_api_or_cache(self, username):
        """
        If the user was already fetched from the api it will return that copy,
        otherwise it will fetch him from the api.
        :param username: for which user to return data
        :return: dictionary with user data from github's api
        """
        if username in self.cached_users_json:
            return self.cached_users_json[username]

        user_json = requests.get('https://api.github.com/users/' + username, headers=headers).json()

        if 'login' in user_json.keys():
            self.cached_users_json[user_json["login"]] = user_json
        else:
            print("Ne postji github korisnik")
            return False

        return user_json

    def get_or_create_user_node(self, user_json):
        """
        If a node with name user_json['login'] does not exist in the database
        a new node will be created from user_json and saved to the database
        :param user_json data from which to create Node:
        :return: Node
        """
        try:
            return Node.objects.get(name=user_json["login"])
        except Node.DoesNotExist:
            return self.create_user_node(user_json)

    def create_user_node(self, user_json):
        """
        Creates a node for the user and saves it in the database
        :param user_json: data fetched from api
        :return: Node
        """

        # root node should stand out in the graph
        if user_json["login"] == self.main_username:
            influence = 70
            group = 1
        else:
            influence = random.randrange(35, 50)
            group = 0

        user_node = Node(name=user_json["login"], influence=influence, group=group)
        user_node.save()
        self.create_attributes(user_node, user_json)
        return user_node

    def create_attributes(self, user_node, user_json):
        """
        Creates attributes for a given user and saves them to the database
        :param user_node: attributes are added to this node
        :param user_json: provides data for attributes
        :return: None
        """
        name_val = "" if user_json['name'] is None else user_json['name']
        name = Attribute(
            name="Name", value=name_val, node_id=user_node.get_id())

        num_followers = Attribute(
            name="Number of followers", value=user_json["followers"], node_id=user_node.get_id())
        num_following = Attribute(
            name="Number of followings", value=user_json["following"], node_id=user_node.get_id())
        num_repos = Attribute(name="Number of public repositories",
                              value=user_json["public_repos"], node_id=user_node.get_id())
        name.save()
        num_followers.save()
        num_following.save()
        num_repos.save()
        user_node.attributes.add(name, num_following, num_followers, num_repos)

    def load_followers(self, user_node, followers_url):
        """
        Fetches a list of followers, creates nodes for them (if they are not already created)
        and connects those nodes with the user_node
        :param user_node: represents a user for which followers are being loaded
        :param followers_url: url to fetch a list of followers
        :return: None
        """
        # get list of followers from api
        followers = requests.get(followers_url, headers=headers).json()
        if len(followers) > self.limit:
            followers = followers[:self.limit]

        for follower_json in followers:
            # add to queue if not visited or already added to queue
            if follower_json['login'] not in self.visited_nodes \
                    and follower_json['login'] not in self.queue:
                self.queue[follower_json["login"]] = self.current_depth + 1

            # get or create follower node
            follower_json = self.get_user_json_from_api_or_cache(follower_json["login"])
            follower_node = self.get_or_create_user_node(follower_json)
            # add user to cache
            self.cached_users_json[follower_json["login"]] = follower_json
            self.create_link(follower_node, user_node)

    def create_link(self, follower_node, user_node):
        """
        Creates a link from follower_node to user_node and saves it to the database.
        :param follower_node: 
        :param user_node: 
        :return: 
        """
        weight = (follower_node.influence + user_node.influence) / 2
        link = Link(source=follower_node, target=user_node, weight=weight)
        link.save()
