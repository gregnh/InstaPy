import json
import os

from .util import interruption_handler


def load_json(file_path):
    if not file_path.endswith('.json'):
        if not os.path.exists(file_path):
            raise OSError('{} not found'.format(file_path))

        file_path = '{}.json'.format(file_path)

    if not os.path.isfile(file_path):
        raise FileNotFoundError('{} not found'.format(file_path))

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    return data


def save_users_followers_followed_json(data_dict, logfolder, logger):
    """
    Saving users' followers followed in json
    :param data_dict: data format - {"user" : {"date" :[]}}
    :param logfolder:
    :param logger:
    :return:
    """
    if not isinstance(data_dict, dict):
        raise TypeError('Data must be a dictionary')

    file_path = '{}users_followers.json'.format(logfolder)
    try:

        if not os.path.isfile(file_path):
            with interruption_handler():
                with open(file_path, 'w') as users_followers_json:
                    json.dump(data_dict,
                              users_followers_json,
                              indent=4)
                    users_followers_json.close()

        """ Loads the existing users' follower followed json data """
        with open(file_path, 'a') as users_followers_json:
            users_followers_dict = load_json(file_path)
            stored_usernames = [username for username in users_followers_dict.keys()]
            for username in data_dict.keys():
                if username not in stored_usernames:
                    users_followers_dict.update(data_dict[username])
                else:
                    stored_dates = [date for date in users_followers_dict[username].keys()]
                    for date in data_dict[username]:
                        if date not in stored_dates:
                            users_followers_dict[username].update(data_dict[username][date])
                        else:
                            users_followers_dict[username][date].extend(data_dict[username][date])

            json.dump(users_followers_dict,
                      users_followers_json,
                      indent=4)

        logger.info('Users followers saved !')
    except Exception as exc:
        logger.info("Error occured while saving users' followers \n {}".format(exc))

