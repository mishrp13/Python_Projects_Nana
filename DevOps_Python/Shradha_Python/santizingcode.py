import functools

def sanitized_hostname(func):

    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        
        if 'hostname' not in kwargs:
            raise ValueError("The 'hostname' keyword argument is required ")
        
        original_hostname= kwargs['hostname']

        if not isinstance(original_hostname,str) or not original_hostname.strip():
            raise TypeError("The ''hostname' argument must not be an empty string")
        
        santized= original_hostname.lower().strip()

        kwargs['hostname'] = santized

        return func(*args,**kwargs)
    return wrapper


@sanitized_hostname
def connect_to_server(hostname):
    print(f"coonecting to {hostname}")


connect_to_server(hostname= "     EXAMPLE.COM   ")




        







