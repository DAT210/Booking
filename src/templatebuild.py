from time import strftime
def buildSelectOptions(arrayVal):
    htmlOptions=""
    for val in arrayVal:
        htmlOptions+="<option value='"+val[0]+"'>"+val[1]+"</option>"

    return htmlOptions

def buildTimesButtons(arrayVal,fullTimes):
    htmlButtons=""
    i=0;
    j=0;
    for val in arrayVal:
        if i==0:
            htmlButtons+="<div class='row'>"
        i+=1
        htmlButtons+="<div class='col-lg-6'><button class='btn btn-danger btnTime form-control fullTime"+str(fullTimes[j])+"'>"+str(val[1])+"</button></div>"
        j+=1
        if i==2:
            htmlButtons+="</div><br>"
            i=0
    return htmlButtons