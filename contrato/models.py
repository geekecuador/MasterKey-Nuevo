#-*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.


def cedula_valida(ced):
    if len(ced) == 10:
        valores = [int(ced[x]) * (2 - x % 2) for x in range(9)]
        suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
    return int(ced[9]) == 10 - int(str(suma)[-1:])

def validacion(ced):
    if not cedula_valida(ced):
        raise ValidationError(u'%s no es un número de cédula válido' % ced)

def validar_numeros(numero):
    try:
        assert isinstance(numero, object)
        num = int(numero)
    except:
        raise ValidationError(u'%s debe ser numero' % numero)


class Ciudad(models.Model):
    nombre = models.CharField(max_length=25)
    def __unicode__(self):
        return self.nombre

class Programa(models.Model):
    nombre_del_programa = models.CharField(max_length=25, primary_key=True)
    def __unicode__(self):
        return self.nombre_del_programa

class Sede(models.Model):
    nombre_sede = models.CharField(max_length=20,primary_key=True)
    ciudad = models.ForeignKey(Ciudad)
    direccion = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    def __unicode__(self):
        return self.nombre_sede

class Nivel(models.Model):
    nivel =  models.CharField(max_length=2)
    leccion = models.IntegerField()
    def __unicode__(self):
        return self.nivel + ' '+str(self.leccion)

class Estudiante(models.Model):

    cedula = models.CharField(u"cédula", max_length=10, primary_key=True, validators=[validacion])
    foto  = models.ImageField(upload_to='estudiante')
    usuario = models.OneToOneField(User,unique=True,)
    fecha_nacimiento = models.DateField(u'fecha de nacimiento',blank=True,null=True)
    telefono = models.CharField(u'teléfono',max_length=10, validators=[validar_numeros])
    direccion_domicilio= models.CharField(max_length=25,blank=True)
    telefono = models.CharField(max_length=10,blank=True)
    programa = models.ForeignKey(Programa)
    fecha_de_inicio = models.DateField()
    fecha_de_expiracion = models.DateField()
    lugar_de_trabajo = models.CharField(max_length=30,blank=True)
    contacto_de_emergencia =  models.CharField(max_length=30,blank=True)
    relacion_de_contacto_de_emergencia = models.CharField(max_length=30,blank=True)
    telefono_de_contanto_de_emergencia = models.CharField(max_length=10,blank=True)
    sede = models.ForeignKey(Sede)
    nivel = models.ForeignKey(Nivel)
    def __unicode__(self):
        return  self.cedula

class Contrato(models.Model):

    numero_contrato = models.CharField(max_length=8, primary_key=True)
    numero_factura = models.CharField(max_length=10,blank=True)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField(u'Fecha de nacimiento',blank=True,null=True)
    cedula = models.CharField(u"Cédula", max_length=10, validators=[validacion])
    email = models.EmailField('e-mail',blank=True)
    direccion_domicilio = models.TextField(blank=True)
    telefono = models.CharField(max_length=10,blank=True)
    celular = models.CharField(max_length=10,blank=True)
    empresa = models.CharField(max_length=30,blank=True)
    cargo = models.CharField(max_length=20,blank=True)
    direccion_empresa = models.CharField(max_length=30,blank=True)
    telefono_empresa = models.CharField(max_length=10,blank=True)
    fecha_creacion = models.DateField(u'Fecha de creación')
    duracion = models.DateField()
    sede_firma_contrato = models.ForeignKey(Sede)
    beneficiarios =  models.ManyToManyField(Estudiante)

    def __unicode__(self):
        return self.numero_contrato + ' ' + self.nombre + ' ' + self.apellidos



class Profesor(models.Model):
    cedula = models.CharField(u"Cédula", max_length=10, validators=[validacion])
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    sede = models.ForeignKey(Sede)
    horario_inicio_manana = models.TimeField()
    horario_fin_manana = models.TimeField()
    horario_inicio_tarde = models.TimeField()
    horario_fin_tarde = models.TimeField()
    def __unicode__(self):
        return self.nombre + " "+self.apellido