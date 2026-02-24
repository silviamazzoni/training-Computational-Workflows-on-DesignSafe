currentSlide = {}
firstSlide = {}
lastSlide = {}

function addSlides(divLabel,imgSrc0,imgExt,startSlide,endSlide) {
    console.log('divLabel',divLabel)

    currentSlide[divLabel] = startSlide
    firstSlide[divLabel] = startSlide
    lastSlide[divLabel] = endSlide
    
    divTXT = `
    <div style="text-align:center;">
      <img id="${divLabel}_img" src="${imgSrc0}${startSlide}.${imgExt}" width="100%" style="border:1px solid #ccc; margin-bottom:10px;">
      <br>
      <button onclick='prevSlide("${divLabel}","${imgSrc0}","${imgExt}")' class="pushable"><span class="front">⬅️ Previous</span></button>
      <span id="${divLabel}_ctr" style="margin: 0 20px;">Slide ${startSlide} of ${startSlide}-${endSlide}</span>
      <button onclick='nextSlide("${divLabel}","${imgSrc0}","${imgExt}")' class="pushable"><span class="front">Next ➡️</span></button>
    </div>
    `
    console.log('divTXT',divTXT)
    document.getElementById(divLabel).innerHTML = divTXT;

}
          
function updateImage(divLabel,imgSrc0,imgExt) {
// const filename = `_static/slides/slide_${String(currentSlide).padStart(2, '0')}.jpg`;
const filename = `${imgSrc0}${String(currentSlide[divLabel])}.${imgExt}`;
document.getElementById(divLabel+"_img").src = filename;
document.getElementById(divLabel+"_ctr").innerText = `Slide ${currentSlide[divLabel]} of ${firstSlide[divLabel]}-${lastSlide[divLabel]}`;
}

function nextSlide(divLabel,imgSrc0,imgExt) {
currentSlide[divLabel] = currentSlide[divLabel] < lastSlide[divLabel] ? currentSlide[divLabel] + 1 : firstSlide[divLabel];
updateImage(divLabel,imgSrc0,imgExt);
}

function prevSlide(divLabel,imgSrc0,imgExt) {
currentSlide[divLabel] = currentSlide[divLabel] > firstSlide[divLabel]  ? currentSlide[divLabel] - 1 : lastSlide[divLabel];
updateImage(divLabel,imgSrc0,imgExt);
}