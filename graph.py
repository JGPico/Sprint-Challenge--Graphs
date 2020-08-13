class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


class RoomG():
    def __init__(self, name)
    self.name = name


class Graph:
    def __init__(self):
        self.last_id = 0
        self.rooms = {}
        self.neighbors = {}

    def add_neighbors(self, room_id, neighbor_id):
        """
        Creates a quad-directional map of neighboring rooms
        """
        if room_id == neighbor_id:
            print("WARNING: Rooms cannot be linked to themselves")
            return False
        elif neighbor_id in self.neighbors[room_id] or room_id in self.neighbors[neighbor_id]:
            print("WARNING: Link to neighboring room already exists")
            return False
        else:
            self.neighbors[room_id].add(neighbor_id)
            self.neighbors[neighbor_id].add(room_id)

        return True

    def add_room(self, name):
        """
        Create a new room
        """

        # Here
        self.last_id += 1  # automatically increment the ID to assign the new room
        self.rooms[self.last_id] = RoomG(name)
        self.neighbors[self.last_id] = set()

    def populate_graph(self, num_rooms):
        """
        Takes a number of users and an average number of friendships
        as arguments
        Creates that number of users and a randomly distributed friendships
        between those users.
        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.rooms = {}
        self.neighbors = {}
        # !!!! IMPLEMENT ME

        # Add rooms
        for i in range(0, num_rooms):
            self.add_room(f"Room {i}")

        # Create neighbors
        possible_neighbors = []

        # avoid dups by ensuring first num < second num
        for room_id in self.rooms:
            for neighbor_id in range(room_id + 1, self.last_id + 1):
                possible_neighbors.append((room_id, neighbor_id))

        # shuffle neighbors
        random.shuffle(possible_neighbors)

        N = num_rooms * avg_friendships // 2
        for i in range(N):
            adjacent = possible_neighbors[i]
            room_id, neighbor_id = adjacent
            self.add_neighbors(room_id, neighbor_id)

    def populate_graph2(self, num_users, avg_friendships):
        # reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # add users
        for i in range(num_users):
            self.add_user(f"user {i}")

        # create friendships
        target_friendships = num_users * avg_friendships
        total_friendships = 0
        collisions = 0

        while total_friendships < target_friendships:
            user_id = random.randint(1, self.last_id)
            friend_id = random.randint(1, self.last_id)

            if self.add_friendship(user_id, friend_id):
                total_friendships += 2
            else:
                collisions += 1

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument
        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
        The key is the friend's ID and the value is the path.
        """
        # !!!! IMPLEMENT ME
        q = Queue()
        visited = {}  # Note that this is a dictionary, not a set

        q.enqueue([user_id])

        while q.size > 0:
            path = q.dequeue()
            v = path[-1]

            if v not in visited:
                visited[v] = path

                for friend in self.friendships[v]:
                    path_copy = list(path)  # path.copy
                    path_copy.append(friend)

                    q.enqueue(path_copy)

        return visited
