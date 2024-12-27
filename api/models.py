from collections import OrderedDict
from . import db
from sqlalchemy.orm import validates

art_tag_relations = db.Table('art_tag_relations', db.Column('art_id',
                                                            db.Integer, db.ForeignKey('article.aid')),
                             db.Column('tag_id',
                                       db.Integer, db.ForeignKey('tags.tid')))


class Article(db.Model):
    __tablename__ = 'article'
    _id = db.Column('aid', db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(10), nullable=False)
    createdAt = db.Column(db.DateTime(), nullable=False)
    updatedAt = db.Column(db.DateTime(), nullable=False)
    tagging = db.relationship(
        "Tags", secondary=art_tag_relations, backref='article')

    @validates('title', 'content', 'category')
    def required_fields(self, key, value):
        if len(value) == 0:
            raise ValueError('Value cannot be empty')

        if key == 'title' and len(value) > 50:
            raise ValueError(f'{key} must be less than 50 characters')
        elif key == 'category' and len(value) > 10:
            raise ValueError(f'{key} must be less than 10 characters')
        return value

    def to_dict(self) -> dict:
        return OrderedDict([
            ("id", self._id),
            ("title", self.title),
            ("content", self.content),
            ("category", self.category),
            ("tags", [tag.tags for tag in self.tagging]),
            ("createdAt", self.createdAt),
            ("updatedAt", self.updatedAt)
        ])


class Tags(db.Model):
    __tablename__ = 'tags'
    _tid = db.Column('tid', db.Integer, primary_key=True)
    tags = db.Column(db.String(15), nullable=False)

    @validates('tags')
    def required_fields(self, key, value):
        if len(value) == 0:
            raise ValueError('Value cannot be empty')
        if key == 'tags' and len(value) > 15:
            raise ValueError(f'{key} must be less than 15 characters')
        return value
