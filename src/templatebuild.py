def buildSelectOptions(arrayVal):
    htmlOptions=""
    for val in arrayVal:
        htmlOptions+="<option value='"+val[0]+"'>"+val[1]+"</option>"

    return htmlOptions