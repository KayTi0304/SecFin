from django.http import HttpResponse
from sec_edgar_api import EdgarClient
from django.http import JsonResponse

def getCompanyInfo(request):
    cik_req = request.GET.get('cik', None)
    if cik_req == None:
        return HttpResponse("There is no CIK!")
    else:
        edgar = EdgarClient(user_agent="tmy55770@gmail.com")
        #result = edgar.get_company_concept(cik=cik_req, taxonomy="us-gaap", tag="AccountsPayableCurrent")
        #result_res = {'name': result['entityName'], 'accountsPayableCurrent': result['units']['USD'][-1]}
        result = edgar.get_company_facts(cik=cik_req)

        dei_tags = [
            "EntityCommonStockSharesOutstanding", 
            "EntityPublicFloat",
        ]

        us_gaap_tags = list(result['facts']['us-gaap'].keys())
        
        financial_facts = {}

        for dt in dei_tags:
            if dt == "EntityCommonStockSharesOutstanding":
                financial_facts[dt] = result['facts']['dei'][dt]['units']['shares'][-1]['val']
            else:
                financial_facts[dt] = result['facts']['dei'][dt]['units']['USD'][-1]['val']

        usd_shares = ["CommonStockDividendsPerShareDeclared", "CommonStockDividendsPerShareCashPaid", "CommonStockNoParValue", "CommonStockParOrStatedValuePerShare",
                      "CommonStockParOrStatedValuePerShare", "EarningsPerShareBasic", "EarningsPerShareDiluted", "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsForfeituresWeightedAverageGrantDateFairValue",
                      "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsGrantsInPeriodWeightedAverageGrantDateFairValue",
                      "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsNonvestedIntrinsicValue",
                      "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsNonvestedWeightedAverageGrantDateFairValue",
                      "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsVestedInPeriodWeightedAverageGrantDateFairValue",
                      "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsExercisableWeightedAverageExercisePrice",
                      "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsGrantsInPeriodWeightedAverageGrantDateFairValue",
                      "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsOutstandingWeightedAverageExercisePrice",
                      "ShareBasedCompensationArrangementsByShareBasedPaymentAwardOptionsExercisesInPeriodWeightedAverageExercisePrice",
                      "ShareBasedCompensationArrangementsByShareBasedPaymentAwardOptionsForfeituresInPeriodWeightedAverageExercisePrice",
                      "ShareBasedCompensationArrangementsByShareBasedPaymentAwardOptionsGrantsInPeriodWeightedAverageExercisePrice",
                      ]
        
        shares = [  "AntidilutiveSecuritiesExcludedFromComputationOfEarningsPerShareAmount",
                    "CommonStockSharesAuthorized", 
                    "CommonStockSharesIssued",
                    "CommonStockSharesOutstanding",
                    "PreferredStockSharesAuthorized",
                    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsForfeitedInPeriod",
                    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsGrantsInPeriod",
                    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsNonvestedNumber",
                    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsVestedInPeriod",
                    "ShareBasedCompensationArrangementByShareBasedPaymentAwardNumberOfSharesAvailableForGrant",
                  ]

        for ugt in us_gaap_tags:
            key_list = list(result['facts']['us-gaap'][ugt]['units'].keys())
            unit_tag = key_list[0]
            if result['facts']['us-gaap'][ugt]['units'][unit_tag][-1]['fy'] == 2023:
                financial_facts[ugt] = result['facts']['us-gaap'][ugt]['units'][unit_tag][-1]['val']
            
        return JsonResponse(financial_facts)
    
def getAllCompanyInfo(request):
    cik_req = request.GET.get('cik', None)
    if cik_req == None:
        return HttpResponse("There is no CIK!")
    else:
        edgar = EdgarClient(user_agent="tmy55770@gmail.com")
        result = edgar.get_company_facts(cik=cik_req)
        return JsonResponse(result)