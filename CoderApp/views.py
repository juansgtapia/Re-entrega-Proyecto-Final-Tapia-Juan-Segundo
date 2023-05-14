from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from CoderApp.forms import catedraform, estudiantesform, profesoresform, entregadoforms, buscarcurso, buscarestudiante, UserEditForm, AvatarFormulario, PosteoFormulario
from CoderApp.models import Catedra, Estudiante, Profesor, Entregado, Avatar, Post
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import list
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings

# Create your views here.


#@login_required
def inicio(request):


    #avatares = Avatar.objects.filter(user=request.user.id)
    #request.session["userimage"] = avatares[0].imagen.url
    return render(request, "CoderApp/inicio.html")

#@login_required
def cursos(request):
    
    v = catedraform(request.POST)
    cursos = Catedra.objects.all()
    total_cursos = len(cursos)

    context = {
        "cursos": cursos,
        "total_cursos": total_cursos,
        "form": catedraform,
    }

    if request.method == "POST":
        if v.is_valid():
            Catedra(nombre_de_la_materia = v.data["nombre_de_la_materia"], año = v.data["año"]).save()    
            
    return render(request, "CoderApp/cursos.html", context)

#@login_required
def profesores(request):

    w = profesoresform(request.POST)
    profesores = Profesor.objects.all()
    total_profesores = len(profesores)

    context= {
        "profesores": profesores,
        "total_profesores": total_profesores,
        "form": profesoresform,
    } 

    if request.method == "POST":
        if w.is_valid():
            Profesor(nombre  = w.data["nombre"], apellido = w.data["apellido"], email = w.data["email"]).save()

    return render(request, "CoderApp/profesores.html", context)

#@login_required
def estudiantes(request):
    
    z = estudiantesform(request.POST)
    estudiantes = Estudiante.objects.all()
    total_estudiantes = len(estudiantes)

    context = {
        "estudiantes": estudiantes,
        "total_estudiantes": total_estudiantes,
        "form": estudiantesform,
    }

    if request.method == "POST":
        if z.is_valid():
            Estudiante(nombre = z.data["nombre"], apellido = z.data["apellido"], email = z.data["email"], calificacion = z.data["calificacion"]).save()

    return render(request, "CoderApp/estudiantes.html", context)
            
#@login_required
def mostrar_entregables(request):
    return render(request, "CoderApp/entregables.html")

#@login_required
def buscar_curso(request):

    
    f = buscarcurso()

    context = {
        "form": f,
    }

    try:
        if request.GET["nombre_de_la_materia"]:

            nombre_de_la_materia = request.GET["nombre_de_la_materia"]
            cursos = Catedra.objects.filter(nombre_de_la_materia__icontains = nombre_de_la_materia)
            context = {"form": f,
                    "cursos" : cursos,
            }      
    except:
        pass

    return render(request, "CoderApp/buscarcursos.html", context)


class EstudiantesList(ListView, LoginRequiredMixin):

    model = Estudiante
    template_name = "CoderApp/estudiantes_lists.html"

class EstudiantesDetalle(DetailView,LoginRequiredMixin):

    model = Estudiante
    template_name = "CoderApp/estudiantes_detalle.html"

class EstudiantesCreacion(LoginRequiredMixin, CreateView):

    model = Estudiante 
    success_url = "/CoderApp/estudiantes/list"
    fields = ['nombre', 'email']

class EstudiantesUpdate(UpdateView,LoginRequiredMixin):
    
    model = Estudiante
    template_name = "CoderApp/estudiantes_form.html"
    success_url = "/CoderApp/estudiantes/list"
    fields = ['nombre', 'apellido', 'email', 'calificacion']


class EstudiantesDelete(DeleteView,LoginRequiredMixin):

    model = Estudiante
    template_name = "CoderApp/estudiantes_confirm_delete.html"
    success_url = "/CoderApp/estudiantes/list"

def leerprofesores(request): #CRUD, READ

    profesores = Profesor.objects.all() #Todos los profesores
    context = {"profesores": profesores}

    return render(request, "CoderApp/leerprofesores.html", context)


def eliminarprofesor(request, profesor_nombre): #CRUD, READ

    profesor = Profesor.objects.get(nombre = profesor_nombre)
    profesor.delete()

    #Volver al menu
    profesores = Profesor.objects.all()
    context = {"profesores": profesores}

    return render(request, "CoderApp/leerprofesores.html", context)

def editarprofesor(request, profesor_nombre):

    profesor = Profesor.objects.get(nombre = profesor_nombre)

    if request.method == "POST":

        formulario = profesoresform(request.POST) 
        print(formulario)

        if formulario.is_valid:

            informacion = formulario.cleaned_data

            profesor.nombre = informacion['nombre'] 
            profesor.apellido = informacion['apellido']
            profesor.email = informacion['email']

            profesor.save()

            return redirect(reverse('LeerProfesores')) 
        
        else:
            return redirect(reverse('LeerProfesores'))
        
    else:
        formulario = profesoresform(initial={'nombre': profesor.nombre, 'apellido':profesor.apellido, 'email': profesor.email})
        
        

    return render(request, "CoderApp/editarprofesores.html", {"formulario":formulario, "profesor_nombre": profesor_nombre})


