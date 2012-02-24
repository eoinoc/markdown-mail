/*
 * If 'wednesday' is passed in, then return next Wednesday's date in the format YYYY-MM-DD.
 * If today is Wednesday, then today's date will be given.
 */
function nextDayOccurence(default_next_day) {
	var days = {
		sunday: 0, 
		monday: 1, 
		tuesday: 2,
		wednesday: 3, 
		thursday: 4, 
		friday: 5, 
		saturday: 6
	};
	
	var returnDate = new Date();
	
	// Try to find next Wednesday's date (or whatever the day that's been passed in)
	var dayIndex = days['default_next_day'];
	var returnDay = returnDate.getDay();
	var i = 0;
	while (dayIndex !== returnDay && i < 7) {
		returnDay = returnDate.getDay();
		returnDate.setDate(returnDate.getDate() + (dayIndex + (7 - returnDay)) % 7);
		i = i + 1;
	}
	
	// Construct the date in the required YYYY-MM-DD format.
	var dd=returnDate.getDate();
	if(dd<10)dd='0'+dd;
	var mm=returnDate.getMonth()+1;
	if(mm<10)mm='0'+mm;
	var yyyy=returnDate.getFullYear();
	return String(yyyy+'-'+mm+'-'+dd)
}

// Transform the input to the desired output
function process($prepend_plain_email, $appent_plain_email) {
	var list_name = $('[name=list]:checked').val();
	var traffic_source = list_name;
	var medium = 'email';
	var campaign = $('#campaign').val();
	var url_params = URLparams(traffic_source, medium, campaign);

	// HTML
	$('#output_html').val(marked($('#text_input').val()));
	templateHTML('#output_html', list_name);
	tagHTMLURLs('#output_html', url_params);
	
	// Plain text
	$('#output_plain').val($('#text_input').val());
	templatePlain('#output_plain', appent_plain_email, prepend_plain_email);
	tagPlainTextURLs('#output_plain', url_params);
}

/*
 * Returns Google Analytics URL parameter
 */
function URLparams(traffic_source, medium, campaign) {
	return 'utm_source='+traffic_source+'&utm_medium='+medium+'&utm_campaign='+campaign;
}

function templateHTML(output_textarea, list_name) {
	var header = getTemplateInclude(list_name, 'header');
	var footer = getTemplateInclude(list_name, 'footer');
	$(output_textarea).val(header+$(output_textarea).val()+footer);
}

function tagHTMLURLs(output_textarea, url_params) {
	$(output_textarea).val($(output_textarea).val().replace(/(a href=\")((ftp|http|https|gopher|mailto|news|nntp|telnet|wais|file|prospero|aim|webcal):(([A-Za-z0-9$_.+!*(),;/?:@&~=-])|%[A-Fa-f0-9]{2}){2,}(#([a-zA-Z0-9][a-zA-Z0-9$_.+!*(),;/?:@&~=%-]*))?([A-Za-z0-9$_+!*();/?:~-]))/g, "$1$2?"+url_params));
	return false;
}

function tagPlainTextURLs(output_textarea, url_params) {
	$(output_textarea).val($(output_textarea).val().replace(/(\[.*\])(\()(.*)(\))/g, "$1$2$3?" + url_params + "$4"));
}

function templatePlain(output_textarea, header, footer) {
	$(output_textarea).val(header+$(output_textarea).val()+footer);
}

/*
 * Goes to search on the same server for /templates/[list_name].{header|footer}.txt
 */
function getTemplateInclude(list_name, section) {
	var result;
	$.ajax({
		type: "GET",
		url: './templates/'+list_name+'.'+section+'.html',
		async: false,
		success: function(data){
			result = data;
		}
	});
	return result;
}