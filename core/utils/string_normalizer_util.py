import unicodedata
from core import constants


class StringNormalizerUtil:
    def handle(org_str: str) -> str:
        form = constants.DEFAULT_NORMALIZE_FORM

        return unicodedata.normalize(form, org_str)
