// Nav Toggle
      $(document).ready(function(){
    $('.menu-toggle').click(function(){
      $('nav').toggleClass('active');
    })
  })


//   Header Sticky
   window.addEventListener("scroll", function () {
    const header = document.getElementById("main-header");
    header.classList.toggle("scrolled", window.scrollY > 50);
  });


// Search Bar
async function showSuggestions(value) {
    const suggestionList = document.getElementById("suggestionsList");
    suggestionList.innerHTML = "";

    if (value.trim() === "") {
      suggestionList.style.display = "none";
      return;
    }

    try {
      const response = await fetch(`/search-packages/?q=${encodeURIComponent(value)}`);
      const data = await response.json();
      const suggestions = data.results;

      if (suggestions.length === 0) {
        suggestionList.style.display = "none";
        return;
      }

      suggestions.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item.title;

        // Redirect to the package detail URL provided by Django
        li.onclick = () => {
          window.location.href = item.url;
        };

        suggestionList.appendChild(li);
      });

      suggestionList.style.display = "block";
    } catch (error) {
      console.error("Error fetching suggestions:", error);
    }
  }


// Hero Carousel
const slides = document.querySelectorAll('.carousel-slide');
const thumbnailContainer = document.getElementById('thumbnails');
let currentIndex = 0;

function updateCarousel() {
  slides.forEach((slide, i) => {
    slide.classList.toggle('active', i === currentIndex);
  });

  // Clear and add next 3 thumbnails (excluding current)
  thumbnailContainer.innerHTML = '';

  for (let i = 1; i <= 3; i++) {
    const nextIndex = (currentIndex + i) % slides.length;
    const thumb = document.createElement('img');
    thumb.src = slides[nextIndex].querySelector('img').src;
    thumb.className = 'thumb';
    thumb.dataset.index = nextIndex; // store target slide index
    thumb.style.cursor = 'pointer';

    // Make thumb clickable
    thumb.addEventListener('click', () => {
      currentIndex = nextIndex;
      updateCarousel();
    });

    thumbnailContainer.appendChild(thumb);
  }
}

function nextSlide() {
  currentIndex = (currentIndex + 1) % slides.length;
  updateCarousel();
}

// Initial setup
updateCarousel();
setInterval(nextSlide, 3000);


// Counter
 document.addEventListener("DOMContentLoaded", () => {
    const counters = document.querySelectorAll(".counter");
    let counterStarted = false;

    const runCounter = (counter) => {
      const target = +counter.getAttribute("data-target");
      const speed = 200;

      const updateCount = () => {
        const current = +counter.innerText.replace("+", "");
        const increment = Math.ceil(target / speed);

        if (current < target) {
          counter.innerText = `${current + increment}+`;
          setTimeout(updateCount, 20);
        } else {
          counter.innerText = `${target}+`;
        }
      };

      updateCount();
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !counterStarted) {
          counters.forEach(counter => runCounter(counter));
          counterStarted = true;
          observer.disconnect(); // Stop observing after animation starts
        }
      });
    }, { threshold: 0.4 });

    const section = document.querySelector(".why-chooswe-wrapper");
    if (section) {
      observer.observe(section);
    }
  });

  
// FAQ Accordian
   const items = document.querySelectorAll('.faq-accordian-item');

    items.forEach(item => {
      item.addEventListener('click', () => {
        item.classList.toggle('active');
      });
    });