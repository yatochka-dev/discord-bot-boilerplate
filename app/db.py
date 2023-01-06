import prisma.models
from prisma import Prisma
from prisma.models import BaseModel


class UpdatedBaseModel(BaseModel):

    @property
    def id(self):
        if hasattr(self, "snowflake"):
            return int(self.snowflake)

        return None


prisma.models.BaseModel = UpdatedBaseModel

__all__ = ["prisma"]

prisma = Prisma()
