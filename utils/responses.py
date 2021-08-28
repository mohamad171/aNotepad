from rest_framework.response import Response

def error_response(code,message,data = None):
    return Response(
        {
            'data' : data,
            'code' : code,
            'message' : message
        }, 
        status=400
    )
    
def success_response(code='success',message='success',data=None):
    return Response(
        {
            'data' : data,
            'code' : code,
            'message' : message
        }, 
        status=200
    ) 
