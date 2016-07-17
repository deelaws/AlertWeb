from enum import Enum, unique

@unique
class AdventureType(Enum):
    BackCounntry = 1
    Hike = 2
    SnowBoarding = 3
    Kayaking = 4

    def describe(self):
        # self is the memeber here
        return self.name

    def __str__(self):
        return self.name

def generate_adventure_tuple():
    ret = []
    ad_map = AdventureType._member_map_
    for k in ad_map:
        ret.append((k,ad_map[k].value))
    return ret

adventure_type_tuples = generate_adventure_tuple()

def int_to_adventure_type(i):
    # TODO: for now return BackCountry
    return AdventureType.BackCountry