<template>
  <div>
    <div id="nav">
      <img
        src="https://static.vecteezy.com/system/resources/previews/009/385/307/original/quiz-time-neon-signs-style-text-free-vector.png"
        alt="Quiz Master Logo" />
      <h4>HOME</h4>
      <h4>QUIZZES</h4>
      <h4>LEADERBOARD</h4>
      <h4>ABOUT US</h4>
      <h4 @click="goToLogin">LOGIN</h4>
    </div>
    <div id="cursor"></div>
    <div id="cursor-blur"></div>

    <video autoplay loop muted id="background-video">
      <source src="@/assets/background_video.mp4" type="video/mp4">
    </video>
    <div id="main">
      <div id="page1">
        <h1>LEARN. QUIZ. WIN.</h1>
        <h2>WELCOME TO QUIZ MASTER!</h2>
        <p>
          Quiz Master is a comprehensive quiz platform designed to make learning fun and accessible to everyone.
          Challenge yourself, compete with friends, and expand your knowledge with our diverse range of quiz categories.
        </p>
        <div id="arrow">
          <i class="ri-arrow-down-line"></i>
        </div>
      </div>
      <div id="page2">
        <div id="scroller">
          <div id="scroller-in">
            <h4>CHALLENGE YOURSELF</h4>
            <h4>TEST YOUR KNOWLEDGE</h4>
            <h4>COMPETE WITH FRIENDS</h4>
            <h4>LEARN SOMETHING NEW</h4>
            <h4>WIN BADGES</h4>
          </div>
          <div id="scroller-in">
            <h4>CHALLENGE YOURSELF</h4>
            <h4>TEST YOUR KNOWLEDGE</h4>
            <h4>COMPETE WITH FRIENDS</h4>
            <h4>LEARN SOMETHING NEW</h4>
            <h4>WIN BADGES</h4>
          </div>
        </div>
        <div id="about-us">
          <img src="https://img.freepik.com/free-vector/quiz-neon-sign_1262-15913.jpg" alt="Quiz Image 1" />
          <div id="about-us-in">
            <h3>ABOUT US</h3>
            <p>
              Quiz Master is a dynamic platform for knowledge enthusiasts. Our mission is to make learning engaging and
              fun through interactive quizzes across various subjects.
              Whether you're a student looking to test your knowledge, a teacher seeking educational tools, or just
              someone who loves quizzes, Quiz Master has something for everyone.
            </p>
          </div>
          <img src="https://img.freepik.com/free-vector/quiz-word-concept_23-2147844150.jpg" alt="Quiz Image 2" />
        </div>
        <div id="cards-container">
          <div class="card" id="card1">
            <div class="overlay">
              <h4>Daily Challenges</h4>
              <p>
                Test your knowledge with new quizzes every day. Earn points and compete on our global leaderboard with
                daily challenges.
              </p>
            </div>
          </div>
          <div class="card" id="card2">
            <div class="overlay">
              <h4>Multiple Categories</h4>
              <p>
                Explore quizzes in science, history, literature, sports, entertainment, and more. There's always
                something new to discover.
              </p>
            </div>
          </div>
          <div class="card" id="card3">
            <div class="overlay">
              <h4>Create Your Own</h4>
              <p>
                Become a quiz master yourself! Create custom quizzes and share them with friends, classmates, or
                colleagues.
              </p>
            </div>
          </div>
        </div>
        <div id="green-div">
          <img src="https://eiwgew27fhz.exactdn.com/wp-content/themes/puttosaurus/img/dots-side.svg" alt="" />
          <h4>
            SIGN UP FOR QUIZ MASTER NEWS AND SPECIAL CHALLENGES STRAIGHT TO YOUR INBOX
          </h4>
          <img src="https://eiwgew27fhz.exactdn.com/wp-content/themes/puttosaurus/img/dots-side.svg" alt="" />
        </div>
      </div>
      <div id="page3">
        <p>
          "Quiz Master has completely transformed how I study. The interactive quizzes make learning fun, and I've seen
          a significant improvement in my test scores since I started using the platform. Highly recommend to all
          students!"
        </p>
        <img id="colon1" src="https://eiwgew27fhz.exactdn.com/wp-content/themes/puttosaurus/img/quote-left.svg"
          alt="" />
        <img id="colon2" src="https://eiwgew27fhz.exactdn.com/wp-content/themes/puttosaurus/img/quote-right.svg"
          alt="" />
      </div>
      <div id="page4">
        <h1>WHAT ARE YOU WAITING FOR?</h1>
        <div class="elem">
          <h2>DAILY CHALLENGES</h2>
          <img src="https://img.freepik.com/free-vector/quiz-neon-sign_1262-15913.jpg" alt="" />
        </div>
        <div class="elem">
          <h2>LEARN & GROW</h2>
          <img src="https://img.freepik.com/free-vector/quiz-word-concept_23-2147844150.jpg" alt="" />
        </div>
        <div class="elem">
          <h2>WIN REWARDS</h2>
          <img src="https://as1.ftcdn.net/v2/jpg/05/76/95/42/1000_F_576954224_h8GVzpgILGLHGQXEeFjlQ8G3Wrk5cSxY.jpg"
            alt="" />
        </div>
      </div>
      <div id="footer">
        <img src="https://eiwgew27fhz.exactdn.com/wp-content/themes/puttosaurus/img/dots-footer.svg" alt="" />
        <div id="f1">
          <img
            src="https://static.vecteezy.com/system/resources/previews/009/385/307/original/quiz-time-neon-signs-style-text-free-vector.png"
            alt="" />
        </div>
        <div id="f2">
          <h3>QUIZZES</h3>
          <h3>CHALLENGES</h3>
          <h3>LEADERBOARD</h3>
        </div>
        <div id="f3">
          <h3>ACCOUNT</h3>
          <h3>CREATE QUIZ</h3>
          <h3>ABOUT US</h3>
        </div>
        <div id="f4">
          <h4>
            QUIZ MASTER <br />
            YOUR KNOWLEDGE HUB <br />
            COPYRIGHT © 2024 <br />
            ALL RIGHTS RESERVED <br />
            CONTACT@QUIZMASTER.COM <br />
          </h4>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  data() {
    return {
      isLoggedIn: false
    };
  },
  mounted() {
    // Load GSAP library for animations
    this.loadGSAP().then(() => {
      this.setupGSAPAnimations();
    });
    
    this.setupCursor();
    this.checkLoginStatus();
    
    // Add Remix icons for the arrow
    const link = document.createElement('link');
    link.href = "https://cdn.jsdelivr.net/npm/remixicon@3.4.0/fonts/remixicon.css";
    link.rel = "stylesheet";
    document.head.appendChild(link);
  },
  methods: {
    loadGSAP() {
      return new Promise((resolve) => {
        // Load GSAP and ScrollTrigger from CDN
        const gsapScript = document.createElement('script');
        gsapScript.src = "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.1/gsap.min.js";
        gsapScript.onload = () => {
          const scrollTriggerScript = document.createElement('script');
          scrollTriggerScript.src = "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.1/ScrollTrigger.min.js";
          scrollTriggerScript.onload = () => resolve();
          document.head.appendChild(scrollTriggerScript);
        };
        document.head.appendChild(gsapScript);
      });
    },
    setupCursor() {
      const crsr = document.querySelector("#cursor");
      const blur = document.querySelector("#cursor-blur");
      
      if (crsr && blur) {
        document.addEventListener("mousemove", function (dets) {
          crsr.style.left = dets.x + "px";
          crsr.style.top = dets.y + "px";
          blur.style.left = dets.x - 250 + "px";
          blur.style.top = dets.y - 250 + "px";
        });

        const h4all = document.querySelectorAll("#nav h4");
        h4all.forEach(function (elem) {
          elem.addEventListener("mouseenter", function () {
            crsr.style.scale = 3;
            crsr.style.border = "1px solid #fff";
            crsr.style.backgroundColor = "transparent";
          });
          elem.addEventListener("mouseleave", function () {
            crsr.style.scale = 1;
            crsr.style.border = "0px solid #6a3de8";
            crsr.style.backgroundColor = "#6a3de8";
          });
        });
      }
    },
    setupGSAPAnimations() {
      if (window.gsap && window.gsap.ScrollTrigger) {
        const gsap = window.gsap;
        
        // Nav background animation - make it solid on scroll
        gsap.to("#nav", {
          backgroundColor: "#000", // Solid black
          boxShadow: "0 5px 15px rgba(0, 0, 0, 0.3)", // Add shadow for depth
          duration: 0.5,
          height: "110px",
          scrollTrigger: {
            trigger: "#nav",
            scroller: "body",
            start: "top -5%", // Start earlier
            end: "top -10%", 
            scrub: 1,
          },
        });

        // Main background animation - make it fully opaque sooner
        gsap.to("#main", {
          backgroundColor: "rgba(0, 0, 0, 1)", // Fully opaque black
          scrollTrigger: {
            trigger: "#main",
            scroller: "body",
            start: "top -5%", // Start earlier
            end: "top -20%", // End earlier
            scrub: 1,
          },
        });
        
        // Fade out video when scrolling
        gsap.to("#background-video", {
          opacity: 0,
          scrollTrigger: {
            trigger: "#page1",
            scroller: "body",
            start: "bottom 90%",
            end: "bottom 70%",
            scrub: 1,
          },
        });

        // About us section animations
        gsap.from("#about-us img, #about-us-in", {
          y: 90,
          opacity: 0,
          duration: 1,
          scrollTrigger: {
            trigger: "#about-us",
            scroller: "body",
            start: "top 70%",
            end: "top 65%",
            scrub: 1,
          },
        });

        // Card animations
        gsap.from(".card", {
          scale: 0.8,
          duration: 1,
          stagger: 0.1,
          scrollTrigger: {
            trigger: ".card",
            scroller: "body",
            start: "top 70%",
            end: "top 65%",
            scrub: 1,
          },
        });

        // Quote marks animations
        gsap.from("#colon1", {
          y: -70,
          x: -70,
          scrollTrigger: {
            trigger: "#colon1",
            scroller: "body",
            start: "top 55%",
            end: "top 45%",
            scrub: 4,
          },
        });
        
        gsap.from("#colon2", {
          y: 70,
          x: 70,
          scrollTrigger: {
            trigger: "#colon1",
            scroller: "body",
            start: "top 55%",
            end: "top 45%",
            scrub: 4,
          },
        });

        // Page 4 heading animation
        gsap.from("#page4 h1", {
          y: 50,
          scrollTrigger: {
            trigger: "#page4 h1",
            scroller: "body",
            start: "top 75%",
            end: "top 70%",
            scrub: 3,
          },
        });
        
        // Page 4 cards animation
        gsap.from(".elem", {
          y: 100,
          opacity: 0,
          duration: 1,
          stagger: 0.2,
          scrollTrigger: {
            trigger: ".elem",
            scroller: "body",
            start: "top 80%",
            end: "top 70%",
            scrub: 1,
          },
        });
      }
    },
    checkLoginStatus() {
      // Check if user is logged in
      const token = localStorage.getItem('token');
      this.isLoggedIn = !!token;
    },
    goToLogin() {
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: system-ui;
  color: #fff;
}

html, body {
  height: 100%;
  width: 100%;
  overflow-x: hidden;
}

*::selection {
  background-color: #fff;
  color: #6a3de8;
}

body::-webkit-scrollbar {
  display: block;
  width: 8px;
  background: #6a3de8;
}

body::-webkit-scrollbar-thumb {
  background-color: #fff;
  border-radius: 50px;
}

#cursor {
  height: 20px;
  width: 20px;
  background-color: #6a3de8;
  border-radius: 50%;
  position: fixed;
  z-index: 99;
  transition: all linear 0.1s;
  pointer-events: none;
}

