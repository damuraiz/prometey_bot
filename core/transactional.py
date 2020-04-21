def Transactional(method):

    def wrapped_method(self, *args, **kwargs):
        try:
            #print("try")
            result = method(self, *args, **kwargs)
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
        finally:
            pass
            #print("finally")
            #self.session.close()
        return result

    return wrapped_method

def TransactionalClass(Cls):
    pass #todo