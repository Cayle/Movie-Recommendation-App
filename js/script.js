
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

	const cardDiv = document.createElement("div");
	cardDiv.className = "card";


	const cardDivImg = document.createElement("div");
	cardDivImg.className = "card-image waves-effect waves-block waves-light";
	const img = document.createElement("img");
	img.className = 'activator';
	img.src = "images/xxx.jpeg";
	cardDivImg.appendChild(img);

	const cardContent = document.createElement("div");
	cardContent.className = 'card-content';
	const spanContent = document.createElement("span");
	spanContent.className = "card-title activator grey-text text-darken-4";
	spanContent.innerHTML = movie.title + '<i class="material-icons right">more_vert</i>'
	const pContent = document.createElement("p");
	pContent.innerHTML = '<a href="#">Watch trailer</a>';
	cardContent.appendChild(spanContent);
	cardContent.appendChild(pContent);

	const cardReveal = document.createElement("div");
	cardReveal.className = "card-reveal";
	const spanReveal = document.createElement("span");
	spanReveal.className = "card-title grey-text text-darken-4";
	spanReveal.innerHTML = '<i class="material-icons right">close</i>'
	cardReveal.appendChild(spanReveal);
	cardReveal.appendChild(createMovieDetails(movie));

	cardDiv.appendChild(cardDivImg);
	cardDiv.appendChild(cardContent);
	cardDiv.appendChild(cardReveal);

	colDiv.append(cardDiv);
	return colDiv;
}

function getEachMovieRow(movie_1, movie_2) {
	const mainDiv  = document.createElement("div");
	mainDiv.className = "row";
	mainDiv.appendChild(generateEachMovie(movie_1));
	mainDiv.appendChild(generateEachMovie(movie_2));
	return mainDiv;
}

async function generateRandomMovies() {
	const response = await fetch('http://172.20.10.5:105/random');
	const response_in_json = await response.json();
	console.log(response_in_json);

	const contentSection = document.getElementById("mainContent");
	contentSection.appendChild(getEachMovieRow(response_in_json[0], response_in_json[1]));
	contentSection.appendChild(getEachMovieRow(response_in_json[2], response_in_json[3]));
}

