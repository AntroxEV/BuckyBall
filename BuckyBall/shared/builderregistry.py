'''
Registry class for Model Builder.
It is a service class to register any class initiated by the user
To hold shared state that spans:

- multiple object instantiations
- multiple collectors
- arbitrary ordering of creation

Objects must self-register by calling the register method using super().__init__ method, 
passing the app_name as argument.

@author: Dr Alessandro Tombari
'''
from typing import List, Type, Dict, Any, ClassVar
from collections import defaultdict
import weakref

class ModelBuilderRegistry:
    _registry: ClassVar[
        Dict[str, Dict[Type, List[object]]]
    ] = defaultdict(lambda: defaultdict(list))

    @classmethod
    def _register(
        cls,
        app_name: str,
        role: Type,
        obj: object
    ) -> None:
        cls._registry[app_name][role].append(obj)

    @classmethod
    def _get_list_obj(
        cls,
        app_name: str,
        role: Type
    ) -> List[object]:
        return list(cls._registry.get(app_name, {}).get(role, []))

    @classmethod
    def _clear_app(cls, app_name: str) -> None:
        cls._registry.pop(app_name, None)
