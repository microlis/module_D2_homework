from django.contrib.auth.models import User
from news.models import Author
import random
from news.models import Category
from news.models import PostCategory
from news.models import Comment
from news.models import Post


first_user = User.objects.create_user(username='Irina', email='irina@gmail.com', password='12345')
second_user = User.objects.create_user(username='Andrey', email='andrey@gmail.com', password='qwerty')

irina = Author.objects.create(user=first_user)
andrey = Author.objects.create(user=second_user)

cat_sport = Category.objects.create(name="Спорт")
cat_music = Category.objects.create(name="Музыка")
cat_cinema = Category.objects.create(name="Кино")
cat_politics = Category.objects.create(name="Политика")

article_for_irina = Post.objects.create(author=irina, post_type=Post.article, title="Статьи для Ирины")
article_for_andrey = Post.objects.create(author=andrey, post_type=Post.article, title="Статья для Андрея")
news_for_andrey = Post.objects.create(author=andrey, post_type=Post.news, title="Новость для Андрея")

PostCategory.objects.create(post=article_for_irina, category=cat_sport)
PostCategory.objects.create(post=article_for_irina, category=cat_cinema)
PostCategory.objects.create(post=article_for_andrey, category=cat_music)
PostCategory.objects.create(post=news_for_andrey, category=cat_politics)

comment1 = Comment.objects.create(post=article_for_irina, user=andrey.user)
comment2 = Comment.objects.create(post=article_for_andrey, user=irina.user)
comment3 = Comment.objects.create(post=news_for_andrey, user=andrey.user)
comment4 = Comment.objects.create(post=news_for_andrey, user=irina.user)

list_for_like = [article_for_irina,
                 article_for_andrey,
                 news_for_andrey,
                 comment1,
                 comment2,
                 comment3,
                 comment4]

for i in range(100):
    random_obj = random.choice(list_for_like)
    if i % 2:
        random_obj.like()
    else:
        random_obj.dislike()

rating_irina = (sum([post.rating * 3 for post in Post.objects.filter(author=irina)])
                + sum([comment.rating for comment in Comment.objects.filter(user=irina.user)])
                + sum([comment.rating for comment in Comment.objects.filter(post__author=irina)]))

irina.update_rating(rating_irina)

rating_andrey = (sum([post.rating * 3 for post in Post.objects.filter(author=andrey)])
                 + sum([comment.rating for comment in Comment.objects.filter(user=andrey.user)])
                 + sum([comment.rating for comment in Comment.objects.filter(post_author=andrey)]))

andrey.update_rating(rating_andrey)

best_author = Author.objects.all().order_by('-rating')[0]
print("Лучший автор")
print("Логин:", best_author.user.username)
print("Рейтинг:", best_author.rating)

best_article = Post.objects.filter(post_type=Post.article).order_by('-rating')[0]
print("Лучшая статья")
print("Дата:", best_article.created)
print("Автор:", best_article.author.user.username)
print("Рейтинг:", best_article.rating)
print("Заголовок:", best_article.title)
print("Превью:", best_article.preview())

for comment in Comment.objects.filter(post=best_article):
    print("Дата:", comment.created)
print("Автор:", comment.user.username)
print("Рейтинг:", comment.rating)
print("Комментарий:", comment.text)
