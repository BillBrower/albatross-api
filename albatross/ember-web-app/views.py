from django.core.files.storage import default_storage
from django.http import Http404, HttpResponse

def ember_web_app_view(request):
    """
    get:
    Renders index.html for the Ember Web App deployed to the
    S3 bucket in your Django Storages settings.
    """
    page_name = 'index.html'
    revision = request.GET.get('revision')
    if revision:
        page_name += ':{}'.format(revision)
    try:
        if default_storage.exists(page_name):
            page = default_storage.open(page_name, 'r')
            page_contents = page.read()
            page.close()
            return HttpResponse(page_contents, content_type='text/html')
        else:
            raise Http404()
    except Exception:
        raise Http404()