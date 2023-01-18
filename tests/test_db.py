from www_eaveson_co_uk import Post

post = Post(body="this is a post")
db.session.add(post)
db.session.commit()
