$(function() {

  // Get the form fields and hidden div
  var checkbox = $("#exampleCheck1");
  var hidden = $("#out_ip");

  // Hide the fields.
  // Use JS to do this in case the user doesn't have JS
  // enabled.
  hidden.show();

  // Setup an event listener for when the state of the
  // checkbox changes.
  checkbox.change(function() {
    // Check to see if the checkbox is checked.
    // If it is, show the fields and populate the input.
    // If not, hide the fields.
    if (checkbox.is(':checked')) {
      // Show the hidden fields.
      hidden.hide();
      // Populate the input.
    } else {
      // Make sure that the hidden fields are indeed
      // hidden.
      hidden.show();

      // You may also want to clear the value of the
      // hidden fields here. Just in case somebody
      // shows the fields, enters data to them and then
      // unticks the checkbox.
      //
      // This would do the job:
      //
      // $("#hidden_field").val("");
    }
  });
});