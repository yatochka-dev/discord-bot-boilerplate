import disnake

from app.services.index import CRUDXService


class MemberService(CRUDXService):
    async def remove_member(
        self,
        member: disnake.Member,
        *,
        ignore_not_found: bool = False,
    ):
        if not isinstance(member, disnake.Member):
            raise TypeError("member must be a disnake.Member")

        exists = await self.bot.prisma.member.find_first(
            where={
                "guild": {"snowflake": self.to_safe_snowflake(member.guild.id)},
                "user": {"snowflake": self.to_safe_snowflake(member.id)},
            },
        )

        if exists:
            await self.bot.prisma.member.delete(
                where={
                    "guild": {"snowflake": member.guild.id},
                    "user": {"snowflake": member.id},
                }
            )

        elif not ignore_not_found:
            raise ValueError("member not found")

        return None
