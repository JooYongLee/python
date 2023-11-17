
class HelloContextManager:

    def __init__(self, *args, **kwargs):
        print('init')
        self.name = kwargs.get('name')
    def __enter__(self):
        print("Entering the context...")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        print("Leaving the context...")
        print(exc_type, exc_value, exc_tb, sep="\n")
        self.close()

    def close(self):
        print(f'*********{self.name} closed*********')
        pass

with HelloContextManager('dsf', abc='df', name='this is with') as hello:
    print(hello)


thisis = HelloContextManager(name='this is normal function')
# thisis.close()
#
# with open('dsfsdf', 'w') as f:
#
