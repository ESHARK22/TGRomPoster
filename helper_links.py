import re

patern = re.compile(r"\[[ -~]+\]\(http(s)?:\/\/[ -~]+\)")


def is_valid_link(link: str) -> bool:
    """

    :param link: str: 

    """
    if patern.match(link):
        return True
    else:
        return False
