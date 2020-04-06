def Transactional(method):

    def wrapped_method(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.session.commit()
        #self.session.close()
        return result

    return wrapped_method
