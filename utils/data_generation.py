import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)["test_config"]


def get_user(index=0):
    """
    Returns a user from config by index (default: first user).
    """
    return config["test_users"][index]


def get_transaction(index=0):
    """
    Returns a transaction from config by index (default: first transaction).
    """
    return config["test_transactions"][index]