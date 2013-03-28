from browser import Browser
from builtin import explain

class NineDict:
    def __init__(self):
        _br = Browser()

    def get_recomm(self, gag_id):
        gag_id = int(gag_id)
        if gag_id not in explain:
            words = []
        else:
            words = [x['keyword'] for x in explain[gag_id]]
        return words

    def get_defis(self, word, gag_id):
        defis = []
        defis += self._get_defis_in_gag(word, gag_id)
        if len(defis) == 0:
            defis += self._get_defis_in_general(word, gag_id)
        if len(defis) == 0:
            defis += self._get_defis_from_web(word, gag_id)
        return defis

    def _get_defis_in_gag(self, word, gag_id):
        defis = []
        if gag_id not in explain:
            return defis
        for keyword in filter(lambda x: x['keyword'].lower() == word.lower(), explain[gag_id]):
            defis += keyword['explain']
        return defis

    def _get_defis_in_general(self, word, gag_id):
        defis = []
        for gid in explain:
            for keyword in filter(lambda x: x['keyword'].lower() == word.lower(), explain[gid]):
                defis += keyword['explain']
        return defis

    def _get_defis_from_web(self, word, gag_id):
        defis = []
        defis += _get_defis_from_dr_eye(word)
        defis += _get_defis_from_google_image(word)
        return defis

    def _get_defis_from_dr_eye(self, word):
        return []

    def _get_defis_from_google_image(self, word):
        return []
