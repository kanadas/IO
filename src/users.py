import uuid
from .user_agent import generate_user_agents, load_statistics
from .user_geo import generate_geoids

statistics = load_statistics()


class User:
    def __init__(self, agent, geoid):
        self.cid = uuid.uuid4()
        self.agent = agent
        self.geoid = geoid


# Generates the desired amount of users, together with all their data.
def generate_users(visits_no):
    agents = generate_user_agents(statistics, visits_no)
    geoids = generate_geoids(visits_no)
    users = [User(agent, geoid) for agent, geoid in zip(agents, geoids)]
    return users
