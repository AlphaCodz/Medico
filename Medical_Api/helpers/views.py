from rest_framework.decorators import APIView
from rest_framework.response import Response

class BaseView(APIView):
    required_post_fields=set() 
    def post(self, request, format=None):
        for fields in self.required_post_fields:
            if not fields:
                resp = {
                    "code": 400,
                    "message": f"{fields} not found"
                }
                return Response(resp, 400)
            
            
            