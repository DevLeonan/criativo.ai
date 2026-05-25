from django.db import models
from apps.brands.models import BrandProfile

class GeneratedContent(models.Model):
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, default='post') # post, story, reels
    caption_text = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    image_prompt = models.TextField(blank=True, null=True) # Guardamos o prompt para histórico
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.brand_name} - {self.content_type} - {self.created_at.strftime('%Y-%m-%d')}"