#cursor-blur {
  height: 500px;
  width: 500px;
  background-color: rgba(106, 61, 232, 0.3);
  border-radius: 50%;
  position: fixed;
  filter: blur(80px);
  z-index: 9;
  transition: all linear 0.4s;
  pointer-events: none;
}

#nav {
  height: 130px;
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0 120px;
  gap: 50px;
  position: fixed;
  justify-content: flex-start;
  z-index: 999;
  transition: all ease 0.5s;
  background-color: rgba(0, 0, 0, 0.3); /* Semi-transparent initial state */
}

#nav img {
  height: 4.5vw;
}

#nav h4 {
  text-transform: uppercase;
  font-weight: 500;
  cursor: pointer;
  font-size: 1.15vw;
  transition: all ease 0.3s;
}

#nav h4:hover {
  color: #6a3de8;
}

#background-video {
  height: 100%;
  width: 100%;
  object-fit: cover;
  z-index: -1;
  position: fixed;
  top: 0;
  left: 0;
}

#main {
  position: relative;
  background-color: rgba(0, 0, 0, 0.39);
  transition: background-color 0.5s ease; /* Faster transition */
}

#page1 {
  height: 100vh;
  width: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  text-align: center;
  z-index: 10;
  padding: 0 20px;
}

#page1 h1 {
  font-size: 6vw;
  font-weight: 900;
  line-height: .86;
  letter-spacing: .02em;
  position: relative;
}

