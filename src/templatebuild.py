from time import strftime
def buildSelectOptions(arrayVal):
    htmlOptions=""
    for val in arrayVal:
        htmlOptions+="<option value='"+val[0]+"'>"+val[1]+"</option>"

    return htmlOptions

def buildTimesButtons(arrayVal):
    htmlButtons=""
    i=0;
    for val in arrayVal:
        if i==0:
            htmlButtons+="<div class='row'>"
        i+=1
        htmlButtons+="<div class='col-lg-6'><button class='btn btn-danger btnTime form-control'>"+str(val[0])+"</button></div>"
        if i==2:
            htmlButtons+="</div><br>"
            i=0
    return htmlButtons