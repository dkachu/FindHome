from django.db import models
from cloudinary.models import CloudinaryField

# --- HOUSE MODELS ---

class House(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    sqft = models.IntegerField()
    
    #  Cloudinary handles the main thumbnail
    photo_main = CloudinaryField('image', folder='houses/')
    
    # Owner contact info
    whatsapp_number = models.CharField(
        max_length=20, 
        help_text="Enter with country code (e.g., +254741450193)"
    )
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True)

    def get_whatsapp_url(self):
        # Clean number and return a click-to-chat link
        clean_number = self.whatsapp_number.replace("+", "").replace(" ", "")
        return f"https://wa.me{clean_number}"

    def __str__(self):
        return self.title


class HouseImage(models.Model):
    # Link to the main House model
    house = models.ForeignKey(House, related_name='gallery', on_delete=models.CASCADE)
    
    #  Cloudinary handles the gallery images
    image = CloudinaryField('image', folder='gallery/')

    def __str__(self):
        return f"Image for {self.house.title}"
    

# --- COMPANY & CONTACT MODELS ---

class CompanyProfile(models.Model):
    name = models.CharField(max_length=100, default="Kiota")
    
    #  Cloudinary handles the logo
    logo = CloudinaryField('image', folder='company/', help_text="Upload company logo")
    
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, help_text="Format: 254700000000")
    address = models.CharField(max_length=255)
    about_description = models.TextField()
    facebook_url = models.URLField(max_length=255 ,blank=True, null=True)
    instagram_url = models.URLField(max_length=255,blank=True, null=True)
    twitter_url = models.URLField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Ensures only one profile exists
        if not self.pk and CompanyProfile.objects.exists():
            return 
        return super(CompanyProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Company Profile"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.name} ({self.email})"
