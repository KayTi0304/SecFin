from django.http import HttpResponse
from sec_edgar_api import EdgarClient
from django.http import JsonResponse

def getCompanyInfo(request):
    cik_req = request.GET.get('cik', None)
    if cik_req == None:
        return HttpResponse("There is no CIK!")
    else:
        edgar = EdgarClient(user_agent="tmy55770@gmail.com")
        result = edgar.get_company_concept(cik=cik_req, taxonomy="us-gaap", tag="AccountsPayableCurrent")
        result_res = {'name': result['entityName'], 'accountsPayableCurrent': result['units']['USD'][-1]}
        return JsonResponse(result_res)