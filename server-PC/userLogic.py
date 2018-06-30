nodeId = None
sensorId = None
value = None


def onChange(nodeId, sensorId, value, db):
    ans = ""
    ans += "{}\t{}\t{}\n".format(nodeId, (sensorId + 1), ((db[(nodeId, sensorId)].valueInt / 1000) % 2))
    return ans