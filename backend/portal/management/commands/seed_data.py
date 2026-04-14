from django.core.management.base import BaseCommand
from portal.models import User, Book
from django.contrib.auth.hashers import make_password

AUTHORS_DATA = [
    {
        "author_id": "AUTH001",
        "name": "Priya Sharma",
        "email": "priya.sharma@email.com",
        "phone": "+91-98765-43210",
        "city": "Mumbai",
        "joined_date": "2023-03-15",
        "username": "priya_sharma",
        "password": "author123",
        "books": [
            {
                "book_id": "BK001",
                "title": "Whispers of the Ganges",
                "isbn": "978-93-5XXXX-01-1",
                "genre": "Literary Fiction",
                "publication_date": "2023-06-20",
                "status": "Published & Live",
                "mrp": 399,
                "author_royalty_per_copy": 35,
                "copies_sold": 342,
                "royalty_earned": 11970,
                "royalty_paid": 8400,
                "royalty_pending": 3570,
                "last_royalty_payout_date": "2025-10-15",
                "print_partner": "In-House",
                "available_on": ["Amazon India", "Flipkart", "BookLeaf Store"]
            },
            {
                "book_id": "BK002",
                "title": "The Saffron Diaries",
                "isbn": "978-93-5XXXX-02-8",
                "genre": "Non-Fiction / Memoir",
                "publication_date": "2024-01-10",
                "status": "Published & Live",
                "mrp": 450,
                "author_royalty_per_copy": 42,
                "copies_sold": 189,
                "royalty_earned": 7938,
                "royalty_paid": 7938,
                "royalty_pending": 0,
                "last_royalty_payout_date": "2025-12-01",
                "print_partner": "In-House",
                "available_on": ["Amazon India", "BookLeaf Store"]
            }
        ]
    },
    {
        "author_id": "AUTH002",
        "name": "Rohit Kapoor",
        "email": "rohit.kapoor@email.com",
        "phone": "+91-87654-32109",
        "city": "Delhi",
        "joined_date": "2022-11-08",
        "username": "rohit_kapoor",
        "password": "author123",
        "books": [
            {
                "book_id": "BK003",
                "title": "Code & Karma",
                "isbn": "978-93-5XXXX-03-5",
                "genre": "Self-Help / Technology",
                "publication_date": "2023-02-14",
                "status": "Published & Live",
                "mrp": 350,
                "author_royalty_per_copy": 30,
                "copies_sold": 876,
                "royalty_earned": 26280,
                "royalty_paid": 21000,
                "royalty_pending": 5280,
                "last_royalty_payout_date": "2025-09-01",
                "print_partner": "Repro India",
                "available_on": ["Amazon India", "Flipkart", "Amazon US", "BookLeaf Store"]
            },
            {
                "book_id": "BK004",
                "title": "Startup Sutra",
                "isbn": "978-93-5XXXX-04-2",
                "genre": "Business / Entrepreneurship",
                "publication_date": "2024-05-22",
                "status": "Published & Live",
                "mrp": 499,
                "author_royalty_per_copy": 48,
                "copies_sold": 1203,
                "royalty_earned": 57744,
                "royalty_paid": 50000,
                "royalty_pending": 7744,
                "last_royalty_payout_date": "2025-11-15",
                "print_partner": "In-House",
                "available_on": ["Amazon India", "Flipkart", "Amazon US", "Amazon UK", "BookLeaf Store"]
            }
        ]
    },
    {
        "author_id": "AUTH003",
        "name": "Ananya Reddy",
        "email": "ananya.reddy@email.com",
        "phone": "+91-76543-21098",
        "city": "Hyderabad",
        "joined_date": "2024-02-20",
        "username": "ananya_reddy",
        "password": "author123",
        "books": [
            {
                "book_id": "BK005",
                "title": "Between Two Temples",
                "isbn": "978-93-5XXXX-05-9",
                "genre": "Historical Fiction",
                "publication_date": "2024-07-05",
                "status": "Published & Live",
                "mrp": 425,
                "author_royalty_per_copy": 38,
                "copies_sold": 67,
                "royalty_earned": 2546,
                "royalty_paid": 0,
                "royalty_pending": 2546,
                "last_royalty_payout_date": None,
                "print_partner": "Epitome Books",
                "available_on": ["Amazon India", "BookLeaf Store"]
            }
        ]
    },
    {
        "author_id": "AUTH004",
        "name": "Vikram Joshi",
        "email": "vikram.joshi@email.com",
        "phone": "+91-65432-10987",
        "city": "Pune",
        "joined_date": "2023-07-12",
        "username": "vikram_joshi",
        "password": "author123",
        "books": [
            {
                "book_id": "BK006",
                "title": "Debugging Life",
                "isbn": "978-93-5XXXX-06-6",
                "genre": "Self-Help",
                "publication_date": "2023-11-30",
                "status": "Published & Live",
                "mrp": 299,
                "author_royalty_per_copy": 25,
                "copies_sold": 534,
                "royalty_earned": 13350,
                "royalty_paid": 10000,
                "royalty_pending": 3350,
                "last_royalty_payout_date": "2025-08-20",
                "print_partner": "In-House",
                "available_on": ["Amazon India", "Flipkart", "BookLeaf Store"]
            },
            {
                "book_id": "BK007",
                "title": "The Last Monsoon",
                "isbn": "978-93-5XXXX-07-3",
                "genre": "Poetry",
                "publication_date": "2024-08-15",
                "status": "Published & Live",
                "mrp": 199,
                "author_royalty_per_copy": 15,
                "copies_sold": 123,
                "royalty_earned": 1845,
                "royalty_paid": 1845,
                "royalty_pending": 0,
                "last_royalty_payout_date": "2025-12-01",
                "print_partner": "In-House",
                "available_on": ["Amazon India", "BookLeaf Store"]
            }
        ]
    },
    {
        "author_id": "AUTH005",
        "name": "Meera Nair",
        "email": "meera.nair@email.com",
        "phone": "+91-54321-09876",
        "city": "Kochi",
        "joined_date": "2023-01-05",
        "username": "meera_nair",
        "password": "author123",
        "books": [
            {
                "book_id": "BK008",
                "title": "Cardamom & Chaos",
                "isbn": "978-93-5XXXX-08-0",
                "genre": "Contemporary Fiction",
                "publication_date": "2023-04-18",
                "status": "Published & Live",
                "mrp": 375,
                "author_royalty_per_copy": 32,
                "copies_sold": 445,
                "royalty_earned": 14240,
                "royalty_paid": 14240,
                "royalty_pending": 0,
                "last_royalty_payout_date": "2025-12-01",
                "print_partner": "Repro India",
                "available_on": ["Amazon India", "Flipkart", "BookLeaf Store"]
            },
            {
                "book_id": "BK009",
                "title": "Letters from Lakshadweep",
                "isbn": "978-93-5XXXX-09-7",
                "genre": "Travel / Non-Fiction",
                "publication_date": "2024-03-01",
                "status": "Published & Live",
                "mrp": 550,
                "author_royalty_per_copy": 55,
                "copies_sold": 201,
                "royalty_earned": 11055,
                "royalty_paid": 8000,
                "royalty_pending": 3055,
                "last_royalty_payout_date": "2025-10-15",
                "print_partner": "In-House",
                "available_on": ["Amazon India", "Amazon US", "BookLeaf Store"]
            }
        ]
    },
    {
        "author_id": "AUTH006",
        "name": "Arjun Malhotra",
        "email": "arjun.malhotra@email.com",
        "phone": "+91-43210-98765",
        "city": "Chandigarh",
        "joined_date": "2024-06-01",
        "username": "arjun_malhotra",
        "password": "author123",
        "books": [
            {
                "book_id": "BK010",
                "title": "Turban Tales",
                "isbn": "978-93-5XXXX-10-3",
                "genre": "Humor / Essays",
                "publication_date": "2024-09-10",
                "status": "Published & Live",
                "mrp": 325,
                "author_royalty_per_copy": 28,
                "copies_sold": 88,
                "royalty_earned": 2464,
                "royalty_paid": 0,
                "royalty_pending": 2464,
                "last_royalty_payout_date": None,
                "print_partner": "In-House",
                "available_on": ["Amazon India", "BookLeaf Store"]
            }
        ]
    },
    {
        "author_id": "AUTH007",
        "name": "Sneha Kulkarni",
        "email": "sneha.kulkarni@email.com",
        "phone": "+91-32109-87654",
        "city": "Bangalore",
        "joined_date": "2022-09-18",
        "username": "sneha_kulkarni",
        "password": "author123",
        "books": [
            {
                "book_id": "BK011",
                "title": "The Algorithm of Love",
                "isbn": "978-93-5XXXX-11-0",
                "genre": "Romance",
                "publication_date": "2022-12-25",
                "status": "Published & Live",
                "mrp": 299,
                "author_royalty_per_copy": 25,
                "copies_sold": 1567,
                "royalty_earned": 39175,
                "royalty_paid": 35000,
                "royalty_pending": 4175,
                "last_royalty_payout_date": "2025-11-15",
                "print_partner": "Repro India",
                "available_on": ["Amazon India", "Flipkart", "Amazon US", "BookLeaf Store"]
            },
            {
                "book_id": "BK012",
                "title": "Ctrl+Alt+Delete My Ex",
                "isbn": "978-93-5XXXX-12-7",
                "genre": "Romance / Humor",
                "publication_date": "2024-02-14",
                "status": "Published & Live",
                "mrp": 350,
                "author_royalty_per_copy": 30,
                "copies_sold": 723,
                "royalty_earned": 21690,
                "royalty_paid": 18000,
                "royalty_pending": 3690,
                "last_royalty_payout_date": "2025-10-15",
                "print_partner": "In-House",
                "available_on": ["Amazon India", "Flipkart", "BookLeaf Store"]
            },
            {
                "book_id": "BK013",
                "title": "Midnight in Mysore",
                "isbn": "978-93-5XXXX-13-4",
                "genre": "Thriller",
                "publication_date": None,
                "status": "In Production - Cover Design",
                "mrp": None,
                "author_royalty_per_copy": None,
                "copies_sold": 0,
                "royalty_earned": 0,
                "royalty_paid": 0,
                "royalty_pending": 0,
                "last_royalty_payout_date": None,
                "print_partner": None,
                "available_on": []
            }
        ]
    },
    {
        "author_id": "AUTH008",
        "name": "Farhan Sheikh",
        "email": "farhan.sheikh@email.com",
        "phone": "+91-21098-76543",
        "city": "Lucknow",
        "joined_date": "2023-10-01",
        "username": "farhan_sheikh",
        "password": "author123",
        "books": [
            {
                "book_id": "BK014",
                "title": "Ghazal of the Forgotten",
                "isbn": "978-93-5XXXX-14-1",
                "genre": "Poetry / Urdu Literature",
                "publication_date": "2024-01-26",
                "status": "Published & Live",
                "mrp": 250,
                "author_royalty_per_copy": 20,
                "copies_sold": 156,
                "royalty_earned": 3120,
                "royalty_paid": 3120,
                "royalty_pending": 0,
                "last_royalty_payout_date": "2025-12-01",
                "print_partner": "Epitome Books",
                "available_on": ["Amazon India", "BookLeaf Store"]
            }
        ]
    },
    {
        "author_id": "AUTH009",
        "name": "Kavita Deshmukh",
        "email": "kavita.deshmukh@email.com",
        "phone": "+91-10987-65432",
        "city": "Nagpur",
        "joined_date": "2024-04-10",
        "username": "kavita_deshmukh",
        "password": "author123",
        "books": [
            {
                "book_id": "BK015",
                "title": "Raising Roots",
                "isbn": "978-93-5XXXX-15-8",
                "genre": "Parenting / Non-Fiction",
                "publication_date": None,
                "status": "In Production - Typesetting",
                "mrp": None,
                "author_royalty_per_copy": None,
                "copies_sold": 0,
                "royalty_earned": 0,
                "royalty_paid": 0,
                "royalty_pending": 0,
                "last_royalty_payout_date": None,
                "print_partner": None,
                "available_on": []
            },
            {
                "book_id": "BK016",
                "title": "The Nagpur Notebooks",
                "isbn": "978-93-5XXXX-16-5",
                "genre": "Essays / Memoir",
                "publication_date": "2024-11-05",
                "status": "Published & Live",
                "mrp": 299,
                "author_royalty_per_copy": 25,
                "copies_sold": 34,
                "royalty_earned": 850,
                "royalty_paid": 0,
                "royalty_pending": 850,
                "last_royalty_payout_date": None,
                "print_partner": "In-House",
                "available_on": ["Amazon India", "BookLeaf Store"]
            }
        ]
    },
    {
        "author_id": "AUTH010",
        "name": "Diya Chatterjee",
        "email": "diya.chatterjee@email.com",
        "phone": "+91-09876-54321",
        "city": "Kolkata",
        "joined_date": "2023-05-22",
        "username": "diya_chatterjee",
        "password": "author123",
        "books": [
            {
                "book_id": "BK017",
                "title": "Durga\u2019s Daughters",
                "isbn": "978-93-5XXXX-17-2",
                "genre": "Literary Fiction",
                "publication_date": "2023-10-15",
                "status": "Published & Live",
                "mrp": 475,
                "author_royalty_per_copy": 45,
                "copies_sold": 612,
                "royalty_earned": 27540,
                "royalty_paid": 25000,
                "royalty_pending": 2540,
                "last_royalty_payout_date": "2025-11-15",
                "print_partner": "Repro India",
                "available_on": ["Amazon India", "Flipkart", "Amazon US", "BookLeaf Store"]
            },
            {
                "book_id": "BK018",
                "title": "Howrah Nights",
                "isbn": "978-93-5XXXX-18-9",
                "genre": "Crime / Thriller",
                "publication_date": "2025-01-20",
                "status": "Published & Live",
                "mrp": 399,
                "author_royalty_per_copy": 35,
                "copies_sold": 45,
                "royalty_earned": 1575,
                "royalty_paid": 0,
                "royalty_pending": 1575,
                "last_royalty_payout_date": None,
                "print_partner": "In-House",
                "available_on": ["Amazon India", "BookLeaf Store"]
            }
        ]
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with all 10 authors and 18 books from the Bookleaf dataset'

    def handle(self, *args, **kwargs):
        # ── Admin ──────────────────────────────────────────────────────────────
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@bookleaf.com',
                'password': make_password('admin123'),
                'role': 'admin',
                'first_name': 'Super',
                'last_name': 'Admin',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Admin created  ->  admin / admin123'))
        else:
            self.stdout.write('  Admin already exists, skipping.')

        # -- Authors & Books -------------------------------------------------------
        for data in AUTHORS_DATA:
            first, *rest = data['name'].split()
            last = ' '.join(rest) if rest else ''

            author, a_created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'password': make_password(data['password']),
                    'role': 'author',
                    'first_name': first,
                    'last_name': last,
                    'author_id': data['author_id'],
                    'phone': data['phone'],
                    'city': data['city'],
                    'joined_date': data['joined_date'],
                }
            )
            status = '[NEW]  ' if a_created else '[SKIP] '
            self.stdout.write(f'{status} Author: {data["name"]}  ({data["author_id"]})')

            for b in data['books']:
                book, b_created = Book.objects.get_or_create(
                    isbn=b['isbn'],
                    defaults={
                        'author': author,
                        'book_id': b['book_id'],
                        'title': b['title'],
                        'genre': b['genre'],
                        'publication_date': b.get('publication_date'),
                        'status': b['status'],
                        'mrp': b.get('mrp'),
                        'author_royalty_per_copy': b.get('author_royalty_per_copy'),
                        'copies_sold': b.get('copies_sold', 0),
                        'royalty_earned': b.get('royalty_earned', 0),
                        'royalty_paid': b.get('royalty_paid', 0),
                        'royalty_pending': b.get('royalty_pending', 0),
                        'last_royalty_payout_date': b.get('last_royalty_payout_date'),
                        'print_partner': b.get('print_partner'),
                        'available_on': b.get('available_on', []),
                    }
                )
                b_status = '    [NEW]  Book:' if b_created else '    [SKIP] Book:'
                self.stdout.write(f'{b_status} {b["title"]}  ({b["book_id"]})')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('\nCredentials:')
        self.stdout.write('  Authors  ->  password: author123')
        self.stdout.write('  Admin    ->  admin / admin123')
