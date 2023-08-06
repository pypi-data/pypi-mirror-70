from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class Thread(StructuredData):
	def __init__(self, stats, sdata):
		super(Thread, self).__init__(sdata)
		self.stats = Stats(stats)