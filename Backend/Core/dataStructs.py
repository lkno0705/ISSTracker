from dataclasses import dataclass
import datetime


# parse timestring to timestamp
def parseTimeToTimestamp(time):
    # splitting timestamp string into date and time
    date, time = time.split(" ")

    # splitting date into Year, Month, Day
    date = date.split("-")

    # splitting time into Hour, Minute, Second
    time = time.split("-")

    # creating tupel out of splitted values
    timeTupel = (int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

    # calculating timestamp (UTC)
    timestamp = datetime.datetime(year=timeTupel[0],
                                  month=timeTupel[1],
                                  day=timeTupel[2],
                                  hour=timeTupel[3],
                                  minute=timeTupel[4],
                                  second=timeTupel[5]).timestamp()
    return timestamp


# dataclass for ISSDBKeys (comparable to a struct from C & C++)
@dataclass()
class ISSDBKey:
    timeValue: str
    key: str
    value: str

    def __post_init__(self):
        # calculate timestamp automatically on init
        self.timestamp = parseTimeToTimestamp(self.timeValue)

    def __hash__(self):
        # define how hashvalues should get calculated -> sets etc. in pythons are hashed
        return hash((self.timeValue, self.key))

    def __eq__(self, other):
        # define condition when two ISSDBKeys are equal
        return self.timeValue == other.timeValue and self.key == other.key

@dataclass()
class Astronaut:
    name: str
    pic: str
    flag: str
    nation: str

    def __hash__(self):
        return hash((self.name, self.pic, self.flag, self.nation))

    def __eq__(self, other):
        return self.name == other.name and self.pic == other.pic and self.flag == other.pic and self.nation == other.nation