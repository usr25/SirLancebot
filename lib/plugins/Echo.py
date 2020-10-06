from lib.plugins.Plugin import Plugin


class Echo(Plugin):
    def __init__(self, data):
        super().__init__("Echo",
                         "Repeats the msg. (limited to 400chars) cmd: !echo <msg>",
                         ["echo"])
        self.data = data


    def echo(self, data):
        err_msg = "Error: Echo needs a msg, try !h echo"

        if data["args"] == None or data["args"] == []:
            return err_msg
        msg = " ".join(data["args"])
        if len(msg) > 400:
            return err_msg
        return msg