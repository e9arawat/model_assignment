from django.db import models
import random
from datetime import datetime, timedelta


# Create your models here.   


class Profile(models.Model):

    slug = models.SlugField()
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.username
    
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

   
          
    



class Author(models.Model):

    slug = models.SlugField()
    name = models.CharField(max_length=255)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.name

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
    
    


class Publisher(models.Model):
    
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=255)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name

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


    


class Book(models.Model):

    slug = models.SlugField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_related")
    title = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    date_of_pub = models.DateTimeField(verbose_name="Published Date")

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
        


class Collection(models.Model):

    
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    book = models.ManyToManyField(Book)

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
