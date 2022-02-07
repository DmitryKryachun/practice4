from django.db import models

def calc_bunker(bunker):
    bunker_data = bunker.transactions.aggregate(models.Sum('qty'))
    if bunker_data.get('qty__sum') :
        return bunker_data['qty__sum']
    else:
        return 0

def recalc_bunker(bunker):
    bunker_data = bunker.transactions.aggregate(models.Sum('qty'))
    if bunker_data.get('qty__sum') :
        bunker.qty = bunker_data['qty__sum']
    else:
        bunker.qty = 0
    bunker.save()