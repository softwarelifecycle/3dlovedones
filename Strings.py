from prometheus_client import Enum


class EventList(Enum):
    About = '-ABOUT-'
    Ping = "-PING-"
    Register = "-REGISTER-"
    UpdateCode = "-UPDATECODE-"
    Reload = '-RELOAD-'
    Restart = '-RESTART-'
    Reboot = '-REBOOT-'
    Shutdown = '-SHUTDOWN-'
    Snap = '-SNAP-'
    Retake = '-RETAKE-'
    PictureTaken = '-PICTURETAKEN-'
    DeleteTransferFolder = '-DELETETRANSFERFOLDER-'
    DeleteDestFolder = '-DELETEDESTFOLDER-'
    CameraPinged = '-CAMERAPINGED-'
    CameraRegistered = '-CAMERAREGISTERED-'
    CameraTable = '-CAMERATABLE-'
    ConvertPics = '-CONVERTPICS-'


class ObjectList(Enum):
    StatusText = '-STATUSTEXT-'
    CameraTable = '-CAMERATABLE-'