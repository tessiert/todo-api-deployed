import django


def main():
    django.setup()

    from todos_app.models import Todo
    from django.contrib.auth.models import User
    User.objects.create_superuser(
        username='admin', email='admin@example.com', password='admin')

    ADMIN_TASKS = [
        ('Send update email to board', True),
        ('Release staging version', False),
        ('Review sprint next week', False),
    ]
    for title, completed in ADMIN_TASKS:
        Todo.objects.create(title=title, completed=completed)

if __name__ == '__main__':
    main()
