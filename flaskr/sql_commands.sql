SELECT user.id, post.id, post.title, likes.likes, likes.dislikes FROM likes
INNER JOIN post ON likes.post_id = post.id
INNER JOIN user ON post.author_id = user.id;