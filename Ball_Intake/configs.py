import json

from cscore import CameraServer, MjpegServer, UsbCamera, VideoSource


class CameraConfig: pass


class Vision:
    def __init__(self, configFile="/boot/frc.json"):
        self.configFile = configFile
        self.team = None
        self.server = False
        self.cameraConfigs = []
        self.switchedCameraConfigs = []
        self.cameras = []
        self.config_was_read = self.readConfig()
        self.startCamera()
        self.startSwitchedCamera()

    def parseError(self, str):
        """Report parse error."""
        print("config error in '" + self.configFile + "': " + str, file=sys.stderr)


    def readCameraConfig(self, config):
        """Read single camera configuration."""
        cam = CameraConfig()

        # name
        try:
            cam.name = config["name"]
        except KeyError:
            self.parseError("could not read camera name")
            return False

        # path
        try:
            cam.path = config["path"]
        except KeyError:
            self.parseError("camera '{}': could not read path".format(cam.name))
            return False

        # stream properties
        cam.streamConfig = config.get("stream")

        cam.config = config

        self.cameraConfigs.append(cam)
        return True


    def readSwitchedCameraConfig(self, config):
        """Read single switched camera configuration."""
        cam = CameraConfig()

        # name
        try:
            cam.name = config["name"]
        except KeyError:
            self.parseError("could not read switched camera name")
            return False

        # path
        try:
            cam.key = config["key"]
        except KeyError:
            self.parseError("switched camera '{}': could not read key".format(cam.name))
            return False

        self.switchedCameraConfigs.append(cam)
        return True


    def readConfig(self):
        """Read configuration file."""
        # parse file
        try:
            with open(self.configFile, "rt", encoding="utf-8") as f:
                j = json.load(f)
        except OSError as err:
            print("could not open '{}': {}".format(self.configFile, err), file=sys.stderr)
            return False

        # top level must be an object
        if not isinstance(j, dict):
            self.parseError("must be JSON object")
            return False

        # team number
        try:
            self.team = j["team"]
        except KeyError:
            self.parseError("could not read team number")
            return False

        # ntmode (optional)
        if "ntmode" in j:
            str = j["ntmode"]
            if str.lower() == "client":
                self.server = False
            elif str.lower() == "server":
                self.server = True
            else:
                self.parseError("could not understand ntmode value '{}'".format(str))

        # cameras
        try:
            self.cameras = j["cameras"]
        except KeyError:
            self.parseError("could not read cameras")
            return False
        for camera in self.cameras:
            if not self.readCameraConfig(camera):
                return False

        # switched cameras
        if "switched cameras" in j:
            for camera in j["switched cameras"]:
                if not self.readSwitchedCameraConfig(camera):
                    return False

        return True


    def startCamera(self):
        for config in self.cameraConfigs:
            """Start running the camera."""
            print("Starting camera '{}' on {}".format(config.name, config.path))
            inst = CameraServer.getInstance()
            camera = UsbCamera(config.name, config.path)
            server = inst.startAutomaticCapture(camera=camera, return_server=True)

            camera.setConfigJson(json.dumps(config.config))
            camera.setConnectionStrategy(VideoSource.ConnectionStrategy.kKeepOpen)

            if config.streamConfig is not None:
                server.setConfigJson(json.dumps(config.streamConfig))

            self.cameras.append(camera)


    def startSwitchedCamera(self):
        for config in self.switchedCameraConfigs:
            """Start running the switched camera."""
            print("Starting switched camera '{}' on {}".format(config.name, config.key))
            server = CameraServer.getInstance().addSwitchedCamera(config.name)

            def listener(fromobj, key, value, isNew):
                if isinstance(value, float):
                    i = int(value)
                    if i >= 0 and i < len(self.cameras):
                        server.setSource(self.cameras[i])
                elif isinstance(value, str):
                    for i in range(len(self.cameraConfigs)):
                        if value == self.cameraConfigs[i].name:
                            server.setSource(self.cameras[i])
                            break

            NetworkTablesInstance.getDefault().getEntry(config.key).addListener(
                listener,
                ntcore.constants.NT_NOTIFY_IMMEDIATE |
                ntcore.constants.NT_NOTIFY_NEW |
                ntcore.constants.NT_NOTIFY_UPDATE)
