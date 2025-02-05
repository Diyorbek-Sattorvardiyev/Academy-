function runExample3() {
    $("#custom-places").mapsed({
		showOnLoad: 	
		[
			// Random made up CUSTOM place
			{
				// flag that this place should have the tooltip shown when the map is first loaded
				autoShow: true,
				lat: 41.555033, // Xorazm viloyati, Urganch
				lng: 60.641312,
				
				name: "TATU",
				street: "Y",
				userData: 99
			}

		]
		
	});									
}


$(document).ready(function() {
	runExample3();
});


