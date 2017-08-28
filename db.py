from user import User
import pymongo


#Make sure you have Mongodb and the DB itself
#Is named appropriately
client = pymongo.MongoClient()
db = client.plebr


class Memory:


    def __init__(self):
        self.users = []


    def upsert_user(self, user: User):
        """
        Update or Insert the current user in the db
        :param user: user with updated values
        :return: None
        """
        sid = user.sid
        reg = user.region
        sum = user.summoner
        db.users.find_one_and_update({'id': user.id}, {'$set': {'sid': sid, 'region': reg, 'summoner': sum}},
                                     upsert=True)


    def remove_user(self, discord_id: str):
        """
        Get user from DB by discord id
        :param discord_id: str: unique discord user ID
        :return: User: if user exists, None if user doesn't exist
        """

        db.users.find_one_and_delete({'id': discord_id})

    def get_user(self, discord_id: str):
        """
        Get user from DB by discord id
        :param discord_id: str: unique discord user ID
        :return: User: if user exists, None if user doesn't exist
        """
        d_user = None
        for i in range(len(self.users)):
            prsn = db.users.find_one({'id': self.users[i].id})
            if (prsn['id']) == discord_id:
                d_user = prsn['id']
                break

        return d_user


    def get_summoner(self, discord_id: str):
        """
        Get summoner name from DB by discord id
        :param discord_id: str: unique discord user ID
        :return: summoner name: str: summoner name of user
        """
        summon = None
        prsn = db.users.find_one({'id': discord_id})
        if (prsn['id']) == discord_id:
            summon = str(prsn['summoner'])

        return summon


    def get_region(self, discord_id: str):
        """
        Get region from DB by discord id
        :param discord_id: str: unique discord user ID
        :return: region: str: region of user
        """
        region = None
        prsn = db.users.find_one({'id': discord_id})
        if (prsn['id']) == discord_id:
            region = str(prsn['region'])

        return region
