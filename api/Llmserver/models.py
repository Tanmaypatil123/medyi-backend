from django.db import models

class LLMServers(models.Model):
    name = models.CharField(max_length=100)
    server_url = models.CharField(max_length=100)
    def __str__(self):
        return self.name