#page1 h1::before {
  content: "LEARN. QUIZ. WIN.";
  position: absolute;
  color: #000;
  top: -.4rem;
  left: -.4rem;
  width: 100%;
  -webkit-text-stroke: 1.5px #6a3de8;
  z-index: -1;
}

#page1 h2 {
  font-size: 30px;
  font-weight: 800;
  margin-top: 10px;
  margin-bottom: 20px;
}

#page1 p {
  font-size: 1.2vw;
  font-weight: 500;
  width: 40%;
}

#page1 #arrow {
  height: 250px;
  width: 250px;
  background-color: transparent;
  border: 2px solid #6a3de8;
  position: absolute;
  display: flex;
  left: -2%;
  bottom: 0%;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all ease 0.5s;
  cursor: pointer;
}

#page1 #arrow i {
  font-size: 50px;
  font-weight: 100;
}

#page1 #arrow:hover {
  scale: 0.4;
  background-color: #6a3de8;
}

#page2 {
  min-height: 100vh;
  width: 100%;
  z-index: 10;
  background-color: #000; /* Ensure page2 has a black background */
}

#scroller {
  white-space: nowrap;
  overflow-x: auto;
  overflow-y: hidden;
  position: relative;
  z-index: 10;
}

#scroller::-webkit-scrollbar {
  display: none;
}

