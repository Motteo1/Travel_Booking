const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
	event.preventDefault();
	
	const destination = document.querySelector('#destination').value;
	const checkIn = document.querySelector('#check-in').value;
	const checkOut = document.querySelector('#check-out').
