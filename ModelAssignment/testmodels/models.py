from django.db import models
import random


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
        slugs = set()
        usernames = set() 
        emails = set() 
        phones = set()
        addresses = set()
    
        while len(slugs) < 50000:
            slug = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
            slugs.add(slug)

        while len(usernames) < 50000:
            username = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
            usernames.add(username)

        while len(emails) < 50000:
            email = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)) + '@gmail.com'
            emails.add(email)

        while len(phones) < 50000:
            phone = ''.join(random.choice('0123456789') for _ in range(10))
            phones.add(phone)

        while len(addresses) < 50000:
            address = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(20))
            addresses.add(address)

        profiles = []

        for slug, username, email, phone, address in zip(slugs, usernames, emails, phones, addresses):
            profile = Profile(slug=slug, username=username, email=email, phone=phone, address=address)
            profiles.append(profile)

        Profile.objects.bulk_create(profiles)            
    



class Author(models.Model):

    slug = models.SlugField()
    name = models.CharField(max_length=255)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @classmethod
    def generate_random_data(self):
        slugs = set()
        names = set() 

        while len(slugs) < 50000:
            slug = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
            slugs.add(slug)

        while len(names) < 50000:
            name = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
            names.add(name)

        profile_query_set = Profile.objects.all()
        profiles = set(profile_query_set)
        authors = []

        for slug, name, profile in zip(slugs, names, profiles):
            author = Author(slug=slug, name=name, profile=profile)
            authors.append(author)

        Author.objects.bulk_create(authors) 



class Publisher(models.Model):
    
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=255)
    email = models.EmailField()
    address = models.TextField()

    @classmethod
    def generate_random_data(self):

        slugs = set()
        names = set()
        websites = set()
        emails = set()
        addresses = set()

        while len(slugs) < 50000:
            slug = "".join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
            slugs.add(slug)

        while len(names) < 50000:
            name = "".join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
            names.add(name)

        while len(websites) < 50000:
            website = "www." + "".join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)) + ".com"
            websites.add(website)
        
        while len(emails) < 50000:
            email = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)) + '@gmail.com'
            emails.add(email)

        while len(addresses) < 50000:
            address = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(20))
            addresses.add(address)


        publishers = []

        for slug, name, website, email, address in zip(slugs, names, websites, emails, addresses):
            publisher = Publisher(slug=slug, name=name, website=website, email=email, address=address)
            publishers.append(publisher)

        Publisher.objects.bulk_create(publishers)


# class Book(models.Model):

#     slug = models.SlugField()
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
#     date_of_pub = models.DateTimeField(verbose_name="Published Date")

# class Collection(models.Model):

#     slug = models.SlugField()
#     name = models.CharField(max_length=255)
#     book = models.ManyToManyField(Book)

