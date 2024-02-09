#direciona os dados para a base de dados temporaria
#O None quer dizer que outros rooteadores devem decidir
class OptmoduleRouter:
    app_label = 'opt_module'
    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'otp_dbtemp' 
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'otp_dbtemp' 
        return None
    def allow_relation(self, obj1, obj2, **hints):
        return True
