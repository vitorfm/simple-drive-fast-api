from abc import ABC, abstractmethod


class StorageBackend(ABC):
    @abstractmethod
    async def store(self, blob_id: str, data: bytes) -> None:
        pass

    @abstractmethod
    async def retrieve(self, blob_id: str) -> bytes:
        pass

    @abstractmethod
    async def exists(self, blob_id: str) -> bool:
        pass

    async def delete(self, blob_id: str) -> None:
        raise NotImplementedError("Delete operation not supported")

