def application(env,start_response):
    status = '200 OK'
    headers = [('Content-type','text/plain')]
    param = env['QUERY_STRING'].replace('&','\n')
    start_response(status,headers)
    return iter(param)
