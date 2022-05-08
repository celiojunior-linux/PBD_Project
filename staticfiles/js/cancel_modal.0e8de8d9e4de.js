function assignToCancel(objectDetails, cancelUrl) {
    $("#cancelObject").text(objectDetails);
    $("#cancelForm").attr("action", cancelUrl);
}