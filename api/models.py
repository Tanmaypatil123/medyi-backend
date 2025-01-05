from django.db import models

# Create your models here.


gender_choices = (
    ("Man","Man"),
    ("Woman","Woman"),
    ("Gay","Gay")
)

categories = (
    ("Realistic","Realistic"),
    ("Anime","Anime"),
)

identification_of_charecter = (
    ("Straight","Straight"),
    ("Lesbian","Lesbian"),
    ("Bisexual","Bisexual"),
    ("Queer","Queer"),
)
girl_ethinicity_choices = (
    ('Asian', 'Asian'),
    ('Caucasian', 'Caucasian'),
    ('Latin', 'Latin'),
    ('Black', 'Black'),
    ('South Asian', 'South Asian'),
    ('Middle Eastern', 'Middle Eastern'),
    ('Native American', 'Native American'),
)    

girl_Body_type_choices = (
    ("Skinny", "Skinny"),
    ("Athletic", "Athletic"),
    ("Average", "Average"),
    ("Curvy", "Curvy"),
    ("BBW", "BBW"),
)

girl_occupation_choices = (
    ("Student", "Student"),
    ("Teacher", "Teacher"),
    ("Nurse", "Nurse"),
    ("Doctor", "Doctor"),
    ("Police", "Police"),
    ("Firefighter", "Firefighter"),
    ("Soldier", "Soldier"),
    ("Engineer", "Engineer"),
    ("Scientist", "Scientist"),
    ("Artist", "Artist"),
    ("Musician", "Musician"),
    ("Actress", "Actress"),
    ("Model", "Model"),
    ("Writer", "Writer"),
    ("Chef", "Chef"),
    ("Athlete", "Athlete"),
    ("Businesswoman", "Businesswoman"),
    ("Politician", "Politician"),
    ("Housewife", "Housewife"),
    ("Unemployed", "Unemployed"),
    # Newly added occupations
    ("Massage Therapist", "Massage Therapist"),
    ("Fitness Coach", "Fitness Coach"),
    ("Librarian", "Librarian"),
    ("Secretary", "Secretary"),
    ("Yoga Instructor", "Yoga Instructor"),
    ("Flight Attendant", "Flight Attendant"),
    ("Dancer", "Dancer"),
    ("Spy", "Spy"),
    ("Bartender", "Bartender"),
    ("IT Girl", "IT Girl"),
)


girl_personality_choices = (
    ("Caregiver", "Caregiver"),
    ("Sage", "Sage"),
    ('Shy', 'Shy'),
    ('Innocent', 'Innocent'),
    ('Optimistic', 'Optimistic'),
    ('Adventurous', 'Adventurous'),
    ('Sarcastic', 'Sarcastic'),
    ('Sassy', 'Sassy'),
    ('Nerdy', 'Nerdy'),
    ('Tomboy', 'Tomboy'),
    ('Girly', 'Girly'),
    ('Sporty', 'Sporty'),
    ('Elegant', 'Elegant'),
    ('Gothic', 'Gothic'),
    ('Emo', 'Emo'),
    ('Punk', 'Punk'),
    ('Hippie', 'Hippie'),
    ('Gamer', 'Gamer'),
    ('Bookworm', 'Bookworm'),
    ("Jester", "Jester"),
)


girl_charector_relation_ship_choices = (
    ("Stranger", "Stranger"),
    ("Colleague", "Colleague"),
    ("GirlFriend", "GirlFriend"),
    ("Wife", "Wife"),
    ("Mother", "Mother"),
    ("Friend", "Friend"),
    ("Single", "Single"),
    ("Boss", "Boss"),
    ("Girl next door","Girl next door"),
    ("Ex","Ex"),
    ("AI","AI"),
    ("Transgender","Transgender"),
)

girl_charector_voice_choices = (
    ("Seducing", "Seducing"),
    ("Attrative", "Attrative"),
    ("Commanding", "Commanding"),
    ("Whispering", "Whispering"),
    ("Deep", "Deep"),
    ("Lovely", "Lovely"),
    ("Sassy", "Sassy"),
    ("Sad" , "Sad" ),
    ("Calm" , "Calm" ),
    ("Intense" , "Intense" ),
    ("Warm" , "Warm" ),
    ("Rich" , "Rich" ),
)

girl_charector_conversation_skill_choices = (
    ("Short", "Short"),
    ("Medium", "Medium"),
    ("Long", "Long"),
)

girl_breast_size_choices = (
    ("Flat", "Flat"),
    ("Small", "Small"),
    ("Medium", "Medium"),
    ("Large", "Large"),
    ("Huge", "Huge"),
)

girl_booty_size_choices = (
    ("Skinny", "Skinny"),
    ("Small", "Small"),
    ("Medium", "Medium"),
    ("Large", "Large"),
    ("Athletic", "Athletic"),
)

girl_pubic_hair_choices = (
    ("Shaved", "Shaved"),
    ("Trimmed", "Trimmed"),
    ("Hairy", "Hairy"),
)

girl_hair_style_choices = (
    ("Straight", "Straight"),
    ("Curly", "Curly"),
    ("Braids", "Braids"),
    ("Bangs", "Bangs"),
    ("Bun", "Bun"),
    ("Ponytail", "Ponytail"),
    ("Pigtails", "Pigtails"),
)

girl_hair_color_choices = (
    ("Black", "Black"),
    ("Brown", "Brown"),
    ("Blonde", "Blonde"),
    ("Red", "Red"),
    ("Grey", "Grey"),
    ("White", "White"),
    ("Blue", "Blue"),
    ("Green", "Green"),
    ("Pink", "Pink"),
    ("Purple", "Purple"),
)

girl_eye_color_choices = (
    ("Brown", "Brown"),
    ("Blue", "Blue"),
    ("Green", "Green"),
)

class FriendDetails(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    # ethinicity = models.CharField(max_length=100, choices=ethinicity_choices)



    def __str__(self):
        return self.name