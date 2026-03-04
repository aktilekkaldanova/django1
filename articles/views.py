from django.shortcuts import render

def arcticles_list(request):
    arcticles = Arcticles.objects.all()
    return render(request,'arcticles/arcticles_list.html',{
        'arcticles':articles 
        })