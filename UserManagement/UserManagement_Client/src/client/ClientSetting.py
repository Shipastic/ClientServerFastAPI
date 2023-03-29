
class ClientSetting:
    host: str = "127.0.0.1"
    protocol: str = "http"
    port: int = "8000"   

    def __init__(self,protocol, host, port):
        self.host = host
        self.protocol = protocol
        self.port = port

    
