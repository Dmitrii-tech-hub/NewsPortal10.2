
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category

@shared_task
def send_new_post_email(post_id):
    post = Post.objects.get(pk=post_id)

    for category in post.categories.all():
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            html_content = render_to_string(
                'new_post_email.html',
                {
                    'user': subscriber,
                    'post': post,
                    'preview': post.content[:50],  # Первые 50 символов
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Новая статья в категории {category.name}: {post.title}',
                body=post.content[:50],
                from_email='dmitrij.croitoru@yandex.com',
                to=[subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()



@shared_task
def send_weekly_posts():
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        new_posts = Post.objects.filter(
            categories=category,
            created_at__gte=timezone.now() - timedelta(days=7)
        )

        if new_posts.exists():
            for subscriber in subscribers:
                html_content = render_to_string(
                    'weekly_news_email.html',
                    {
                        'user': subscriber,
                        'category': category,
                        'posts': new_posts,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'Еженедельная рассылка новостей в категории {category.name}',
                    body='Смотрите новые статьи за неделю!',
                    from_email='dmitrij.croitoru@yandex.com',
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
