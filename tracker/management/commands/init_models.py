"""
Django management command to initialize AI models in the database
"""
from django.core.management.base import BaseCommand
from tracker.models import AIModel


class Command(BaseCommand):
    help = 'Initialize AI models in the database'

    def handle(self, *args, **options):
        models_data = [
            ('chatgpt', 'ChatGPT', 1.0),
            ('claude', 'Claude', 0.9),
            ('gemini', 'Gemini', 0.8),
        ]
        
        for model_name, display_name, weight in models_data:
            model, created = AIModel.objects.get_or_create(
                name=model_name,
                defaults={
                    'display_name': display_name,
                    'weight': weight,
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created model: {display_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Model already exists: {display_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ AI models initialized successfully!')
        )
