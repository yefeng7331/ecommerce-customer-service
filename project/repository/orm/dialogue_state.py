"""
@Author:叶枫
@Time:2026/9/9
@Desc:
"""


from sqlalchemy import String,Text
from sqlalchemy.orm import Mapped, mapped_column

from project.repository.orm.base import Base


class DialogueStateRecord(Base):
    __tablename__ = "dialogue_states"
    #Mapped类型：映射类型，用于映射数据库表的字段
    sender_id:Mapped[str] = mapped_column(String(255),primary_key=True)
    state_json:Mapped[str] = mapped_column(Text,nullable=False)

