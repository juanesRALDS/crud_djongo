from django.shortcuts import render;
from django.conf import settings;
from django.db import Error;
from appPeliculas.models import genero, peliculas;
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render, redirect
import os
from bson import ObjectId
# Create your views here.

def inicio (request):
    return render (request, "1Vista.html")

def vistaAgregargenero(request):
    return render (request, "agregarGenero.html")

@csrf_exempt
def agregarGenero (request):
    try :
        nombre = request.POST['nombre'];
        #Crear objeto de tipo genero
        gener = genero(gen_nombre=nombre);
        #Salvar el genero y guardarlo en la base de datos
        gener.save();
        mensaje = "Genero agrgado exitosamente";
    except Error as error :
        mensaje = str(error);
    
    retorno = {"mensaje":mensaje};
    # return JsonResponse(retorno);
    return render(request, "agregargenero.html", retorno);

def listarPeliculas (request):
    movies = peliculas.objects.all();
    
    retorno = {"movies" : movies}
    
    # return JsonResponse(retorno);
    return render (request, "listarPeliculas.html", retorno)


def vistaAgregarPeliculas (request):
    generos = genero.objects.all()
    
    retorno = {"generos":generos}
    
    return render (request, "agregarPelicula.html", retorno)

# @csrf_exempt
def agregarPelicula (request):
    try:
        codigo = request.POST["cod"]
        titulo = request.POST["title"]
        protagonista = request.POST["prota"]
        duracion = int(request.POST["dure"])
        sinopsis = request.POST["sinop"]
        foto = request.FILES["photo"]
        idGenero =ObjectId( request.POST["idGenero"])
        
        gener = genero.objects.get(pk=idGenero);
        
        peli = peliculas (pel_codigo = codigo,
                          pel_titulo = titulo,
                          pel_protagonista = protagonista,
                          pel_duracion = duracion,
                          pel_sinopsis = sinopsis,
                          pel_foto = foto,
                          pel_genero = gener);
        
        peli.save()
        mensaje ="Pelicula agregada exitosamente";
        
        
    except Error as error :
        mensaje = str (error);
    
    retorno = {"mensaje":mensaje, 'idPelicula':peli.pk}
    
    # return JsonResponse (retorno)
    # return render (request, "agregarPelicula.html", retorno);
    return redirect ("/", retorno)

def consultarPelicula(request, id):
    pelicula = peliculas.objects.get(pk=ObjectId(id))
    generos = genero.objects.all()
    retorno = {"pelicula":pelicula, "generos":generos}
    return render(request,"actualizarPelicula.html",retorno)

def actualizarPelicula(request):
    try:
        idPelicula = ObjectId(request.POST['idPelicula'])
        peliculaActualizar = peliculas.objects.get(pk=idPelicula)
        
        peliculaActualizar.pel_codigo = request.POST["cod"]
        peliculaActualizar.pel_titulo = request.POST["title"]
        peliculaActualizar.pel_protagonista = request.POST["prota"]
        peliculaActualizar.pel_duracion = int(request.POST["dure"])
        peliculaActualizar.pel_sinopsis = request.POST["sinop"]
        
        
        if 'photo' in request.FILES:
            foto = request.FILES["photo"]
            if peliculaActualizar.pel_foto:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(peliculaActualizar.pel_foto)))
            peliculaActualizar.pel_foto = foto
        
        idGenero = ObjectId(request.POST["idGenero"])
        
        gener = genero.objects.get(pk=idGenero)
        peliculaActualizar.pel_genero = gener
        
        peliculaActualizar.save()
        
        mensaje = "Película actualizada exitosamente"
        
    except Error as error:
        mensaje = str(error)
    
    retorno = {"mensaje": mensaje}
    
    return redirect("/")


def eliminarPelicula(request, id):
    try:
        peliculaEliminar = peliculas.objects.get(pk=ObjectId(id))
        peliculaEliminar.delete()
        mensaje = "Pelicula Eliminada Correctamente"
    except Error as error:
        mensaje = str(error)
    retorno={"mensaje":mensaje}
    return redirect ("/")