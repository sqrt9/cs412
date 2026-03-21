#models.py 2026
# Voter model and loading function
# reads the csv which should be placed
# next to this file
# Theodore Harlan
# hpt@bu.edu

from datetime import datetime
from django.db import models
import csv
import os

# Create your models here.

class Voter(models.Model):
    last_name = models.CharField()
    first_name = models.CharField()
    street_number = models.CharField()
    street_name = models.CharField()
    apartment_number = models.CharField(blank=True, null=True)
    zip_code = models.CharField()
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_registration = models.DateField(blank=True, null=True)
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField()
    
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

def load_data():
    Voter.objects.all().delete()
    data = os.path.join(os.path.dirname(__file__), 'newton_voters.csv')
    with open(data, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            # try and make a format of dates that djano wants otherwise none
            try:
                dob = datetime.strptime(row['Date of Birth'].strip(), '%Y-%m-%d').date()
            except ValueError:
                dob = None
            try:
                dor = datetime.strptime(row['Date of Registration'].strip(), '%Y-%m-%d').date()
            except ValueError:
                dor = None

            Voter.objects.create(
                last_name=row['Last Name'].strip(),
                first_name=row['First Name'].strip(),
                street_number=row['Residential Address - Street Number'].strip(),
                street_name=row['Residential Address - Street Name'].strip(),
                apartment_number=row['Residential Address - Apartment Number'].strip() or None,
                zip_code=row['Residential Address - Zip Code'].strip(),
                #there is invalid dates in here for somereaosn
                date_of_birth=dob,
                date_of_registration=dor,
                party_affiliation=row['Party Affiliation'].strip(),
                precinct_number=row['Precinct Number'].strip(),
                v20state=row['v20state'].strip() == 'TRUE',
                v21town=row['v21town'].strip() == 'TRUE',
                v21primary=row['v21primary'].strip() == 'TRUE',
                v22general=row['v22general'].strip() == 'TRUE',
                v23town=row['v23town'].strip() == 'TRUE',
                voter_score=int(row['voter_score'].strip()),
            )
    print(f"Loaded {Voter.objects.count()} voters.")