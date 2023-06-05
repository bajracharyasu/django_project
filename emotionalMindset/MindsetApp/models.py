from django.db import models

# Create your models here.
class user (models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    def __str__(self):
        return self.email
    class Meta:
        db_table ='MindsetApp_user'
    
class Result(models.Model):
    always = models.IntegerField()
    often = models.IntegerField()
    sometimes = models.IntegerField()
    none = models.IntegerField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
class Disease(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    symptoms = models.CharField(max_length=200)
    treatment = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    class Meta:
        db_table ='MindsetApp_disease'

class Questions(models.Model):
    title = models.CharField(max_length=200)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        db_table ='MindsetApp_questions'

class Patient(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    class Meta:
        db_table ='MindsetApp_patient'
class Output(models.Model):
        patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
        question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
        disease_id = models.ForeignKey(Disease, on_delete=models.CASCADE, null=False)
        always = models.IntegerField(null = True)
        often = models.IntegerField(null = True)
        sometimes = models.IntegerField(null = True)
        never = models.IntegerField(null = True)
        prediction = models.CharField(max_length=200, null=True)
        def __str__(self):
            return self.prediction
        class Meta:
            db_table ='MindsetApp_output'

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='images/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table ='MindsetApp_hospital'
class ChatRoom(models.Model):
    location = models.CharField(max_length=200)
    def __str__(self):
        return self.location
    class Meta:
        db_table ='MindsetApp_chatroom'
class Chat(models.Model):
    hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.patient} {self.content}'
    class Meta:
        db_table ='MindsetApp_chat'
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.IntegerField(null=True)
    message = models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        db_table ='MindsetApp_contact'
