from qa.models import Session

def get_user_by_session(request):
    print("request cookies:", request.COOKIES)
    sessionid = request.COOKIES.get('sessionid')
    if sessionid is not None:
        print("Search session:", sessionid)
        try:
            session = Session.objects.get(key=sessionid) 
        except Exception:
            print("Session not found:", sessionid)
            return None
        return session.user
    else:
        print("Session not specified")
        return None