from dataclasses import dataclass
import datetime


def parseTimeToTimestamp(time):
    date, time = time.split(" ")
    date = date.split("-")
    time = time.split("-")
    timeTupel = (int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
    timestamp = datetime.datetime(year=timeTupel[0],
                                  month=timeTupel[1],
                                  day=timeTupel[2],
                                  hour=timeTupel[3],
                                  minute=timeTupel[4],
                                  second=timeTupel[5]).timestamp()
    return timestamp


@dataclass()
class ISSDBKey:
    timeValue: str
    key: str
    value: str

    def __post_init__(self):
        self.timestamp = parseTimeToTimestamp(self.timeValue)

    def __hash__(self):
        return hash((self.timeValue, self.key))

    def __eq__(self, other):
        return self.timeValue == other.timeValue and self.key == other.key

