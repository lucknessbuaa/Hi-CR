from functools import wraps    

def active_tab(tab, sub_tab=None):
    def outer_wrapper(func):
        @wraps(func)
        def wrapper(request):
            request.nav = { 
                "active_tab": tab,
                "active_sub_tab": sub_tab
            }   
            return func(request)
        return wrapper
    return outer_wrapper
