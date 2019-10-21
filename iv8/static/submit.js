function submit(url, element) {
  var msg = $("#"+element).val();
  console.log("submitting", url, msg);
  $.ajax({
    type: "POST",
    data :JSON.stringify(msg),
    url: url,
    contentType: "application/json"
  });
}
