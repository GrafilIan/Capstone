const progressBar = document.getElementById('daily-progress-bar');

// Set the total duration in days for your progress bar
const totalDurationInDays = 30;

function updateDailyProgressBar() {
    const currentDate = new Date();
    const startDate = new Date('2023-08-01'); // Replace with your start date
    const elapsedDays = Math.floor((currentDate - startDate) / (1000 * 60 * 60 * 24));
    const progressPercentage = (elapsedDays / totalDurationInDays) * 100;

    progressBar.style.width = `${progressPercentage}%`;

    requestAnimationFrame(updateDailyProgressBar);
}

updateDailyProgressBar();



//setting date and time

