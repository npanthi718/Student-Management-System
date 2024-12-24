function filterByCourse() {
    const course = document.getElementById('courseFilter').value;
    if (course === "all") {
        window.location.href = "/";
    } else {
        window.location.href = `/filter?course=${course}`;
    }
}
