"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

def add(*args):
    sm = 0.0
    for i in args: sm += float(i)
    add_sum = str(sm)
    return add_sum


def subtract(*args):
    sm = float(args[0])*2
    for i in args: sm -= float(i)
    sub_sum = str(sm)
    return sub_sum


def multiply(*args):
    sm = 1.0
    for i in args: sm *= float(i)
    mul_sum = str(sm)
    return mul_sum


def divide(*args):
    sm = float(args[0])*float(args[0])
    for i in args: sm /= float(i)
    div_sum = str(sm)
    return div_sum


def how_to():
    the_stuff = """
    <html>
    <head><title>Its MATH!</title></head>
    <h1>How2 Calculator</h1>
    <h2>Addition</h2>
    <p>Go to localhost:8080/add/x/x/x...
    <p>Where x is the numbers you would like to add together.</p>
    <p>Each x can be different, and there is no limit to the number of x's you use.</p>
    <p>Be sure to include '/' after 8080 and 'add' and after each input variable.</p>
    <h2>Subtraction</h2>
    <p>
    See Addition but in place of 'add' use 'subtract'.
    </p>
    <h2>Multiplication</h2>
    <p>
    See Addition but in place of 'add' use 'multiply'.
    </p>
    <h2>Division</h2>
    <p>
    See Addition but in place of 'add' use 'divide'.
    </p>
    </html>
    """
    return the_stuff


def resolve_path(path):
    # from books stuff, ~should~ work fine
    funcs = {
    '': how_to, 
    'add': add,
    'subtract': subtract,
    'multiply': multiply,
    'divide': divide
    }
    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args



def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = '404 Not Found stupid'
        body = '<h1>Not Found stupid</h1>'
    except ZeroDivisionError:
        status = 'x/0 is undefined bro!'
        body = '<h1>x/0 is undefined bro!!</h1>'
    except Exception as e:
        status = '500 Internal Server Error dummy'
        body = f'<h1>Internal Server Error\ndummy {e}</h1>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf-8')]


if __name__ == '__main__':
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