def login_request(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            clave = form.cleaned_data.get('password')

            user = authenticate(username=usuario, password=clave)

            if user is not None:
                login(request, user)

                avatares = Avatar.objects.filter(user=request.user.id)

                if avatares.exists():
                    request.session["userimage"] = avatares[0].imagen.url

                return render(request, "CoderApp/inicio.html", {"mensaje": f"Bienvenido {usuario}"})

            else:
                return render(request, "CoderApp/inicio.html", {"mensaje": "Error, datos incorrectos"})

        else:
            return render(request, "CoderApp/inicio.html", {"mensaje": "Error, formulario erroneo"})

    form = AuthenticationForm()

    return render(request, "CoderApp/login.html", {"form": form})


def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)
        
        if form.is_valid():

            form.save()
            return render(request, "CoderApp/inicio.html",{"mensaje": "Usuario creado"})
    
    else:
        form = UserCreationForm()

    return render(request, "CoderApp/registro.html", {"form": form})



def editarperfil(request):

    usuario = request.user

    if request.method == "POST":
        formulario = UserEditForm(request.POST)
        if formulario.is_valid():
            
            informacion = formulario.cleaned_data

            #Datos que se modifican
            usuario.email = informacion['email']
            usuario.set_password(informacion['password1'])
            print(informacion, usuario)
            usuario.save()

            return render(request, "CoderApp/inicio.html")
    else: 
            
        formulario= UserEditForm(initial={'email':usuario.email}) 

      
    return render(request, "CoderApp/editarperfil.html", {"formulario":formulario, "username":usuario})


@login_required
def agregarAvatar(request):

    formulario = AvatarFormulario()
    if request.method == "POST":

        formulario = AvatarFormulario(request.POST, request.FILES)

        if formulario.is_valid():

            u = User.objects.get(username=request.user)
            avatares = Avatar.objects.filter(user=request.user.id)
            for avatar in avatares:
                avatar.delete()
            avatar = Avatar(user=u, imagen=formulario.cleaned_data['imagen'])
            avatar.save()

            return render(request, "CoderApp/inicio.html")
        else:
            formulario=AvatarFormulario()

    return render(request, "CoderApp/agregaravatar.html", {"formulario":formulario})

class CursosList(ListView, LoginRequiredMixin):

    model = Catedra
    template_name = "CoderApp/cursos_list.html"

class CursosDetalle(DetailView,LoginRequiredMixin):

    model = Catedra
    template_name = "CoderApp/curso_detalle.html"


class CursosCreacion(CreateView,LoginRequiredMixin):

    model = Catedra 
    success_url = "/CoderApp/cursos/list"
    fields = ['nombre_de_la_materia', 'año']



class CursosUpdate(UpdateView,LoginRequiredMixin):
    
    model = Catedra
    template_name = "CoderApp/cursos_form.html"
    success_url = "/CoderApp/cursos/list"
    fields = ['nombre_de_la_materia', 'año']


class CursosDelete(DeleteView,LoginRequiredMixin):

    model = Catedra
    template_name = "CoderApp/curso_confirm_delete.html"
    success_url = "/CoderApp/cursos/list"


class UsuarioDetalle(DetailView,LoginRequiredMixin):
    model = User
    template_name = "CoderApp/perfil.html"

class PostList(ListView, LoginRequiredMixin):
    model = Post
    template_name = "CoderApp/post_list.html"

class PostDelete(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = "CoderApp/post_delete.html"
    success_url = "/CoderApp/inicio.html"


def resize_image(image, new_width):
    img = Image.open(image)
    w_percent = (new_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((new_width, h_size), Image.ANTIALIAS)
    img = img.convert('RGB')  
    img_io = BytesIO()
    if img.format == 'PNG':
        img.save(img_io, format='PNG')
    else:
        img.save(img_io, format='JPEG')
    img_file = img_io.getvalue()
    return img_file


@login_required
def postear(request):
    formulario = PosteoFormulario()
    if request.method == "POST":
        formulario = PosteoFormulario(request.POST, request.FILES)
        if formulario.is_valid():
            f = formulario.save(commit=False)
            if f.imagen_post:
                f.imagen_post = ContentFile(resize_image(f.imagen_post, 800), f.imagen_post.name)
            
            f.autor = request.user
            
            f.save()
            return render(request, "CoderApp/inicio.html")
        else:
            formulario = PosteoFormulario()
    
    return render(request, "CoderApp/postear.html", {"formulario": formulario})


@login_required
def verposteos(request):#CRUD,READ
    posteos = Post.objects.all()
    context = {"posteos": posteos}

    return render(request, "CoderApp/post_list.html", context)

from django.shortcuts import redirect

@login_required
def eliminarpost(request, titulo_posteo): #CRUD, DELETE
    posteo = Post.objects.get(titulo=titulo_posteo)
    posteo.delete()
    return redirect('post-detail')








