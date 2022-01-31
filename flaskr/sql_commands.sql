SELECT user.id, post.id AS post_id, post.title, post.body, post.created, likes.likes, likes.dislikes FROM user
INNER JOIN post ON post.author_id = user.id
LEFT JOIN likes ON likes.post_id = post.id
ORDER BY created DESC;

SELECT user.id, post.id, post.title, post.body, post.created FROM post
INNER JOIN user ON post.author_id = user.id
ORDER BY created DESC;

INSERT INTO likes (post_id, likes) VALUES(1, 1)
ON DUPLICATE KEY DO UPDATE 
SET likes = likes + 1 WHERE post_id = 1;

INSERT INTO likes (post_id, dislikes) VALUES(2, 1)
ON CONFLICT (post_id) DO UPDATE 
SET dislikes = dislikes + 1 WHERE post_id = 2;

DELETE FROM likes WHERE post_id = 2;