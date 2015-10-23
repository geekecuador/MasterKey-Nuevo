from django.db import models
from contrato.models import Sede,Estudiante,Profesor,Nivel
# Create your models here.

class Taller(models.Model):
    tema = models.CharField(max_length=30)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    capacidad = models.IntegerField()
    profesor = models.ForeignKey(Profesor)
    lugar = models.ForeignKey(Sede)
    nivel = models.CharField(max_length=2)
    estudiantes = models.ManyToManyField(Estudiante,related_name='alumnos', blank=True)
    class meta:
        app_label = 'Taller'
        verbose_name = 'taller'
        verbose_name_plural = 'talleres'
    def __unicode__(self):
        return self.tema

class TallerGeneral(models.Model):
    tema = models.CharField(max_length=30)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    capacidad = models.IntegerField()
    profesor = models.ForeignKey(Profesor)
    lugar = models.ForeignKey(Sede)
    alumnos = models.ManyToManyField(Estudiante, blank=True)
    class meta:
        app_label = 'Tallerg'
        verbose_name = 'taller general'
        verbose_name_plural = 'talleres generales'
    def __unicode__(self):
        return self.tema

class Curso(models.Model):
    fecha =  models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    capacidad_maxima = models.PositiveSmallIntegerField(default=6)
    sede = models.ForeignKey(Sede)
    profesor =  models.ForeignKey(Profesor)
    estudiantes  =  models.ManyToManyField(Estudiante,blank=True)
    tipo_nivel  = models.CharField(max_length='2',default='xx')
    tipo_leccion = models.PositiveSmallIntegerField(default=0)
    max_tipo = models.PositiveSmallIntegerField(default=3)
    tipo_estudiante = models.ManyToManyField(Nivel,related_name='tipo_estudiante', blank=True)
    class meta:
        app_label = 'Curso'
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'
    def __unicode__(self):
        return "Fecha: "+str(self.fecha)+" Hora Inicio: "+str(self.hora_inicio) +\
               " Capacidad: "+str(self.capacidad_maxima)


class Academic_Rank(models.Model):
    EXC = 'Excellent'
    VG = 'Very Good'
    G = 'Good'
    OK = 'Needs to work at home'
    R = 'Repeat'
    CONT = 'Continue'
    ACADEMIC_RANK_CHOICES = (
        (EXC, 'Excellent'),
        (VG, 'Very Good'),
        (G, 'Good'),
        (OK, 'Needs to work at home'),
        (R, 'Repeat'),
        (CONT, 'Continue'),
    )
    estudiante = models.ForeignKey(Estudiante)
    fecha = models.DateField()
    hora = models.TimeField()
    actividad = models.CharField(max_length=35)
    nota = models.CharField(max_length=15,
                                      choices=ACADEMIC_RANK_CHOICES,
                                      default=G)
    nivel = models.ForeignKey(Nivel)
    firma_alumno = models.BooleanField()
    profesor = models.ForeignKey(Profesor)


class Estado(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre


class Seguimiento(models.Model):
    estudiante =  models.ForeignKey(Estudiante)
    comentario = models.TextField()
    estado = models.ForeignKey(Estado)

    def __unicode__(self):
        return "%s -  %s-  %s" % (self.estudiante,self.comentario,self.estado)