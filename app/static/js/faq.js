
// qid : question ID that toggles display of p-tag in faq.html
function showAnswer(qid) {
    var x = document.getElementById(qid);
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    else {
        x.style.display = "none";
    }
}