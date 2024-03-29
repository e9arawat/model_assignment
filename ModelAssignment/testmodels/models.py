from django.db import models
import random
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404


# Create your models here.   


class Profile(models.Model):

    slug = models.SlugField()
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(primary_key=True)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "profile"
    
    @classmethod
    def generate_random_data(self): 
        unique_datas = set()
        slugs = []
        usernames = []
        emails = []
        phones = set()
        addresses = set()
    
        while len(unique_datas) < 50000:
            unique_data = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
            unique_datas.add(unique_data)
            
        for username in unique_datas:
            usernames.append(username)
            emails.append(username + "@gmail.com")
            slugs.append(username + "-slug")

        while len(phones) < 50000:
            phone = ''.join(random.choice('123456789') for _ in range(10))
            phones.add(phone)

        while len(addresses) < 50000:
            address = "H.No. " + random.choice('123456789') + ", " + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)) + ", India"
            addresses.add(address)

        profiles = []

        for slug, username, email, phone, address in zip(slugs, usernames, emails, phones, addresses):
            profile = Profile(slug=slug, username=username, email=email, phone=phone, address=address)
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
        unique_datas = set()
        slugs = []
        names = []
        profiles = list(Profile.objects.all())
        while len(unique_datas) < 50000:
            unique_data = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
            unique_datas.add(unique_data)

        for user in unique_datas:
            names.append(user)
            slugs.append(user + "-slug")

        authors = []

        for slug, name, profile in zip(slugs, names, profiles):
            author = Author(slug=slug, name=name, profile=profile)
            authors.append(author)

        Author.objects.bulk_create(authors) 


    def get_all_authors(self):
        all_data = Author.objects.all()
        authors = [x.name for x in all_data]
        return authors


    # def get_author_details(self):
    #     all_authors = Author.objects.all()
    #     ans = []

    #     for author in all_authors:
    #         profile_data = author.profile.all()
    #         ans.append({author.name : [profile_data.username, profile_data.email, profile_data.address]})

    #     return ans
    
    def get_all_books(self):
        authors = Author.objects.all()

        return [author.author_related.all()[0].title for author in authors if author.name[0].lower() == 'a']


    def get_author_book(self, author_name):
        author_data = Author.objects.get(name=author_name)
        books_data = author_data.author_related.all()
        books = [book.title for book in books_data] 
        return books
    
    def get_authors(self):
        authors = Author.objects.all()
        ans = [author.name for author in authors if len(author.author_related.all()) > 1]
        return ans
    
    def get_all_books(self):
        authors = Author.objects.all()

        return [author.author_related.all()[0].title for author in authors if author.name[-1].lower() == 'a']
    
    def get_profile_details(self, author_name):
        author = Author.objects.get(name=author_name.lower())
        
        p = author.profile
        return [p.slug, p.username, p.email, p.phone, p.address]
        
    def get_author_books(self):
        authors = Author.objects.all()
        
        ans = {author.name : [x.title for x in author.author_related.all()] for author in authors}
        
        return ans
    
    def get_books_except(self, author_name):
        authors = Author.objects.exclude(name = author_name)
        
        ans = [x.title for author in authors for x in author.author_related.all()]
        return ans

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

        unique_datas = set()
        slugs = []
        names = []
        websites = []
        emails = []
        addresses = set()

        while len(unique_datas) < 50000:
            unique_data = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
            unique_datas.add(unique_data)


        for user in unique_datas:
            names.append(user)
            slugs.append(user + "-slug")
            websites.append("www." + user + ".com")
            emails.append(user + "@gmail.com")

        while len(addresses) < 50000:
            address = "H.No. " + random.choice('123456789') + ", " + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)) + ", India"
            addresses.add(address)

        publishers = []

        for slug, name, website, email, address in zip(slugs, names, websites, emails, addresses):
            publisher = Publisher(slug=slug, name=name, website=website, email=email, address=address)
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
    date_of_pub = models.DateTimeField(verbose_name="Published Date")
    is_deleted = models.BooleanField(default=False)
    genre = models.CharField(max_length=100, default='horror', choices=genre_choices)

    class Meta:
        unique_together = ('author', 'title', 'date_of_pub')
        ordering = ['date_of_pub']
        verbose_name = 'book'

    def __str__(self):
        return self.title
    

    def generate_random_data(self):

        slugs = set()
        authors = Author.objects.all()
        titles = set()
        publishers = set(Publisher.objects.all())
        date_of_pubs = set()

        while len(slugs) < 50000:
            slug = "".join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)) 
            slugs.add(slug)

        while len(titles) < 50000:
            title = "".join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)) 
            titles.add(title)

        while len(date_of_pubs) < 50000:
            start_date = datetime.now() - timedelta(days=random.randint(1, 3650)) 
            end_date = datetime.now() 
            date_of_pub = start_date + (end_date - start_date) * random.random()
            date_of_pubs.add(date_of_pub)

        books = []

        for slug, title, publisher, date_of_pub in zip(slugs, titles, publishers, date_of_pubs):
            book = Book(slug=slug, author=random.choice(authors), title=title, publisher=publisher, date_of_pub=date_of_pub)
            books.append(book)

        Book.objects.bulk_create(books)

    def get_books(self, author_name, publisher_name):
        books = Book.objects.all()

        ans = [book.title for book in books if book.author.name==author_name and book.publisher.name == publisher_name]
        return ans
            
    def get_year_books(self, input_year):
        books = Book.objects.all()

        ans = [book.title for book in books if book.date_of_pub.year == input_year]
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

        unique_datas = set()
        slugs = []
        names = []
        books = Book.objects.all()
        

        while len(unique_datas) < 50000:
            unique_data = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
            unique_datas.add(unique_data)


        for user in unique_datas:
            names.append(user)
            slugs.append(user + "-slug")

        collections = []

        for slug, name in zip(slugs, names):
            collection = Collection(slug=slug, name=name)
            collection.save()
            collection.book.set([random.choice(books)])
            collections.append(collection)

        Collection.objects.bulk_create(collections)
