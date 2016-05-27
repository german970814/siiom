from django.db.models import Manager


class EncuentroManager(Manager):
    """
    Manager para los encuentros
    """
    def activos(self):
        return self.filter(estado='A')

    def inactivos(self):
        return self.filter(estado='I')