#scroller-in {
  display: inline-block;
  white-space: nowrap;
  animation-name: scroll;
  animation-duration: 40s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

#scroller h4 {
  display: inline-block;
  font-size: 120px;
  font-weight: 900;
  font-family: sans-serif;
  margin-right: 20px;
  transition: all linear 0.3s;
  color: #000;
  -webkit-text-stroke: 2px #ffffff;
}

#scroller h4:hover {
  color: #6a3de8;
  -webkit-text-stroke: 2px #6a3de8;
}

@keyframes scroll {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-100%);
  }
}

#about-us {
  height: 40vh;
  width: 100%;
  display: flex;
  padding: 0 50px;
  align-items: center;
  position: relative;
  z-index: 10;
  justify-content: space-around;
}

#about-us img {
  height: 220px;
  width: 220px;
  border-radius: 20px;
  object-fit: cover;
}

#about-us-in {
  width: 50%;
  text-align: center;
}

#about-us-in h3 {
  font-size: 54px;
  font-weight: 800;
  margin-bottom: 30px;
}

#about-us-in p {
  font-size: 20px;
  line-height: 26px;
}

#cards-container {
  height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 70px;
  position: relative;
  z-index: 10;
}

.card {
  height: 80%;
  width: 24%;
  border-radius: 20px;
  background-size: cover;
  background-position: center;
  overflow: hidden;
  transition: all ease 0.6s;
}

#card1 {
  background-image: url(https://img.freepik.com/premium-vector/quiz-comic-pop-art-style_175838-505.jpg);
}

#card2 {
  background-image: url(https://img.freepik.com/free-vector/flat-design-illustration-customer-support_23-2148887720.jpg);
}

#card3 {
  background-image: url(https://img.freepik.com/free-vector/online-certification-illustration_23-2148575636.jpg);
}

.overlay {
  height: 100%;
  width: 100%;
  background-color: #6a3de8;
  padding: 30px;
  padding-top: 160px;
  opacity: 0;
  transition: all ease 0.6s;
}

.overlay h4 {
  color: #fff;
  font-size: 40px;
  text-transform: uppercase;
  white-space: nowrap;
  margin-bottom: 20px;
  font-weight: 800;
}

.overlay p {
  color: #fff;
  font-size: 18px;
}

.card:hover .overlay {
  opacity: 1;
}

.card:hover {
  transform: rotate3d(-1, 1, 0, 20deg);
}

#green-div {
  height: 30vh;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(to left bottom, #3a28b1, #8a6bff);
}

#green-div h4 {
  width: 45%;
  line-height: 50px;
  color: #fff;
  text-align: center;
  font-weight: 800;
  font-size: 27px;
  text-transform: uppercase;
}

#green-div img {
  height: 100%;
  object-fit: cover;
  width: 14%;
}

#page3 {
  height: 100vh;
  width: 100%;
  background-color: #000;
  display: flex;
  align-items: center;
  position: relative;
  justify-content: center;
}

