const comment = document.getElementById("mycomment");
const btnComment = document.getElementById("comment-post");
const email = document.getElementById("myemail");
const picText = document.getElementById("comm-text");
const proj_id = JSON.parse(document.getElementById("myproj_id").textContent);
const postLike = document.getElementById("post-like");
const likeCount = document.getElementById("like-count");
const showMessage = document.getElementById("show-messageId");
var commentImg = document.getElementById("comment-img");

// USER LIKE COUNT
const getLikeCount = () => {
  fetch(`http://127.0.0.1:8000/port_like_count/${proj_id}/`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      likeCount.textContent = data.res;
    });
};

getLikeCount();

commentImg.src = "{% static 'images/avatar.jpeg' %}".replace(/&amp;/g, "&");

let myEmailInput;
let myCommentInput;

//  INPUT EMAIL HERE
email.addEventListener("keyup", (e) => {
  myEmailInput = e.target.value;
});

// INPUT COMMENT HERE
comment.addEventListener("keyup", (e) => {
  myCommentInput = e.target.value;
});

// BUTTON TO SEND COMMENT
btnComment.addEventListener("click", (e) => {
  e.preventDefault();

  fetch(`http://127.0.0.1:8000/port-comment/${proj_id}/`, {
    body: JSON.stringify({
      email: myEmailInput,
      comment: myCommentInput,
    }),
    method: "POST",
  })
    .then((res) => res.json())
    .then((data) => {
      let json_data = JSON.parse(data);
      console.log(json_data);
      if (json_data) {
        var bb = document.createElement("div");
        bb.classList.add("mm");
        bb.innerHTML = `
        <img src="${commentImg.src}" alt="" srcset="" alt="hello">
            <div class="comment-text">
                <h5>${json_data["email"]}</h5>
                <span>${json_data["comment"]}</span>
                <span>${json_data["date"]}</span>
            </div>
        `;
        picText.insertBefore(bb, picText.firstChild);
        console.log("posted");
      }
      email.value = "";
      comment.value = "";
    });
});

function myGreeting() {
  showMessage.style.display = "none";
}

// BUTTON TO LIKE
postLike.addEventListener("click", (e) => {
  e.preventDefault();
  fetch(`http://127.0.0.1:8000/port_like_unlike/${proj_id}/`, {
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
