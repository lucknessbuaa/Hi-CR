<<<<<<< HEAD
import logging
from functools import wraps    


=======
from functools import wraps    

>>>>>>> hello/master
def active_tab(tab, sub_tab=None):
    def outer_wrapper(func):
        @wraps(func)
        def wrapper(request):
<<<<<<< HEAD
            request.nav = {
                "active_tab": tab,
                "active_sub_tab": sub_tab
            }
            return func(request)
        return wrapper
    return outer_wrapper

=======
            request.nav = { 
                "active_tab": tab,
                "active_sub_tab": sub_tab
            }   
            return func(request)
        return wrapper
    return outer_wrapper
>>>>>>> hello/master
