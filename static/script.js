// Function to play the video based on user input
function playVideo(videoPath) {
    const videoPlayer = document.getElementById("video-player");
    videoPlayer.src = videoPath;
    videoPlayer.load();
    videoPlayer.play();
}

// Function to handle search form submit
document.getElementById("search-form").addEventListener("submit", function(e) {
    e.preventDefault(); // Prevent form submission
    const searchInput = document.getElementById("search-input").value;
    // You should replace 'video_path.mp4' with the actual path to your video
    const videoPath = 'video_path.mp4'; // Replace with your video path
    
    // Show the loading sign
    document.getElementById("loading").style.display = "block";
    
    // Hide the video player
    document.getElementById("video-player").style.display = "none";
    
    playVideo(videoPath);
});

// Function to handle chat input
document.getElementById("chat-input").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        const chatInput = document.getElementById("chat-input");
        const chatMessage = chatInput.value;
        const chatbot = document.getElementById("chatbot");
        chatbot.innerHTML += `<p>User: ${chatMessage}</p>`;
        chatInput.value = "";
        chatbot.scrollTop = chatbot.scrollHeight; // Scroll to the bottom of the chat
    }
});
