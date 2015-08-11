var message_form = '<div class="input-group">' +
  '<span class="input-group-addon" id="sender_id_field">Optional</span>' +
  '<input type="text" class="form-control" id="sender_id" placeholder="Sender Name" aria-describedby="sender_id_field">' +
'</div>' +
'<div class="input-group">' +
  '<span class="input-group-addon" id="sender_email_field">Optional</span>' +
  '<input type="text" class="form-control" id="sender_reply_address" placeholder="Sender Email" aria-describedby="sender_email_field">' +
'</div>' +
'<div class="input-group">' +
  '<span class="input-group-addon" id="recipient_id_field">Optional</span>' +
  '<input type="text" class="form-control" id="recipient_id" placeholder="Recipient Name" aria-describedby="recipient_id_field">' +
'</div>' +
'<div class="input-group">' +
  '<span class="input-group-addon" id="recipient_email_field">Required</span>' +
  '<input type="text" class="form-control" id="recipient_email" placeholder="Recipient Email" aria-describedby="recipient_email_field">' +
'</div>' +
'<div class="input-group">' +
  '<span class="input-group-addon" id="secret_content_field">Message</span>' +
  '<textarea class="form-control" id="secret_content" aria-describedby="secret_content_field"></textarea>' +
'</div>' +
'<div class="input-group">' +
  '<span class="input-group-addon" id="key_delivery_field">Key Delivery By</span>' +
  '<select name="key_delivery_channel" class="form-control" id="key_delivery_channel" aria-describedby="key_delivery_field"><option selected="true" value="1">Email</option><option value="2">SMS</option></select>' +
'</div>' +
'<div class="input-group" id="sms_field_div">' +
  '<input type="text" class="form-control" id="recipient_mobile" placeholder="Recipient Mobile" aria-describedby="sms_field">' +
'</div><br clear="all">';

$(document).on('click', '#send-msg', function(e) {
  bootbox.dialog({
  message:  message_form,
  title: "Send Encrypted Message",
  buttons: {
    send: {
      label: "Send!",
      className: "btn-danger",
      callback: function() {
        
      }
    },
    
  }
});
});

function send_secret_message() {
  var sender_reply_address = $('#sender_reply_address').val();
  var sender_id = $('#sender_id').val();
  var recipient_id = $('#recipient_id').val();
  var recipient_email = $('#recipient_email').val();
  var message_content = $('#message_content').val();
  var key_delivery_channel = $('#key_delivery_channel').val();
  var recipient_mobile = $('#recipient_mobile').val();

  
}

$(document).on('change', '#key_delivery_channel', function(e){
  var channel = $('#key_delivery_channel').val();
  if (channel == 1) {
    $('#sms_field_div').hide();
  } else if (channel == 2) {
    $('#sms_field_div').show();
  }
});
      /*
      posts:
        add: {
          url: api/v1/create
          post: 
            {
            "sender_reply_address": "phil@phil.com", 
            "secret": {"expiry_type": 1, 
                      "expiry_timestamp": '2015-08-08',
                      "content": "hello world"}, 
            "recipient": {"phone": 18001231234, 
                        "id": "eric", 
                        "email": "eric@lan.com"}, 
            "content_delivery_channel": 2, 
            "sender_id": "philip", 
            "key_delivery_channel": 2
            }
          receive:
            {uid: '',
            management_key: ''}
          
      */