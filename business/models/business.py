# # -*- coding: utf-8 -*-
# from exts import db
#
#
# class Blog(db.Model):
#     __tablename__ = "blog_detail"
#     __table_args__ = {"comment": "博客详情表"}
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     # 添加作者外键
#     author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     author = db.relationship("User", backref="blogs")
