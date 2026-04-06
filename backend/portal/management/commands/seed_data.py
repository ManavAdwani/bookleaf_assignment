from django.core.management.base import BaseCommand
from portal.models import User, Book
from datetime import date
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        # Create Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@bookleaf.com',
                'password': make_password('admin123'),
                'role': 'admin',
                'first_name': 'Super',
                'last_name': 'Admin'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Admin created (admin / admin123)'))

        # Create Author
        author_user, created = User.objects.get_or_create(
            username='john_author',
            defaults={
                'email': 'john@example.com',
                'password': make_password('author123'),
                'role': 'author',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Author created (john_author / author123)'))
        else:
            # If already exists, we might need to get it to attach books
            pass
            
        # Ensure John has a book
        if author_user:
            book, b_created = Book.objects.get_or_create(
                isbn='978-3-16-148410-0',
                defaults={
                    'author': author_user,
                    'title': 'The Great Indian Novel',
                    'genre': 'Fiction',
                    'publication_date': date(2023, 1, 15),
                    'status': 'Published',
                    'mrp': 299.00,
                    'copies_sold': 1500,
                    'royalty_earned': 45000.00,
                    'royalty_paid': 20000.00,
                    'royalty_pending': 25000.00
                }
            )
            if b_created:
                self.stdout.write(self.style.SUCCESS(f'Book created: {book.title}'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
