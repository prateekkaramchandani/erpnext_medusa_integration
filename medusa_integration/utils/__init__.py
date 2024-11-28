import re


def generate_slug(text, replace_slash=True):
    if not text:
        return ""

    CLEANUP_PATTERN_1 = re.compile(r'[~!@#$%^&*+()<>,."\'\?]')

    if replace_slash:
        CLEANUP_PATTERN_2 = re.compile("[_:/]")
    else:
        CLEANUP_PATTERN_2 = re.compile("[_:]")

    CLEANUP_PATTERN_3 = re.compile(r"([-/])\1+")

    name = text.lower()

    name = CLEANUP_PATTERN_1.sub("", name)
    name = CLEANUP_PATTERN_2.sub("-", name)
    name = "-".join(name.split())
    # replace repeating hyphens and slashes
    name = CLEANUP_PATTERN_3.sub(r"\1", name)

    return name[:140]
