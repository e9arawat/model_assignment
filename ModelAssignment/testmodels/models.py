from django.db import models
import random
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from faker import Faker
from django.utils.text import slugify
from django.db.models import Q


# Create your models here.   


class Profile(models.Model):
    
    username = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()
    email = models.EmailField(primary_key=True)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "profile"
    
    @classmethod
    def generate_random_data(self): 
        usernames = set()
        phones = set()
        addresses = set()
        fake = Faker()
    
        while len(usernames) < 50000:
            usernames.add(fake.user_name())

        while len(phones) < 50000:
            phones.add(f'+91 {fake.msisdn()[3:]}')

        while len(addresses) < 50000:
            addresses.add(fake.address())

        profiles = []

        for username, phone, address in zip(usernames, phones, addresses):
            profile = Profile(slug=slugify(username), username=username, email=f'{username}@gmail.com', phone=phone, address=address)
            profiles.append(profile)

        Profile.objects.bulk_create(profiles)  


    def get_author_details(self):
        profiles = Profile.objects.all()

        ans = {}
        for profile in profiles:
            author = profile.profile_related.all()[0]
            ans[author.name] = {'slug' : profile.slug, 'username' : profile.username, 'email' : profile.email, 'phone' : profile.phone, 'address' : profile.address}
    
        return ans
    



class Author(models.Model):

    slug = models.SlugField()
    name = models.CharField(max_length=255)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="profile_related")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "author"

    @classmethod
    def generate_random_data(self):
        fake = Faker()
        names = set()
        profiles = list(Profile.objects.all())

        while len(names) < 50000:
            names.add(fake.name())

        authors = []
        for name, profile in zip(names, profiles):
            author = Author(slug=slugify(name), name=name, profile=profile)
            authors.append(author)

        Author.objects.bulk_create(authors) 


    def get_all_authors(self):
        all_data = Author.objects.all()
        authors = [x.name for x in all_data]
        return authors

    
    def get_all_books_startswith(self):
        authors = Author.objects.filter(name__startswith = 'a')

        return [author.title for x in authors for author in x.author_related.all()]


    def get_author_book(self, author_name):
        author_data = Author.objects.get(name=author_name)
        books_data = author_data.author_related.all()
        books = [book.title for book in books_data] 
        return books
    
    def get_authors(self):
        authors = Author.objects.all()
        ans = [author.name for author in authors if len(author.author_related.all()) > 1]
        return ans
    
    def get_all_books_endswith(self):
        authors = Author.objects.filter(name__endswith = 'a')

        return [author.title for x in authors for author in x.author_related.all()]
    
    def get_profile_details(self, author_name):
        author = Author.objects.get(name__icontains=author_name)
        p = author.profile
        return [p.slug, p.username, p.email, p.phone, p.address]
        
    def get_author_books(self):
        authors = Author.objects.all()
        
        ans = {author.name : len(author.author_related.all()) for author in authors}
        
        return ans
    
    def get_books_except(self, author_name):
        authors = Author.objects.exclude(name__iexact = author_name)
        
        ans = [x.title for author in authors for x in author.author_related.all()]
        return ans
    

    def author_books(self, author_A, author_B):
        authors =  Author.objects.filter(Q(author__name__iexact=author_A) | Q(author__name__iexact=author_B))

        return [x.title for author in authors for x in author.author_related.all()]


