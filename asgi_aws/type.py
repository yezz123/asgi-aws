from typing import Any, Awaitable, Callable, MutableMapping

Message = MutableMapping[str, Any]
Scope = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
Request = Any
Response = Any
