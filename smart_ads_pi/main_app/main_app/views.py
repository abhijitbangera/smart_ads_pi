from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from localpi.models import adsDetails

def test(request):
    my_record = adsDetails.objects.filter(client_id_id=request.user.id).values()
    ad_header = my_record[0]['header']
    ad_left_top = my_record[0]['left_top']
    ad_left_bottom = my_record[0]['left_bottom']
    ad_right_bottom = my_record[0]['right_bottom']
    ad_right_top = my_record[0]['right_top']
    ad_footer = my_record[0]['footer']
    context = {
        'ad_header':ad_header,
        'ad_left_top':ad_left_top,
        'ad_left_bottom':ad_left_bottom,
        'ad_right_bottom':ad_right_bottom,
        'ad_right_top':ad_right_top,
        'ad_footer':ad_footer
    }
    print (ad_header)
    return render(request, 'index.html', context=context)
