function assignToDelete(objectDetails, deleteUrl) {
    $("#deleteObject").text(objectDetails);
    $("#deleteForm").attr("action", deleteUrl);
}