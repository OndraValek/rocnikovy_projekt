"""
Middleware pro zachycení OAuth2 callback požadavků.
"""
import logging

logger = logging.getLogger('accounts')

class OAuth2LoggingMiddleware:
    """Middleware pro logování OAuth2 callback požadavků."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Zaznamenat Microsoft callback
        if '/accounts/microsoft/login/callback/' in request.path:
            logger.info("=" * 70)
            logger.info("MICROSOFT CALLBACK REQUEST")
            logger.info(f"Path: {request.path}")
            logger.info(f"GET params: {request.GET}")
            logger.info(f"Method: {request.method}")
            logger.info("=" * 70)
        
        response = self.get_response(request)
        
        # Zaznamenat odpověď
        if '/accounts/microsoft/login/callback/' in request.path:
            logger.info("=" * 70)
            logger.info("MICROSOFT CALLBACK RESPONSE")
            logger.info(f"Status code: {response.status_code}")
            logger.info(f"Location header: {response.get('Location', 'N/A')}")
            logger.info("=" * 70)
        
        return response

