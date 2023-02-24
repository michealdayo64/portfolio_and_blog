let readMoreValue = 3;
let portBox = document.getElementById("port-box");
let spinnerBox = document.getElementById("spinner-box");
const readMoreBtn = document.getElementById("btnReadMore");

const url = window.location.origin;

const handleGetData = () => {
  //spinnerBox.style.display = "block";
  // OR
  spinnerBox.classList.add("spinner-border");

  fetch(`${url}/read-more/${readMoreValue}/`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((result) => {
      let data = result.data;
      data.map((p) => {
        portBox.innerHTML += `<div class="col-sm-4">
      <div class="my-card"> <img class="my-card-img" src="${p["img"]}" />
      <div class="my-card-body trainer-card-body">
          <h5>${p["title"]}</h5>
          <p>${p["desc"].substring(0, 40)}...</p>
          <div class="social-icons">
              <i class="fa fa-heart"></i>
                            <span class="ms-1 views">${
                              p["user_like_count"]
                            }</span>
                            <i class="fa fa-comment"></i>
                            <span class="ms-1 views">${
                              p["comment_count"]
                            }</span>
          </div> 
          <br>
          <a href="${url}/port-detail/${p["id"]}/" class="my-card-btn">View</a>
      </div>
  </div>
  </div>`;
      });
      //spinnerBox.style.display = "none";
      // OR
      spinnerBox.classList.remove("spinner-border");
      if (result.max_size) {
        readMoreBtn.style.display = "none";
      }
    });
};

handleGetData();

readMoreBtn.addEventListener("click", (e) => {
  e.preventDefault();
  readMoreValue += 3;
  handleGetData();
});
