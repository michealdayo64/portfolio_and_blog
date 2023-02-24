const comment = document.getElementById("mycomment");
const btnComment = document.getElementById("comment-post");
const email = document.getElementById("myemail");
const picText = document.getElementById("comm-text");
const proj_id = JSON.parse(document.getElementById("myproj_id").textContent);
const postLike = document.getElementById("post-like");
const likeCount = document.getElementById("like-count");
const showMessage = document.getElementById("show-messageId");
var commentImg = document.getElementById("comment-img");

const url = window.location.origin;
// USER LIKE COUNT
const getLikeCount = () => {
  fetch(`${url}/port_like_count/${proj_id}/`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      likeCount.textContent = data.res;
    });
};

getLikeCount();

console.log(commentImg.src);

let myEmailInput;
let myCommentInput;

function myGreeting() {
  showMessage.style.display = "none";
}

// BUTTON TO LIKE
postLike.addEventListener("click", (e) => {
  e.preventDefault();
  fetch(`${url}/port_like_unlike/${proj_id}/`, {
    body: null,
    method: "POST",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.result == "User not Authenticated") {
        getLikeCount();
        showMessage.style.display = "block";
        setTimeout(myGreeting, 3000);
        //console.log(data.result);
      } else {
        likeCount.textContent = data.num_likes;
      }
    });
});
