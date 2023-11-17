class Call:
  def __init__(self, opCalled, repDefect, glpi, locale, status, resp):
        self.id = 0  # O ID será atribuído automaticamente (AUTO_INCREMENT)
        self.opCalled = opCalled
        self.repDefect = repDefect
        self.glpi = glpi
        self.locale = locale
        self.status = status
        self.resp = resp
        self.endCalled = 0