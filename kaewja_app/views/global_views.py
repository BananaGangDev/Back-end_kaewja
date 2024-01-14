def import_setup_views():
    global math
    global Response
    global api_view
    global status
    global JsonResponse
    
    math = __import__("math", globals(), locals())
    Response = __import__("rest_framework.response", globals(), locals())
    api_view = __import__("rest_framework.decorators", globals(), locals())
    status = __import__("rest_framework", globals(), locals())
    JsonResponse = __import__("django.http", globals(), locals())