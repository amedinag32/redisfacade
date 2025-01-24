from redis import Redis, ConnectionError, TimeoutError
from threading import Lock
from os import getenv

class RedisSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._connections = {}
        return cls._instance
    
    def __init__(self, REDIS_HOST, REDIS_PORT: int, REDIS_PASSWORD: str):
        self.REDIS_HOST = REDIS_HOST
        self.REDIS_PORT = REDIS_PORT
        self.REDIS_PASSWORD = REDIS_PASSWORD

    def get_connection(self, db: int) -> Redis:
        """
        Obtiene una conexión a Redis para una base de datos específica.
        Si la conexión no existe o está dañada, se crea una nueva.
        """
        if db not in self._connections:
            return self._create_connection(db)
        if not self._is_connection_alive(self._connections[db]):
            return self._create_connection(db)
        return self._connections[db]

    def _create_connection(self, db: int) -> Redis:
        """
        Crea una nueva conexión de Redis y la almacena.
        """
        with self._lock:
            self._connections[db] = Redis(
                host=self.REDIS_HOST,  # Cambia según tu configuración
                port=self.REDIS_PORT,
                db=db,
                password=self.REDIS_PASSWORD  # Configura la contraseña si es necesario
            )
        return self._connections[db]

    def _is_connection_alive(self, connection: Redis) -> bool:
        """
        Verifica si la conexión a Redis está viva.
        """
        try:
            # Verifica con un comando básico (PING)
            connection.ping()
            return True
        except (ConnectionError, TimeoutError):
            return False
