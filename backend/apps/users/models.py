import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models




# Modèle pour représenter les rôles des utilisateurs de l'application
class Role(models.Model):

    ROLE_CHOICES = [
        ('etudiant','Etudiant'),
        ('enseignant','Enseignant'),
        ('superviseur','Superviseur'),
        ('responsable','Responsable de Master'),
        ('admin','Administrateur'),
        ('jury','Membre de jury'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, choices=ROLE_CHOICES, unique=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.name


# Manager personnalisé pour gérer la création d'utilisateurs et de superutilisateurs
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("L'email est obligatoire")

        email = self.normalize_email(email)

        role_name = extra_fields.get('role')

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        # Attribution automatique du rôle ManyToMany
        if role_name:

            role_obj, created = Role.objects.get_or_create(name=role_name)

            user.roles.add(role_obj)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)





# Modèle personnalisé pour représenter les utilisateurs de l'application  
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
        ('superviseur', 'Superviseur'),
        ('responsable', 'Responsable de Master'),
        ('admin', 'Administrateur'),
        ('jury', 'Membre de Jury'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    roles = models.ManyToManyField(Role, related_name='users', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'role']

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"




# Modèle pour représenter les enseignants de l'application
class Teacher(models.Model):
    GRADE_CHOICES = [
        ('Assistant', 'Assistant'),
        ('Maitre_Assistant', 'Maître Assistant'),
        ('Maitre_Conferences', 'Maître de Conférences'),
        ('Professeur', 'Professeur'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES)
    specialite = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'teachers'

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom} - {self.grade}"


# Modèle pour représenter les étudiants de l'application
class Student(models.Model):

    SEMESTER_CHOICES = [
        ('S1', 'Semestre 1'),
        ('S2', 'Semestre 2'),
        ('S3', 'Semestre 3'),
        ('S4', 'Semestre 4'),   
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    matricule = models.CharField(max_length=50, unique=True)
    promotion = models.CharField(max_length=50, blank=True, null=True)
    master = models.CharField(max_length=100, blank=True, null=True)
    semestre = models.CharField(max_length=2,choices=SEMESTER_CHOICES, blank=True, null=True)

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.matricule} - {self.user.prenom} {self.user.nom}"