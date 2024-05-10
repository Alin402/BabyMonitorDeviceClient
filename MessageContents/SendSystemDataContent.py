class SendSystemDataContent:
    def __init__(self, userID, systemTemperature):
        self.UserID = userID
        self.SystemTemperature = systemTemperature

    def __json__(self):
        return {
            "UserID": self.UserID,
            "SystemTemperature": self.SystemTemperature,
        }