def Transactional(method):

    def wrapped_method(self, *args, **kwargs):
        method(self, *args, **kwargs)
        self.session.commit()
        self.session.close()

    return wrapped_method
