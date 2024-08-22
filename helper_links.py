import re

patern = re.compile(r"\[[ -~]+\]\(http(s)?:\/\/[ -~]+\)")


def is_valid_link(link: str) -> bool:
    if patern.match(link):
        return True
    else:
        return False


def parse_link(link: str) -> str:
    link_name = link.split("]")[0].removeprefix("[")
