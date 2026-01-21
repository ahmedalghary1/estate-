from django.shortcuts import render

def custom_404(request, exception):
    """Custom 404 error page"""
    language = request.session.get('lang', 'en')
    return render(request, '404.html', {'language': language}, status=404)

def custom_500(request):
    """Custom 500 error page"""
    language = request.session.get('lang', 'en')
    return render(request, '500.html', {'language': language}, status=500)

def custom_403(request, exception):
    """Custom 403 error page"""
    language = request.session.get('lang', 'en')
    return render(request, '403.html', {'language': language}, status=403)
