image = 1;
images_Pontarlier = Array('|',
	'css/saint_pet_1.jpg',
	'css/saint_pet_2.jpg',
'|');

function imageSuivante() {
	new_image = images_Pontarlier[image + 1]
	if(new_image != '|') {
	    document.getElementById('galerie').src = new_image;
	    image = image + 1;
	}
}

function imagePrecedente() {
	new_image = images_Pontarlier[image - 1]
	if(new_image != '|') {
	    document.getElementById('galerie').src = new_image;
	    image = image - 1;
	}
}