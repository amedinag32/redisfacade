from .singleton import RedisSingleton
from os import getenv
from typing import Any, List
from datetime import timedelta
from json import dumps, loads

class RedisFacade:
    """
        Fachada de base de datos, crea conexion con un singleton a mssql
    """
    def __init__(self, REDIS_HOST: str = getenv("REDIS_HOST"), REDIS_PORT: int = getenv("REDIS_PORT"), REDIS_PASSWORD: str = getenv("REDIS_PASSWORD")):
        self.redis_manager = RedisSingleton(REDIS_HOST=REDIS_HOST, REDIS_PORT=REDIS_PORT, REDIS_PASSWORD=REDIS_PASSWORD)

    def set_key_value(self, db: int, key:str, value: Any) -> bool: 
        """
            Guarda un valor del tipo key - value de base de datos.
        """       
        
        return self.redis_manager.get_connection(db).set(name=key, value=value, ex=timedelta(days=3))
        
    def get_key_value(self, db: int, key:str) -> Any: 
        """
            Obtiene un valor del tipo key - value de base de datos.
        """       
        
        return self.redis_manager.get_connection(db).get(name=key).decode("utf-8")
               
    def set_list_str(self, db: int, list_name: str, intems: List[str]) -> bool:
        try:
            for item in intems:
                self.redis_manager.get_connection(db).rpush(list_name, item)    
            return True
        except Exception as e:
            print("Error al almacenar datos de lista:", e)
            return False
            
    def get_list_str(self, db: int, list_name: str) -> List[str]:
        list_data = []
        list_data = self.redis_manager.get_connection(db).lrange(list_name, 0, -1)
        list_data = [item.decode('utf-8') for item in list_data]
        return list_data
        
    def pop_list_str(self, db: int, list_name: str) -> str:
        return self.redis_manager.get_connection(db).lpop(list_name).decode('utf-8')
    
    def len_list(self, db: int, list_name: str) -> str:
        return self.redis_manager.get_connection(db).llen(list_name)
    
    def set_json_data(self, db: int, json_name, json_key, json_data: Any) -> bool:
        is_saved: bool = False
        if isinstance(json_data, dict):
            is_saved = self.redis_manager.get_connection(db).set((json_name + ":" + json_key), dumps(json_data))
        else:
            is_saved = self.redis_manager.get_connection(db).set((json_name + ":" + json_key), json_data)
            
        return is_saved
        
    def get_key_json_data(self, db: int, json_name: str, json_key: str) -> Any:
        retrieved_json = self.redis_manager.get_connection(db).get((json_name + ":" + json_key))
        if isinstance(retrieved_json, dict):
            return loads(retrieved_json)  # Convert JSON string back to a Python dictionary
        else:
            return retrieved_json.decode("utf-8")
    
    def get_json_data(self, db: int, json_name: str) -> Any:
        connection = self.redis_manager.get_connection(db)
        data_keys = connection.scan_iter((json_name + ":*"))
        # Recuperar todas las claves
        data = {}
        for key in data_keys:
            retrieved_json = connection.get(key)
            key = key.decode('utf-8').replace((json_name + ":"), "", 1)
            if retrieved_json:  # Verificar si el valor existe
                if isinstance(retrieved_json, dict):
                    data[key] = loads(retrieved_json)
                else:
                    data[key] = retrieved_json.decode('utf-8')

        return data