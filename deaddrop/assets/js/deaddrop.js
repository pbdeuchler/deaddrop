var message_form = '<div class="input-group">' +
  '<span class="input-group-addon" id="sender_id_field">Optional</span>' +
  '<input type="text" class="form-control" name="sender_id" id="sender_id" placeholder="Sender Name" aria-describedby="sender_id_field">' +
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

var del_form = '<div class="input-group">' +
  '<span class="input-group-addon" id="msg_guid_field">Required</span>' +
  '<input type="text" class="form-control" name="msg_guid" id="msg_guid" placeholder="Message GUID" aria-describedby="sender_id_field">' +
'</div>' + 
'<div class="input-group">' +
  '<span class="input-group-addon" id="manage_key_field">Required</span>' +
  '<input type="text" class="form-control" name="manage_key" id="manage_key" placeholder="Management Key" aria-describedby="sender_id_field">' +
'</div>' 
;


$(document).on('click', '#send-msg, #nav-new-msg', function(e) {
  bootbox.dialog({
  message:  message_form,
  title: "Send Encrypted Message",
  buttons: {
    send: {
      label: "Send!",
      className: "btn-danger",
      callback: send_secret_message
    },
    done: {
      label: "Done!",
      className: "btn-success",
      callback: function(){
         $('body').removeClass('modal-open');
        $('.modal .modal-backdrop').remove();
      }
    },
  }
  });
});

$(document).on('click', '#nav-del-msg', function(e) {
  bootbox.dialog({
  message:  del_form,
  title: "Delete Message",
  buttons: {
    send: {
      label: "Delete!",
      className: "btn-danger",
      callback: process_delete,
      id: "send_msg_button"
    },
  }
  });
});

function process_delete(){
  var postdata = {"management_key": $('#manage_key')}
  $.post('http://localhost:8000/api/v1/delete/' + $('#msg_guid').val(),
    JSON.stringify(postdata)) 
    .done(function() {
      window.open('https://www.youtube.com/watch?v=fkXGGhuQs0o&t=50');
    })
    .fail(function() {
      alert('fail');
    });
}

function send_secret_message() {
  var sender_reply_address = $('#sender_reply_address').val();
  var sender_id = $('#sender_id').val();
  var recipient_id = $('#recipient_id').val();
  var recipient_email = $('#recipient_email').val();
  var message_content = $('#secret_content').val();
  var key_delivery_channel = parseInt($('#key_delivery_channel').val());
  var recipient_mobile = $('#recipient_mobile').val();

  var post_content = {
            "sender_reply_address": sender_reply_address, 
            "secret": {"expiry_type": 1, 
                      "expiry_timestamp": '2015-08-08 00:00:00',
                      "content": message_content },
            "recipient": {"id": recipient_id, 
                        "email": recipient_email}, 
            "content_delivery_channel": 1, 
            "sender_id": sender_id,
            "key_delivery_channel": key_delivery_channel
            };
  if (recipient_mobile) {
    post_content.recipient.phone = recipient_mobile;
  }

  var url = '/api/v1/create/';

  // set spinner
  $('.modal-body').html('<img src="/static/img/giphy.gif" />');
  // post
  $.ajax({
    type: "POST",
    url: url,
    data: JSON.stringify(post_content),
    dataType: 'json',
    contentType: 'application/json; charset=utf-8',
    success: post_success});
  return false;
}

function post_success(data){
  $('h4.modal-title').html('Message Sent!');
  $('.btn-success').show();
  $('.btn-danger').hide();
  $('.modal-body').html('<p class="message_success">Your message has been sent.</p><p class="message_success">Please keep the following info to manage this later:</p><ul class="message_success"><li>GUID: ' + data.uid + '</li><li>Management Key: ' + data.management_key + '</li></ul>');
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
