from django.shortcuts import render_to_response


def specific_secret(request, uid=None):
    return render_to_response('secret.html', {'uid': uid})