class Publisher(models.Model):
    
    slug = models.SlugField()
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(max_length=255)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "publisher"

    @classmethod
    def generate_random_data(self):
        fake = Faker()
        names = set()
        websites = set()
        addresses = set()

        while len(names) < 50000:
            names.add(fake.company())

        while len(addresses) < 50000:
            addresses.add(fake.address())

        while len(websites) < 50000:
            websites.add(fake.url())

        publishers = []

        for name, website, address in zip(names, websites, addresses):
            publisher = Publisher(slug=slugify(name), name=name, website=website, email=f'{name.replace(" ", "")}@{fake.domain_name()}', address=address)
            publishers.append(publisher)

        Publisher.objects.bulk_create(publishers)

    @classmethod
    def get_publisher_book(self, publisher_name):
        
        publisher_data = Publisher.objects.all()
        ans = []
        for publisher in publisher_data:
            if publisher.name == publisher_name:
                book = publisher.publisher_related.all()
                for x in book:
                    ans.append(x.title)
                
        return ans
    
    @classmethod
    def get_books(self, publisher_name):
        publishers = Publisher.objects.filter(name=publisher_name)
        
        ans = set()
        for publisher in publishers:
            book = publisher.publisher_related.all()
            for x in book:
                ans.add(x.title)
                
        return ans
    
    def get_publisher_books(self, publisher_website):
        publisher = Publisher.objects.get(website=publisher_website)
        
        ans = set()
        book = publisher.publisher_related.all()
        for x in book:
            ans.add(x.title)
                
        return ans
    
    def get_all_publishers_books(self, input_list):
        
        ans = set()
        for publisher_name in input_list:
            publishers = Publisher.objects.filter(name=publisher_name)            
            for publisher in publishers:
                book = publisher.publisher_related.all()
                for x in book:
                    ans.add(x.title)
                
        return list(ans)


class Book(models.Model):

    genre_choices = [
        ('horror','horror'),
        ('self help','self help'),
        ('adventure','adventure'),
        ('others','others')
    ]

    slug = models.SlugField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_related")
    title = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name="publisher_related")
    date_of_pub = models.DateField(verbose_name="Published Date")
    is_deleted = models.BooleanField(default=False)
    genre = models.CharField(max_length=100, default='others', choices=genre_choices)

    class Meta:
        unique_together = ('author', 'title', 'date_of_pub')
        ordering = ['date_of_pub']
        verbose_name = 'book'

    def __str__(self):
        return self.title
    

    def generate_random_data(self):
        fake = Faker()
        authors = Author.objects.all()
        titles = set()
        publishers = Publisher.objects.all()
        date_of_pubs = set()

        while len(titles) < 50000:
            titles.add(fake.sentence(nb_words=3))

        # while len(date_of_pubs) < 50000:
        #     date_of_pubs.add(datetime.date(fake.date()))


        while len(date_of_pubs) < 50000:
            start_date = datetime.now() - timedelta(days=random.randint(1, 10000)) 
            
            date_of_pubs.add(start_date)

        books = []

        for title, date_of_pub in zip(titles, date_of_pubs):
            book = Book(slug=slugify(title), author=random.choice(authors), title=title, publisher=random.choice(publishers), date_of_pub=date_of_pub)
            books.append(book)

        Book.objects.bulk_create(books)

    def get_books(self, author_name, publisher_name):
        books = Book.objects.all()

        ans = [book.title for book in books if book.author.name==author_name and book.publisher.name == publisher_name]
        return ans
            
    def get_year_books(self, input_year):
        books = Book.objects.filter(date_of_pub__year = input_year)

        ans = [book.title for book in books]
        return ans
    
    def get_status(self, *args):
        book, created = Book.objects.get_or_create(
            slug=args[0],
            author=args[1],
            title = args[2],
            publisher = args[3],
            date_of_pub = args[4]
        )
        
        return [book, created]
    
    
    def delete_book(self, book_title):
        book = get_object_or_404(Book, title=book_title)
        book.delete()
        return "Deleted"
    
    def soft_delete_book(self, book_id):
        book = get_object_or_404(Book, id=book_id)
        
        book.is_deleted = True
        book.save()
        
        return "Soft deleted successfully"


class Collection(models.Model):

    
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    book = models.ManyToManyField(Book)

    class Meta:
        verbose_name = "collection"
        db_table = 'book_collection'

    def __str__(self):
        return self.name

    def get_books(self):
        return "\n".join([p.title for p in self.book.all()])

    def generate_random_data(self):

        fake = Faker()
        names = set()
        books = Book.objects.all()
        

        while len(names) < 50000:
            names.add(fake.sentence(nb_words=2))

        collections = []

        for name in names:
            collection = Collection(slug=slugify(name), name=name)
            collection.save()
            collection.book.set([random.choice(books)])
            collections.append(collection)

        Collection.objects.bulk_create(collections)
