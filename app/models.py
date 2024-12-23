from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    BigInteger,
    Text,
    Date,
)

from .database import Base


class DimType(Base):
    __tablename__ = "dim_type"
    type_id = Column(Integer, primary_key=True, comment="分区 ID")
    name = Column(String(255), nullable=False, comment="分区名称")


class DimUser(Base):
    __tablename__ = "dim_user"
    user_id = Column(BigInteger, primary_key=True, comment="用户 ID")
    name = Column(String(255), nullable=False, comment="用户名")
    face = Column(String(255), comment="用户头像 URL")


# DimVocal is not yet finished
# class DimVocal(Base):
#     __tablename__ = "dim_vocal"
#     vocal_id = Column(Integer, primary_key=True, comment="虚拟歌手 ID")
#     name = Column(String(255), nullable=False, comment="虚拟歌手名称")
#     group_ = Column(String(255), nullable=False, comment="虚拟歌手组团")


class IdentifierMap(Base):
    __tablename__ = "identifier_map"
    id = Column(BigInteger, primary_key=True, comment="ID")
    identifier = Column(
        String(255), nullable=False, comment="标识符", collation="utf8mb4_bin"
    )
    aid = Column(BigInteger, comment="视频的 AV 号")
    stat = Column(Integer, comment="状态")  # 只看到了1


class OlapRelVideoVocal(Base):
    __tablename__ = "olap_rel_video_vocal"
    aid = Column(BigInteger, primary_key=True, comment="视频的 AV 号")
    vocal_id = Column(Integer, primary_key=True, comment="虚拟歌手 ID")


class VideoDynamic(Base):
    __tablename__ = "video_dynamic"
    record_date = Column(Date, primary_key=True, comment="记录日期")
    aid = Column(BigInteger, primary_key=True, comment="视频的 AV 号")
    bvid = Column(
        String(255),
        nullable=False,
        comment="视频的 BV 号",
        collation="utf8mb4_0900_ai_ci",
    )
    coin = Column(Integer, nullable=False, comment="硬币")
    favorite = Column(Integer, nullable=False, comment="收藏")
    danmaku = Column(Integer, nullable=False, comment="弹幕")
    view = Column(Integer, nullable=False, comment="播放")
    reply = Column(Integer, nullable=False, comment="评论")
    share = Column(Integer, nullable=False, comment="分享")
    like = Column(Integer, nullable=False, comment="点赞")


class VideoMinute(Base):
    __tablename__ = "video_minute"
    time = Column(Integer, primary_key=True, comment="记录时间戳")
    aid = Column(BigInteger, primary_key=True, comment="视频的 AV 号")
    bvid = Column(
        String(255),
        nullable=False,
        comment="视频的 BV 号",
        collation="utf8mb4_0900_ai_ci",
    )
    coin = Column(Integer, comment="硬币")
    favorite = Column(Integer, comment="收藏")
    danmaku = Column(Integer, comment="弹幕")
    view = Column(Integer, comment="播放")
    reply = Column(Integer, comment="评论")
    share = Column(Integer, comment="分享")
    like = Column(Integer, comment="点赞")


class VideoStatic(Base):
    __tablename__ = "video_static"
    aid = Column(BigInteger, primary_key=True, comment="视频的 AV 号")
    bvid = Column(
        String(50),
        nullable=False,
        comment="视频的 BV 号",
        collation="utf8mb4_0900_ai_ci",
    )
    pubdate = Column(Integer, nullable=False, comment="投稿时间")
    title = Column(
        String(255), nullable=False, comment="标题", collation="utf8mb4_0900_ai_ci"
    )
    description = Column(Text, comment="简介", collation="utf8mb4_0900_ai_ci")
    tag = Column(Text, comment="标签", collation="utf8mb4_0900_ai_ci")
    pic = Column(String(255), comment="封面 URL", collation="utf8mb4_0900_ai_ci")
    type_id = Column(Integer, comment="分区 ID")
    user_id = Column(BigInteger, comment="UP主 ID")
    priority = Column(Integer, comment="优先级")
