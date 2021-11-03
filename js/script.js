
async function test(){
	alert("Hey");
	const response = await fetch('http://172.20.10.5:105/new');
	const resp_json = await response.json();
	const name = resp_json.name;
	const age = resp_json.age;
	console.log(name + " " + age);
	const parElement = document.getElementById('test1');
	parElement.innerHTML = name + " " + age;
}

function createEachCollapsibleElement(title,  content) {
	const listItem = document.createElement("li");
	const divHeader = document.createElement("div");
	divHeader.className = "collapsible-header";
	divHeader.innerText = title;
	const divBody = document.createElement("div");
	divBody.className = "collapsible-body";
	divBody.innerHTML = "<p>" + content + "</p>"

	listItem.appendChild(divHeader);
	listItem.appendChild(divBody);

	return listItem;
}

function createMovieDetails(movie) {
	const details_list = document.createElement('ul');
	details_list.className = "collapsible";

	details_list.appendChild(createEachCollapsibleElement("Title", "The Creep"));
	details_list.appendChild(createEachCollapsibleElement("Genres", "K-pop, Comedy"));
	details_list.appendChild(createEachCollapsibleElement("Description", "This is just test Description"));
	details_list.appendChild(createEachCollapsibleElement("Cast", "Test, casts, for, some, confirmation."));
	details_list.appendChild(createEachCollapsibleElement("Directors", "Test director."));

	return details_list;
}

function generateEachMovie(movie) {
	const colDiv = document.createElement("div");
	colDiv.className = 'col s12 m6';

	const detailsLink = document.createElement("a");
	detailsLink.href = 'movie.html?name='+movie.title;

	const cardDiv = document.createElement("div");
	cardDiv.className = "card";


	const cardDivImg = document.createElement("div");
	cardDivImg.className = "card-image waves-effect waves-block waves-light";
	const img = document.createElement("img");
	img.className = 'activator';
	img.src = movie.poster_image;
	img.width  = 150;
	img.height = 300;
	cardDivImg.appendChild(img);

	const cardContent = document.createElement("div");
	cardContent.className = 'card-content';
	const spanContent = document.createElement("span");
	spanContent.className = "card-title activator grey-text text-darken-4";
	spanContent.innerHTML = movie.title;

	cardContent.appendChild(spanContent);


	const cardReveal = document.createElement("div");
	cardReveal.className = "card-reveal";
	const spanReveal = document.createElement("span");
	spanReveal.className = "card-title grey-text text-darken-4";
	spanReveal.innerHTML = '<i class="material-icons right">close</i>'
	cardReveal.appendChild(spanReveal);
	cardReveal.appendChild(createMovieDetails(movie));

	cardDiv.appendChild(cardDivImg);
	cardDiv.appendChild(cardContent);


	detailsLink.appendChild(cardDiv);
	colDiv.append(detailsLink);
	return colDiv;
}

function getEachMovieRow(movie_1, movie_2) {
	const mainDiv  = document.createElement("div");
	mainDiv.className = "row";
	mainDiv.appendChild(generateEachMovie(movie_1));
	mainDiv.appendChild(generateEachMovie(movie_2));
	return mainDiv;
}

const url = "http://172.18.3.15:5000";

async function generateRandomMovies() {
	const response = await fetch(url+'/random');
	const response_in_json = await response.json();
	console.log(response_in_json);

	const contentSection = document.getElementById("mainContent");
	contentSection.appendChild(getEachMovieRow(response_in_json[0], response_in_json[1]));
	contentSection.appendChild(getEachMovieRow(response_in_json[2], response_in_json[3]));
	console.log("hey!!");
}

function getParam(){
	const urlParams = new URLSearchParams(location.search);
	var val;
	for (const [key, value] of urlParams) {
		val = value;
		break;
	}
	console.log(val);
	return val;
}

async function getAMovieDetail() {
	const movie_name = getParam();
	const response = await fetch(url+'/movie/'+movie_name);
	const response_in_json = await response.json();
	console.log(response_in_json);
	document.getElementById("title").innerText = response_in_json.title;
	document.getElementById("description").innerText = response_in_json.description;
	document.getElementById("trailer_img").src = response_in_json.poster_path;
	document.getElementById("trailer_link").href = response_in_json.trailer_url;
}



