from antibiobank.models import *


def get_antibio_datas(bactery_id, filter_mode=None, filter_ids=None):
	
	atb = []
	records    = Record.objects.filter(bactery_id = bactery_id)

	if filter_ids != None:
		for id in filter_ids:
			records = records.filter(resistance__antibiotic_id=id, resistance__value=filter_mode)



	atbTesting = records.values("resistance__antibiotic__id","resistance__antibiotic__name").distinct()
	resistances = Resistance.objects.filter(record__in=records)
	for item in atbTesting:

		obj = {}
		print item
		obj["name"] = item["resistance__antibiotic__name"]
		obj["id"]   = item["resistance__antibiotic__id"]
		obj["S"] = int(resistances.filter(value="S", antibiotic__id = item["resistance__antibiotic__id"]).count())
		obj["R"] = int(resistances.filter(value="R", antibiotic__id = item["resistance__antibiotic__id"]).count())
		obj["I"] = int(resistances.filter(value="I", antibiotic__id = item["resistance__antibiotic__id"]).count())
		obj["count"] = obj["S"] + obj["R"] + obj["I"]

		atb.append(obj)

	results = {}
	results["name"] = str(Bactery.objects.get(pk=bactery_id));
	results["total"]= str(records.count())
	results["data"] = atb

	print "RESULTS"

	return results

