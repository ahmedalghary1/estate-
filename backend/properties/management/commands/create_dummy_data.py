from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from properties.models import Property
import random


class Command(BaseCommand):
    help = 'Create dummy property data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy data...')
        
        # Create a seller user if none exists
        seller, created = User.objects.get_or_create(
            username='seller_demo',
            defaults={
                'email': 'seller@demo.com',
                'first_name': 'Demo',
                'last_name': 'Seller'
            }
        )
        
        if created:
            seller.set_password('demo1234')
            seller.save()
            self.stdout.write(self.style.SUCCESS(f'Created seller user: {seller.username}'))
            
            # Create user profile if it doesn't exist
            try:
                from users.models import Profile
                Profile.objects.get_or_create(
                    user=seller,
                    defaults={'user_type': 'seller'}
                )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not create profile: {e}'))
        
        # Sample property data
        properties_data = [
            {
                'title_en': 'Luxury Villa in New Cairo',
                'title_ar': 'فيلا فاخرة في القاهرة الجديدة',
                'description_en': 'A beautiful 4-bedroom villa with swimming pool and garden. Modern design with all amenities.',
                'description_ar': 'فيلا جميلة بأربعة غرف نوم مع حمام سباحة وحديقة. تصميم عصري مع جميع المرافق.',
                'location_en': 'New Cairo',
                'location_ar': 'القاهرة الجديدة',
                'price': 8500000,
                'property_type': 'Villa',
                'sale_type': 'Sale',
                'phone': '+20 100 123 4567'
            },
            {
                'title_en': 'Modern Apartment in Zamalek',
                'title_ar': 'شقة حديثة في الزمالك',
                'description_en': 'Spacious 3-bedroom apartment with Nile view. Fully furnished with modern appliances.',
                'description_ar': 'شقة واسعة بثلاثة غرف نوم مع إطلالة على النيل. مفروشة بالكامل مع أجهزة حديثة.',
                'location_en': 'Zamalek, Cairo',
                'location_ar': 'الزمالك، القاهرة',
                'price': 25000,
                'property_type': 'Apartment',
                'sale_type': 'Rent',
                'phone': '+20 100 234 5678'
            },
            {
                'title_en': 'Commercial Office in Smart Village',
                'title_ar': 'مكتب تجاري في القرية الذكية',
                'description_en': 'Premium office space 150 sqm, perfect for tech companies. High-speed internet included.',
                'description_ar': 'مساحة مكتبية فاخرة 150 متر مربع، مثالية لشركات التكنولوجيا. إنترنت عالي السرعة متضمن.',
                'location_en': 'Smart Village, Giza',
                'location_ar': 'القرية الذكية، الجيزة',
                'price': 45000,
                'property_type': 'Office',
                'sale_type': 'Rent',
                'phone': '+20 100 345 6789'
            },
            {
                'title_en': 'Investment Land in 6th October',
                'title_ar': 'أرض استثمارية في 6 أكتوبر',
                'description_en': '500 sqm land plot in prime location. Perfect for residential or commercial development.',
                'description_ar': 'قطعة أرض 500 متر مربع في موقع رئيسي. مثالية للتطوير السكني أو التجاري.',
                'location_en': '6th October City',
                'location_ar': 'مدينة 6 أكتوبر',
                'price': 3500000,
                'property_type': 'Land',
                'sale_type': 'Sale',
                'phone': '+20 100 456 7890'
            },
            {
                'title_en': 'Cozy Apartment in Maadi',
                'title_ar': 'شقة مريحة في المعادي',
                'description_en': 'Charming 2-bedroom apartment in quiet neighborhood. Close to metro and amenities.',
                'description_ar': 'شقة ساحرة من غرفتي نوم في حي هادئ. قريبة من المترو والمرافق.',
                'location_en': 'Maadi, Cairo',
                'location_ar': 'المعادي، القاهرة',
                'price': 18000,
                'property_type': 'Apartment',
                'sale_type': 'Rent',
                'phone': '+20 100 567 8901'
            },
            {
                'title_en': 'Beachfront Villa in North Coast',
                'title_ar': 'فيلا على البحر في الساحل الشمالي',
                'description_en': 'Stunning villa directly on the beach with private access. 5 bedrooms, fully equipped.',
                'description_ar': 'فيلا مذهلة مباشرة على الشاطئ مع وصول خاص. 5 غرف نوم، مجهزة بالكامل.',
                'location_en': 'North Coast',
                'location_ar': 'الساحل الشمالي',
                'price': 12000000,
                'property_type': 'Villa',
                'sale_type': 'Sale',
                'phone': '+20 100 678 9012'
            },
            {
                'title_en': 'Downtown Office Space',
                'title_ar': 'مساحة مكتبية وسط البلد',
                'description_en': 'Central office location, 200 sqm, ideal for startups and small businesses.',
                'description_ar': 'موقع مكتبي مركزي، 200 متر مربع، مثالي للشركات الناشئة والصغيرة.',
                'location_en': 'Downtown Cairo',
                'location_ar': 'وسط القاهرة',
                'price': 35000,
                'property_type': 'Office',
                'sale_type': 'Rent',
                'phone': '+20 100 789 0123'
            },
            {
                'title_en': 'Family Apartment in Heliopolis',
                'title_ar': 'شقة عائلية في مصر الجديدة',
                'description_en': 'Spacious 4-bedroom apartment perfect for families. Near schools and shopping centers.',
                'description_ar': 'شقة واسعة بأربعة غرف نوم مثالية للعائلات. بالقرب من المدارس ومراكز التسوق.',
                'location_en': 'Heliopolis, Cairo',
                'location_ar': 'مصر الجديدة، القاهرة',
                'price': 4500000,
                'property_type': 'Apartment',
                'sale_type': 'Sale',
                'phone': '+20 100 890 1234'
            },
            {
                'title_en': 'Agricultural Land in Fayoum',
                'title_ar': 'أرض زراعية في الفيوم',
                'description_en': '2000 sqm agricultural land with water access. Great investment opportunity.',
                'description_ar': 'أرض زراعية 2000 متر مربع مع إمكانية الوصول للمياه. فرصة استثمارية رائعة.',
                'location_en': 'Fayoum',
                'location_ar': 'الفيوم',
                'price': 800000,
                'property_type': 'Land',
                'sale_type': 'Sale',
                'phone': '+20 100 901 2345'
            },
            {
                'title_en': 'Studio Apartment in New Capital',
                'title_ar': 'شقة استوديو في العاصمة الإدارية',
                'description_en': 'Modern studio apartment with smart home features. Perfect for young professionals.',
                'description_ar': 'شقة استوديو حديثة مع ميزات المنزل الذكي. مثالية للمهنيين الشباب.',
                'location_en': 'New Administrative Capital',
                'location_ar': 'العاصمة الإدارية الجديدة',
                'price': 15000,
                'property_type': 'Apartment',
                'sale_type': 'Rent',
                'phone': '+20 101 012 3456'
            },
            {
                'title_en': 'Luxury Penthouse in Sheikh Zayed',
                'title_ar': 'بنتهاوس فاخر في الشيخ زايد',
                'description_en': 'Exclusive penthouse with panoramic views, 300 sqm, rooftop terrace and jacuzzi.',
                'description_ar': 'بنتهاوس حصري مع إطلالات بانورامية، 300 متر مربع، تراس على السطح وجاكوزي.',
                'location_en': 'Sheikh Zayed City',
                'location_ar': 'مدينة الشيخ زايد',
                'price': 9500000,
                'property_type': 'Apartment',
                'sale_type': 'Sale',
                'phone': '+20 101 123 4567'
            },
            {
                'title_en': 'Medical Office in Dokki',
                'title_ar': 'عيادة طبية في الدقي',
                'description_en': 'Professional medical office, ground floor, 100 sqm with waiting area.',
                'description_ar': 'عيادة طبية احترافية، الطابق الأرضي، 100 متر مربع مع منطقة انتظار.',
                'location_en': 'Dokki, Giza',
                'location_ar': 'الدقي، الجيزة',
                'price': 30000,
                'property_type': 'Office',
                'sale_type': 'Rent',
                'phone': '+20 101 234 5678'
            },
            {
                'title_en': 'Twin House in Compound',
                'title_ar': 'توين هاوس في كمبوند',
                'description_en': 'Beautiful twin house in gated community with pool, gym and security.',
                'description_ar': 'توين هاوس جميل في مجمع سكني مغلق مع حمام سباحة وصالة رياضية وأمن.',
                'location_en': '5th Settlement, New Cairo',
                'location_ar': 'التجمع الخامس، القاهرة الجديدة',
                'price': 6500000,
                'property_type': 'Villa',
                'sale_type': 'Sale',
                'phone': '+20 101 345 6789'
            },
            {
                'title_en': 'Commercial Land in Alexandria',
                'title_ar': 'أرض تجارية في الإسكندرية',
                'description_en': '1000 sqm commercial land on main road. High traffic area, excellent for retail.',
                'description_ar': 'أرض تجارية 1000 متر مربع على طريق رئيسي. منطقة ذات حركة مرور عالية، ممتازة للبيع بالتجزئة.',
                'location_en': 'Alexandria',
                'location_ar': 'الإسكندرية',
                'price': 5500000,
                'property_type': 'Land',
                'sale_type': 'Sale',
                'phone': '+20 101 456 7890'
            },
            {
                'title_en': 'Furnished Apartment in Nasr City',
                'title_ar': 'شقة مفروشة في مدينة نصر',
                'description_en': 'Fully furnished 3-bedroom apartment, ready to move in. All utilities included.',
                'description_ar': 'شقة مفروشة بالكامل من 3 غرف نوم، جاهزة للانتقال. جميع المرافق متضمنة.',
                'location_en': 'Nasr City, Cairo',
                'location_ar': 'مدينة نصر، القاهرة',
                'price': 22000,
                'property_type': 'Apartment',
                'sale_type': 'Rent',
                'phone': '+20 101 567 8901'
            },
        ]
        
        # Create properties
        created_count = 0
        for prop_data in properties_data:
            property_obj, created = Property.objects.get_or_create(
                title_en=prop_data['title_en'],
                defaults={
                    **prop_data,
                    'owner': seller,
                    'views': random.randint(10, 500)
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'  Created: {property_obj.title_en}')
                
                # Add property images using Picsum Photos
                # Create 1-3 images per property
                from properties.models import PropertyImage
                import urllib.request
                from django.core.files.base import ContentFile
                
                num_images = random.randint(1, 3)
                
                for i in range(num_images):
                    # Using Picsum Photos for reliable random images
                    # Each property gets unique seed for consistent images
                    seed = property_obj.id * 100 + i
                    img_url = f'https://picsum.photos/seed/{seed}/800/600'
                    
                    try:
                        # Download image
                        img_data = urllib.request.urlopen(img_url, timeout=15).read()
                        
                        # Create PropertyImage with ContentFile
                        PropertyImage.objects.create(
                            property=property_obj,
                            image=ContentFile(img_data, name=f'property_{property_obj.id}_{i}.jpg'),
                            order=i
                        )
                        self.stdout.write(f'[OK] Added image {i+1}')
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'[WARN] Could not download image {i+1}: {e}'))


        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} properties with images!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Total properties in database: {Property.objects.count()}'
            )
        )
