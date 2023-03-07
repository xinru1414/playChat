var chat_history = [];

function sendChat() {
    var userChat = document.getElementById("user_input").value;
    req = {
        "user_input": userChat,
        "history": chat_history
    }
    fetch("/api/chat", {
        method: "POST", headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(req),
    }).then((response) => response.json()).then((data) => {
        document.getElementById("result").innerText = data['next_line']
        console.log("Success:", data);
      })
}