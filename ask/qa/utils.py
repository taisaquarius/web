from qa.models import Session

def get_user_by_session(request):
    sessionid = request.COOKIES.get('sessionid')
    if sessionid is not None:
        print("Search session:", sessionid)
        session = Session.objects.get(key=sessionid) 
        if session is None:
            return None
        return session.user
    else:
        return None