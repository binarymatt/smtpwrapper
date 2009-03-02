#coding: utf-8
r"""
# import tests
>>> from swrap import Message
>>> from swrap import Connection
>>> from swrap import send_mail

# test instantiation

>>> email = Message('from@example.com',['to@example.com'],'subject')

"""

def test_message():
    from swrap import Message
    email = Message('from@example.com',['to@example.com'], 'subject')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
