var CHAT = {
    send_message_call: undefined,
    get_message_call: undefined,
    default_sleep: 1000,
    sleep: 1000,
    pk: 1,

    sendMessage: function(data){
        CHAT.send_message_call = $.ajax({
            url:"/send/",
            type: "POST",
            data: data,
            success: function(e){
            CHAT.sleep = CHAT.default_sleep;
            }});
    },

    longPolling: function(){
        get_message_call = $.ajax({
            url: '/get-messages/',
            type: 'GET',
            success: CHAT.onSuccess,
            data: {pk: CHAT.pk},
            error: CHAT.onError});
    },

    onSuccess: function(data){
        data = $.parseJSON(data);
        if (data.length && CHAT.pk < data[data.length - 1].pk){
            CHAT.pk = data[data.length - 1].pk
            for(var i=0; i < data.length; i++)
                CHAT.writeMessage(data[i]);
        }
        CHAT.sleep = CHAT.default_sleep;
        window.setTimeout(CHAT.longPolling, 100);
    },

    onError: function(){
        CHAT.sleep *= 2;
        window.setTimeout(CHAT.longPolling, CHAT.sleep);
    },

    writeMessage: function(msg){
        if(!msg) return;
        var content = $('#js-messages');
            content.prepend("<p>[" + msg.created_at + "] <b>" + msg.username + "</b>: " + msg.msg + "</p>");
    }
}

$(document).ready(function(){
    $(document).on("submit", "form#js-send-message", function(e){
        e.preventDefault();
        CHAT.sendMessage($(this).serialize());
        $('#js-msg').val('');
    });

    CHAT.longPolling();
});
