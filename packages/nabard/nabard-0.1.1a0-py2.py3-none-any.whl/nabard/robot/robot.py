class Robot(object):
    """
    Robot is the base class of user robots.
    it must implement the `step` method.
    """

    def __init__(self, robot_id):
        self.sock = None
        self.id = robot_id

    def step(self, data):
        """
        It must be implemented.
        """
        raise NotImplementedError()

    def run(self):
        """
        Runs the robot.
        """
        if self.sock is None:
            raise Exception("the socket has not been injected")
        while True:
            data = self.sock.recv(1048576).decode()  # 1 KiB
            if data == "TIMEOUT":
                continue
            res = self.step(data)
            self.sock.send(res.encode())
