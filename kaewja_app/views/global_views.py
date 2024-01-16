def import_setup_views():
    global Response
    global api_view
    global status
    global JsonResponse
    
    Response = __import__("rest_framework.response", globals(), locals())
    api_view = __import__("rest_framework.decorators", globals(), locals())
    status = __import__("rest_framework", globals(), locals())
    JsonResponse = __import__("django.http", globals(), locals())


import_setup_views()