#page3 > p {
  font-size: 35px;
  font-weight: 700;
  width: 60%;
  line-height: 45px;
  text-align: center;
}

#page3 img {
  position: absolute;
  height: 60px;
}

#page3 #colon1 {
  left: 15%;
  top: 25%;
}

#page3 #colon2 {
  bottom: 30%;
  right: 15%;
}

#page4 {
  min-height: 60vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 70px;
  position: relative;
  padding: 150px 0 100px;
  flex-wrap: wrap;
}

.elem {
  height: 300px;
  width: 26%;
  overflow: hidden;
  border-radius: 20px;
  position: relative;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  margin: 15px;
}

.elem h2 {
  height: 100%;
  width: 100%;
  background-color: #6a3de8;
  display: flex;
  color: #fff;
  font-weight: 800;
  align-items: center;
  justify-content: center;
  transition: all ease 0.5s;
  font-size: 2vw;
  position: absolute;
  z-index: 10;
}

.elem img {
  height: 100%;
  width: 100%;
  object-fit: cover;
  transition: all ease 0.5s;
  scale: 1.1;
}

.elem:hover h2 {
  color: #fff;
  background-color: rgba(106, 61, 232, 0.7);
}

.elem:hover img {
  scale: 1;
}

#page4 h1 {
  font-size: 6.4vw;
  position: absolute;
  top: 5%;
  font-weight: 900;
  font-family: sans-serif;
  color: #000;
  -webkit-text-stroke: 2px #fff;
  width: 100%;
  text-align: center;
}

#footer {
  height: 40vh;
  width: 100%;
  background: linear-gradient(to left bottom, #3a28b1 0%, #8a6bff 80%);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 6.5vw;
  padding: 0 100px;
}

#footer > img {
  position: absolute;
  left: 0;
  height: 100%;
  z-index: 0;
}

#f1 img {
  height: 100px;
}

#f1, #f2, #f3, #f4 {
  width: fit-content;
  position: relative;
  z-index: 99;
}

#f2 h3 {
  font-size: 1.6vw;
  white-space: nowrap;
  text-transform: uppercase;
  color: #fff;
  font-weight: 900;
  margin-bottom: 8px;
}

#f3 h3 {
  font-size: 1.6vw;
  white-space: nowrap;
  text-transform: uppercase;
  color: #fff;
  font-weight: 800;
  margin-bottom: 8px;
}

#f4 h4 {
  font-size: 1vw;
  white-space: nowrap;
  text-transform: uppercase;
  color: #fff;
  font-weight: 600;
  line-height: 20px;
  margin-bottom: 8px;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  #nav {
    padding: 0 20px;
    gap: 10px;
    height: 80px;
  }
  
  #nav img {
    height: 40px;
  }
  
  #nav h4 {
    font-size: 12px;
  }
  
  #page1 h1 {
    font-size: 40px;
  }
  
  #page1 h2 {
    font-size: 20px;
  }
  
  #page1 p {
    font-size: 14px;
    width: 80%;
  }
  
  #scroller h4 {
    font-size: 50px;
  }
  
  #about-us {
    flex-direction: column;
    height: auto;
    padding: 40px 20px;
  }
  
  #about-us img {
    height: 150px;
    width: 150px;
    margin: 10px 0;
  }
  
  #about-us-in {
    width: 90%;
  }
  
  #about-us-in h3 {
    font-size: 30px;
  }
  
  #cards-container {
    flex-direction: column;
    height: auto;
    gap: 20px;
    padding: 40px 0;
  }
  
  .card {
    width: 80%;
    height: 200px;
  }
  
  #green-div h4 {
    font-size: 14px;
    width: 60%;
    line-height: 20px;
  }
  
  #page3 > p {
    width: 90%;
    font-size: 20px;
  }
  
  #page4 {
    flex-direction: column;
    min-height: 80vh;
    padding: 100px 20px 60px;
  }
  
  .elem {
    width: 85%;
    height: 180px;
    margin: 10px 0;
  }
  
  .elem h2 {
    font-size: 20px;
  }
  
  #page4 h1 {
    font-size: 8vw;
    top: 2%;
  }
  
  #footer {
    flex-direction: column;
    height: auto;
    padding: 40px 20px;
    gap: 20px;
    align-items: flex-start;
  }
  
  #f2 h3, #f3 h3 {
    font-size: 16px;
  }
  
  #f4 h4 {
    font-size: 12px;
  }
}
</style>
