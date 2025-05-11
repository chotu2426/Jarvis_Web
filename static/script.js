const micBtn = document.getElementById("micBtn");
const output = document.getElementById("output");

const synth = window.speechSynthesis;
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.continuous = false;

micBtn.onclick = () => {
  output.innerText = "Listening...";
  recognition.start();
};

recognition.onresult = function (event) {
  const speech = event.results[0][0].transcript;
  output.innerText = "Heard: " + speech;
  fetch("/process", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ command: speech }),
  })
    .then((res) => res.json())
    .then((data) => {
      output.innerText = "Jarvis: " + data.response;
      const utter = new SpeechSynthesisUtterance(data.response);
      synth.speak(utter);
    });
};
